# aiogram-bot-structure

A structured template for a Telegram bot.  
**Tech Stack**: `aiogram`, `SQLAlchemy`, `Alembic`, `PostgreSQL`, `Pydantic Settings`, `Uvicorn`.

## Project Overview

This project provides a structured foundation for building Telegram bots using the `aiogram` framework. It includes database integration, configuration management, and deployment support.

### Features:
- **Configuration Management**: The project uses `Pydantic Settings` for managing environment variables and configurations.
- **Database Integration**: PostgreSQL is used as the database, with `SQLAlchemy` for ORM and `Alembic` for migrations.
- **Docker Support**: A `docker-compose` file is included for running the project in Docker containers.
- **Nginx Example**: An example `nginx` configuration file (`nginx.example`) is provided for deploying the bot on a server.

## Setup Instructions

### Prerequisites:
1. **PostgreSQL Database**:
   - Create a PostgreSQL server (e.g., using `pgAdmin4`) or run it via Docker.
   - Update the database credentials in the `.env` file.

2. **Environment Variables**:
   - Use the provided `env.example` file as a template to create your `.env` file.
   - Configure the required variables for the bot, database, and admin settings.

### Running the Project:
1. **Local Setup**:
   - Install dependencies using `pip install -r requirements.txt`.
   - Set the webhook URL. For development, you can use [ngrok](https://ngrok.com) to expose your local server to the internet.
   - Run the bot locally using `uvicorn app.main:app`.

2. **Docker Setup**:
   - Use the `docker-compose.yml` file to build and run the project in Docker containers:
     ```bash
     docker-compose up --build
     ```

3. **Database Migrations**:
   - Use `Alembic` to create and apply database migrations:
     ```bash
     alembic revision --autogenerate -m "Initial migration"
     alembic upgrade head
     ```

### Deployment:
- Use the `nginx.example` file as a reference for configuring Nginx to deploy the bot on a server.

## File Structure

```plaintext
├── app/
│   ├── bot/                # Bot-related logic (handlers, filters, etc.)
│   ├── core/               # Core utilities (config, database, logging)
│   ├── dao/                # Data Access Objects (DAO) for database operations
│   ├── users/              # User-related models and DAO
│   └── migrations/         # Alembic migrations
├── docker-compose.yml      # Docker Compose configuration
├── nginx.example           # Example Nginx configuration for deployment
├── env.example             # Example environment variables file
└── README.md               # Project documentation