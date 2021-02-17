.PHONY: brainz help run

run:
	PYTHONPATH=$(shell pwd) python src/main.py

brainz:
	(cd infra/quira-brainz-virtuoso; docker-compose up)

help:
	@echo
	@echo 'Comandos disponíveis:'
	@echo
	@echo '- run: inicia o programa'
	@echo '- imdb: utilizar servidor semanticweb via vpn'
	@echo '- brainz: inicia virtuoso com MusicBrainz'
	@echo '- help: exemplos de uso'
	@echo
