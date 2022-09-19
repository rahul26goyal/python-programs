# python-programs
Data Structure and Algorithms implemented in Python

The project is divided into multiple packages based on the 
Data Structure and Algorithm used.

To unit test the code, I have used `unittest` package provided by default.

Tests are writte inside `tests` package.


## Code Style 
Python [PEP 8](https://peps.python.org/pep-0008/)  is a document that provides guidelines and best practices on how to write Python code.

There are tools which are built and maintained by community to help us follow the rules across our project without 
having to teach each developer during code review. 
The tools which are used in this project are as follows:
1. [pycodestyle](https://pypi.org/project/pycodestyle/)  is a linter tool to check your Python code against the style conventions in PEP 8. It does not fix the issues
   rather it shows what the issues are. In order to fix it, there are other tools available.
2. [flake8](https://flake8.pycqa.org/en/latest/user/index.html) is also a linter which can be used to identify the PEP 8 violation in the code. It is a super set of pycodestyle and other tools.
3. [black](https://github.com/psf/black): Black is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting. You will save time and mental energy for more important matters.
I use `black` in this project to keep our code guide and style consistent.


Example: 
The below command when executed on a file will list out all the PEP 8 violation present on it.
It will not make any change to your code. That has to be done by the developer or use other tools
which can do that for you. 
```python
pycodestyle python_file.py
or
flake8 python_file.py # preferred tool
```

The below command will fix the PEP 8 violation which are reported by `pycodestyle`.
```python
black {source_file_or_directory}
```
Other alternative tools can be found [here](https://github.com/pycqa/pycodestyle/wiki/RelatedTools).
1. isort: A tool to sort the import in your python files. Black also does this for you. 
2. 