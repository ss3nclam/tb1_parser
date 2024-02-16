# from configparser import ConfigParser
from src.tb1 import TB1
from src.tb1_sheet import TB1Sheet
from pandas import ExcelFile, set_option
from src.config import config


# Вывод всей таблички целиком
set_option("display.max_rows", None)


def main():
    
    file = ExcelFile(config['TB1']['file_path'])
    tb1 = TB1(file)

    tb1.read()
    Ai_sheet: TB1Sheet = tb1.get('Ai')
    print(Ai_sheet)