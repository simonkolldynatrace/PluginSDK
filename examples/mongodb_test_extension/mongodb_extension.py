from collections import defaultdict
import logging
import ssl
from typing import Optional
from datetime import datetime

import pymongo
from pymongo.errors import ConnectionFailure
from utils_replication import usedmb, logsizemb, timediff

from ruxit.api.base_plugin import BasePlugin
from ruxit.api.selectors import ListenPortSelector

log = logging.getLogger(__name__)

TIMEOUT = 15 * 1000

states = {
    0: "STARTUP",
    1: "PRIMARY",
    2: "SECONDARY",
    3: "RECOVERING",
    5: "STARTUP2",
    6: "UNKNOWN",
    7: "ARBITER",
    8: "DOWN",
    9: "ROLLBACK",
}


class MongoDBExtended(BasePlugin):
    def initialize(self, **kwargs):

        # This is a dictionary of metric_key: profiles
        # For instance, "write_tickets_available: ["Basic", "Standard", "Advanced"]"
        self.profiles_per_metric = defaultdict(list)
        for metric in kwargs["json_config"]["metrics"]:
            self.profiles_per_metric[metric["timeseries"]["key"]] = metric["source"]["profiles"]

        self.mongodb_client = self.create_client()

    def create_client(self) -> Optional[pymongo.MongoClient]:
        port = self.config.get("port")
        user = self.config.get("auth_user")
        password = self.config.get("auth_password")
        self.profile = self.config.get("profile")

        self.oplog_threshold = int(self.config.get("oplog_threshold", 2))

        if not user or not password:
            url = f"mongodb://localhost:{port}"
        else:
            url = f"mongodb://{user}:{password}@localhost:{port}"
        auth_db = self.config.get("auth_db", False)
        if auth_db:
            url = f"{url}/?authSource={auth_db}"

        try:
            mongodb_client = pymongo.MongoClient(url, ssl=True, ssl_cert_reqs=ssl.CERT_NONE, serverSelectionTimeoutMS=TIMEOUT)
            mongodb_client.list_databases()
            log.info("Connected to mongodb[SSL]")
            return mongodb_client
        except ConnectionFailure:
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
        self.send_metric("available_connections", server_status["connections"]["available"])
        self.send_metric("insert_operations", server_status["opcounters"]["insert"], metric_type="per_second")
        self.send_metric("query_operations", server_status["opcounters"]["query"], metric_type="per_second")
        self.send_metric("update_operations", server_status["opcounters"]["update"], metric_type="per_second")
        self.send_metric("delete_operations", server_status["opcounters"]["delete"], metric_type="per_second")
        self.send_metric("getmore_operations", server_status["opcounters"]["getmore"], metric_type="per_second")
        self.send_metric("command_operations", server_status["opcounters"]["command"], metric_type="per_second")
        self.send_metric("resident_memory", server_status["mem"]["resident"])
        self.send_metric("resident_memory", server_status["mem"]["virtual"])
        self.send_metric("virtual_memory", server_status["mem"]["virtual"])
        self.send_metric("current_queue", server_status["globalLock"]["currentQueue"]["total"])
        self.send_metric("active_clients", server_status["globalLock"]["activeClients"]["total"])
        self.send_metric("regular_asserts", server_status["asserts"]["regular"], metric_type="per_second")
        self.send_metric("warning_asserts", server_status["asserts"]["warning"], metric_type="per_second")
        self.send_metric("message_asserts", server_status["asserts"]["msg"], metric_type="per_second")
        self.send_metric("user_asserts", server_status["asserts"]["user"], metric_type="per_second")
        self.send_metric("rollover_asserts", server_status["asserts"]["rollovers"], metric_type="per_second")
        self.send_metric("read_tickets_available", server_status["wiredTiger"]["concurrentTransactions"]["read"]["available"])
        self.send_metric("write_tickets_available", server_status["wiredTiger"]["concurrentTransactions"]["write"]["available"])

    def send_metric(self, key, value, metric_type="absolute", dimensions=None):
        methods = {
            "state": self.results_builder.state_metric,
            "per_second": self.results_builder.per_second,
            "absolute": self.results_builder.absolute,
        }

        if self.profile in self.profiles_per_metric[key]:
            methods[metric_type](
                key=key, value=value, dimensions=dimensions, entity_selector=ListenPortSelector(self.config.get("port"))
            )