from consumers.handlers import router
from faststream import FastStream
from faststream.kafka.broker import KafkaBroker

from settings.config import get_config

config = get_config()


broker = KafkaBroker(config.kafka_url)
broker.include_router(router)
app = FastStream(broker)
