import requests
import requests.exceptions
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name


class DemoPlugin(BasePlugin):
    def query(self, **kwargs):
        user = self.config["user"]
        password = self.config["password"]
        pgi = self.find_single_process_group(pgi_name('plugin_sdk.demo_app_auth'))
        pgi_id = pgi.group_instance_id
        stats_url = "http://localhost:8090"

        stats = requests.get(stats_url, auth=(user, password)).json()

        self.results_builder.absolute(key='random', value=stats['random'], entity_id=pgi_id)
        self.results_builder.relative(key='counter', value=stats['counter'], entity_id=pgi_id)
