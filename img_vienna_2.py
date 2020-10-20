import os, requests
import urllib.request
from time import sleep
import http
import urllib3
from tqdm import tqdm
import pandas as pd
from sqlalchemy import create_engine
import xmltodict, json


class DataBase:
    def __init__(self, host, user, password, database_name):
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name
        self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database_name}')
        self.conn = self.engine.connect()
        self.TABLELIST = []
        self.checkTables()

    def checkTables(self):
        self.TABLELIST = []
        sql = 'SHOW TABLES;'
        result = self.conn.execute(sql)
        row = result.fetchall()
        table_list = []
        for i in row:
            table_list.append(i[0])
        self.TABLELIST = table_list

    def executeSQL(self, sql):
        # create new table: "CREATE TABLE book_details(book_id INT(5), title VARCHAR(20), price INT(5))"
        # alter table(ADD COLUMN): "ALTER TABLE book_details ADD column_name datatype"
        # alter table(MODIFY COLUMN): "ALTER TABLE book_details MODIFY column_name datatype"
        self.conn.execute(sql)

    def appendDataFrameToTable(self, df, table_name):
        df.to_sql(name=table_name, con=self.engine, if_exists='append', index=False)

    def appendDataToTable(self, data, table_name):
        column_names = []
        sql = f'SHOW columns From {table_name};'
        result = self.conn.execute(sql)
        row = result.fetchall()
        for i in row:
            column_names.append(i[0])
        result = ', '.join(column_names)
        sql = f'INSERT INTO {table_name} ({result}) VALUES {data};'
        self.conn.execute(sql)

    def updateTable(self, df, table_name):
        df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)

    def exportData(self, table_name):
        return pd.read_sql_table(table_name, self.conn)

    def dropTable(self, table_name):
        sql = f'DROP TABLE {table_name};'
        self.conn.execute(sql)


