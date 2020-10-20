from db_attribute import user, password, host, database_name
from img_vienna import *
import pandas as pd
import os

imgPath = 'E:/data/viennacode_total_img_19600101_20191231_unique_preprocessed/imgs'
db = DataBase(user=user, password=password, host=host, database_name=database_name)
df = db.exportData('total_vienna_small_category')
df = df[['applicationNumber', 'viennaCode']]
app_nums = os.listdir(imgPath)
app_nums = [filename.split('.')[0] for filename in app_nums]
new_df = pd.DataFrame({'applicationNumber':app_nums})
new_df = pd.merge(new_df, df, left_on='applicationNumber', right_on='applicationNumber', how='left')
new_df.to_csv('E:/data/viennacode_total_img_19600101_20191231_unique_preprocessed/labels.csv', index=False, encoding='euc-kr')