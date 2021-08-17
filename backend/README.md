# Technologies used

- Flask (web server)
- GraphQL (interface)
- PostgreSQL (database)
- SQLAlchemy (ORM)

## NOTES

- When creating new models, import them in migrations/env.py

To create the schema, run:

```sh
flask db init
```

```sh
flask db migrate
```

```sh
flask db upgrade
```
