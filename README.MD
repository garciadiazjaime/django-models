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

## How to export DB to JSON

- Open sqlite shell

```bash
sqlite3 db.sqlite3
```

- Generate JSON

```bash
.mode json
.once gift.json
SELECT g.id, g.title, g.description, g.price, g.store_url, g.image_url, c.name as category, p.name as price_range FROM gift_gift g INNER JOIN gift_category c ON g.category_id == c.id INNER JOIN gift_pricerange p ON g.price_range_id == p.id;
```

- Show tables

```bash
.tables
```

- Describe table

```bash
pragma table_info('table_name');
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

The backup file will be saved in the `./data` directory, defined by the `DBBACKUP_STORAGE_OPTIONS ` var in the [settings.py](https://github.com/garciadiazjaime/django-models/blob/main/mint_models/settings.py) file.

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
select count(*) as count, provider from event_event where updated > (CURDATE() - INTERVAL 1 MONTH)  group by provider order by provider desc;
```
