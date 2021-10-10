$ErrorActionPreference= 'silentlycontinue'

Set-Location backend

$run = $Env:MEEDIKAL_HAS_RUN_YET

if ((-not $run) -or ($run -eq 0)) {
    python -m venv venv 

    ./venv/Scripts/activate
    pip install -r requirements.txt

    Move-Item .example.env .env
    Move-Item config.example.py config.py
    $Env:MEEDIKAL_HAS_RUN_YET = 1
}
else {
    ./venv/Scripts/activate
}

flask run | Start-Process "http://localhost"