VERSION = $(shell python setup.py --version)

test:
	python setup.py nosetests

release:
	git tag $(VERSION)
	git push origin $(VERSION)
	git push origin master
	python setup.py sdist bdist_wheel upload

watch:
	bundle exec guard

run:
	cd example_project && python manage.py runserver

.PHONY: test release watch run
