# render shortcut handles template loading, context creation, template rendering and HttpResponse return 
from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.conf import settings

from human.models import User, Branch, Dept, Lc, Contestazione, Sanzione
from human.forms import NewContestazione

import MySQLdb, datetime

def take_pic():
	""" Takes pic of found resource """
	# check if PhantomJS is installed?

	resource = 'human/render_cd.html'
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys # not really needed
	from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

	phantomJs_specs = DesiredCapabilities.PHANTOMJS
	driver = webdriver.PhantomJS( desired_capabilities = phantomJs_specs )
	# Do i need all this DesiredCapabilities crap? what does it do ?

	driver = webdriver.PhantomJS()
	time.sleep(2) # wait for resource to load
	driver.set_window_size(1024, 768)
	driver.get(resource)
	driver.save_screenshot('wor'+".pdf")
	driver.quit()

def render_cd(request, *args, **kwargs):

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NewContestazione(request.POST)
		if form.is_valid():

			values = [None, ] # id must be blank so it nows to use CREATE instead of UPDATE
			values.append(form.cleaned_data['user_id'])
			values.append(346) # Turco
			values.append(datetime.datetime.now())
			values.append(form.cleaned_data['note'])
			values.append(form.cleaned_data['suspend'])
			# if form.cleaned_data['suspend']:
			# 	values[5] = form.cleaned_data['suspend']

			new_contestazione = Contestazione(values)
			new_contestazione.save()

			contested_user = User.find(
				strict_constraints={
					'id' : new_contestazione.user_id,
				}
			)[0]

			if new_contestazione.suspend == True:
				suspend_string = 'Mentre attendiamo Sue eventuali giustificazioni entro 5 giorni dal ricevimento della presente, disponiamo la Sua sospensione cautelare immediata dal lavoro ma non dalla retribuzione.'
			else :
				suspend_string = 'Lei potrà presentare se lo riterrà opportuno, le Sue giustificazioni entro 5 giorni dal ricevimento della presente.'


			# problems twith italian TEST_CHARSET: db collation ???

			return render( request, 'human/render_cd.html', {
				'suspend': suspend_string,
				'user': contested_user,

				'id': new_contestazione.id,
				# will need to set this after creating entry

				'note': new_contestazione.note,
				'punisher_id': new_contestazione.punisher_id,
				'date': new_contestazione.date
			})
			
	else:
		return HttpResponseRedirect('/contestazioni')

def users(request):

	hr_users = User.find(
		restrictions={
			'email' : ['.agency@auto1.com', '.branch@auto1.com'],
		}
	)
	return render(request, 'human/users.html', {
	    'user_count' : len(hr_users),
	    'users' : hr_users,
	})


def depts(request):

	all_depts = Dept.find()
	return render(request, 'human/depts.html', {
	    'dept_count' : len(all_depts),
	    'depts' : all_depts,
	})

def branches(request):

	branches = Branch.find(
		strict_restrictions={
			'filiale' : ['Milano HQ'],
		}, order='filiale'
	)
	lcs = Lc.find()
	return render(request, 'human/branches.html', {
	    'branches' : branches,
	    'branch_count' : len(branches),
	    'lcs' : lcs,
	})

def lcs(request):

	lcs = Lc.find()
	return render(request, 'human/lcs.html', {
	    'lcs' : lcs,
	    'lc_count' : len(lcs),
	})


def disciplina(request):

	form = NewContestazione()

	hr_users = User.find(
		restrictions={
			'email' : ['.agency@auto1.com', '.branch@auto1.com'],
		}
	)
	contestazioni = Contestazione.find()
	sanzioni = Sanzione.find()

	return render(request, 'human/disciplina.html', {
		'form': form,
	    'contestazioni' : contestazioni,
	    'active_contestazioni' : 999,
	    'contestazioni_count' : len(contestazioni),
	    'sanzioni' : sanzioni,
	    'sanzioni_count' : len(sanzioni),
	    'users' : hr_users
	})

def dipendente(request):
	return redirect(request, 'human/dipendente.html', {
	})

# if __name__ == '__main__':
