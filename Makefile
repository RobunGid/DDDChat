DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

APP_FILE = docker_compose/app.yaml
MESSAGING_FILE = docker_compose/messaging.yaml
STORAGES_FILE = docker_compose/storages.yaml
TG_BOT_FILE = docker_compose/tg_bot.yaml

APP_CONTAINER = main-app
MESSAGING_CONTAINER = main-kafka
TG_BOT_CONTAINER = telegram-bot

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

.PHONY: all
all:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} -f ${TG_BOT_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} ${ENV} down

.PHONY: test
app-test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: tg-bot
tg-bot:
	${DC} -f ${TG_BOT_FILE} ${ENV} up --build -d

.PHONY: tg-bot-down
tg-bot-down:
	${DC} -f ${TG_BOT_CONTAINER} down	

.PHONY: tg-bot-logs
tg-bot-logs:
	${LOGS} ${TG_BOT_CONTAINER} -f

.PHONY: tg-bot-shell
tg-bot-shell:
	${EXEC} ${TG_BOT_CONTAINER} bash	