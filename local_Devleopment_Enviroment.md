this short guide will help you setup local development environment.

# clone the repository
```
git clone https://github.com/afaki077/minitweet.git
cd minitweet
```

# Setup virtual environment
virtualenv and virtualenvwrapper is preferred
run the following command

```
mkvirtualenv minitweet
```

### install dependencies
assuming you are in the root directory of the project `minitweet/`

```
pip install -r requirements.txt
```

### create database
install postgresql if you don't have it and create two databases
one for development and another one for testing

### initializing the database with Flask-SQLAlchemy

```
python createdb.py
```


### environment variables
in order to run the app you need to set some environment variables

```
export CONFIG="config.DevConfig"
export SECRET_KEY="you-secret-key-here-use-os.urandom()"
export DATABASE_URL="postgresql:///your_dev_database_url_here"
export TESTING_DATABASE="postgresql:///your_testing_database_url_here"
export SECURITY_PASSWORD_SALT="this-should-be-complex"
export MAIL_USERNAME ="your-google-email-here"
export MAIL_PASSWORD ="you-gmail-password"
# if you have one sender (change the config if not)
export MAIL_DEFAULT_SENDER="deafult-sender"
```


# Run the server
```
python manage.py runserver
```

open your browser and go to `localhost:8000` to see the website in action.
