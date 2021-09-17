rm -r -Force .\backend\build
.\backend\venv\Scripts\activate

pip install -r backend\requirements.txt

Set-Location .\frontend
yarn build
Move-Item build ../backend/build

Set-Location ..\backend
python server.py # Flask will serve the compiled react app, and the api
Set-Location ..\