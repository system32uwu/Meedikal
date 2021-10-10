Set-Location backend

if (-not $Env:MEEDIKAL_HAS_RUN_YET){
    python -m venv venv 

    ./venv/Scripts/activate
    pip install -r requirements.txt

    Move-Item .example.env .env
    $Env:MEEDIKAL_HAS_RUN_YET = 1
}

flask run | Start-Process "http://localhost"