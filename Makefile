.PHONY: brainz help

brainz:
	(cd infra/quira-brainz-virtuoso; docker-compose up)

help:
	@echo
	@echo 'Comandos disponíveis:'
	@echo
	@echo '- imdb: utilizar servidor semanticweb via vpn'
	@echo '- brainz: inicia virtuoso com MusicBrainz'
	@echo '- help: exemplos de uso'
	@echo
