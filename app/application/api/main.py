from fastapi import FastAPI

def create_app():
    return FastAPI(
		title="DDDChat with Kafka",
		docs_url="/api/docs",
  		description="Kafka DDD chat"
	)