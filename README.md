# BookLib

## Run Fastapi app
```
uvicorn src:app --reload
```

## API backend Fastapi
```
http://localhost:8000/docs
```

## Pg admin
```
http://localhost:5050/browser/
```

## Alembic
#### Create alembic template for async database migration
```
alembic init -t async migrations
```

#### generate a revision base on our moedel
```
alembic revision --autogenerate -m "init"
```


#### Run the latest migration
```
alembic upgrade head
```


#### How to generate a JWT SECRET KEY
```
import secrets
secrets.token_hex(16)
```