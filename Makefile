install:
	poetry install

project:
	poetry run python -m labyrinth_game.main

lint:
	poetry run ruff check .

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install --force-reinstall dist/*.whl
