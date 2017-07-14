# from django.db import models
from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost:27017/'
MONGO_DB = 'bi'

class Document:
	def __init__(self, coll_name):
		self.collection_name = coll_name

	def set_fields(self, **kwargs):
		for k in kwargs:
			if k.isdigit():
				setattr(self, 'no_' + k, kwargs[k])
			else:
				setattr(self, k, kwargs[k])

	def get_field(self, k):
		return getattr(self, k, '"{}" field NOT Found'.format(k))

	def get_fields(self):
		return sorted(self.__dict__.items())

	def get_field_keys(self):
		return sorted(self.__dict__.keys())

	def get_field_values(self):
		return self.__dict__.values()



def get_mongoDb_collection(col):
	mongodb_connection = MongoClient(MONGO_HOST)
	database = mongodb_connection[MONGO_DB]
	collection = database[col]
	return collection

def create_object_dict_from_documents(col):
	selected_collection = get_mongoDb_collection(col)
	documents = selected_collection.find( {} )
	# print ('Found Documents: {}'.format(documents.count()))

	instance_dict = {}
	i = 2 # simulates rows in excel sheet
	for document in documents:
		# print('+++++++++++++++++++ Creating instance[{}] +++++++++++++++++++'.format(i))
		# print(type(document))
		instance_dict[i] = Document(col)  # create an object in instance_dict for each document
		instance_dict[i].set_fields(**document)
		# pprint.pprint(instance_dict[i].__dict__)
		i += 1
	return instance_dict

def find(col, value):
	selected_collection = get_mongoDb_collection(col)
	result = selected_collection.find_one( { "stock_number": value } )
	print(result)

# do i really need to always have an array with all objects at hand
yesterday_sold_cars_objects = create_object_dict_from_documents('yesterday_sold_cars')
sales_data_objects = create_object_dict_from_documents('sales_data')
merchant_debt_status_objects = create_object_dict_from_documents('merchant_debt_status')

if __name__ == '__main__' :
	from termcolor import cprint, colored
	# print(sales_data_objects[4].get_fields())
	# print(yesterday_sold_cars_objects[4].get_field_values())
	# find('yesterday_sold_cars', 'YF02158')

	# bar = Collection('yesterday_sold_cars', MONGO_DB)
	# # print(bar.__dict__)
	# # print(type(bar))

	# bar.find( {} )