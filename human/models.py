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

		self.handle.commit()
		self.disconnect()
		return rows

	def get_columns(self, table):
		self.connect()
		query = 'SELECT * FROM {} LIMIT 1'.format(table)
		self.cursor.execute(query)

		column_names = [i[0] for i in self.cursor.description]

		self.disconnect()
		return column_names

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
		self.setters = ''
		self.limit = ''
		self.order = ''

	def _parse_arguments(self, *args, **kwargs):
		for k, v in sorted(kwargs.items()): 
			# sorted makes sure 'constraints' are dealt before 'restrictions'
			self._set_constraints(k, v)
			self._set_setters(k, v)
			self._set_columns(k, v)
			self._set_limit(k, v)
			self._set_order(k, v)

	def _set_constraints(self, k, v):
		operator = '' if k.startswith('strict_') else '%'

		if k.endswith('constraints') and type(v) == dict and len(v) > 0 :
			for foo, bar in v.items():
				if type(bar) == list:
					for item in bar:
						self.constraints += '{f} LIKE "{o}{i}{o}" AND '.format(f=foo, i=item, o=operator)
				else:
					self.constraints += '{f} LIKE "{o}{b}{o}" AND '.format(f=foo, b=bar, o=operator)
			self.constraints = 'WHERE ' + self.constraints[:-5]

		if k.endswith('restrictions') and type(v) == dict and len(v) > 0 :
			for foo, bar in v.items():
				if self.constraints != '':
					if type(bar) == list:
						for item in bar:
							self.constraints += ' AND {f} NOT LIKE "{o}{i}{o}"'.format(f=foo, i=item, o=operator)
					else:
						self.constraints += ' AND {f} NOT LIKE "{o}{b}{o}"'.format(f=foo, b=bar, o=operator)
				else :
					if type(bar) == list:
						for item in bar:
							self.constraints += '{f} NOT LIKE "{o}{i}{o}" AND '.format(f=foo, i=item, o=operator)
					else:
						self.constraints += '{f} NOT LIKE "{o}{b}{o}" AND '.format(f=foo, b=bar, o=operator)
					self.constraints = 'WHERE ' + self.constraints[:-5]

	def _set_setters(self, k, v):
		calling_function = inspect.stack()[2][3]
		if k == 'set' and type(v) == dict and len(v) > 0 :
			if calling_function == 'create':
				columns, values = [], []
				for foo, bar in v.items():
					columns.append(str(foo))
					if bar == True : bar = '1'
					elif bar == False : bar = '0'
					values.append(str(bar))
				foo = ', '.join(columns)
				bar = '", "'.join(values)
				self.setters = '(' + foo + ') VALUES ("' + bar + '")'
			elif calling_function == 'update':
				for foo, bar in v.items():
					self.setters += '{} = "{}", '.format(foo, bar)
				self.setters = self.setters[:-2]
	
	def _set_columns(self, k, v):
		if k == 'what' and type(v) == tuple :
			self.columns = ', '.join(v)

	def _set_limit(self, k, v):
		if k == 'limit' and type(v) == int :
			self.limit = 'LIMIT {}'.format(v)

	def _set_order(self, k, v):
		if k == 'order' and type(v) == str :
			self.order = 'ORDER BY {}'.format(v)

	def create(self, *args, **kwargs):
		''' INSERT INTO my_table () VALUES () '''
		self._parse_arguments(**kwargs)
		query = r'INSERT INTO {t} {s}'.format(t=self.table, s=self.setters)
		# print(query)
		return self.db.run_query(query)

	def read(self, *args, **kwargs):
		''' SELECT * FROM my_table WHERE 1 = 1 AND 2 = 2 ORDER BY id LIMIT 1 '''
		self._parse_arguments(**kwargs)
		self.query = r'SELECT {w} FROM {t} {c} {l} {o}'.format(w=self.columns, t=self.table, c=self.constraints, l=self.limit, o=self.order)
		# print(self.query)
		return self.db.run_query(self.query)

	def update(self, *args, **kwargs):
		''' UPDATE my_table SET user_id = 3, suspend = 1 WHERE id = 2 LIMIT 1 '''
		self.limit = 'LIMIT 1'
		self._parse_arguments(**kwargs)
		query = r'UPDATE {t} SET {s} {c} {l}'.format(t=self.table, s=self.setters, c=self.constraints, l=self.limit)
		# print(query)
		return self.db.run_query(query)

	def delete(self, *args, **kwargs):
		''' DELETE FROM my_table WHERE id = 1 LIMIT 1 '''
		self.limit = 'LIMIT 1'
		self._parse_arguments(**kwargs)
		query = r'DELETE FROM {t} {c} {l}'.format(t=self.table, c=self.constraints, l=self.limit)
		# print(query)
		return self.db.run_query(query)

