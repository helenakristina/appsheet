debug:
	python ./app/app.py --debug True

test:
	pytest ./tests/ --cov=app tests/

run:
	python ./app/app.py --debug False
