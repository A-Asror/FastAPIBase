#!/bin/sh

# Install package
# pip install -r src/requirements/dev.txt

echo "DB Connection --- Establishing . . ."

# fast-api-postgresql this name of db, if the database name is called differently,set another name
while ! nc -z fast-api-base-project-postgres-name 5432; do

    echo "DB Connection -- Failed!"

    sleep 1

    echo "DB Connection -- Retrying . . ."

done

echo "DB Connection --- Successfully Established!"

until alembic upgrade head
do
    echo "Migration..."
    sleep 7
done

# Start Uvicorn
uvicorn main:backend_app --host 0.0.0.0 --port 8000 --workers 4 --reload

exec "$@"
