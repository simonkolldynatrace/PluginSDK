import pymongo
from pymongo.errors import ConnectionFailure
import logging
import ssl
from typing import Optional
from datetime import datetime
import requests

from ruxit.api.base_plugin import BasePlugin
from ruxit.api.selectors import ListenPortSelector

log = logging.getLogger(__name__)

class CustomMongoExtension(BasePlugin):
    def initialize(self, **kwargs):
        self.mongodb_client = self.create_client()

    def create_client(self) -> Optional[pymongo.MongoClient]:
        url = f"mongodb://d1pacmworkshop:dynatrace@127.0.0.1:27017/test"
        try:
            url = f"mongodb://d1pacmworkshop:dynatrace@127.0.0.1:27017/test"
            mongodb_client = pymongo.MongoClient(url, ssl=True, ssl_cert_reqs=ssl.CERT_NONE, serverSelectionTimeoutMS=TIMEOUT)
            mongodb_client.list_databases()
            log.info("Connected to mongodb[SSL]")
            return mongodb_client
        except ConnectionFailure:
            url = f"mongodb://d1pacmworkshop:dynatrace@127.0.0.1:27017/test"
            mongodb_client = pymongo.MongoClient(url, serverSelectionTimeoutMS=TIMEOUT)
            mongodb_client.list_databases()
            log.info("Connected to mongodb")
            return mongodb_client

    def query(self, **kwargs) -> None:
        if self.mongodb_client is None:
            self.mongodb_client = self.create_client()
        else:
            self.get_server_metrics()

    def get_server_metrics(self):
        server_status = self.mongodb_client.db.command("serverStatus")
        self.send_metric("current_connections", server_status["connections"]["current"])

    def send_metric(self, key, value):
        self.results_builder.absolute(key=key, value=value, dimensions=NONE, entity_selector=ListenPortSelector(self.config.get("port")))
        
