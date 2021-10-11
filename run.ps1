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
    
    Set-Location statc/styles 
    npm install # install dependencies #
    npm run build:css # build and minify tailwindcss file #
    $Env:MEEDIKAL_HAS_RUN_YET = 1
}
else {
    ./venv/Scripts/activate
}

flask run | Start-Process "http://localhost"