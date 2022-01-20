#!/usr/bin/env python3

import os
import logging
import time
import psycopg2


logger = logging.getLogger("postgres-ping")

state = 1
while state > 0:
    try:
        connection = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('POSTGRES_IP'),
            port=5432)
        state = connection.closed
        logger.info("Database is ready!")
    except Exception as connection_exception:
        logger.error(connection_exception)
        time.sleep(1)
        pass
