$ErrorActionPreference= 'silentlycontinue'

Set-Location backend

$run = $Env:MEEDIKAL_HAS_RUN_YET

if ((-not $run) -or ($run -eq 0)) {
    python -m venv venv # create virtual environment #

    ./venv/Scripts/activate # activate virtual environment #
    pip install -r requirements.txt # install requirements #

    Move-Item .example.env .env # replace dotenv file #
    Move-Item config.example.py config.py # replace config file #
    ./util/createDb.py && ./util/createAdmin.py # create db and admin #
    
    Set-Location frontend/static/styles 
    npm install # install dependencies #
    npm run build # build and minify tailwindcss file #
    Set-Location ../../../
    $Env:MEEDIKAL_HAS_RUN_YET = 1
}
else {
    ./venv/Scripts/activate
}

waitress-serve --port=80 wsgi:app | Start-Process "http://127.0.0.1/"