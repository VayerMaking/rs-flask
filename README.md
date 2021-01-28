# rs-flask
flask site project for the subject rs (software development)

[![time tracker](https://wakatime.com/badge/github/VayerMaking/rs-flask.svg)](https://wakatime.com/badge/github/VayerMaking/rs-flask)

## the task

  ```sh
  http://tp-elsys.com/tasks/4
  ```

## How to use

  use our installer - ```install.sh``` or prepare manually

  change permissions of the file so it can be executed

  ```sh
  sudo chmod +x ./install.sh
  ```

  run the installer

  ```sh
  ./install.sh
  ```

  change the default value of the secret_key in ```config.py```

### OR

  create a virtual enviroment

  ```sh
  python3 -m venv rs-flask
  ```
  enter the newly created virtual enviroment

  ```sh
  source rs-flask/bin/activate
  ```
  install the requirements

  ```sh
  pip install -r requirements.txt
  ```

  create a folder for pictures

  ```sh
  mkdir /static/uploads
  ```

  start the server script

  ```sh
  python main.py
  ```

  navigate to ```http://127.0.0.1``` to see the website

## ToDo list

  - [x] register page
  - [x] login page
  - [x] index page
  - [x] add new post/ topic for logged users
  - [x] password encryption
  - [x] images in posts
  - [x] limit post to 25
  - [x] beautify design?

## Authors

  Martin Vayer - [VayerMaking](https://github.com/VayerMaking)

  Peter Damianov - [petardmnv](https://github.com/petardmnv)

  Victor Dimitrov - [Vic-Dim](https://github.com/Vic-Dim)
