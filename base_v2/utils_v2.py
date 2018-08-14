# coding=utf8
import xlrd
import xlwt

from qbsy import settings as st


def excel_to_list(path, start_row):
    table = xlrd.open_workbook(st.BASE_DIR + path).sheets()[0]
    temp_list = []
    for index_i in range(start_row, table.nrows):
        temp_list.append(table.row_values(index_i))
    return temp_list


def write_list_to_excel(list, filename):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    for index_i, l_1 in enumerate(list):
        for index_j, l_2 in enumerate(l_1):
            worksheet.write(index_i, index_j, label=l_2)
    path = st.BASE_DIR + '/media/temp/{0}'.format(filename)
    workbook.save(path)
    return '/media/temp/{filename}'.format(filename=filename)
