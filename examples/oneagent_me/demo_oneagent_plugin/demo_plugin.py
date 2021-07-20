import requests
from ruxit.api.base_plugin import BasePlugin

class DemoPlugin(BasePlugin):
    def query(self, **kwargs):
        self.logger.info("Activation context: %s", self.get_activation_context())
        stats_url = "http://localhost:8769"
        stats = requests.get(stats_url).json()
        #get the list of monitored entities related to the plugin activation context
        entities = self.get_monitored_entities()
        for entity in entities:
            self.logger.info("Monitored entity: id=%s, type=%s, group name=%s", entity.id, entity.type, entity.process_name)
            #since this plugin runs as singleton multiple entries can be related to activation context so make sure that data is reported to correct entity
            if entity.process_name == 'plugin_sdk.demo_app':
                entity.absolute(key='random', value=stats['random'])
                entity.relative(key='counter', value=stats['counter'])
                entity.property(key="Demo_app version", value=stats['version'])