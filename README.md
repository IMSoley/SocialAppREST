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
- Change all `.env` variable values as per your PostgreSQL set up except [`ALGORITHM`](env_demo#L7)
  - To generate [`secret_key`](env_demo#L6), run the following command on a bash/cmd prompt: `openssl rand -hex 32` _(openssl must be installed)_
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

Without authentication, the application does not allow any user to create, update, or delete posts. The application also does not allow a user to vote on a post. It will show an authentication error message if a user tries to create, update, or delete a post without authentication. It will show an authentication error message if a user tries to vote on a post without authentication.

![authentication](https://user-images.githubusercontent.com/13655344/184506280-68c395ea-46bf-4d9e-ac31-4d2f1701c448.png)

To create an account, the user must provide a email, and password. The email must be unique. The password must be at least 8 characters long. `/users` endpoint will return a `201 Created` response if the user is successfully created.

Upon requestiong a `/login` endpoint, the application verifies the credentials and returns a JWT bearer token for authentication and authorization.

![login](https://user-images.githubusercontent.com/13655344/184506581-fd15ece1-c773-4973-b901-695da0db5e27.png)

Here's how the JWT bearer token works in the application:

![JWT Diagram](https://user-images.githubusercontent.com/13655344/184510184-b9ec5e90-a393-4141-b0ee-b35755cbb20d.png)

At the end of the token in blue color is the token signature. The token signature is a hash of the token [`payload`](app/oauth2.py#L24) and the [`secret key`](app/oauth2.py#L11).

The purpose of the signature is to prevent tampering with the token by an attacker:

![JWT Signature](https://user-images.githubusercontent.com/13655344/184509974-a25f6cfa-da21-467c-9f0e-011693164481.png)

Once the user is authenticated, user access to the application is granted. The user can use all the endpoints in the application.

## Unit tests with `pytest`

The configuration for unit testing is done in the [`conftest.py`](tests/conftest.py) file:

- defined test database
- defined all the fixtures
- all the fixtures are available in the tests directory

Test cases are defined in the [`tests/test_*.py`](tests/test_*.py) files, where `*.py` is the name of the test file.

## CI/CD pipeline

Automate the deployment of the application to cloud using GitHub Actions and Workflows.

```yaml
# deploy to cloud on push and pull request events
on: [push, pull_request]
```

On `build-app.yml`, there are two jobs `build` and `deploy`. The `deploy` job is [dependent](.github/workflows/build-app.yml#L69) on the `build` job. If the `build` job fails, the `deploy` job will not run and production servers will not be deployed.

1. [`build`](.github/workflows/build-app.yml#L6) job builds the application, runs [`unit tests`](#unit-tests-with-pytest) and creates a Docker image
    - Docker image: [`social-app-rest:latest`](https://hub.docker.com/r/soleyman/social-app-rest)
2. [`deploy`](.github/workflows/build-app.yml#L67) job deploys the application to production servers
    - Production: [api.soleyman.xyz](https://api.soleyman.xyz)
    - Heroku: [socialapprest.herokuapp.com](https://socialapprest.herokuapp.com)

**Production server has been optimized for performance and scalability. Tmux panes explained below.**

1. API service has been up and running using the config defined in pane 2
2. Here is the config for the API service: [`api.service`](gunicorn.service)
3. [`Ngix`](nginx) is used to proxy the API service to the production server.

![production optimization](https://user-images.githubusercontent.com/13655344/184505955-48fe3edf-fff6-47cc-9f12-14a057513fb0.png)

## License

MIT License
