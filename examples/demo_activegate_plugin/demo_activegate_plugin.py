import requests
from ruxit.api.base_plugin import RemoteBasePlugin
import logging

logger = logging.getLogger(__name__)

class DemoPluginRemote(RemoteBasePlugin):
    def initialize(self, **kwargs):
        logger.info("Config: %s", self.config)
        self.url = self.config["url"]

    def query(self, **kwargs):
        #Create topology
        url = self.url + "/topology"
        topology = requests.get(url).json()
        for group_t in topology:
            group_name = group_t['name']
            group = self.topology_builder.create_group(group_name, group_name)
            for device_t in group_t['devices']:
                device_name = device_t['name']
                device = group.create_device(device_name, device_name)
                logger.info("Topology: group name=%s, device name=%s", group.name, device.name)
                #Collect stats
                stats = device_t['stats']
                device.absolute(key='countercd', value=stats['counter'])
                device.relative(key='randomcd', value=stats['random'])