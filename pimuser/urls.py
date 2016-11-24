# coding: utf-8
"""PIM User urls"""

from django.conf.urls import url
from pimuser import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]