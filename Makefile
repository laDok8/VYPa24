PIP = pip3

all: setup

setup:
	$(PIP) install -r requirements.txt


#TODO: add docs
zip:
	tar czf xdokou14.tgz src/* Makefile README.md division extensions Makefile requirements.txt Vyp.g4

.PHONY: all setup zip
