coverage:
	coverage run --source manta -m pytest

test:
	tox -e "black,mypy,flake8"

test-full:
	tox

test-short:
	tox -e "black,mypy,flake8,py36"

format:
	tox -e format

clean-test: 
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/