#! /usr/bin/env python3
import argparse
import configparser
import logging
import sys

from peewee import CharField, Model, PostgresqlDatabase, ProgrammingError


_db = PostgresqlDatabase(None)
_schema = 'public'


class JambiModel(Model):
    ref = CharField(primary_key=True)

    class Meta:
        db_table = 'jambi'
        database = _db
        schema = _schema


class Jambi(object):
    """A database migration helper for peewee."""
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('jambi')
        self.db, self.db_schema = self.__get_db_and_schema_from_config()

    def upgrade(self, ref):
        """migrate the database to the supplied reference hash"""
        ref = ref or 'head'
        self.logger.info('migrating to "{}"'.format(ref))
        self.db.connect()
        self.db.close()
        return

    def inspect(self):
        """inspect the database and report its version"""
        self.db.connect()
        result = None
        try:
            jambi_versions = JambiModel.select().limit(1)
            if any(jambi_versions):
                self.logger.info('jambi found ref "{}"'.format(jambi_versions[0].ref))
                result = jambi_versions[0]
            else:
                self.logger.info('this database hasn\'t been migrated yet')
        except ProgrammingError:
            # table is not created
            self.logger.info('run \'init\' to create a jambi version table first')
            result = None
        finally:
            self.db.close()
        return result

    def init(self):
        """initialize the jambi database version table"""
        self.db.connect()
        self.db.create_tables([JambiModel], safe=True)
        self.db.close()
        self.logger.info('jambi was initialized')

    def wish_from_kwargs(self, **kwargs):
        """Processes keyword arguments in to a jambi wish."""
        try:
            wish = kwargs.pop('wish')
        except KeyError:
            self.logger.error('there was no wish to process')

        if wish == 'upgrade':
            result = self.upgrade(kwargs.pop('ref', None))
        elif wish == 'inspect':
            result = self.inspect()
        elif wish == 'init':
            result = self.init()
        else:
            self.logger.error('unknown wish')
            result = None

        return result

    def __get_db_and_schema_from_config(self):
        config = configparser.ConfigParser()
        config.read('jambi.conf')
        _db.init(config['database']['database'],
                 user=config['database']['user'],
                 password=config['database']['password'],
                 host=config['database']['host'])
        _schema = config['database']['schema']
        return _db, _schema


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Migration tools for the db.')
    subparsers = parser.add_subparsers(title='actions', dest='wish')

    wish_inspect = subparsers.add_parser('inspect', help='check database version')
    wish_inspect = subparsers.add_parser('init', help='create jambi table')

    wish_migrate = subparsers.add_parser('upgrade', help='run migrations')
    wish_migrate.add_argument('ref', type=str, help='reference hash')

    opts = parser.parse_args()

    if opts.wish is None:
        parser.print_help()
        sys.exit(1)

    # create jambi and process command
    jambi = Jambi()
    jambi.wish_from_kwargs(**vars(opts))
