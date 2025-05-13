# Cloud Insights Test

This repository is an API that can be used to register plans and users subscriptions.

### Install

a) Configure environment file

```bash
cp .env-sample .env
```

b) Up the docker containers

```bash
docker-compose up -d --build
```

c)  Run migrations

```bash
docker-compose exec app flask db upgrade  
```