## How to Setup

- Clone repo

```bash
git clone git@github.com:garciadiazjaime/django-models.git
```

- Move inside repo

```bash
cd django-models
```

- Install virtualenv

```bash
brew install virtualenv
```

- Create virtual environment

```bash
virtualenv venv
```

- Activate virtual environment

```bash
source venv/bin/activate
```

- Install packages

```bash
pip install -r requirements.txt
```

- Run Migrations

```bash
./manage.py migrate
```

- Create super user (_Optional_)

```bash
./manage.py createsuperuser
```

You can use super user on [admin site](http://127.0.0.1:8000/admin)

- Run Server

```bash
./manage.py runserver
```

## Database

### spin mysql container

```bash
docker run -e MYSQL_ROOT_PASSWORD=admin -d -p 3306:3306 mysql
```

### connect to DB

```bash
mysql -h 127.0.0.1 -uroot -p
```

## Deploy

```bash
fab2 deploy
```

## DB

### Backup DB

[django-dbbackup](https://django-dbbackup.readthedocs.io/en/master/index.html)

```bash
./manage.py dbbackup
```

If there's an error with mysql-dump try installing:

```bash
apg-get update
apt-get install -y mariadb-client
```

The backup file will be saved in the `./data` directory, defined by the `DBBACKUP_STORAGE_OPTIONS` var in the [settings.py](https://github.com/garciadiazjaime/django-models/blob/main/mint_models/settings.py) file.

### Restore DB

```bash
./manage.py dbrestore
```

### spin api container

```bash
docker run -e DB_NAME=livemusic -e DB_USER=root -e DB_HOST=host.docker.internal -d -p 8000:8000 garciadiazjaime/django-models
```

### Events Updated Last Month

```
SELECT
  DATE_FORMAT(updated, '%Y-%m-%d') as date,
  count(*) AS count,
  provider
FROM event_event
WHERE updated > (CURDATE() - INTERVAL 1 MONTH)
GROUP BY provider, date
ORDER BY date DESC, count DESC
;
```

## Export Tensorflow model

`fab2 model` takes care of all the tasks needed: `generate .csv`, `save model`, and `convert  model`

```sh
fab2 model
```

### Generate `.csv`

```sh
./manage.py report
```

### Saved model

```sh
./manage.py artist_popularity_model
```

### Convert model

```sh
tensorflowjs_converter --input_format=tf_saved_model data/model/saved_model data/public
```
