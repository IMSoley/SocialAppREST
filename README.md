# SocialAppREST

A social platform `REST-API` with voting system, `JWT` authentication and authorization. **The complete software life cycle of this project has been implemented.**

- API endpoint: `api.soleyman.xyz`
- Documentation: `api.soleyman.xyz/docs`

## How to run locally

- Install `python` 3.8+, with `pip` package manager
- Clone the repository `git clone https://github.com/IMSoley/SocialAppREST`
- Determine python version for virtual environment set up: `python --version` or `python3 --version` _(on linux)_
  - If you see `Python 3.*`, then you are good to go
  - Make sure you're in the `SocialAppREST` directory
  - Install virtualenv package: `pip install virtualenv`
  - Create virtual environment: `python -m venv venv`
  - Activate virtual environment
    - On linux: `source venv/bin/activate`
    - On windows: `.\venv\Scripts\activate`
  - Install dependencies: `pip install -r requirements.txt`
- Install PostgreSQL: `sudo apt install postgresql postgresql-contrib`, for windows [install postgresql](https://www.postgresql.org/download/windows/)
  - Create a database in PostgreSQL
- Rename `env_demo` to `.env`
- Change all `.env` variable values as per your PostgreSQL set up except `ALGORITHM`
  - To generate `secret_key`, run the following command on a bash/cmd prompt: `openssl rand -hex 32` _(openssl must be installed)_
- Run `alembic upgrade head`
- Run `uvicorn app.main:app --reload` _(--reload flag enables auto-reload on code changes, useful for development)_
- Visit `localhost:8000` to see the app

## Technology stack used

- [Python](https://www.python.org) - programming language
- [FastAPI](https://fastapi.tiangolo.com/) - framework for fast, scalable and secure APIs
- [JWT](https://jwt.readthedocs.io/) - JWT OAuth 2.0 authentication for secure API endpoints
- [PostgreSQL](https://www.postgresql.org/) - relational database management system
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for SQL databases
- [psycopg2](https://www.psycopg.org/) - PostgreSQL driver for Python
- [Alembic](https://alembic.sqlalchemy.org/) - database migration tool for SQLAlchemy
- [PyTest](https://docs.pytest.org/en/latest/) - unit testing framework
- [Postman](https://www.getpostman.com/) - for API testing
- [Docker](https://www.docker.com/) - containerizing the application for deployment using [`CI/CD`](#cicd-pipeline) pipelines
- [Heroku](https://www.heroku.com/) - [`CI/CD`](#cicd-pipeline) platform for deploying to cloud
- [Ubuntu](https://www.ubuntu.com/) - deployment on production server

## Features

The application is a `REST-API` with the following endpoints and features:

- [`/login`](app/routers/auth.py): authentication endpoint, returns a JWT bearer token for authentication and authorization
- [`/users`](app/routers/user.py): user management endpoint. To create a new user and to update an existing user the endpoint requires the `Authorization` header with the JWT bearer token
- [`/posts`](app/routers/post.py): post management endpoint, creates, updates, and deletes posts
- [`/vote`](app/routers/vote.py): vote management endpoint. A user can vote on a post and the vote is recorded in the database. Also, support self voting like Reddit

## How the application works

## Unit tests with `pytest`

## CI/CD pipeline

Automate the deployment of the application to cloud using GitHub Actions and Workflows.

```yaml
# deploy to cloud on push and pull request events
on: [push, pull_request]
```

On `build-app.yml`, there are two jobs `build` and `deploy`. The `deploy` job is [dependent](.github/workflows/build-app.yml#L69) on the `build` job. If the `build` job fails, the `deploy` job will not run and production servers will not be deployed.

1. [`build`](.github/workflows/build-app.yml#L6) job builds the application, runs unit tests and creates a Docker image
    - Docker image: [`social-app-rest:latest`](https://hub.docker.com/r/soleyman/social-app-rest)
2. [`deploy`](.github/workflows/build-app.yml#L67) job deploys the application to production servers
    - Production: [api.soleyman.xyz](https://api.soleyman.xyz)
    - Heroku: [socialapprest.herokuapp.com](https://socialapprest.herokuapp.com)

**Production server has been optimized for performance and scalability. Tmux panes explained below.**

1. API service has been up and running using the config defined in pane 2
2. Here is the config for the API service: [`api.service`](gunicorn.service)
3. [`Ngix`](nginx) is used to proxy the API service to the production server.