class DbObject():

	db = portale_nca_db

	@classmethod
	def find(cls, *args, **kwargs):
		rows = DbQuery(cls.db, cls.table_name).read(**kwargs)
		if 'instantiate' in kwargs and kwargs['instantiate'] == False:
			# remember that not instantiating means getting tuples with no keys that are very hard to parse for data 
			return rows
		else:
			CallingClass = getattr(sys.modules[__name__], cls.__name__)
			# this returns the current class object even if the method is called from child classes
			instantiated_objects = []
			for row in rows:
				instance = CallingClass(row)
				instantiated_objects.append(instance)
			return instantiated_objects

	@classmethod
	def find_by_id(cls, *args, **kwargs):
		return cls.find(
			strict_constraints={
				'id' : args[0],
			},
		limit=1, **kwargs
		)

	def remove(self, *args, **kwargs):
		return DbQuery(self.db, self.table_name).delete(
			strict_constraints={'id': self.id},
			# limit=1,
			**kwargs
		)

	def save(self, *args, **kwargs):
		only_sql_columns = { key : value for key, value in self.__dict__.items() if key in self.table_columns and key != 'id' }
		if self.id and self.id is not '' :
			return DbQuery(self.db, self.table_name).update(
				set=only_sql_columns, 
				strict_constraints={'id': self.id}, 
				**kwargs
			)
		else :
			return DbQuery(self.db, self.table_name).create(
				set=only_sql_columns,
				**kwargs
			)

users_table = 'users'
users_columns = portale_nca_db.get_columns(users_table)

class User(DbObject):

	table_name = users_table
	table_columns = users_columns

	def __init__(self, values):
		try:
			self.id = values[0]
			self.branch_id = values[1]
			self.dept_id = values[2]
			self.email = values[3]
			self.full_name = values[4]
			# self.pwd = values[5]
			self.ddi = values[6]
			self.access = values[7]
			self.su = values[8]
			self.address = values[9]

			self._set_dept()
			self._set_branch()
		except IndexError:
			pass

	@classmethod
	def find_by_dept_id(cls, *args, **kwargs):
		return cls.find(
			strict_constraints={
				'dept_id' : args[0],
			}, **kwargs,
		)

	@classmethod
	def find_by_branch_id(cls, *args, **kwargs):
		return cls.find(
			strict_constraints={
				'branch_id' : args[0],
			}, **kwargs,
		)

	def _set_dept(self):
		# self.dept = Dept.find_by_id(self.dept_id)[0].reparto if self.dept_id else ''
		self.dept = Dept.find_by_id(self.dept_id, instantiate=False)[0][1] if self.dept_id else ''

	def _set_branch(self):
		# self.branch = Branch.find_by_id(self.branch_id)[0].filiale if self.branch_id else ''
		self.branch = Branch.find_by_id(self.branch_id, instantiate=False)[0][2] if self.branch_id else ''

	@classmethod
	def ids_to_users(cls, *args, **kwargs):
		all_users = cls.find(
			restrictions={
				'email' : ['.agency@auto1.com', '.branch@auto1.com'],
			}, instantiate=False,
			**kwargs,
		)
		ids_to_user = list((user[0], user[4]) for user in all_users)
		return ids_to_user

branches_table = 'branches'
branches_columns = portale_nca_db.get_columns(branches_table)

