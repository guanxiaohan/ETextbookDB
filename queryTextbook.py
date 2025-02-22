import json
import os
import sys
from time import strftime

path = os.path.dirname(os.path.abspath(__file__))
INDEX_FILEPATH = os.path.join(path, "textbookIndex.json")
CODENAME_FILEPATH = os.path.join(path, "textbookCodeNames.json")

def Log(message):
    print(f"[{strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def search_textbooks(index_tree, args: dict[str, str]):
    textbooks = index_tree["textbooks"]
    categories = index_tree["categories"]
    results = set(range(len(textbooks)))

    try:
        for arg, value in args.items():
            if arg == "v":
                if value.upper() in categories["version_codes"]:
                    results &= set(categories["version_codes"][value.upper()])
                else:
                    return []
            elif arg == "s":
                possible_ids = set()
                for subject in categories["subjects"].keys():
                    if subject.startswith(value.capitalize()):
                        possible_ids |= set(categories["subjects"][subject])

                Log(possible_ids)
                if not possible_ids:
                    return []
                else:
                    results &= possible_ids

            elif arg == "g":
                if value in categories["grades"]:
                    results &= set(categories["grades"][value])
                else:
                    return []
            elif arg == "e":
                if value.lower() in categories["extensions"]:
                    results &= set(categories["extensions"][value.lower()])
                else:
                    return []
            else:
                return []
    except:
        Log(f"Error in searching textbooks. Arg {arg}: {value} incorrect.")
        Log("Check the parameters and try again.")
        return []
    
    return [textbooks[i] for i in results]

def translate_textbook(textbook, codenames, language="en_us"):
    result_str = ""
    result_str += f"{codenames["VersionCodes"][textbook['version_code']][0 if language=='en_us' else 1]} "
    result_str += f"{codenames["Subjects"][textbook['subject']][0 if language=='en_us' else 1]} "
    result_str += f"{codenames["Grades"][str(textbook['grade'])][0 if language=='en_us' else 1]} "
    result_str += f"{codenames["Semesters"][str(textbook['semester'])][0 if language=='en_us' else 1]}"
    return result_str

def show_search_results(textbooks, codenames, args) -> bool:
    if not textbooks:
        print(f"No textbooks found under {args}.")
        return

    print(f"Found {len(textbooks)} textbooks under arg {args}:")
    print()
    for id, textbook in enumerate(textbooks):
        print(f"#{id} Textbook (index id " + str(textbook["index_id"]) + "): " + translate_textbook(textbook, codenames) + " / " + translate_textbook(textbook, codenames, "zh_cn"))
        print("    - Path: " + textbook["file_dir_absolute"])
    print()

    print("Enter the # of the textbook to open, or press enter to modify the args.")
    print("Open multiple textbooks by separating the # with spaces.")
    i = input("Textbook(s): ")
    if i:
        for name in i.split(" "):
            try:
                os.system(f"start {textbooks[int(name)]['file_dir_absolute']}")
                Log(f"Opened textbook #{name} {textbooks[int(name)]['file_dir_absolute']}.")

            except:
                print("Invalid index: " + name)
    print()
    

def main(index_file_path = INDEX_FILEPATH):
    args = {}
    # Read args from sys.argv
    # Command line argument format: -v VCODE -s SUBJECT -g GRADE -e EXTENSION
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv), 2):
            if sys.argv[i] == "-v":
                args["v"] = sys.argv[i+1]
                Log(f"Read argument VersionCodes from command line: {args['v']}")
            elif sys.argv[i] == "-s":
                args["s"] = sys.argv[i+1]
                Log(f"Read argument Subjects from command line: {args['s']}")
            elif sys.argv[i] == "-g":
                args["g"] = sys.argv[i+1]
                Log(f"Read argument Grades from command line: {args['g']}")
            elif sys.argv[i] == "-e":
                args["e"] = sys.argv[i+1]
                Log(f"Read argument Extensions from command line: {args['e']}")
            else:
                Log("Invalid command line arguments.")
                Log("Usage: -v VCODE -s SUBJECT -g GRADE -e EXTENSION")
                args = {}
                break

    # Load index file.
    with open(index_file_path, "r") as f:
        index_tree = json.load(f)

    Log("Index file loaded.")
    Log(f"Index time: {index_tree['index_time']}")
    Log(f"Root directory: {index_tree['root_dir']}")
    Log(f"Textbooks in Total: {len(index_tree['textbooks'])}")

    # Load textbooks from index tree.
    with open(CODENAME_FILEPATH, "r") as f:
        codenames = json.load(f)
    Log("Code names loaded.")

    Log("Welcome to the textbook database.")
    print()

    cleared = True

    print("Query mode.")
    
    while True:
        # operation = input("Enter operation ([q]uery, [e]xit): ")
        operation = "q"
        if not operation:
            continue

        if operation[0] == "e":
            return
        
        try:
            if operation[0] == "q":
                print("Select arguments to query textbooks.")

                while True:
                    print()
                    if not cleared:
                        print("Arguments: [v]ersion_code, [s]ubject, [g]rade, [e]xtension, (no input for clearing)")
                    else:
                        print("Arguments: [v]ersion_code, [s]ubject, [g]rade, [e]xtension, (no input to search)")

                    print("Current arguments: ", args)
                    arg = input("Select a argument type: ")
                    if arg == "":
                        if not cleared:
                            args = {}
                            cleared = True
                            print("Arguments cleared.")
                            continue
                        break
                    
                    cleared = True
                    letter = arg[0].lower()
                    letter_dict = {"v": "VersionCodes", "s": "Subjects", "g": "Grades", "e": "Extensions"}
                    if letter in ["v", "s", "g", "e"]:
                        print()
                        print(f"Available {letter_dict[letter]} choices: ")
                        for code, name in codenames[letter_dict[letter]].items():
                            print(f"{code}: {' '.join(name)}")
                        print()

                        if letter in args:
                            print(f"Current argument {letter_dict[letter]} value: {args[letter]}")
                        value = input(f"Enter one: ")
                        args[letter] = value
                        
                    else:
                        print("Invalid argument type.")
                        continue
                if args:
                    cleared = False
                Log(f"Querying textbooks with args: {args}")
                results = search_textbooks(index_tree, args)
                Log("Finished seaching.")
                show_search_results(results, codenames, args)

                if not cleared:
                    print("To clear the args, press enter. Or modify the args by entering its codename.")
                
        except KeyboardInterrupt:
            try:
                print()
                input("Press Ctrl+C again to exit, or press enter to go back to querying.")
            except KeyboardInterrupt:
                print()
                print("Goodbye. Have fun reading textbooks.")
                print()
                return

if __name__ == "__main__":
    main()
