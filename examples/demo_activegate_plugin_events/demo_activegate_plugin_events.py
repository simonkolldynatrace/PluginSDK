from ruxit.api.base_plugin import RemoteBasePlugin
import logging

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

        # Report problems
        device.report_performance_event(title="Performance Event",
                                      description="Use it to focus on some performance issue",
                                      properties={"property_key": "property_value"})

        device.report_error_event(title="Error Event",
                                description="Use it to report some error",
                                properties={"property_key": "property_value"})
        logger.info("Report error event")

        device.report_availability_event(title="Availability Event",
                                       description="Use it to focus on some availability issue",
                                       properties={"property_key": "property_value"})
        logger.info("Report availability event")

        device.report_resource_contention_event(title="Resources Contention Event",
                                              description="Use it to focus on some resource contention issue",
                                              properties={"property_key": "property_value"})
        logger.info("Report resource contention event")

        # report information
        device.report_custom_info_event(title="Custom Info Event",
                                      description="Use it to report some custom info",
                                      properties={"property_key": "property_value"})
        logger.info("Report custom info event")

        device.report_custom_deployment_event(source="demo source",
                                            project="demo plugin",
                                            version="1.001",
                                            ci_link=self.url + "/deployment",
                                            remediation_action_link=self.url + "/remediation",
                                            deployment_name="Demo deployment",
                                            properties={"property_key": "property_value"})
        logger.info("Report custom deployment event")

        device.report_custom_annotation_event(description="Annotation event",
                                            annotation_type="demo",
                                            source="demo source",
                                            properties={"property_key": "property_value"})
        logger.info("Report custom annotation event")
