# from django.db import models
from pymongo import MongoClient

class Document:
	def __init__(self):
		pass

	def set_fields(self, **kwargs):
		for k in kwargs:
			if k.isdigit():
				setattr(self, 'no_' + k, kwargs[k])
			else:
				setattr(self, k, kwargs[k])

	def get_field(self, k):
		return getattr(self, k, '"{}" field NOT Found'.format(k))

	def get_fields(self):
		return self.__dict__.items()

	def get_field_keys(self):
		return self.__dict__.keys()

	def get_field_values(self):
		return self.__dict__.values()

def get_mongoDb_collection(conn, db, col):
	mongodb_connection = MongoClient(conn)
	database = mongodb_connection[db]
	collection = database[col]
	return collection

def create_object_dict_from_documents(db, col):
	sales_collection = get_mongoDb_collection('mongodb://localhost:27017/', db, col)
	documents = sales_collection.find( {} )
	# print ('Found Documents: {}'.format(documents.count()))

	instance_dict = {}
	i = 2 # simulates rows in excel sheet
	for document in documents:
		# print('+++++++++++++++++++ Creating instance[{}] +++++++++++++++++++'.format(i))
		# print(type(document))
		instance_dict[i] = Document()  # create an object in instance_dict for each document
		instance_dict[i].set_fields(**document)
		# pprint.pprint(instance_dict[i].__dict__)
		i += 1
	return instance_dict

# returns a dict with objects
it_yesterday_sold_cars_objects = create_object_dict_from_documents('bi', 'it_yesterday_sold_cars')
sales_data_objects = create_object_dict_from_documents('bi', 'sales_data')
