DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

APP_FILE = docker_compose/app.yaml
MESSAGING_FILE = docker_compose/messaging.yaml
STORAGES_FILE = docker_compose/storages.yaml
TG_BOT_FILE = docker_compose/tg-bot.yaml
TG_BOT_CONSUMER_FILE = docker_compose/tg-bot-consumer.yaml

APP_CONTAINER = main-app
MESSAGING_CONTAINER = main-kafka
STORAGES_CONTAINER = mongodb
TG_BOT_CONTAINER = telegram-bot
TG_BOT_CONSUMER_CONTAINER = telegram-bot-consumer

.PHONY: all
all:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} -f ${TG_BOT_FILE} -f ${TG_BOT_CONSUMER_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} -f ${TG_BOT_FILE} -f ${TG_BOT_CONSUMER_FILE} ${ENV} down

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down	

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash	

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: messaging
messaging:
	${DC} -f ${MESSAGING_FILE} ${ENV} up --build -d

.PHONY: messaging-down
messaging-down:
	${DC} -f ${MESSAGING_FILE} down	

.PHONY: messaging-logs
messaging-logs:
	${DC} -f ${MESSAGING_FILE} logs -f

.PHONY: storages
storages: 
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down	

.PHONY: test
app-test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: tg-bot
tg-bot:
	${DC} -f ${TG_BOT_FILE} ${ENV} up --build -d

.PHONY: tg-bot-down
tg-bot-down:
	${DC} -f ${TG_BOT_FILE} down	

.PHONY: tg-bot-logs
tg-bot-logs:
	${LOGS} ${TG_BOT_CONTAINER} -f

.PHONY: tg-bot-shell
tg-bot-shell:
	${EXEC} ${TG_BOT_CONTAINER} bash	

.PHONY: tg-bot-consumer
tg-bot-consumer:
	${DC} -f ${TG_BOT_CONSUMER_FILE} ${ENV} up --build -d

.PHONY: tg-bot-consumer-down
tg-bot-consumer-down:
	${DC} -f ${TG_BOT_CONSUMER_FILE} ${ENV} down	

.PHONY: tg-bot-consumer-logs
tg-bot-consumer-logs:
	${LOGS} ${TG_BOT_CONSUMER_CONTAINER} -f

.PHONY: tg-bot-consumer-shell
tg-bot-consumer-shell:
	${EXEC} ${TG_BOT_CONSUMER_CONTAINER} bash