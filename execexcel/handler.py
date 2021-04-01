import pandas as pd
import time


class ExecExcel:
    def __init__(self, path, sheet='Sheet1', nana=None):
        """
        read xlsx and csv
        :param path: str
        :param sheet: str
        :param nana: null display NaNa/None/''
        """
        if path.split('.')[-1] == 'csv':
            self.excel_file = pd.read_csv(path)
            ex_data = self.excel_file
        else:
            self.excel_file = pd.ExcelFile(path)
            ex_data = self.excel_file.parse(sheet)
        self.ex_data = ex_data.where(
            ex_data.notnull(), nana)

    def read(self, orient='records', empty=False):
        """
        :param empty: if True show empty value
        :param orient:
        {
        orient=’records’: [{column -> value}, … , {column -> value}],
        orient=’index’  : {index -> {column -> value}},
        orient=’dict’   : {column -> {index -> value}},
        orient=’list’   : {column -> [values]} ,
        orient=’series’ : {column -> Series(values)},
        orient=’split’  : {index -> [index], columns -> [columns], data -> [values]},
        }
        :return: dict : generator object
        """
        data_load = self.ex_data.to_dict(orient=orient)
        if orient == 'records':
            for index, value in enumerate(data_load):
                yield {k: v for k, v in value.items()} if empty else {k: v for k, v in value.items() if v}
        else:
            for index, value in data_load.items():
                if value is dict:
                    yield index, {k: v for k, v in value.items()} if empty else {k: v for k, v in value.items() if v}
                else:
                    yield {index: value}

    @staticmethod
    def write(data: list, filename, path='~/Desktop/'):
        """
        Write data to excel.
        :param data: dict in list
        :param filename: create excel file name
        :param path: excel file save path, default will savet to desktop.
        """

        pd_data = pd.concat([pd.DataFrame(item, index=[0]) for item in data], axis=0)
        pd_data.to_excel(path+filename+f'_{int(time.time())}.xlsx', index=False, sheet_name='data')
