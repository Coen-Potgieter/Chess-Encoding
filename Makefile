
init:
	pip install -r requirements.txt

run:
	python3 src/encrytion.py

api: 
	python3 src/api.py

upgrade:
	python3 src/upgrade_bots.py


a:
	python3 src/play_a.py

b: 
	python3 src/play_b.py