import requests
from ruxit.api.base_plugin import BasePlugin, EntityType

class DemoPluginSnapshot(BasePlugin):
    def initialize(self, **kwargs):
        self.logger.info("Agent version: %s", self.agent_version)
        self.logger.info("ME: Activation context: %s", self.get_activation_context())
        entities = self.get_monitored_entities(EntityType.PROCESS_GROUP_INSTANCE)
        for entity in entities:
            self.logger.info("ME: Monitored entity: id=%s, type=%s, process name=%s, snapshot:%s", entity.id, entity.type,
                             entity.process_name, entity.snapshot)
            for snapshot_entry in entity.snapshot:
                self.logger.info("ME: Print entity.snapshot elements:")
                self.logger.info("ME:           group_id: %s", snapshot_entry.group_id)
                self.logger.info("ME:  group_instance_id: %s", snapshot_entry.group_instance_id)
                self.logger.info("ME:         group_name: %s", snapshot_entry.group_name)
                self.logger.info("ME:       technologies: %s", snapshot_entry.technologies)
                for process_info in snapshot_entry.processes:
                    self.logger.info("ME:             Process info PID : %s", process_info.pid)
                    self.logger.info("ME:             Process info name : %s", process_info.name)
                    for key, value in process_info.properties.items():
                        self.logger.info("ME:               Process info properties : %s=%s", key, value)

    def query(self, **kwargs):
        self.logger.info("ME: " + "*" * 100)
        #get the list of all monitored entities with reporting on PGI level
        entities = self.get_monitored_entities(EntityType.PROCESS_GROUP_INSTANCE)
        self.logger.info("ME: No of found entities related to the activation context: %d", len(entities))
        for entity in entities:
            snapshot = entity.snapshot
            self.logger.info("ME: " + "-" * 100)
            self.logger.info(
                "ME:     Monitored entity: id=%s, type=%s, process name=%s, no of snapshot entries related to the entity = %d",
                entity.id, entity.type, entity.process_name, len(snapshot))
            entity.property("Python plugin activation_name_pattern", entity.process_name)
            technologies = []
            for snapshot_entry in snapshot:
                self.logger.info("ME:         Process group instance: %s", snapshot_entry)
                technologies.append(snapshot_entry.technologies or "None")
                for process in snapshot_entry.processes:
                    self.logger.info("ME:             Process info: %s", process)

            entity.property("Python plugin activation technologies", str(technologies))

