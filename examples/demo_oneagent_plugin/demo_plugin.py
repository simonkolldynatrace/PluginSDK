import requests

from ruxit.api.base_plugin import BasePlugin
from ruxit.api.data import MEAttribute
from ruxit.api.snapshot import pgi_name


class DemoPlugin(BasePlugin):
    def query(self, **kwargs):
        pgi = self.find_single_process_group(pgi_name('plugin_sdk.demo_app'))
        pgi_id = pgi.group_instance_id
        stats_url = "http://localhost:8769"
        stats = requests.get(stats_url).json()
        self.results_builder.absolute(key='random', value=stats['random'], entity_id=pgi_id)
        self.results_builder.relative(key='counter', value=stats['counter'], entity_id=pgi_id)
        self.results_builder.state_metric(key="state", value=stats['state'], dimensions={'app': 'demo'}, entity_id=pgi_id)
        self.results_builder.report_property(key="version", value=stats['version'],
                                             me_attribute=MEAttribute.CUSTOM_PG_METADATA, entity_id=pgi_id)
