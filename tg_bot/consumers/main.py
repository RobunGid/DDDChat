from faststream import FastStream
from faststream.kafka.broker import KafkaBroker

from consumers.handlers import router
from settings.config import get_config


def get_app():
    config = get_config()
    broker = KafkaBroker(config.kafka_url)
    broker.include_router(router)
    app = FastStream(broker)
    return app
