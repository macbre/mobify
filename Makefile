project_name = mobify
coverage_options = --include='$(project_name)/*' --omit='$(project_name)/test/*,$(project_name)/config.py,*__init__.py'

install:
	python setup.py install

test:
	py.test -x $(project_name)

coverage:
	rm -f .coverage*
	rm -rf htmlcov/*
	coverage run -p -m py.test -x $(project_name)
	coverage combine
	coverage html -d htmlcov $(coverage_options)
	coverage xml -i
	coverage report $(coverage_options)

lint:
	pep8 $(project_name)/; pylint $(project_name)/

publish:
	python setup.py sdist upload -r pypi
