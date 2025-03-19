1. Complie binar by setup.py 
a) change name of pyproject.toml to any other as a backend file. It is requried 
to isolate the file during running setup.py! 
b) run python setup.py bdist_wheel
c) uv add dist/name_binary.whl is to add the library to venv python

2. Compile all project 
# add  library to project which was created by hatching
uv build pyRunOF
uv add pyRunOF/dist/pyrunof-0.1.0-py3-none-any.whl

Могут быть проблемы с локальной установкой pyRUnOF удалить uv.lock
or run command with --freez

uv build --build-constraint constraints.txt --require-hashes
pip install dist/pyRunOF-0.1b0-py3-none-any.whl

#### DEVELOPMENT by uv#####

An editable installation is not used for path dependencies by default. An editable 
installation may be requested for project directories:
uv add --editable ./pyRunOF

OR add in toml

[project]
...
dependencies = ["pyRunOF",
    ...
]

[tool.uv.sources]
pyRunOF = {path = "./pyRunOF", editable = true }
OR
[tool.uv.sources]
pyRunOF = {path = "./pyRunOF", package = true }
