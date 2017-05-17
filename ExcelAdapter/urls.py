from django.conf.urls import url
from data import views as vs

urlpatterns = [
    url(r'^$', vs.main_page, name='test'),
    url(r'get_table_csv/$', vs.get_table_csv, name='get_table_csv'),
    url(r'get_table_excel/$', vs.get_table_excel, name='get_table_excel'),
    url(r'set_file/$', vs.set_table, name="set_table_csv"),
    url(r'show_table/$', vs.show_table, name="show_table")
]
