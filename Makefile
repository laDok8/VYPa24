PIP = pip3

all: nothing

nothing:
	@echo ""

zip:
	tar czf xdokou14.tgz src/* Makefile README.md division extensions Makefile Vyp.g4 vypcomp doc/*

.PHONY: all setup zip nothing
