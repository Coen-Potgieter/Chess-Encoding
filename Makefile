
init:
	pip install -r requirements.txt

run:
	python3 src/main.py

api: 
	python3 src/api.py

upgrade:
	python3 src/upgrade_bots.py