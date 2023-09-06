import os
import shutil
import re
import tempfile

from django.core import management
from django.db import connection
from django.utils import functional


def delete_line(filename, pattern, stdout):
    pattern_compiled = re.compile(pattern)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                if pattern_compiled.findall(line):
                    stdout.write('Deleting line in %s' % filename)
                    continue
                tmp_file.write(line)

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


# Heavily inspired on open-source published package `django-reset-migrations`
# See https://github.com/valdergallo/django-reset-migrations/blob/master/reset_migrations/management/commands/reset_migrations.py#L25

class Command(management.BaseCommand):
    help = "Delete all migrations from one app, reset database and create one new migration"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('apps', nargs='+', type=str)

        # Named (optional) arguments
        parser.add_argument('--cached',
                            action='store_true',
                            dest='cached',
                            help='Dont delete the migrations files')

    @functional.cached_property
    def cursor(self):
        return connection.cursor()

    def delete_database_app(self, app):
        self.stdout.write("Deleting APP (%s) in database" % app)
        self.cursor.execute("DELETE from django_migrations WHERE app = %s", [app])

    def delete_files_app(self, app):
        self.stdout.write("Deleting APP (%s) migrations files" % app)
        migrations_dir = os.path.join(app, 'migrations')
        if os.path.exists(migrations_dir):
            shutil.rmtree(migrations_dir)

    def delete_dependence_app(self, app):
        self.stdout.write("Deleting dependences in migrations for (%s)" % app)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in dirs:
                if name == 'migrations':
                    migration_dir = os.path.join(root, name)
                    for r, d, f in os.walk(migration_dir):
                        for n in f:
                            file_name = os.path.join(r, n)
                            if '.pyc' in file_name:
                                continue
                            if '.py' in file_name:
                                regex = r'\(\'%s\'' % app
                                delete_line(file_name, regex, self.stdout)

    def handle(self, *args, apps=None, cached=False, **kwargs):
        self.stdout.write("Reseting APP %s" % apps)
        for app in apps:
            self.delete_database_app(app)
            if cached:
                self.delete_files_app(app)
                self.delete_dependence_app(app)
            self.stdout.write("APP (%s) deleted with success" % app)

        if not cached:
            management.call_command('makemigrations', *apps)

        for app in apps:
            management.call_command('migrate', app, '--fake')
