import os

from jambi.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIABLE = "JAMBI_CONFIG"

def get_config_file():
    config_file = os.environ.get(ENVIRONMENT_VARIABLE, 'jambi.conf')
    if config_file:
        if os.path.isfile(config_file):
            return config_file
        else:
            raise ImproperlyConfigured(
                "{} environment variable is set, but no file was found" \
                .format(ENVIRONMENT_VARIABLE)
            )
    else:
        raise ImproperlyConfigured(
            "No configuration file found. Either pass an absolute path " \
            "when you invoke jambi, or set the {} environment variable." \
            .format(ENVIRONMENT_VARIABLE)
        )
