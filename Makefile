PIP = pip3

all: nothing

nothing:
	@echo ""

#TODO: add docs
zip:
	tar czf xdokou14.tgz src/* Makefile README.md division extensions Makefile Vyp.g4 vypcomp.sh

.PHONY: all setup zip nothing
