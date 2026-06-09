<p align="center">
  <h1 align="center">🎧 DSupport</h1>
  <p align="center"><strong>Support service — Real-Time Tech Support using WebSockets, Kafka, Telegram</strong></p>
  <p align="center"></p>
</p>

**DSupport** is a real-time, multi-platform technical support service designed for seamless communication between users and support teams

- creation and management of support chats  
- real-time messaging  
- WebSocket-based connections for live communication  
- message streaming via WebSocket  
- chat deletion and lifecycle management  

### Tech Stack

- **FastAPI** — high-performance async python framework  
- **Aiogram** — Telegram bot integration  
- **WebSockets** — real-time communication  
- **Kafka (aiokafka)** — event streaming and messaging  
- **MongoDB (Motor)** — asynchronous non-sql database layer  
- **SQLite (aiosqlite)** — lightweight local DBMS  
- **FastStream** — message broker abstraction  
- **Dishka & Punq** — dependency injection libs
- **Pytest** — automated test coverage 

Built with scalability, async-first design, and real-time performance in mind.

## How to Use

1. **Clone the repository and move into it:**

```bash
git clone https://github.com/RobunGid/DSupport.git
cd DSupport
```

2. **Copy and fill .env file:**

```bash
cp .env.example .env
vim .env
```

3. **Run `make all` to start all containers**

```bash
make all
```

### Make Commands

#### All Services
* `make all` - up all services (app, messaging, storages, tg-bot)
* `make all-down` - down all services

#### App
* `make app` - up application container
* `make app-down` - down application container
* `make app-logs` - follow the logs in app container
* `make app-shell` - run app container shell
* `make app-test` - run app unit tests
* `make app-test-debugger` - run app tests with debugpy listener on port 5679

#### Messaging
* `make messaging` - up messaging services (Zookeeper, Kafka, Kafka UI)
* `make messaging-down` - down messaging services
* `make messaging-logs` - follow the logs in all messaging containers

#### Storages
* `make storages` - up storage services (MongoDB, Mongo Express)
* `make storages-down` - down storage services
* `make storages-logs` - follow the logs in all storage containers

#### Telegram Bot
* `make tg-bot` - up telegram bot services
* `make tg-bot-down` - down telegram bot services

---

#### Zookeeper
* `make zookeeper-logs` - follow the logs in Zookeeper container
* `make zookeeper-shell` - run Zookeeper container shell

#### Kafka
* `make kafka-logs` - follow the logs in Kafka container
* `make kafka-shell` - run Kafka container shell

#### Kafka UI
* `make kafka-ui-logs` - follow the logs in Kafka UI container
* `make kafka-ui-shell` - run Kafka UI container shell

#### MongoDB
* `make mongo-logs` - follow the logs in MongoDB container
* `make mongo-shell` - run MongoDB container shell

#### Mongo Express
* `make mongo-express-logs` - follow the logs in Mongo Express container
* `make mongo-express-shell` - run Mongo Express container shell

#### Telegram Bot
* `make tg-bot-logs` - follow the logs in telegram bot container
* `make tg-bot-shell` - run telegram bot container shell
* `make tg-bot-consumer-logs` - follow the logs in telegram bot consumer container
* `make tg-bot-consumer-shell` - run telegram bot consumer container shell

#### SQLite Web
* `make sqliteweb-logs` - follow the logs in SQLite Web container
* `make sqliteweb-shell` - run SQLite Web container shell

* `poetry run pre-commit run --all-files` - run all pre-commit hooks (linters, formatters)