"""set up the project to be run locally

Make sure:
    * you have docker installed
    * you have python installed
    * you have all the requirements installed

Steps:
    1. start postgres.
    2. create tables using migration.py.
    3. populate database using populate.py
    4. docker-compose up
"""

import os
from os.path import dirname, realpath, join
import asyncio as aio
import logging.config


logging.config.fileConfig("logging.conf")
log = logging.getLogger("setup")

PATH = dirname(realpath(__file__))

try:
    import docker
    from docker.models.containers import Container
    from dotenv import load_dotenv

    from populate import (
        init as populate_init,
        up as populate_up,
    )

except ImportError:
    log.error("failed to import some libraries.")
    log.info("please run `py -3.10 -m pip install -r requirements.txt` to install the missing requirements")
    exit()


load_dotenv()
os.environ["HOST"] = "127.0.0.1"


async def main():
    log.info("connecting to docker")
    try:
        client = docker.from_env()
    except docker.tls.errors.DockerException:
        log.error(
            "error occurred while trying to connect to Docker. is it installed and running?",
            exc_info=True,
        )
        return
    except Exception as e:
        _ = e
        log.error(
            "error occurred while trying to connect to docker. is it installed and running?",
            exc_info=True
        )
        return
    else:
        log.info("connected to docker")

    log.info("pulling postgres:latest please wait a bit...")
    client.images.pull("postgres:latest")
    log.info("postgres:latest pulled successfully")

    log.info("postgres starting...")
    try:
        postgres: Container = client.containers.run(
            "postgres:latest",
            ports={5432: 5432},
            volumes={
                join(PATH, ".postgres"): {
                    "bind": "/var/lib/postgresql/data",
                    "mode": "rw",
                }
            },
            environment={
                "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD")
            },
            detach=True
        )
    except Exception as e:
        _ = e
        log.exception(
            "failed to start postgres. please check the exception",
            exc_info=True
        )
        return
    else:
        log.info("postgres started")

    log.info("waiting for postgres to get ready")
    await aio.sleep(10)
    log.info("postgres should be ready by now")

    await populate_init()
    await populate_up()

    postgres.stop()
    postgres.remove()

    log.info("building mavefund_api container started")
    server, _ = client.images.build(
        path=".",
        tag="ddjerqq/server:latest"
    )
    log.info("building mavefund_api container finished successfully")

    log.info("SUCCESS!!! the application is fully setup and ready to be ran")
    log.info("to run the app run `docker-compose up`")


if __name__ == "__main__":
    aio.run(main())
