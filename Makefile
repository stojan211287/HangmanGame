.PHONY: play venv

dev: venv requirements.txt .pre-commit-config.yaml
	./venv/bin/pip-sync requirements.txt
	./venv/bin/pre-commit install
format:
	./venv/bin/black ./hangman
lint:
	./venv/bin/flake8 ./hangman
play:
	python3 ./hangman/main.py

requirements.txt: requirements.in
	./venv/bin/pip-compile requirements.in --output-file=requirements.txt

venv:
	python3 -m venv venv
	./venv/bin/pip3 install --upgrade pip
	./venv/bin/pip3 install pip-tools
