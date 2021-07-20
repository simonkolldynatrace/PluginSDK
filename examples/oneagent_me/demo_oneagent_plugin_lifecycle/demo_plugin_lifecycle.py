import requests

from ruxit.api.base_plugin import BasePlugin
from ruxit.api.selectors import EntityType

class DemoPluginLifeCycle(BasePlugin):
    def initialize(self, **kwargs):
        self.logger.info("Initializing plugin, activation context: %s", self.get_activation_context())


    def query(self, **kwargs):
        stats_url = "http://localhost:8769"
        stats = requests.get(stats_url).json()
        #get the list of monitored entities related to the plugin activation context
        entities = self.get_monitored_entities(EntityType.PROCESS_GROUP_INSTANCE)
        for entity in entities:
            self.logger.info("Monitored entity: id=%s, type=%s, group name=%s, snapshot=%s", entity.id, entity.type, entity.process_name, entity.snapshot)
            #one monitored entity contains one or more processes
            processes = entity.snapshot
            for process_info in processes:
                self.logger.info("Process info: %s", process_info)
            #since this plugin runs as singleton multiple entries can be related to activation context, which is all Python processess, so make sure that data is reported to correct entity
            if entity.process_name == 'plugin_sdk.demo_app':
                entity.absolute(key='random_pgi', value=stats['random'])
                entity.relative(key='counter_pgi', value=stats['counter'])
                entity.state_metric(key="state", value=stats['state'], dimensions={'app': 'demo'})
                entity.property(key="version", value=stats['version'])
                entity.event_performance(description="Event description", title="Performance event")
                entity.event_error(description="Event description", title="Error event")
                entity.event_availability(description="Event description", title="Availability event")
                entity.event_resource_contention(description="Event description", title="Resource contention event")
                entity.event_custom_info(description="Event description", title="Custom info event")
                entity.event_custom_deployment(source="source", project="project")
                entity.event_custom_annotation(description="Event description", annotation_type="Custom annotation event", source="source")

        entities = self.get_monitored_entities(EntityType.PROCESS_GROUP)
        for entity in entities:
            self.logger.info("Monitored entity: id=%s, type=%s, group name=%s, snapshot=%s", entity.id, entity.type,
                             entity.process_name, entity.snapshot)
            # one monitored entity contains one or more processes
            processes = entity.snapshot
            for process_info in processes:
                self.logger.info("Process info: %s", process_info)
            # since this plugin runs as singleton multiple entries can be related to activation context so make sure that data is reported to correct entity
            if entity.process_name == 'plugin_sdk.demo_app':
                entity.absolute(key='random_pg', value=stats['random'])
                entity.relative(key='counter_pg', value=stats['counter'])
                entity.property(key="version", value=stats['version'])

        entities = self.get_monitored_entities(EntityType.HOST)
        for entity in entities:
            self.logger.info("Monitored entity: id=%s, type=%s, group name=%s, snapshot=%s", entity.id, entity.type,
                             entity.process_name, entity.snapshot)
            entity.absolute(key='random_host', value=stats['random'])
            entity.relative(key='counter_host', value=stats['counter'])
            entity.property(key="version", value=stats['version'])


