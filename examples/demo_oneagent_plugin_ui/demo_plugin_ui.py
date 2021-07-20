import requests
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name


class DemoPlugin(BasePlugin):
    def query(self, **kwargs):
        pgi = self.find_single_process_group(pgi_name('plugin_sdk.demo_app'))
        pgi_id = pgi.group_instance_id
        stats_url = "http://localhost:8769"
        stats = requests.get(stats_url).json()
        self.results_builder.absolute(key='random', value=stats['random'], entity_id=pgi_id)
        self.results_builder.relative(key='counter', value=stats['counter'], entity_id=pgi_id)
        self.results_builder.absolute(key='randbar_red', value=stats['randbar_red'], entity_id=pgi_id)
        self.results_builder.absolute(key='randbar_yellow', value=stats['randbar_yellow'], entity_id=pgi_id)
        self.results_builder.absolute(key='randbar_green', value=stats['randbar_green'], entity_id=pgi_id)
        self.results_builder.absolute(key='rand_stacked1', value=stats['rand_stacked1'], entity_id=pgi_id)
        self.results_builder.absolute(key='rand_stacked2', value=stats['rand_stacked2'], entity_id=pgi_id)
        self.results_builder.absolute(key='rand_stacked3', value=stats['rand_stacked3'], entity_id=pgi_id)
        self.results_builder.absolute(key='sin_small_noise', value=stats['sin_small_noise'], entity_id=pgi_id)
        self.results_builder.absolute(key='sin_big_noise', value=stats['sin_big_noise'], entity_id=pgi_id)
        self.results_builder.absolute(key='sin_rounded', value=stats['sin_rounded'], entity_id=pgi_id)



