DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
MESSAGING_FILE = docker_compose/messaging.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = main-app
MESSAGING_CONTAINER = main-kafka

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: messaging
messaging:
	${DC} -f ${MESSAGING_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down	

.PHONY: messaging-down
messaging-down:
	${DC} -f ${MESSAGING_FILE} down	

.PHONY: storages
storages: 
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down	

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash	

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: messaging-logs
messaging-logs:
	${DC} -f ${MESSAGING_FILE} logs -f

.PHONE: all
all:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} ${ENV} up --build -d

.PHONE: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} ${ENV} down

.PHONY: test
app-test:
	${EXEC} ${APP_CONTAINER} pytest