import os
import sys

from pkg_resources import resource_filename
from alta import ConfigurationFromYamlFile
from alta.browsers import Browsers


def get_conf(logger, config_file):
    config_file_path = paths_setup(logger, config_file)

    # Load YAML configuration file
    return ConfigurationFromYamlFile(config_file_path)


def get_vcfminer_client(conf, logger):
    host = conf.get('host')
    username = conf.get('username')
    password = conf.get('password')
    c = Browsers(host, username, password, "vcfminer").browsers
    return c


def paths_setup(logger, cf_from_cli=None):
    home = os.path.expanduser("~")
    minero_config_from_home = os.path.join(home, 'minero',
                                           'minero_config.yml')
    minero_config_from_package = resource_filename('minero',
                                                   'minero/minero_config.yml')
    config_file_paths = []
    if cf_from_cli and path_exists(cf_from_cli, logger, force=False):
        config_file_paths.append(WeightedPath(cf_from_cli, 0))
    if path_exists(minero_config_from_home, logger, force=False):
        config_file_paths.append(WeightedPath(minero_config_from_home, 1))
    if path_exists(minero_config_from_package, logger, force=False):
        config_file_paths.append(WeightedPath(minero_config_from_package, 2))

    logger.debug("config file paths: {}".format(config_file_paths))

    return sorted(config_file_paths)[0].path


def path_exists(path, logger, force=True):
    def file_missing(path, logger, force):
        if force:
            logger.error("path - {} - doesn't exists".format(path))
            sys.exit()
        return False

    return True if os.path.exists(os.path.expanduser(path)) else file_missing(path,
                                                                              logger,
                                                                              force)


class WeightedPath(object):
    def __init__(self, path, weight):
        self.path = path
        self.weight = weight

    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__,
                                  self.path,
                                  self.weight)

    def __cmp__(self, other):
        if hasattr(other, 'weight'):
            return self.weight.__cmp__(other.weight)
