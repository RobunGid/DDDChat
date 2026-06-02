# Chat with FastAPI, DDD, WebSockets


- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/RobunGid/DDDChat.git
   cd DDDChat

2. Install all required packages in `Requirements` section.


### Implemented Commands

* `make app` - up application and database/infrastructure
* `make app-logs` - follow the logs in app container
* `make app-down` - down application and all infrastructure
* `make app-shell` - run app container shell
* `make test` - run app unit tests
* `poetry run pre-commit run --all-files` - run all pre-commit hooks (linters)