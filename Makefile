project_name = mobify
coverage_options = --include='$(project_name)/*' --omit='$(project_name)/test/*,$(project_name)/config.py,*__init__.py'

install:
	python setup.py install

test:
	py.test -x $(project_name)

lint:
	pylint $(project_name)/