class Branch(DbObject):
	
	table_name = branches_table
	table_columns = branches_columns

	def __init__(self, values):
		try:
			self.id = values[0]
			self.lc_id = values[1]
			self.filiale = values[2]
			self.nb_number = values[3]
			self.nas_share = values[4]
			self._set_lc()
			self._set_user_count()
		except IndexError:
			pass

	def _set_lc(self):
		# self.lc = Lc.find_by_id(self.lc_id)[0].centro if self.lc_id else ''
		self.lc = Lc.find_by_id(self.lc_id, instantiate=False)[0][1] if self.lc_id else ''

	def _set_user_count(self):
		# DO NOT instantiate in order to avoid infinite recursion
		self.user_count = len(User.find_by_branch_id(self.id, instantiate=False)) if self.id else 0 

depts_table = 'depts'
depts_columns = portale_nca_db.get_columns(depts_table)

class Dept(DbObject):
	
	table_name = depts_table
	table_columns = depts_columns

	def __init__(self, values):
		try:
			self.id = values[0]
			self.reparto = values[1]
			self._set_user_count()
		except IndexError:
			pass

	def _set_user_count(self):
		# DO NOT instantiate in order to avoid infinite recursion
		# User -> Dept -> User -> Dept ...
		self.user_count = len(User.find_by_dept_id(self.id, instantiate=False)) if self.id else 0 

lcs_table = 'lcs'
lcs_columns = portale_nca_db.get_columns(lcs_table)

class Lc(DbObject):
	
	table_name = lcs_table
	table_columns = lcs_columns

	def __init__(self, values):
		try:
			self.id = values[0]
			self.centro = values[1]
		except IndexError:
			pass

contestazioni_table = 'contestazioni'
contestazioni_columns = portale_nca_db.get_columns(contestazioni_table)

class Contestazione(DbObject):
	
	table_name = contestazioni_table
	table_columns = contestazioni_columns

	def __init__(self, values):
		try:
			self.id = values[0]
			self.user_id = values[1]
			self.punisher_id = values[2]
			self.date = values[3]
			self.note = values[4]
			self.suspend = values[5]

			self._set_user()
		except IndexError:
			pass

	def _set_user(self):
		self.user = User.find_by_id(self.user_id, instantiate=False)[0][4] if self.user_id else ''

sanzioni_table = 'sanzioni'
sanzioni_columns = portale_nca_db.get_columns(sanzioni_table)

class Sanzione(DbObject):
	
	table_name = sanzioni_table
	table_columns = sanzioni_columns

	def __init__(self, values):
		try:
			self.id = values[0]
			self.contestazione_id = values[1]
			self.punisher_id = values[2]
			self.date = values[3]
			self.note = values[4]
			self.user = self._set_user()
		except IndexError:
			pass

	def _set_user(self):
		return Contestazione.find_by_id(self.contestazione_id)[0].user if self.contestazione_id else ''

	def _set_user_without_db(self, contestazioni):
		for contestazione in contestazioni:
			if contestazione.id == self.contestazione_id:
				return contestazione.user
		return ''

# if __name__ == '__main__' :

# READ
	# cont_to_edit = Contestazione.find()[0]
	# print(cont_to_edit.id)
	# print(cont_to_edit.user)
	# print(cont_to_edit.user_id)

	# # cont_to_edit.user = 'bla'
	# cont_to_edit.user_id = '195'
	# cont_to_edit.save()
# UPDATE


# CREATE / UPDATE
	# values = [None, ]
	# # values[0] = 1		# ID auto increment
	# values.append(342)	# user ID
	# values.append(348)	# punisher
	# values.append(datetime.datetime.now())	
	# values.append('Bella li zio')
	# values.append(0)	# suspend

	# # print(values)
	# new_contestazione = Contestazione(values)
	# new_contestazione.save()

# DELETE
	# cont_to_del = Contestazione.find()[0]
	# cont_to_del.remove()

# IM HAVING A PROBLEM WITH INSTANCE ATTRIBUTES NOT BEING DIFFERENTIATED BETWEEN SQL FIELDS AND NOT............



# MAYBE THE PERFORMANCE DIP IS NOT BECAUSE:
# 	I INSTANTIATE OBJECTS FOR EACH SQL RESULT
# BUT BECAUSE:
# 	EVERY TIME I INSTANTIATE OBJECTS I INIT THEM WITH DATA THAT LOOKS INTO OTHER TABLES
# THEREFORE TRY:
# 	TO ONLY GET DATA FROM OTHER TABLES WHEN NEEDED AND NOT AT INIT TIME