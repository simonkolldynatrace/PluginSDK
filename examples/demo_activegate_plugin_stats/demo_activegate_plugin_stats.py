import requests
from ruxit.api.base_plugin import RemoteBasePlugin
import logging

from ruxit.api.data import StatCounterDataPoint

logger = logging.getLogger(__name__)


class DemoPluginRemote(RemoteBasePlugin):
    def initialize(self, **kwargs):
        logger.info("Config: %s", self.config)
        self.url = self.config["url"]

    def query(self, **kwargs):
        # Create group - provide group id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation
        group = self.topology_builder.create_group(identifier="DemoGroup",
                                                   group_name="ActiveGate Demo Group")

        # Create device - provide device id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation
        device = group.create_device(identifier="DemoDevice",
                                    display_name="ActiveGate Demo Device")

        logger.info("Topology: group name=%s, device name=%s", group.name, device.name)

        # Collect stats
        stats = requests.get(self.url).json()

        # report absolute value
        device.relative(key='counter', value=stats['counter'])
        logger.info("1. relative")

        # report per second
        device.per_second(key='counter_persecond', value=stats['counter'])
        logger.info("2. persecond")

        # report relative value calculated based on previous sample
        device.absolute(key='random', value=stats['random'])
        logger.info("3. absolute")

        # report stat counter
        device.stat_counter(key='statcounter', value=StatCounterDataPoint(
            stats['stat_counter'][0],
            stats['stat_counter'][2],
            sum(stats['stat_counter']),
            3)
        )
        logger.info("4. stat counter")

        # report state - value must be one from list located in json file.
        device.state_metric(key='state', value=stats['state'])
        logger.info("5. state")

        # report property - any string-string values pair. It is added to device metadata displayed in dynatrace UI
        device.report_property(key='version', value=stats['version'])
        logger.info("6. property")
