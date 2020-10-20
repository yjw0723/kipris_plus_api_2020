from db_attribute import user,password,host,database_name
from img_vienna import DataBase
DB = DataBase(user=user, password=password, host=host, database_name=database_name)

if __name__ == '__main__':
    DB.dropTable('oa_appnum')
    DB.dropTable('oa_page_num')