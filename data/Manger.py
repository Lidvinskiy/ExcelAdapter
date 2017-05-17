# coding=utf-8
import pandas as pd
from django.db import connection as con
from ExcelAdapter.settings import ENGINE


class Manager(object):
    @staticmethod
    def get_table(table_name):
        return pd.read_sql("Select * From %s" % table_name, ENGINE)
