
init:
	pip install -r requirements.txt

setup:
	python3 src/main.py setup $(word 2, $(MAKECMDGOALS))

encrypt:
	python3 src/main.py encrypt $(word 2, $(MAKECMDGOALS))

play_a:
	python3 src/main.py play_a $(word 2, $(MAKECMDGOALS))

play_b:
	python3 src/main.py play_b $(word 2, $(MAKECMDGOALS))

load:
	python3 src/main.py load $(word 2, $(MAKECMDGOALS))

decrypt:
	python3 src/main.py decrypt $(word 2, $(MAKECMDGOALS))

upgrade:
	python3 src/upgrade_bots.py

# For Debugging

run encr:
	python3 src/encrytion.py

run api: 
	python3 src/api.py

run a:
	python3 src/play_a.py

run b: 
	python3 src/play_b.py
%:
	@:
