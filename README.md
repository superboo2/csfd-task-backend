# csfd-task-backend

### Task
#### Scrape top 300 films from CSFD and save them to the database. 
#### Add search for the films by name without diacritics.
#### Make film and actor details clickable. 
#### After clicking on the actor in the film detail, user can see all the actor's films (the same applies to actor detail).


### Install dependencies
```sh
pip install -r requirements.txt
```

### Settings
#### Add the .env file to the csfd-task-backend directory  (set by .env_example).
### Database (or insert prepared db file (db.sqlite3_csfd_task) to the csfd-task-backend directory)
```sh
python manage.py makemigrations
python manage.py migrate
```

### Run
```sh
python manage.py runserver
```

### Scrapes films with actors from CSFD and saves them to the database.
```sh
python manage.py scrape_and_process
```

### Code
#### Black
```sh
black -l 120 --target-version py310 .
```
#### Pylint (with Django Pylint)
```sh
pylint app
```

### Tests
```sh
python manage.py test
```
# csfd-task-backend
