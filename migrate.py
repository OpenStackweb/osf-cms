"""
Quick hack to migrate from the sqlite dev DB into a MySQL one.
From this gist https://gist.github.com/chappyhome/7117899

Assuming the dev sqlite is configured as the 'default' DB in settings.                                                                                                        
Add the MySQL DB as 'slave' and run migrations on it:

  python manage.py migrate --database slave

In the DB options for MySQL, disable FK checks:
   'OPTIONS': {
       "init_command": "SET foreign_key_checks = 0;",
   }


Then just run this script from the manage.py shell:

  from migrate import run
  run()

Then make MySQL the 'default' DB in settings, and get rid of sqlite.

"""
from django.contrib.contenttypes.models import ContentType
from filebrowser.models import FileBrowser

def run():

	def do(Table):
		print ("\n----------------")
		print (Table)
		if Table is not None and Table is not FileBrowser:
			table_objects = Table.objects.all()
			for i in table_objects:
				print(i)
				i.save(using='slave')

	ContentType.objects.using('slave').all().delete()

	for i in ContentType.objects.all():
		do(i.model_class())

