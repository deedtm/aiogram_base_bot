# Aiogram Base Bot

This repository provides a template for building Telegram bots using [aiogram3](https://docs.aiogram.dev/), offering a well-structured foundation for your bot development.

## Features

- Modern async architecture with aiogram3
- Easy configuration using `.env` and `config.ini`
- User data stored in PostgreSQL
- Dockerized setup for quick deployment

## Getting Started

1. Rename the `config.ini.example` and `.env.example` files to `config.ini` and `.env` in the root directory.
2. Fill in your configuration details in these files.
3. Start the bot using Docker Compose:
   ```sh
   docker-compose up --build -d
   ```
4. To stop the bot, run:
   ```sh
   docker-compose down
   ```

## Database

- User information and other persistent data are stored in a PostgreSQL database.
- Make sure to configure your PostgreSQL connection details in the `.env` and `config.ini` files.

## Requirements

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- Telegram Bot Token (get it from [BotFather](https://t.me/BotFather))
