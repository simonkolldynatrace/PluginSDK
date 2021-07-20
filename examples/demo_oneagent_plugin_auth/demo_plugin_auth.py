import requests
import requests.exceptions
import json
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.exceptions import AuthException, ConfigException
from ruxit.api.snapshot import pgi_name


class DemoPlugin(BasePlugin):
    def query(self, **kwargs):
        user = self.config["user"]
        password = self.config["password"]
        pgi = self.find_single_process_group(pgi_name('plugin_sdk.demo_app_auth'))
        pgi_id = pgi.group_instance_id
        stats_url = "http://localhost:8090"

        try:
            response = requests.get(stats_url, auth=(user, password))
            if response.status_code == 401:
                raise AuthException(response)
            stats = response.json()
        except requests.exceptions.ConnectTimeout as ex:
            raise ConfigException('Timeout on connecting with "%s"' % stats_url) from ex
        except requests.exceptions.RequestException as ex:
            raise ConfigException('Unable to connect to "%s"' % stats_url) from ex
        except json.JSONDecodeError as ex:
            raise ConfigException('Server response from %s is not json' % stats_url) from ex

        self.results_builder.absolute(key='random', value=stats['random'], entity_id=pgi_id)
        self.results_builder.relative(key='counter', value=stats['counter'], entity_id=pgi_id)
