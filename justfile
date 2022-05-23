set shell := ["powershell.exe", "-c"]

test:
 coverage run -m unittest discover

cov: test
 coverage html
 Start-Process "http://localhost:8000/htmlcov/"
 python -m http.server

publish: build_doc test bump
 python setup.py sdist bdist_wheel
 twine check dist/*
 twine upload dist/*

build_doc:
 python build_readme_examples.py

bump flags="":
 python version_machine.py -L {{flags}}