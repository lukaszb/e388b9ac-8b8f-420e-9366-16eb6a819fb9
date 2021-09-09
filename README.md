
Run with docker:

    docker compose up


For local development:

    python -m venv .venv --prompt swheros
    source .venv/bin/activate
    pip install -r requirements.txt
    ./src/manage.py migrate
    ./src/manage.py runserver
    
