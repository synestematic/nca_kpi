from django.db import models
from django.conf import settings
from django.core import exceptions as django_exceptions
from django import forms
from human.models import User

import MySQLdb, datetime, sys, inspect

class NewContestazione(forms.Form):
	note = forms.CharField(initial= 'Descrizione contestazione...', widget=forms.Textarea, max_length=1000)
	suspend = forms.BooleanField(label='Sospensione Immediata', required=False)
	user_id = forms.ChoiceField(choices=User.ids_to_users())


# if __name__ == '__main__' :

