import sys
import csv
import os
import io
import sys
import importlib

class StockListProvider():

    folder_name = 'data'
    stock_list_file_name = 'StockList.csv'
    path_to_stock_list = '{0}/{1}'.format(folder_name, stock_list_file_name)
    stock_dict = {}

    def __init__(self):
        importlib.reload(sys)
        self.__read_stock_list()

    def __read_stock_list(self):
        if not os.path.isfile(self.path_to_stock_list):
            return None

        file = io.open(self.path_to_stock_list, 'r', encoding='utf-8')
        csv_cursor = csv.reader(file)
        for row in csv_cursor:
            self.stock_dict[row[0]] = row[1]

    def stock_id_exists(self, id):
        if id in self.stock_dict:
            return True
        else:
            return False

    def get_stock_id_list(self):
        return self.stock_dict.keys()

#
# def main():
#     provider = StockListProvider()
#
# if __name__ == '__main__':
#         main()