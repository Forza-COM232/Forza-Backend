# Docker Development Setup

This guide explains how to set up and run the Forza Backend development environment using Docker.

With Docker, you do **not** need to manually install Python, PostgreSQL, or create a Python virtual environment. Docker will provide the required application and database environment.

---

## Prerequisites

Before starting, make sure you have the following installed:

- Git
- Docker
- Docker Compose

Docker Compose is included with modern Docker installations as the `docker compose` command.

Verify your installation:

```bash
docker --version
docker compose version
git --version
```

If all commands return version information, you are ready to continue.

---

# 1. Clone the Repository

Clone the repository:

```bash
git clone <REPOSITORY_URL>
```

Navigate into the project:

```bash
cd Forza-Backend
```

---

# 2. Configure Environment Variables

Create a `.env` file in the project root.

If the project contains an `.env.example` file, copy it:

```bash
cp .env.example .env
```

Your `.env` file should contain the required PostgreSQL configuration:

```env
POSTGRES_USER=forza
POSTGRES_PASSWORD=change_me
POSTGRES_DB=forza_db
```

> **Important:** Never commit `.env` to Git. The `.env` file is intended for local development only.

---

# 3. Start the Development Environment

From the project root, run:

```bash
docker compose up --build
```

The first time you run this command, Docker will:

1. Build the FastAPI application image.
2. Install the Python dependencies using `uv`.
3. Create the PostgreSQL container.
4. Create the PostgreSQL database.
5. Create the required Docker network.
6. Start the FastAPI application.
7. Connect the FastAPI application to PostgreSQL.

Once the containers are running, the development environment is ready.

---

# 4. Access the API

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation:

```text
http://localhost:8000/docs
```

Alternative ReDoc documentation:

```text
http://localhost:8000/redoc
```

---

# 5. Verify the Containers

Open another terminal while Docker Compose is running:

```bash
docker compose ps
```

You should see the application and database containers running.

For example:

```text
NAME          STATUS
forza-api     Up
forza-db      Up (healthy)
```

The PostgreSQL container should eventually show:

```text
Up (healthy)
```

This means PostgreSQL is ready to accept connections.

---

# 6. Development Workflow

Once the Docker environment is running, you can proceed with development normally.

Start the development environment:

```bash
docker compose up
```

Make changes to the source code.

If the application is configured for automatic reload, changes to the source code will be reflected automatically.

If automatic reload is not enabled, restart the API container:

```bash
docker compose restart api
```

If you modify dependencies in `pyproject.toml`, rebuild the containers:

```bash
docker compose up --build
```

---

# 7. Running Docker in the Background

If you don't want Docker Compose logs occupying your terminal, run:

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs -f api
```

View PostgreSQL logs:

```bash
docker compose logs -f db
```

---

# 8. Stopping the Development Environment

To stop the containers:

```bash
docker compose down
```

This stops and removes the containers and Docker network.

Your PostgreSQL data will **not** be deleted because the database uses a persistent Docker volume.

You can start the environment again with:

```bash
docker compose up
```

---

# 9. Resetting the Database

If you need to completely reset the local PostgreSQL database, including all stored data:

```bash
docker compose down -v
```

Then start the environment again:

```bash
docker compose up --build
```

> **Warning:** `docker compose down -v` permanently removes the PostgreSQL Docker volume and therefore deletes the local database data.

Only use this when you intentionally want a fresh database.

---

# 10. Useful Docker Commands

### Start the environment

```bash
docker compose up
```

### Start and rebuild the application

```bash
docker compose up --build
```

### Start in the background

```bash
docker compose up -d
```

### Stop the environment

```bash
docker compose down
```

### Check container status

```bash
docker compose ps
```

### View all logs

```bash
docker compose logs
```

### Follow API logs

```bash
docker compose logs -f api
```

### Follow PostgreSQL logs

```bash
docker compose logs -f db
```

### Restart the API

```bash
docker compose restart api
```

### Open a shell inside the API container

```bash
docker compose exec api bash
```

If `bash` is not available:

```bash
docker compose exec api sh
```

### Connect to PostgreSQL

```bash
docker compose exec db psql -U forza -d forza_db
```

---

# 11. Installing New Python Dependencies

Python dependencies are managed through:

```text
pyproject.toml
uv.lock
```

When adding a new Python dependency, update the project using `uv`.

Make sure changes to both files are committed:

```text
pyproject.toml
uv.lock
```

After changing dependencies, rebuild the Docker environment:

```bash
docker compose up --build
```

This ensures that the new dependency is installed inside the API container.

---

# 12. PostgreSQL Connection

When the FastAPI application is running inside Docker, PostgreSQL is accessed using the Docker Compose service name.

The connection format is:

```text
postgresql://<USER>:<PASSWORD>@db:5432/<DATABASE>
```

For example:

```text
postgresql://forza:change_me@db:5432/forza_db
```

The hostname is:

```text
db
```

> **Important:** Do not use `localhost` as the PostgreSQL hostname from inside the API container.

`localhost` refers to the API container itself, not the PostgreSQL container.

Docker Compose provides internal DNS, allowing the API container to communicate with PostgreSQL using:

```text
db:5432
```

---

# 13. Project Structure

The Docker-related files are located in the project root:

```text
Forza-Backend/
├── src/
│   └── forza_backend/
│       ├── __init__.py
│       ├── main.py
│       └── ...
│
├── .env                  # Local environment variables (DO NOT COMMIT)
├── .env.example          # Environment variable template
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 14. First-Time Setup

For a new developer joining the project, the complete setup should only require:

```bash
git clone <REPOSITORY_URL>
cd Forza-Backend
cp .env.example .env
docker compose up --build
```

After Docker finishes starting the services, open:

```text
http://localhost:8000/docs
```

The FastAPI development environment is now ready.

---

# Troubleshooting

## Port 8000 Is Already in Use

If you receive an error indicating that port `8000` is already in use, another application may already be using the port.

You can change the host port in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"
```

The API would then be accessible at:

```text
http://localhost:8001
```

The container will still use port `8000`.

---

## Port 5432 Is Already in Use

This usually means another PostgreSQL installation or container is already running on your machine.

You can either stop the existing PostgreSQL service or change the host port:

```yaml
ports:
  - "5433:5432"
```

The API should still connect to:

```text
db:5432
```

because `5432` is the PostgreSQL port **inside the Docker network**.

---

## Check Why a Container Stopped

Check the container status:

```bash
docker compose ps
```

Then inspect the API logs:

```bash
docker compose logs api
```

Or PostgreSQL logs:

```bash
docker compose logs db
```

---

## Start From a Completely Clean Environment

If you encounter persistent Docker issues, you can rebuild everything:

```bash
docker compose down -v
docker compose build --no-cache
docker compose up
```

> **Warning:** This removes the local PostgreSQL data.

---

# Development Rules

When working on the project:

1. Do not commit `.env`.
2. Commit changes to `pyproject.toml` and `uv.lock` when dependencies change.
3. Do not commit `.venv/`.
4. Use Docker Compose for the local PostgreSQL database.
5. Use the `db` hostname when connecting to PostgreSQL from the API container.
6. Do not manually modify the PostgreSQL database container's files.
7. Use database migrations for schema changes once migrations are configured.

---

# Quick Start

For experienced developers, the entire setup can be summarized as:

```bash
git clone <REPOSITORY_URL>
cd Forza-Backend
cp .env.example .env
docker compose up --build
```

Then open:

```text
http://localhost:8000/docs
```

The FastAPI application and PostgreSQL database are now running and ready for development.