# jambi
A peewee database migration manager (in development)

### Disclaimer
This is in development, so some of the things you see might not be fully working. I will be sure to update this project and remove this disclaimer once things are in a stable state, but for right now, **use this tool at your own risk**. I claim no responsibility for bugs or other misuse of this tool resulting in loss of data or any other unintended side-effect.

### Getting Started
1. install with pip
    * `pip install jambi`
2. create a jambi config file in your favorite directory
    * `cd myproj/db && touch jambi.conf`
	* see the section entitled 'Configuration' to learn about what must be in `jambi.conf`
2. run jambi!
    * `jambi --help`

### Supported Operations
* **init** -- create the jambi table and set the version to 0
* **inspect** -- return the database's current version.
* **latest** -- retuns the latest migration version.
* **upgrade _&lt;version&gt;_** -- upgrade your database to the supplied version
* **makemigration** -- generate a new migration version from template

### Configuration
Jambi needs to know how to connect to your database, and where your migrations are stored, which can be conveyed though the `jambi.conf` configuration file. Jambi will look for your configuration file in your current working directory.

Here is an example `jambi.conf`, set up to connect to a vanilla postgres database:
```
[database]
database=test
schema=public
host=localhost
user=postgres
password=

[migrate]
location=./migrations/
```

### Contributing
Pull requests are welcome, and please open issues for any bugs, enhancements, or feature requests.
