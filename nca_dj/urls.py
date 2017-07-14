"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from kpi import views as kpi_views
from human import views as human_views
from data_analyst import views as data_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', kpi_views.aftersales),
    url(r'^aftersales$', kpi_views.aftersales),
    url(r'^bookingcenter$', kpi_views.bookingcenter),
    url(r'^log$', kpi_views.log_stats),
    url(r'^aftersales/(?P<day>\d{4}-\d{2}-\d{2})$', kpi_views.day_detail, name='day_url_name'),
    url(r'^d3$', data_views.d3),

    url(r'^hr$', human_views.main),
    url(r'^contestazioni$', human_views.disciplina),
    url(r'^dipendente(?P<day>\d{4})$', human_views.dipendente, name='day'),
    url(r'^render_cd$', human_views.render_cd),
]

    # r'string' denotes a raw_string: DO NOT interpret backslashes
    # ^         caret denotes start of the string
    # $         dollar denotes end of the string
    # ()        parentheses capture unicode strings to pass to the view
    # ?P<day>   sets day as the unique parameter name that will be accepted by the referenced view