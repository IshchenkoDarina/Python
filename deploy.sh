heroku create
git push heroku main

heroku run python manage.py migrate
heroku run docker-compose up -d
heroku open
