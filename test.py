# from pandas import DataFrame, read_excel, set_option


# from src.config import config


# set_option("display.max_rows", None)

# # file = read_excel('table.xlsx', 'Питание', index_col=0)


# class TB1:

#     def __init__(self) -> None:
#         self.__Ai_sheet: DataFrame
#         self.__Di_sheet: DataFrame
#         self.__Do_sheet: DataFrame


#     def read(self):
#         pass


#     def get(self):
#         pass



from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')

xz = config['Ai_SHEET']['name_sheet_regex']

print(xz)