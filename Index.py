import json
import os
from dataclasses import dataclass
import datetime

def Log(message: str):
    print(f"[{datetime.datetime.now()}] {message}")

INDEX_FILEPATH = "./textbookIndex.json"

# Index the textbook files in the sub-directories
# Output into a JSON file

# A textbook file is formatted in:
# (VersionCode)_(Subject)_G(Grade)S(Semester)_(DownloadDate).(Extension)
# VersionCode: Defines which press publishes this textbook.     
#   RJ: People's Education Press
#   SD: Shandong Education Press
#   BS: Beijing Normal University Press
# Subject: Defines the subject of the textbook. One subject of textbooks is stored in one sub-directory named this subject.
#   Chinese, Mathematics, English, Physics, Chemistry, Biology, Politics, History, Geography, etc.
# Grade: Defines the grade of the textbook.
#   1 ~ 6: Primary School
#   7 ~ 9: Junior High School
#   10: Senior High School (Must-Study) 必修
#   11: Senior High School (Optional-Study) 选择性必修
#   12 and above: undefined
# Semester: Defines the semester of the textbook.
#   0: Full Year
#   1: First Semester
#   2: Second Semester
# DownloadDate: Defines the date when the textbook is downloaded.
#   Format: YYYYMMDD (like 20250207)
# Extension: Defines the extension of the textbook.
#   Usually pdf, sometimes epub

@dataclass
class Textbook:
    index_id: int
    version_code: str
    subject: str
    grade: int
    semester: int
    download_date: list[int]
    extension: str
    file_dir_absolute: str
    file_dir_relative: str

def construct_textbook(file_dir_absolute: str) -> Textbook:
    # Use the absolute textbook path to construct a Textbook object
    file_name = file_dir_absolute.split("/")[-1]
    file_name_split = file_name.split(".")[0].split("_")
    version_code = file_name_split[0]
    subject = file_name_split[1]
    grade = int(file_name_split[2].split("S")[0][1:])
    semester = int(file_name_split[2].split("S")[1])
    download_date = datetime.datetime.strptime(file_name_split[3], "%Y%m%d").date()
    extension = file_name.split(".")[1]
    file_dir_relative = "./" + os.path.relpath(file_dir_absolute).replace("\\", "/")
    return Textbook(0, version_code, subject, grade, semester, [download_date.year, download_date.month, download_date.day], 
                    extension, file_dir_absolute, file_dir_relative)

def get_all_textbooks(main_dir: str = "./"):
    # Scan all sub-directories to find textbooks which match the format.
    textbooks = []
    Log("Scanning for textbooks...")
    for root, dirs, files in os.walk(main_dir):
        for file in files:
            if file.endswith(".pdf") or file.endswith(".epub") or file.endswith(".mobi"):
                # Get the textbook file name
                file_name = file.split(".")[0]
                # Check if the file name matches the format
                if len(file_name.split("_")) == 4:
                    fullpath = os.path.join(os.getcwd(), root, file).replace("\\", "/").replace("./", "")
                    # Append the absolute path of the textbook file
                    textbooks.append(fullpath)
                    Log(f"Found textbook: {file}")
    
    Log(f"Found {len(textbooks)} textbooks.")
    return textbooks

def index_textbooks(main_dir: str = "./"):
    # Generate a JSON tree includes all files' data
    textbooks = [construct_textbook(x) for x in get_all_textbooks(main_dir)]
    # add the index id to each textbook element
    for i in range(len(textbooks)):
        textbooks[i].index_id = i

    # Generate index for version codes, subjects, grades, extensions.
    # Index tree format:
    # "categories": {
    #   "version_codes": {"RJ": [1, 4, 10], "SD": [2, 11], "BS": [3, 6, 9] ... },
    #   "subjects": {"Chinese": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "Mathematics": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20] ... },
    #   "grades": {1: [1, 2, 3, 5, 6], 2: [7, 8, 9], 3: [4, 10, 11, 12] ... }
    #   "extensions": {"pdf": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "epub": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20] ... }
    # }

    categories = {
        "version_codes": {},
        "subjects": {},
        "grades": {},
        "extensions": {}
    }
    for textbook in textbooks:
        if textbook.version_code not in categories["version_codes"]:
            categories["version_codes"][textbook.version_code] = []
        categories["version_codes"][textbook.version_code].append(textbook.index_id)

        if textbook.subject not in categories["subjects"]:
            categories["subjects"][textbook.subject] = []
        categories["subjects"][textbook.subject].append(textbook.index_id)

        if textbook.grade not in categories["grades"]:
            categories["grades"][textbook.grade] = []
        categories["grades"][textbook.grade].append(textbook.index_id)

        if textbook.extension not in categories["extensions"]:
            categories["extensions"][textbook.extension] = []
        categories["extensions"][textbook.extension].append(textbook.index_id)


    index_tree = {
        "index_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "root_dir": os.getcwd().replace("\\", "/"),
        "textbooks": [x.__dict__ for x in textbooks],
        "categories": categories
    }
    textbooks_json = json.dumps(index_tree, indent=4)
    Log("Finished constructing JSON tree.")
    
    # If the index file exists, create a backup then overwrite.
    Log(f"Writing index file to {INDEX_FILEPATH}")
    if os.path.exists(INDEX_FILEPATH):
        Log("Index file exists. Backup and overwrite.")
        # Remove old backup file if exists
        if os.path.exists(INDEX_FILEPATH + ".bak"):
            os.remove(INDEX_FILEPATH + ".bak")
        os.rename(INDEX_FILEPATH, INDEX_FILEPATH + ".bak")
    
    with open(INDEX_FILEPATH, "w") as f:
        f.write(textbooks_json)
    Log("Index file written.")

if __name__ == "__main__":
    index_textbooks()
    Log("Indexing completed.")