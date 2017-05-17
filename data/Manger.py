# coding=utf-8
import pandas as pd
from ExcelAdapter.settings import ENGINE


# Повертає таблицю з бд у вигляді DataFrame
def get_table(table_name):
    return pd.read_sql("Select * From %s" % table_name, ENGINE)
