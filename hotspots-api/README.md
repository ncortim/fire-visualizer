# Hotspots REST API
A REST API for forest fire visualizations


# Requirements

- Server with python3.11, docker compose, or docker (new version with compose included)
- Clone the repository and change directory
```bash
$ git clone https://github.com/yahuarlocro/fire-visualizer.git
$ cd fire-visualizer/hotspots-api
```

# Usage

First of all clone the repository

1. install poetry, create a virtual environment, activate it and install dependencies

```bash
$ pip install poetry
$ poetry env use python 3.11
$ poetry shell
$ poetry install
$ poetry show
```

poetry show is used to confirm all dependencies have been installed

2. deploy hotspots api

```bash
$ uvicorn --host 0.0.0.0 --port 8000 main:app
```

If needed, change environment variables defined in ./hotspots/.env

3. To access the REST API go to http://localhost:8000/docs


## Deploy hotspots api using docker

1. Locate to repository hotspots-api directory

```bash
# cd fire-visualizer/hotspots-api
```

2. Build docker image for hotspots-api

```bash
$ bash build.sh 
```

3. Change to dockersetup directory and execute docker command

```bash
$ docker compose up -d
```
