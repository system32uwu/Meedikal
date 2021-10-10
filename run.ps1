Set-Location backend

python -m venv venv 

pip install -r requirements.txt

Move-Item .example.env .env

flask run