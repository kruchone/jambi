import os

from jambi.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIABLE = "JAMBI_CONFIG"
DEFAULT_CONFIG_FILENAME = "jambi.conf"

def get_config_file():
	config_file = os.environ.get(ENVIRONMENT_VARIABLE)
	if config_file:
		if os.path.isfile(config_file):
			return config_file
		else:
			raise ImproperlyConfigured(
				"{} environment variable is set, but no file was found" \
				.format(ENVIRONMENT_VARIABLE)
			)
	else:
		if os.path.isfile(DEFAULT_CONFIG_FILENAME):
			return DEFAULT_CONFIG_FILENAME
		else:
			raise ImproperlyConfigured(
				"No configuration file found. Either create {} in the " \
				"install directory, or set the {} environment variable." \
				.format(DEFAULT_CONFIG_FILENAME, ENVIRONMENT_VARIABLE)
			)
