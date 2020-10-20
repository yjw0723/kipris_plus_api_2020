from db_attribute import user,password,host,database_name
from img_vienna import DataBase
DB = DataBase(user=user, password=password, host=host, database_name=database_name)

BIBLO_TABLE_NAME = 'total_vienna_small_category'
COLUMN = 'regPrivilegeName'
sql = f'alter table {BIBLO_TABLE_NAME} modify {COLUMN} VARCHAR(1500);'
DB.conn.execute(sql)