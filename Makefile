DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

APP_FILE = docker_compose/app.yaml
MESSAGING_FILE = docker_compose/messaging.yaml
STORAGES_FILE = docker_compose/storages.yaml
TG_BOT_FILE = docker_compose/tg-bot.yaml

APP_CONTAINER = main-app
ZOOKEEPER_CONTAINER = zookeeper
KAFKA_CONTAINER = kafka
KAFKA_UI_CONTAINER = kafka-ui
MONGO_CONTAINER = mongodb
MONGO_EXPRESS_CONTAINER = mongo-express
TG_BOT_CONTAINER = telegram-bot
TG_BOT_CONSUMER_CONTAINER = telegram-bot-consumer
SQLITEWEB_CONTAINER = sqliteweb

# ALL
.PHONY: all
all:
	${DC} -f ${APP_FILE} -f ${MESSAGING_FILE} -f ${STORAGES_FILE} -f ${TG_BOT_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${MESSAGING_FILE} -f ${STORAGES_FILE} -f ${TG_BOT_FILE} ${ENV} down


# APP
.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} ${ENV} down	

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash	

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-test
app-test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: app-test-debugger
app-test-debugger:
	${EXEC} ${APP_CONTAINER} debugpy --listen 0.0.0.0:5679 --wait-for-client -m pytest tests/ -v


# Messaging
.PHONY: messaging
messaging:
	${DC} -f ${MESSAGING_FILE} ${ENV} up --build -d

.PHONY: messaging-down
messaging-down:
	${DC} -f ${MESSAGING_FILE} ${ENV} down	

.PHONY: messaging-logs
messaging-logs:
	${DC} -f ${MESSAGING_FILE} logs -f

.PHONY: zookeeper-logs
zookeeper-logs:
	${LOGS} -f ${ZOOKEEPER_CONTAINER} 

.PHONY: zookeeper-shell
zookeeper-shell:
	${EXEC} ${ZOOKEEPER_CONTAINER} bash

.PHONY: kafka-logs
kafka-logs:
	${LOGS} -f ${KAFKA_CONTAINER}

.PHONY: kafka-shell
kafka-shell:
	${EXEC} ${KAFKA_CONTAINER} bash

.PHONY: kafka-ui-logs
kafka-ui-logs:
	${LOGS} -f ${KAFKA_UI_CONTAINER}

.PHONY: kafka-ui-shell
kafka-ui-shell:
	${EXEC} ${KAFKA_UI_CONTAINER} bash


# Storages
.PHONY: storages
storages: 
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-logs
storages-logs:
	${DC} -f ${STORAGES_FILE} logs -f

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} ${ENV} down	

.PHONY: mongo-logs
mongo-logs:
	${LOGS} -f ${MONGO_CONTAINER}

.PHONY: mongo-shell
mongo-shell:
	${EXEC} ${MONGO_CONTAINER} bash

.PHONY: mongo-express-logs
mongo-express-logs:
	${LOGS} -f ${MONGO_EXPRESS_CONTAINER}

.PHONY: mongo-express-shell
mongo-express-shell:
	${EXEC} ${MONGO_EXPRESS_CONTAINER} bash


# Telegram bot
.PHONY: tg-bot
tg-bot:
	${DC} -f ${TG_BOT_FILE} ${ENV} up --build -d

.PHONY: tg-bot-down
tg-bot-down:
	${DC} -f ${TG_BOT_FILE} ${ENV} down	

.PHONY: tg-bot-logs
tg-bot-logs:
	${LOGS} ${TG_BOT_CONTAINER} -f

.PHONY: tg-bot-consumer-logs
tg-bot-consumer-logs:
	${LOGS} ${TG_BOT_CONSUMER_CONTAINER} -f

.PHONY: tg-bot-shell
tg-bot-shell:
	${EXEC} ${TG_BOT_CONTAINER} bash

.PHONY: tg-bot-consumer-shell
tg-bot-consumer-shell:
	${EXEC} ${TG_BOT_CONSUMER_CONTAINER} bash

.PHONY: sqliteweb-logs
sqliteweb-logs:
	${LOGS} -f ${SQLITEWEB_CONTAINER}

.PHONY: sqliteweb-shell
sqliteweb-shell:
	${EXEC} ${SQLITEWEB_CONTAINER} bash