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

### Implemented Commands

* `make app` - up application and database/infrastructure
* `make app-logs` - follow the logs in app container
* `make app-down` - down application and all infrastructure
* `make app-shell` - run app container shell
* `make test` - run app unit tests
* `poetry run pre-commit run --all-files` - run all pre-commit hooks (linters, formatters)