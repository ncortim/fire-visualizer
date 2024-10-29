# Hotspots web map
A web map for forest fire visualizations


# Requirements

- Server with python3.11, docker compose, or docker (new version with compose included)
- Clone the repository and change directory
```bash
$ git clone https://github.com/ncortim/fire-visualizer.git
$ cd fire-visualizer/visualizer
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

'poetry show' is used to confirm all dependencies have been installed

2. deploy web map visualizer

```bash
$ gunicorn --bind 0.0.0.0:5000 main:app
```

If needed, change environment variables defined in ./visualizer/src/.flaskenv

3. To access the web map go to http://localhost:5000


## Deploy web map visualizer using docker

1. Locate to repository visualizer directory

```bash
# cd fire-visualizer/visualizer
```

2. Build docker image for visualizer

```bash
$ bash build.sh 
```

3. Change to dockersetup directory and execute docker command

```bash
$ docker compose up -d
```
