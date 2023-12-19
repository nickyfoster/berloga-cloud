# Berloga Cloud

## Quickstart
Get up and running with Berloga Cloud using Docker Compose. This guide assumes that you have Docker and Docker Compose installed on your system.

### Starting the Service
To start the service, run:
```bash
docker-compose up -d --build
```

### Migrate the Database
To migrate the database, run:
```bash
docker-compose exec backend aerich upgrade
```

### Accessing the Admin Panel
Once the services are up:
1. Retrieve the admin password by executing:
    ```bash
    curl http://localhost:8081/create_admin
    ```
2. Log in with the username admin and the password from the curl output at http://localhost:8080.


### Local Development
For local development, follow these instructions to set up the frontend and backend environments.

### Frontend

#### Setting Environment Variables
Copy the .env.example file to .env and set the environment variables:
```bash
cp .env.example .env
```

#### Start Vue application
To start the frontend server, run:
````bash
npm run server
````

### Backend

#### Installing Dependencies
Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

#### Setting Environment Variables
Copy the .env.example file to .env and set the environment variables:
```bash
cp .env.example .env
```

#### Initializing Database and Migrations
Initialize the database and set up migrations:
```bash
aerich init -t src.database.config.TORTOISE_ORM
aerich init-db
```

#### Migrating Schemas
To migrate database schemas, run:
```bash
aerich migrate
aerich upgrade
```

#### Starting FastAPI Server
Start the backend service with the following command:
````bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8081
````


