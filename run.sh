source backend/venv/bin/activate && pip install -r backend/requirements.txt

cd frontend & yarn build
mv build ../backend/build
cd ../backend & python server.py
cd ../
# Flask will serve the compiled react app, and the api