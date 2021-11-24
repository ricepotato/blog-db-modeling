PYTHONPATH=$(shell pwd)

test:
	PYTHONPATH=$(PYTHONPATH)/src/blog coverage run -m pytest src/tests -v --junitxml=unittest.xml
	coverage report