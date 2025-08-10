from functions.run_python import run_python_file

print("TEST 1:", run_python_file("calculator", "main.py")) #(should print the calculator's usage instructions)
print("TEST 2:", run_python_file("calculator", "main.py", ["3 + 5"])) #(should run the calculator... which gives a kinda nasty rendered result)
print("TEST 3:", run_python_file("calculator", "tests.py"))
print("TEST 4:", run_python_file("calculator", "../main.py")) #(this should return an error)
print("TEST 5", run_python_file("calculator", "nonexistent.py")) #(this should return an error)