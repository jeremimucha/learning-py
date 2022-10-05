# Complaint system - main application

## Initializing migrations with alembic:

1. Create the models for the application
2. Initialize the migrations:
   ```bash
   $ alembic init migrations
   ```
3. In `alembic.ini` set the `sqlalchemy.url` with a templated string, instead of hardcoding the db credentials.
4. In `migrations/env.py:
   1. import `metadata` from `db` and set `target_metadata = metadata`
   2. import `models`
   3. configure the `alembic.ini` using the `decouple.config`, remember to import with an alias
5. Autogenerate the initial revision and upgrade:
   ```bash
   $ alembic revision --autogenerate -m 'Initial'
   $ alembic upgrade head
   ```
