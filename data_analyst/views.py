from django.shortcuts import render
from data_analyst.models import sales_data_objects, yesterday_sold_cars_objects
from django.http import HttpResponse

def list_field(dict, field):
	d = {}
	for row_no, object in dict.items():
		d[row_no] = object.get_field(field)
	return d

def find_object_by_field(dict, column, value):
	for row_no, object in dict.items():
		if object.get_field(column) == value:
			return object

def d3(request):
	sales_data_objects_amount = len(sales_data_objects)
	yesterday_sold_cars_objects_amount = len(yesterday_sold_cars_objects)
	foo = sales_data_objects.get(8).get_field('buy_price')
	companies = list_field(yesterday_sold_cars_objects, 'company')
	# result_object = find_object_by_field(yesterday_sold_cars_objects, 'company', 'Ferrari Auto Srl')
	result_object = find_object_by_field(sales_data_objects, 'Salesrep_Assigned', 'Account Pool - IT')

	return render(request, 'kpi/d3.html', {
		'companies': companies ,
		'result': result_object ,
		'foo': foo ,
		})
	# return HttpResponse('{}'.format(n))
