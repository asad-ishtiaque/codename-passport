# codename_passport

Check out the project's [documentation](http://asad-ishtiaque.github.io/codename_passport/).

## Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/) (Docker Engine + Compose)

For local Python development without Docker:

- Python 3.12+ and a virtualenv (see below)

## Docker (recommended)

1. Start **Docker Desktop** and wait until it reports the engine is running.
2. Copy environment variables and edit if needed:

```bash
cp .env.example .env
```

3. From the project root:

```bash
docker compose up --build
```

3. Open the app and docs:

| Service       | URL                   |
| ------------- | --------------------- |
| Django API    | http://localhost:8000 |
| MkDocs (live) | http://localhost:8001 |

Run a one-off command in the web container:

```bash
docker compose run --rm web ./manage.py createsuperuser
docker compose run --rm web pytest
```

Stop containers:

```bash
docker compose down
```

Remove the database volume (fresh Postgres):

```bash
docker compose down -v
```

## Local Python (virtualenv)

```bash
cd codename_passport
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You still need Postgres configured (see `DATABASE_URL` in `passport/config/common.py`) or use Docker for the database only:

```bash
docker compose up postgres -d
```

In `.env`, set `DATABASE_URL=postgres://postgres@localhost:5432/postgres` and `POSTGRES_HOST=localhost`, then:

```bash
set -a && source .env && set +a
./manage.py migrate
./manage.py runserver
```
