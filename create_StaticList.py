import zipfile
import csv
import glob
from io import TextIOWrapper
import os.path
import pandas as pd

from utc_to_jst import utc_to_jst

def create_StaticList(AISDATA_FILE_PATH, STATICLIST_FILE_PATH):
    """
    AISデータのメッセージ番号5を読み込み、静的データのStaticListファイルを出力する。
    StaticListファイルを出力後、MMSI番号が重複するデータについて初めの行を採用し、それ以外を削除する。
    重複の削除後、MMSI番号で昇順にソートする。
    AISデータはzipファイルで読み込む。

    Parameters
    ----------
    AISDATA_FILE_PATH : str
        AISデータを格納しているフォルダのパス。
    
    STATICLIST_FILE_PATH : str
        StaticListファイルを出力するフォルダのパス。
    """
    ##### StaticListを作る #####
    path_aisdata_list = glob.glob(AISDATA_FILE_PATH + '/*/*_5.zip') #メッセージ番号1-3のみを抽出

    for path_aisdata in path_aisdata_list:
        with zipfile.ZipFile(path_aisdata) as zip_file:
            for path_csv_file in zip_file.namelist():
                print("Loading " + path_csv_file)
                with zip_file.open(path_csv_file, 'r') as csv_file:
                    reader = csv.reader(TextIOWrapper(csv_file, 'shift_jis'))

                    header = next(reader) #ヘッダーのスキップ

                    for row in reader:
                        mmsi = row[1]
                        date, time = utc_to_jst(row[2], row[3])
                        length = row[22]
                        width = row[23]
                        ship_type = row[24]
                        draught = row[33]

                        os.makedirs(STATICLIST_FILE_PATH + '/' + date, exist_ok=True)
                        
                        with open(STATICLIST_FILE_PATH + '/' + date + '/StaticList_' + date + '.csv', 'a', newline='') as f:
                            writer = csv.writer(f, delimiter=',')
                            writer.writerow([mmsi, length, width, ship_type, draught])

    ##### StaticListの重複を削除し、MMSI番号でソートする #####
    path_StaticList_list = glob.glob(STATICLIST_FILE_PATH + '/*/StaticList_*.csv')

    for path_StaticList in path_StaticList_list:
        df = pd.read_csv(path_StaticList, header=None)
        df = df[~df[0].duplicated()]
        df = df.sort_values([0])
        df.to_csv(path_StaticList, header=False, index=False)
