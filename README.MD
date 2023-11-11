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
