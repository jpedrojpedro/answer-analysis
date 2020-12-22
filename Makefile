.PHONY: imdb help

imdb:
	(cd infra/quira-imdb-virtuoso; docker-compose up)

help:
	@echo
	@echo 'Comandos disponíveis:'
	@echo
	@echo '- imdb: inicia virtuoso com IMDb'
	@echo '- brainz: inicia virtuoso com MusicBrainz (NOT IMPLEMENTED)'
	@echo '- help: exemplos de uso'
	@echo
