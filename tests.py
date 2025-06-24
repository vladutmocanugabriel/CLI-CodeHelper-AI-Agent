#GET_FILES_INFO Tests:

#from functions.get_files_info import get_files_info

#print(get_files_info("calculator", "."))
#print(get_files_info("calculator", "pkg"))
#print(get_files_info("calculator", "/bin"))
#print(get_files_info("calculator", "../"))

#################################################################

#GET_FILE_CONTENT Tests:
#from functions.get_file_content import get_file_content

#print(get_file_content("calculator", "main.py"))
#print(get_file_content("calculator", "pkg/calculator.py"))
#print(get_file_content("calculator", "/bin/cat"))

#################################################################

#WRITE_FILE Tests:
#from functions.write_file import write_file

#print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
#print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
#print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

#################################################################

#RUN_PYTHON Tests:
from functions.run_python import run_python_file

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))