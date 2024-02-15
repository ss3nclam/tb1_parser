from configparser import ConfigParser
from src.tb1 import TB1

from pandas import ExcelFile


config = ConfigParser()
config.read('config.ini')
tb1_config = config['TB1']


def main():
    
    file = ExcelFile(tb1_config['file_path'])
    tb1 = TB1(file)

    try:
        print(tb1.sheets)
    except Exception as error:
        print(error)
    finally:
        tb1.read()
        print(tb1.sheets)