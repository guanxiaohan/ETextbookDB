
pyinstaller queryTextbook.py
REM copy .\dist\queryTextbook\queryTextbook.exe /B C:\Programs\RunTools\textbook.exe
xcopy .\dist\queryTextbook\* C:\Programs\RunTools\ /E /Y
copy .\textbookCodeNames.json C:\Programs\RunTools\_internal
copy .\textbookIndex.json C:\Programs\RunTools\_internal
rename C:\Programs\RunTools\queryTextbook.exe textbook.exe