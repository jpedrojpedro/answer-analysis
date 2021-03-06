.PHONY: brainz help run

run:
	PYTHONPATH=$(shell pwd) python src/main.py

help:
	@echo
	@echo 'Comandos disponíveis:'
	@echo
	@echo '- run: inicia o programa'
	@echo '- imdb: utilizar servidor semanticweb via vpn'
	@echo '- brainz: utilizar servidor semanticweb via vpn'
	@echo '- help: exemplos de uso'
	@echo
