# coding=utf-8
import pandas as pd
from ExcelAdapter.settings import ENGINE


# Повертає таблицю з бд у вигляді DataFrame
def get_table(table_name):
    return pd.read_sql("Select * From '%s'" % table_name, ENGINE)


def get_joined(first_table_name, second_table_name, left_on, right_on):
    df1 = get_table(first_table_name)
    df2 = get_table(second_table_name)
    return df1.merge(df2, left_on=left_on, right_on=right_on)
