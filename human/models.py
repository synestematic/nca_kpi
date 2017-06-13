from django.db import models
from django.conf import settings
from django.core import exceptions as django_exceptions
import _mysql_exceptions
import MySQLdb, datetime, sys, inspect
# How do migrations understand where to sync models ???

class Db():
	def __init__(self, host, user, db):
		try:
			self.host = host
			self.user = user
			self.name = db
		except django_exceptions.ImproperlyConfigured:
			self.host = '10.4.4.205'
			self.user = 'django'
			self.name = 'nca'

	def connect(self):
		self.handle = MySQLdb.connect(host=self.host, user=self.user, db=self.name)
		self.cursor = self.handle.cursor()

	def disconnect(self):
		# check to see if its open
		self.handle.close()

	def run_query(self, query):
		self.connect()

		# self.last_query = query
		self.cursor.execute(query)
		rows = self.cursor.fetchall()

		self.disconnect()
		return rows

try:
	portale_nca_db = Db(
			settings.DATABASES['portale_nca_mysql']['HOST'],
			settings.DATABASES['portale_nca_mysql']['USER'],
			settings.DATABASES['portale_nca_mysql']['NAME']
		)
except:
	portale_nca_db = Db(
			'10.4.4.205',
			'django',
			'nca'
		)


class DbQuery():
	def __init__(self, db, table):
		self.db = db
		self.table = table
		self.columns = '*'
		self.constraints = ''
		self.limit = ''
		self.order = ''
		self.set = ''

	def _check_arguments(self, *args, **kwargs):
		calling_function = inspect.stack()[1][3]
		for k, v in kwargs.items():
			if k == 'set' and type(v) == dict and len(v) > 0 :
				if calling_function == 'create':
					columns, values = [], []
					for foo, bar in v.items():
						columns.append(foo)
						values.append(bar)
					foo = ', '.join(columns)
					bar = '", "'.join(values)
					self.set = '(' + foo + ') VALUES ("' + bar + '")'
				elif calling_function == 'update':
					for foo, bar in v.items():
						self.set = self.set + '{} = "{}" AND '.format(foo, bar)
					# if self.set.endswith(' AND '):
					self.set = self.set[:-5]
			if k == 'constraints' and type(v) == dict and len(v) > 0 :
				for foo, bar in v.items():
					self.constraints = self.constraints + '{} = "{}" AND '.format(foo, bar)
				# if self.constraints.endswith(' AND '):
				self.constraints = self.constraints[:-5]
			if k == 'what' and type(v) == tuple :
				self.columns = ', '.join(v)
			if k == 'limit' and type(v) == int :
				self.limit = 'LIMIT {}'.format(v)

	def create(self, *args, **kwargs):
		''' INSERT INTO my_table () VALUES () '''
		self._check_arguments(**kwargs)
		query = r'INSERT INTO {t} {s}'.format(t=self.table, s=self.set)
		print(query)
		# return self.db.run_query(query)

	def read(self, *args, **kwargs):
		''' SELECT * FROM my_table WHERE 1 = 1 AND 2 = 2 ORDER BY id LIMIT 1 '''
		self._check_arguments(**kwargs)
		query = r'SELECT {w} FROM {t} WHERE {c} {l} {o}'.format(w=self.columns, t=self.table, c=self.constraints, l=self.limit, o=self.order)
		print(query)
		return self.db.run_query(query)

	def update(self, *args, **kwargs):
		''' UPDATE my_table SET id = 3 WHERE id = 2 LIMIT 1 '''
		self.limit = 'LIMIT 1'
		self._check_arguments(**kwargs)
		query = r'UPDATE {t} SET {s} WHERE {c} {l}'.format(t=self.table, s=self.set, c=self.constraints, l=self.limit)
		print(query)
		# return self.db.run_query(query)

	def delete(self, *args, **kwargs):
		''' DELETE FROM my_table WHERE id = 1 LIMIT 1 '''
		self.limit = 'LIMIT 1'
		self._check_arguments(**kwargs)
		query = r'DELETE FROM {t} WHERE {c} {l}'.format(t=self.table, c=self.constraints, l=self.limit)
		print(query)
		# return self.db.run_query(query)

class DbObject():

	@classmethod
	def find(cls, *args, **kwargs):
		CallingClass = getattr(sys.modules[__name__], cls.__name__)
		# this returns the current class object even if the method is called from child classes
		rows = DbQuery(cls.db, cls.table_name).read(**kwargs)
		instantiated_objects = []
		for row in rows:
			instance = CallingClass(row)
			instantiated_objects.append(instance)
		return instantiated_objects

class User(DbObject):

	db = portale_nca_db
	table_name = 'users'

	def __init__(self, list):
		try:
			self.id = list[0]
			self.branch_id = list[1]
			self.dept_id = list[2]
			self.email = list[3]
			self.full_name = list[4]
			# self.pwd = list[5]
			self.ddi = list[6]
			self.access = list[7]
			self.su = list[8]
			self.address = list[9]
		except IndexError:
			pass

	# @classmethod
	# def find_hr_users(cls):
	# 	cls.find(r'SELECT * FROM {} WHERE id = 1'.format(cls.table_name))

class Dept(DbObject):
	
	db = portale_nca_db
	table_name = 'depts'

	def __init__(self, list):
		try:
			self.id = list[0]
			self.reparto = list[1]
		except IndexError:
			pass

if __name__ == '__main__' :

	table = 'depts'

	constraints = {
	'reparto': 'ict',
	'id': '1',
	}
	set = {
	'reparto': 'ict',
	'id': '1',
	}
	what = ['*']

	DbQuery(portale_nca_db, table).create(set=set)
	DbQuery(portale_nca_db, table).update(set=set)

	DbQuery(portale_nca_db, table).read(limit=20000, constraints=constraints)
	DbQuery(portale_nca_db, table).delete(constraints=constraints, what='*', limit=2)

