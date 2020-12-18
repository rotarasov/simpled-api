release: python3 manage.py makemigrations && python3 manage.py migrate
web: daphne simpled.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker channels --settings=simpled.settings -v2