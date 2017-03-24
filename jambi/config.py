import configparser
import logging
import os

from jambi.exceptions import ImproperlyConfigured


logger = logging.getLogger('jambi.config')


class JambiConfig(configparser.ConfigParser):
    """Jambi configuration object.
    """
    def __init__(self, filename):
        """Create a new JambiConfig.

        Args:
            filename: The relative location of the config file to use.

        Raises:
            ImproperlyConfigured:
        """
        filename = filename or 'jambi.conf'
        super().__init__()
        location = os.path.abspath(filename)
        logger.debug('Sourcing configuration file: {}'.format(location))
        self.read(location)
        if not self.valid:
            raise ImproperlyConfigured('Configuration is not valid.')
        logger.debug('Configuration successfully loaded: {}'.format(location))

    @property
    def valid(self):
        return \
            self.has_section('database') and \
            self.has_option('migrate', 'location')

    def _get_db_and_schema(self, db):
        """Initialize and return the database and schema from configuration.

        Args:
            db: the database to initialize

        Returns:
            the initialized db and schema
        """
        db.init(self.get('database', 'database'),
                 user=self.get('database', 'user'),
                 password=self.get('database', 'password'),
                 host=self.get('database', 'host'),
                 port=self.get('database', 'port'))
        schema = self.get('database', 'schema')
        return db, schema
