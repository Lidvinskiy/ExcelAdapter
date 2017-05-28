# coding=utf-8
import codecs
from io import BytesIO
from io import StringIO
import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pandas import ExcelWriter
import pandas as pd
from ExcelAdapter import settings
from data.Manger import get_table, get_joined


# Функція загрузка сторінки
def main_page(request):
    base_tables = ['django_migrations',
                   'sqlite_sequence',
                   'auth_group_permissions',
                   'auth_user_groups',
                   'auth_user_user_permissions',
                   'django_admin_log',
                   'django_content_type',
                   'auth_permission',
                   'auth_user',
                   'django_session',
                   'auth_group']
    tables_ex = settings.ENGINE.connect().execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';").fetchall()
    print(tables_ex)
    tables_new = []
    for i in tables_ex:
        if i[0] not in base_tables:
            tables_new.append(i[0])
    columns = {}
    for i in tables_new:
        cols = settings.ENGINE.connect().execute(
            "select column_name from information_schema.columns where table_name='%s';" % i).fetchall()
        column_names = []
        for names in cols:
            column_names.append(names[1])
        columns[i] = column_names
    context = {
        "tables": tables_new,
        "tables_and_columns": json.dumps(columns)
    }
    return render(request, 'main.html', context)


# Функція надсилання csv файлу
def get_table_csv(request, table_name=''):
    data = get_table(request.GET['table_name'])
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="csv_file.csv"'
    data.to_csv(response, encoding='utf-8', sep=';', index=False, float_format='%.3f')
    return response


# Функція надсилання Excel файлу
def get_table_excel(request, table_name=''):
    data = get_table(request.GET['table_name'])
    sio = BytesIO()
    writer = ExcelWriter(sio, engine='xlsxwriter')
    data.to_excel(writer, encoding='utf-8', index=False)
    writer.save()
    sio.seek(0)
    response = HttpResponse(sio.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="excel.xlsx"'
    return response


# Функція отримання файлу та його збереження до бд
@csrf_exempt
def set_table(request):
    if request.method == 'POST':
        file = request.FILES["file"]
        if file.name.endswith(".csv"):
            file = file.read().decode("utf-8")
            demo_file = StringIO(file)
            df = pd.read_csv(demo_file, sep=";", encoding="utf-8")
            df.to_sql(request.POST.get("table-name"), settings.ENGINE, if_exists="replace", index=False)
            return HttpResponse(True)
        if file.name.endswith(".xlsx"):
            file = file.read()
            demo_file = BytesIO(file)
            df = pd.read_excel(demo_file, index_col=False)
            df.to_sql(request.POST.get("table-name"), settings.ENGINE, if_exists="replace", index=False)
            return HttpResponse(True)
        return HttpResponse(False)


# Функція надсилає HTML таблицю
def show_table(request, table_name=''):
    try:
        df = get_table(request.GET['table_name'])
        data = {"table": df.to_html(
            classes=['table', 'table-striped', 'table-hover', 'table-responsive', 'table-report'], border=0)
        }
        return JsonResponse(data)
    except:
        return HttpResponse(False)


def get_table_join_csv(request, table_name=''):
    data = get_joined(request.GET['first_table_name'], request.GET['second_table_name'], request.GET['left_on'],
                      request.GET['right_on'])
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="csv_file.csv"'
    data.to_csv(response, encoding='utf-8', sep=';', index=False, float_format='%.3f')
    return response


# noinspection PyTypeChecker
def get_table_join_excel(request, first_table_name='', second_table_name='', left_on='', right_on=''):
    data = get_joined(request.GET['first_table_name'], request.GET['second_table_name'], request.GET['left_on'],
                      request.GET['right_on'])
    sio = BytesIO()
    writer = ExcelWriter(sio, engine='xlsxwriter')
    data.to_excel(writer, encoding='utf-8', index=False)
    writer.save()
    sio.seek(0)
    response = HttpResponse(sio.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="excel.xlsx"'
    return response


def show_joined_table(request, first_table_name='', second_table_name='', left_on='', right_on=''):
    df = get_joined(request.GET['first_table_name'], request.GET['second_table_name'], request.GET['left_on'],
                    request.GET['right_on'])
    data = {"table": df.to_html(
        classes=['table', 'table-striped', 'table-hover', 'table-responsive', 'table-report'], border=0)
    }
    return JsonResponse(data)
