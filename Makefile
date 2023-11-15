all: run

run: requirements
	@python create_md.py

requirements:
	@pip install -qr requirements.txt

