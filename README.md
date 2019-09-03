# it_hardware

## How to

1. Install Docker (<https://docs.docker.com/install/>)
1. Build Docker image: ``docker build -t it_hardware:latest .``
1. Run Docker container: ``docker run -p 5000:5000 it_hardware``
1. Open <http://127.0.0.1:5000/>
1. You can also run localy without Docker (install uWSGI first): ``uwsgi --ini uwsgi.ini``

## Tested on following environment

- Docker version 18.06.1-ce
- Python 3.7.3
- Ubuntu 18.04 (VirtualBox)
- Git 2.17.1

## Run tests locally

1. Install requirements: ``pip install -r requirements.txt``
1. Run from main directory: ``pytest --cov=. --cov-report=term-missing tests/``

## Time

Day 1 (02.09)

- Setup repository
- Setup environment
- Install flask and SQLalchemy
- Prepare database models
- uWSGI
- Docker
- Start API
- Documentation, articles, SO...

Day 2 (03.09)

- Finish API
- Improve API documentation
- Security: X-API-KEY header
- Tests (models + api) + Pytest + test coverage
- Commit!
