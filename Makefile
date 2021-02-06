.PHONY: imdb brainz help

imdb:
	(cd infra/quira-imdb-virtuoso; docker-compose up)

brainz:
	(cd infra/quira-brainz-virtuoso; docker-compose up)

help:
	@echo
	@echo 'Comandos disponíveis:'
	@echo
	@echo '- imdb: inicia virtuoso com IMDb'
	@echo '- brainz: inicia virtuoso com MusicBrainz'
	@echo '- help: exemplos de uso'
	@echo
