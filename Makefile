all: compile test

compile:
	echo "Nothing to do here."

test:
	nosetests tests

init:
	test -d env || virtualenv env --python=python2.7
	. env/bin/activate; pip install -r requirements.txt --use-mirrors
