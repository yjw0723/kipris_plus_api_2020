from img_vienna_2 import *
from api_key import API_KEY #API_KEY는 문자열입니다. kipris plus(http://plus.kipris.or.kr/)에서 발급받을 수 있습니다.
from db_attribute import user, password, host, database_name

"""
db_attribute example:

user = 'root'
password = '1234'
host = 'localhost'
database_name = 'db_name'

API_KEY example:
API_KEY = '&ServiceKey=siEj7vZ00RvZGu=2ssRtLL2OP7K0AjJda1n=odrfN7Q='
"""

IMG_SAVE_FOLDER = 'E:/data/viennacode_total_img_19600101_20191231'
BIBLO_TABLE_NAME = 'oa_appnum'
DATE_PAGE_TABLE_NAME = "oa_page_num"
BIBLO_TABLE_SQL = sql = f'CREATE TABLE {BIBLO_TABLE_NAME} (applicationNumber VARCHAR(14));'

DATA_PAGE_TABLE_SQL = f'CREATE TABLE {DATE_PAGE_TABLE_NAME} (DATE VARCHAR(17), CURRENT_PAGE SMALLINT(1), TOTAL_PAGE SMALLINT(1));'
db = DataBase(user=user, password=password, host=host, database_name=database_name)
make_path = MAKEPATH(IMG_SAVE_FOLDER)
download = DOWNLOAD(db, make_path, BIBLO_TABLE_NAME, DATE_PAGE_TABLE_NAME)
execute = EXECUTE(db, download, API_KEY)

LAST_YEAR = 2019
LAST_MONTH = 1

if not BIBLO_TABLE_NAME in db.TABLELIST:
    db.executeSQL(BIBLO_TABLE_SQL)

if __name__ == '__main__':
    if not DATE_PAGE_TABLE_NAME in db.TABLELIST:
        db.executeSQL(DATA_PAGE_TABLE_SQL)
        execute.saveFromLastYear(LAST_YEAR, LAST_MONTH)
    else:
        last_year, last_month, last_page, total_page = execute.getLastYearAndMonth()
        if last_page != total_page:
            execute.saveFromLastMonth(last_year, last_month, last_page, total_page)
            last_year = last_year - 1
            last_month = 1
            execute.saveFromLastYear(last_year, last_month)
        else:
            last_year = last_year - 1
            last_month = 1
            execute.saveFromLastYear(last_year, last_month)