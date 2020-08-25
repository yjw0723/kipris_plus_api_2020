from img_vienna import DataBase, MAKEDATE
import os, requests
import urllib3
import xml.etree.ElementTree as ET
import urllib.request
from time import sleep
import http

class downloadBibilInfo:
    def __init__(self, api_key, start_date, end_date):
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
        self.CHARACTER = '&character=FALSE'
        self.FIGURE = '&figure=TRUE&figureComposition=TRUE'
        self.COMPOSITIONCHARACTER = '&compositionCharacter=FALSE'
        self.NUMOFROWS = '&numOfRows=500'
        self.PAGENUM = '&pageNo=1'
        self.APPLICATIONDATE = f'&applicationDate={self.START_DATE}~{self.END_DATE}'
        self.SERVICEKEY = api_key
        self.URL = f'{self.BASIC_URL}{self.APPLICATION}{self.REGISTRATION}{self.REFUSED}{self.EXPRIATION}{self.WITHDRAWAL}{self.PUBLICATION}{self.CANCEL}{self.ABANDONMENT}{self.TRADEMARK}{self.SERVICEMARK}' \
                   f'{self.TRADEMARKSERVICEMARK}{self.BUSINESSEMBLEM}{self.COLLECTIVEMARK}{self.INTERNATIONALMARK}{self.CHARACTER}{self.FIGURE}{self.COMPOSITIONCHARACTER}{self.NUMOFROWS}' \
                   f'{self.PAGENUM}{self.APPLICATIONDATE}{self.SERVICEKEY}'

    def updateURL(self, idx):
        self.URL = f'{self.BASIC_URL}{self.APPLICATION}{self.REGISTRATION}{self.REFUSED}{self.EXPRIATION}{self.WITHDRAWAL}{self.PUBLICATION}{self.CANCEL}{self.ABANDONMENT}{self.TRADEMARK}{self.SERVICEMARK}' \
                   f'{self.TRADEMARKSERVICEMARK}{self.BUSINESSEMBLEM}{self.COLLECTIVEMARK}{self.INTERNATIONALMARK}{self.CHARACTER}{self.FIGURE}{self.COMPOSITIONCHARACTER}{self.NUMOFROWS}' \
                   f'&pageNo={str(idx)}{self.APPLICATIONDATE}{self.SERVICEKEY}'
        return self.URL

class PARSE_API():
    def __init__(self, url, database, table_name):
        self.URL = url
        self.APP_NUM_LIST = []
        self.VIENNA_CODE_LIST = []
        self.SAVE_FOLDER = 'E:/data/viennacode/'
        self.IMG_SAVE_FOLDER = 'E:/data/viennacode_total_img_19600101_20191231/'
        os.makedirs(self.SAVE_FOLDER, exist_ok=True)
        os.makedirs(self.IMG_SAVE_FOLDER, exist_ok=True)
        self.DB = database
        self.TABLE_NAME = table_name

    def Parsing(self):
        try:
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
        except urllib.error.URLError as e:
            print(e)
            print('urllib.error.URLError. Plz wait for 1 minutes')
            sleep(10)
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
            pass
        except urllib.error.HTTPError as e:
            print(e)
            print('urllib.error.HTTPError. Plz wait for 1 minutes')
            sleep(10)
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
            pass
        except http.client.HTTPException as e:
            print(e)
            print('http.client.HTTPException. Plz wait for 1 minute')
            sleep(10)
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
            pass
        except requests.exceptions.ConnectionError as e:
            print(e)
            print('requests.exceptions.ConnectionError. Plz wait for 1 minute')
            sleep(10)
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
            pass
        except TimeoutError as e:
            print(e)
            print('TimeoutError. Plz wait for 1 minute')
            sleep(10)
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
            pass
        except urllib3.exceptions.NewConnectionError as e:
            print(e)
            print('urllib3.exceptions.NewConnectionError. Plz wait for 1 minute')
            sleep(10)
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
            pass
        except urllib3.exceptions.MaxRetryError as e:
            print(e)
            print('urllib3.exceptions.MaxRetryError. Plz wait for 1 minute')
            sleep(10)
            k_tree = ET.parse(urllib.request.urlopen(self.URL))
            pass
        k_root = k_tree.getroot()

        return k_root