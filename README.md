python
=======
setup
	pip3 install sanic && \
	pip3 install jinja2

run
	python3 main.py

test
	python3 -m unittest discover

javascript
===========
setup
	npm install mocha --save-dev

execute tests
	./node_modules/mocha/bin/mocha
	or
	npm test
