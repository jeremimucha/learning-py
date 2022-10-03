# FastAPI app

## Starting the app

```
$ uvicorn main:app --reload
```


## Setup migrations

Install and initialize alembic migrations
```
pip install alembic
alembic init migrations
```

Generate initial migrations
```
alembic revision --autogenerate -m "initial"
```

## Interactive testing

Go to `127.0.0.1:8000/docs` -> built in SWAGGER - built-in API documentation UI.


## Dependencies

* PostgreSQL
    - username: postgres
    - port: 5432
    - database: fastapi_store
* Postman
