import json
import os
import time

path = os.path.dirname(os.path.abspath(__file__))
INDEX_FILEPATH = os.path.join(path, "textbookIndex.json")
CODENAME_FILEPATH = os.path.join(path, "textbookCodeNames.json")

def Log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

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
                if value.capitalize() in categories["subjects"]:
                    results &= set(categories["subjects"][value.capitalize()])
                else:
                    return []
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

def show_search_results(textbooks, codenames, args):
    if not textbooks:
        print(f"No textbooks found under {args}.")
        return

    print(f"Found {len(textbooks)} textbooks under arg {args}:")
    print()
    for id, textbook in enumerate(textbooks):
        print(f"#{id} Textbook (index id " + str(textbook["index_id"]) + "): " + translate_textbook(textbook, codenames) + "/" + translate_textbook(textbook, codenames, "zh_cn"))
        print("    - Path: " + textbook["file_dir_relative"])
    print()

    i = input("Enter the # of the textbook to open, or press enter to return: ")
    if i:
        try:
            os.system(f"start {textbooks[int(i)]['file_dir_absolute']}")
        except:
            print("Invalid index.")
            return
        

def main(index_file_path = INDEX_FILEPATH):
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

    while True:
        # operation = input("Enter operation ([q]uery, [e]xit): ")
        operation = "q"
        print("Query mode.")
        if not operation:
            continue

        if operation[0] == "e":
            return
        
        try:
            if operation[0] == "q":
                print("Select up to 4 arguments to query textbooks.")
                args = {}
                remaining_args = 4
                while remaining_args > 0:
                    print()
                    print("Arguments: [v]ersion_code, [s]ubject, [g]rade, [e]xtension, (no input for empty)")
                    arg = input("Select a argument type: ")
                    if arg == "":
                        break

                    letter = arg[0].lower()
                    if letter in ["v", "s", "g", "e"]:
                        if letter in args:
                            print("Argument already selected.")
                            continue

                        letter_dict = {"v": "VersionCodes", "s": "Subjects", "g": "Grades", "e": "Extensions"}
                        print()
                        print(f"Available {letter_dict[letter]} choices: ")
                        for code, name in codenames[letter_dict[letter]].items():
                            print(f"{code}: {' '.join(name)}")
                        print()
                        value = input(f"Enter one: ")
                        args[letter] = value
                        remaining_args -= 1

                    else:
                        print("Invalid argument type.")
                        continue
                
                Log(f"Querying textbooks with args: {args}")
                results = search_textbooks(index_tree, args)
                Log("Finished seaching.")
                show_search_results(results, codenames, args)
                
        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    main()
