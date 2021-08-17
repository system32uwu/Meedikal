source backend/venv/bin/activate && pip install -r backend/requirements.txt
cd frontend & yarn build && cd ../backend & python app.py
# Flask will serve the compiled react app, and the api