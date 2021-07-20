import requests
from ruxit.api.base_plugin import BasePlugin

class DemoPluginHost(BasePlugin):
    def query(self, **kwargs):
        stats_url = "http://localhost:8769"
        stats = requests.get(stats_url).json()
        self.results_builder.absolute(key='battery_level', value=stats['battery_level'])