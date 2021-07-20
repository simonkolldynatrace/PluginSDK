'''
Demo plugin which shows how to monitor multiple process groups with single plugin.
'''
import requests
import requests.exceptions
import json
import logging
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import parse_port_bindings
from ruxit.api.exceptions import AuthException, ConfigException
from ruxit.api.snapshot import pgi_name

class DemoPluginMulti(BasePlugin):
    '''
    Class implementing plugin which shows how to monitor multiple process groups with single plugin.
    The group is to be monitored if its name starts with predefined string.
    '''
    _APPL_PREFIX='plugin_sdk.demo_app'

    def query(self, **kwargs):
        '''
        Scan process snapshot for groups with name starting with given prefix, and
        for all matching this prefix find ports on which they are listening. Then use this port
        for building URL to query with http. The result is json with two variables which are
        put into results with entity id of given process group.
        '''
        user = self.config["user"]
        password = self.config["password"]
        # search process snapshot using criteria defined by lambda expression
        pgi_list = self.find_all_process_groups( lambda entry: entry.group_name.startswith(self._APPL_PREFIX))
        for pgi in pgi_list:
            pgi_id = pgi.group_instance_id
            self.logger.info( "Demo pgid=%x application=%s" % (pgi_id,pgi.group_name ))
            port = None
            for process in pgi.processes:
               port = process.properties.get("ListeningPorts", None)
               break
            if port is None:
                raise ValueError( "no port definition for process group with id=%d" % pgi_id )
            # build URL for quering
            url = "http://127.0.0.1:" + port
            self.logger.info( "using url %s for pgid=%x app=%s" % (url,pgi_id,pgi.group_name ))

            try:
                # query URL for results
                response = requests.get(url, auth=(user, password))
                if response.status_code == 401:
                    raise AuthException(response)
                stats = response.json()
            except requests.exceptions.ConnectTimeout as ex:
                raise ConfigException('Timeout on connecting with "%s"' % url) from ex
            except requests.exceptions.RequestException as ex:
                raise ConfigException('Unable to connect to "%s"' % url) from ex
            except json.JSONDecodeError as ex:
                raise ConfigException('Server response from %s is not json' % url) from ex

            # save received results
            self.results_builder.absolute(key='random', value=stats['random'], entity_id=pgi_id)
            self.results_builder.relative(key='counter', value=stats['counter'], entity_id=pgi_id)
