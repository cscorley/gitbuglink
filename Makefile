all: compile test

compile:
	echo "Nothing to do here."

test:
	nosetests tests

init:
	virtualenv env
	pip install -r requirements.txt --use-mirrors
