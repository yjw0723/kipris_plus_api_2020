from db_attribute import user,password,host,database_name
from img_vienna import DataBase
DB = DataBase(user=user, password=password, host=host, database_name=database_name)

if __name__ == '__main__':
    DB.dropTable('total_vienna_small_category')
    DB.dropTable('total_date_page_num')



