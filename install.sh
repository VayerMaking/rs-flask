python3 -m venv rs-flask
source rs-flask/bin/activate
pip install -r requirements.txt
mkdir /static/uploads
echo "secret_key = "qwerty123"" > config.py
