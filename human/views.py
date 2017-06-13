# render shortcut handles template loading, context creation, template rendering and HttpResponse return 
from django.shortcuts import render 
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
import MySQLdb, datetime
from human.models import User, Dept

def default(request):

	constraints = {
		'reparto': 'ict',
		'id': '1',
	}
	found_depts = Dept.find(constraints=constraints)

	constraints = {
		# 'full_name': 'Federico Rizzo',
		# 'id': '1',
		'1': '1',
	}
	found_users = User.find(constraints=constraints)

	return render(request, 'human/hr.html', {
	    'user_count' : len(found_users),
	    'users' : found_users,
	    'dept_count' : len(found_depts),
	    'depts' : found_depts,
	})

# if __name__ == '__main__':
