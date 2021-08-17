.\backend\venv\Scripts\activate && pip install -r backend\requirements.txt

Set-Location .\frontend
yarn build 

Set-Location ..\backend
python app.py # Flask will serve the compiled react app, and the api