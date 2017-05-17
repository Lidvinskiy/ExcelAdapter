"""ExcelAdapter URL Configuration

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
from data import views as vs

urlpatterns = [
    url(r'^$', vs.main_page, name='test'),
    url(r'get_table_csv/$', vs.get_table_csv, name='get_table_csv'),
    url(r'get_table_excel/$', vs.get_table_excel, name='get_table_excel'),
    url(r'set_file/$', vs.set_table_csv, name="set_table_csv"),
    url(r'show_table/$', vs.show_table, name="show_table")
]