class DATE:
    def __init__(self, last_year, last_month=1):
        self.LAST_YEAR = last_year
        self.LAST_MONTH = last_month
        self.MONTH_LIST = []
        self.start_full_date_list = []
        self.end_full_date_list = []
        self.DATE_LIST = []

    def initMonthAndDateList(self):
        self.MONTH_LIST = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.DATE_LIST = ['31', '28', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31']
        if int(self.LAST_YEAR) % 4 == 0:
            self.DATE_LIST[1] = '29'
            if int(self.LAST_YEAR) % 100 == 0:
                self.DATE_LIST[1] = '28'
                if int(self.LAST_YEAR) % 400 == 0:
                    self.DATE_LIST[1] = '29'
            else:
                self.DATE_LIST[1] = '29'

    def makeDateList(self):
        for month, date in zip(self.MONTH_LIST, self.DATE_LIST):
            start_date = f'{self.LAST_YEAR}{month}01'
            end_date = f'{self.LAST_YEAR}{month}{date}'
            self.start_full_date_list.append(start_date)
            self.end_full_date_list.append(end_date)

    def returnDateList(self):
        self.initMonthAndDateList()
        if self.LAST_MONTH != 1:
            self.MONTH_LIST = self.MONTH_LIST[self.LAST_MONTH - 1:]
            self.DATE_LIST = self.DATE_LIST[self.LAST_MONTH - 1:]
            self.makeDateList()
        else:
            self.makeDateList()
        return self.start_full_date_list, self.end_full_date_list


class URL:
    def __init__(self, start_date, end_date, api_key):
        self.BASIC_URL = 'http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch?'
        self.START_DATE = start_date
        self.END_DATE = end_date
        self.APPLICATION = 'application=TRUE'
        self.REGISTRATION = '&registration=TRUE'
        self.REFUSED = '&refused=TRUE'
        self.EXPRIATION = '&expiration=TRUE'
        self.WITHDRAWAL = '&withdrawal=TRUE'
        self.PUBLICATION = '&publication=TRUE'
        self.CANCEL = '&cancel=TRUE'
        self.ABANDONMENT = '&abandonment=TRUE'
        self.TRADEMARK = '&trademark=TRUE'
        self.SERVICEMARK = '&serviceMark=TRUE'
        self.TRADEMARKSERVICEMARK = '&trademarkServiceMark=TRUE'
        self.BUSINESSEMBLEM = '&businessEmblem=TRUE'
        self.COLLECTIVEMARK = '&collectiveMark=TRUE'
        self.INTERNATIONALMARK = '&internationalMark=TRUE'
        self.CHARACTER = '&character=TRUE'
        self.FIGURE = '&figure=TRUE&figureComposition=FALSE'
        self.COMPOSITIONCHARACTER = '&compositionCharacter=TRUE'
        self.FIGURECOMPOSITON = '&figureComposition=TRUE'
        self.NUMOFROWS = '&numOfRows=500'
        self.PAGENUM = '&pageNo=1'
        self.APPLICATIONDATE = f'&applicationDate={self.START_DATE}~{self.END_DATE}'
        self.SERVICEKEY = api_key

    def returnURL(self, idx):
        self.URL = f'{self.BASIC_URL}{self.APPLICATION}{self.REGISTRATION}{self.REFUSED}{self.EXPRIATION}{self.WITHDRAWAL}{self.PUBLICATION}{self.CANCEL}{self.ABANDONMENT}{self.TRADEMARK}{self.SERVICEMARK}' \
                   f'{self.TRADEMARKSERVICEMARK}{self.BUSINESSEMBLEM}{self.COLLECTIVEMARK}{self.INTERNATIONALMARK}{self.CHARACTER}{self.FIGURE}{self.COMPOSITIONCHARACTER}{self.FIGURECOMPOSITON}{self.NUMOFROWS}' \
                   f'&pageNo={str(idx)}{self.APPLICATIONDATE}{self.SERVICEKEY}'
        return self.URL


class PARSE_API():
    def __init__(self, url):
        self.URL = url

    def Parsing(self):
        try:
            response = urllib.request.urlopen(self.URL)
        except urllib.error.URLError as e:
            print(e)
            print('urllib.error.URLError. Plz wait for 1 minutes')
            sleep(10)
            response = urllib.request.urlopen(self.URL)
            pass
        except urllib.error.HTTPError as e:
            print(e)
            print('urllib.error.HTTPError. Plz wait for 1 minutes')
            sleep(10)
            response = urllib.request.urlopen(self.URL)
            pass
        except http.client.HTTPException as e:
            print(e)
            print('http.client.HTTPException. Plz wait for 1 minute')
            sleep(10)
            response = urllib.request.urlopen(self.URL)
            pass
        except requests.exceptions.ConnectionError as e:
            print(e)
            print('requests.exceptions.ConnectionError. Plz wait for 1 minute')
            sleep(10)
            response = urllib.request.urlopen(self.URL)
            pass
        except TimeoutError as e:
            print(e)
            print('TimeoutError. Plz wait for 1 minute')
            sleep(10)
            response = urllib.request.urlopen(self.URL)
            pass
        except urllib3.exceptions.NewConnectionError as e:
            print(e)
            print('urllib3.exceptions.NewConnectionError. Plz wait for 1 minute')
            sleep(10)
            response = urllib.request.urlopen(self.URL)
            pass
        except urllib3.exceptions.MaxRetryError as e:
            print(e)
            print('urllib3.exceptions.MaxRetryError. Plz wait for 1 minute')
            sleep(10)
            response = urllib.request.urlopen(self.URL)
            pass
        print('Converting xml to dictionary')
        responseData = response.read()
        responseData = xmltodict.parse(responseData)
        responseData = json.dumps(responseData)
        responseData = json.loads(responseData)

        return responseData

    def GetPageNum(self):
        responseData = self.Parsing()
        print(responseData)
        count_num = responseData['response']['count']['totalCount']
        if int(count_num) > 500:
            print(f'total number of images:{count_num}')
            page_num = int((int(count_num) / 500) + 2)
            return page_num
        else:
            return 1


class MAKEPATH:
    def __init__(self, img_save_folder):
        self.IMG_SAVE_FOLDER = img_save_folder
        os.makedirs(self.IMG_SAVE_FOLDER, exist_ok=True)

    def MakeImgPath(self, app_num):
        save_path = os.path.join(self.IMG_SAVE_FOLDER, f'{app_num}.jpg')
        return save_path


class DOWNLOAD:
    def __init__(self, database, make_path, biblo_table_name, date_table_name):
        self.DB = database
        self.MAKE_PATH = make_path
        self.BIBLO_TABLE_NAME = biblo_table_name
        self.DATE_TABLE_NAME = date_table_name
        self.BIBLO_LIST = ['applicationNumber']
        self.BIBLIO_DF = pd.DataFrame(columns=self.BIBLO_LIST)

    def bibloDfInit(self):
        self.BIBLIO_DF = pd.DataFrame(columns=self.BIBLO_LIST)

    def DownloadImg(self, img_url, app_num):
        save_path = self.MAKE_PATH.MakeImgPath(app_num)
        if not os.path.exists(save_path):
            try:
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
            except urllib.error.URLError as e:
                print('urllib.error.URLError')
                sleep(10)
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
                    sleep(0.2)
                pass
            except urllib.error.HTTPError as e:
                print('urllib.error.HTTPError')
                sleep(10)
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
                    sleep(0.2)
                pass
            except http.client.HTTPException as e:
                print('http.client.HTTPException')
                sleep(10)
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
                    sleep(0.2)
                pass
            except requests.exceptions.ConnectionError as e:
                print('requests.exceptions.ConnectionError')
                sleep(10)
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
                    sleep(0.2)
                pass
            except TimeoutError as e:
                print('TimeoutError')
                sleep(10)
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
                    sleep(0.2)
                pass
            except urllib3.exceptions.NewConnectionError as e:
                print('urllib3.exceptions.NewConnectionError')
                sleep(10)
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
                    sleep(0.2)
                pass
            except urllib3.exceptions.MaxRetryError as e:
                print('urllib3.exceptions.MaxRetryError')
                sleep(10)
                img = requests.get(img_url).content
                with open(save_path, 'wb') as downloader:
                    downloader.write(img)
                    sleep(0.2)
                pass
            except requests.exceptions.MissingSchema as e:
                print('URL is invaild!')
                pass
            except http.client.IncompleteRead as e:
                print('http.client.IncompleteRead')
                pass
            except urllib3.exceptions.ProtocolError as e:
                print('urllib3.exceptions.ProtocolError')
                pass
            except requests.exceptions.ChunkedEncodingError as e:
                print('requests.exceptions.ChunkedEncodingError')
                pass

    def ifNone(self, data):
        if data == None:
            return ''
        else:
            return str(data)

    def saveBiblioInfoAndImg(self, responseData):
        print('Saving API data')
        biblioinfo = responseData['response']['body']['items']['item']

        for data in tqdm(biblioinfo):
            basket = []
            for biblio_name in self.BIBLO_LIST:
                basket.append(self.ifNone(data[biblio_name]))
            # if data['bigDrawing'] != None:
            #     self.DownloadImg(data['bigDrawing'], str(data['applicationNumber']))
            # else:
            #     if data['drawing'] != None:
            #         self.DownloadImg(data['drawing'], str(data['applicationNumber']))
            #     else:
            #         pass
            self.BIBLIO_DF.loc[len(self.BIBLIO_DF)] = basket
        # self.BIBLIO_DF.to_csv('./test.csv', index=False, encoding='euc-kr')
        print('Update DB table')
        self.DB.appendDataFrameToTable(df=self.BIBLIO_DF, table_name=self.BIBLO_TABLE_NAME)
        self.bibloDfInit()


class EXECUTE():
    def __init__(self, database, download, api_key):
        self.DB = database
        self.DOWNLOAD = download
        self.LAST_YEAR = 0
        self.LAST_MONTH = 0
        self.LAST_PAGE = 0
        self.TOTAL_PAGE = 0
        self.API_KEY = api_key
        self.END_YEAR = 2005

    def getLastYearAndMonth(self):
        sql = f'select * from {self.DOWNLOAD.DATE_TABLE_NAME};'
        result = self.DB.conn.execute(sql)
        row = result.fetchall()
        self.LAST_YEAR = int(row[len(row) - 1][0][0:4])
        self.LAST_MONTH = int(row[len(row) - 1][0][4:6])
        self.LAST_PAGE = row[len(row) - 1][1] + 1
        self.TOTAL_PAGE = row[len(row) - 1][2]
        return self.LAST_YEAR, self.LAST_MONTH, self.LAST_PAGE, self.TOTAL_PAGE

    def downloadImgAndBiblo(self, idx, page_num, start_date, end_date):
        print(f'Connecting {idx}/{page_num - 1}')
        url = URL(start_date, end_date, self.API_KEY).returnURL(idx)
        parsed_data = PARSE_API(url).Parsing()
        current_state = (f'{start_date}~{end_date}', idx, page_num)
        self.DOWNLOAD.saveBiblioInfoAndImg(parsed_data)
        self.DB.appendDataToTable(data=current_state, table_name=self.DOWNLOAD.DATE_TABLE_NAME)
        print(current_state)

    def saveImgAndVienna(self, start_date, end_date):
        url = URL(start_date, end_date, self.API_KEY).returnURL(1)
        page_num = PARSE_API(url).GetPageNum()
        print(f'The number of page: {page_num - 1}')
        if page_num == 1:
            self.downloadImgAndBiblo(1, page_num, start_date, end_date)
        else:
            for idx in range(1, page_num):
                self.downloadImgAndBiblo(idx, page_num, start_date, end_date)

    def saveFromLastMonth(self, last_year, last_month, last_page, total_page):
        print(f'last year:{last_year}, last_month:{last_month}, last_page:{last_page}, total_page:{total_page}')
        start_date_list, end_date_list = DATE(last_year, last_month).returnDateList()
        i = 0
        for start_date, end_date in tqdm(zip(start_date_list, end_date_list)):
            if i == 0:
                for idx in range(last_page, total_page):
                    self.downloadImgAndBiblo(idx, total_page, start_date, end_date)
                i += 1
            else:
                self.saveImgAndVienna(start_date, end_date)

    def saveFromLastYear(self, last_year, last_month):
        print(f'START FROM NEW YEAR! last year:{last_year}, last_month:{last_month}')
        for year in range(last_year, self.END_YEAR, -1):
            start_date_list, end_date_list = DATE(year, last_month).returnDateList()
            for start_date, end_date in tqdm(zip(start_date_list, end_date_list)):
                self.saveImgAndVienna(start_date, end_date)