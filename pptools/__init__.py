import codecs
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import glob
import logging
import os

logging.basicConfig(format='%(name)s: %(message)s')


def path_norm_join(path, *more):
    """Normalize a path using os.path.abspath. If more paths are given,
    they are merged, normalized and returned. Unlike os.path.join, this
    also works when any of the paths is/are absolute."""
    result = [path]
    result.extend(more)
    # if there are two slashes in the start, os.path.abspath won't normalize
    #  TODO: find out why this happens
    joined = os.path.abspath(os.path.sep.join(result))
    if joined.startswith(os.path.sep * 2) and not joined.startswith(os.path.sep * 3):
        return joined[1:]
    return joined


PYTHON_LIBDIRS = [path_norm_join(os.path.sep, 'usr', 'lib', 'python[0-9].[0-9]'),
    path_norm_join(os.path.sep, 'usr', 'lib64', 'python[0-9].[0-9]')]


def load_cf_parsers(location):
    """Loads and returns all configs from given location.

    Args:
        location: a directory to search for configs

    Returns:
        a mapping {config_name: SafeConfigParser object, ...}
    """
    parsers = {}
    for cf in glob.glob(path_norm_join(location, '*.conf')):
        with codecs.open(cf, 'r', 'utf8') as fp:
            parser = configparser.SafeConfigParser()
            parser.readfp(fp)
            parsers[os.path.basename(cf)[:-5]] = parser
    return parsers
