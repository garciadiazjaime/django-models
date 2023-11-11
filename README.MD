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
