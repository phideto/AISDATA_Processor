import zipfile
import csv
import glob
from io import TextIOWrapper
import os
import pandas as pd

from utc_to_jst import utc_to_jst

def create_BaseData(AISDATA_FILE_PATH, BASEDATA_FILE_PATH):
    """
    AISデータのメッセージ番号1-3を読み込み、動的データのBaseDataファイルを出力する。
    BaseDataファイルを出力後、各BaseDataを時間で昇順にソートする。
    AISデータはzipファイルで読み込む。

    Parameters
    ----------
    AISDATA_FILE_PATH : str
        AISデータを格納しているフォルダのパス。
    
    BASEDATA_FILE_PATH : str
        BaseDataファイルを出力するフォルダのパス。
    """
    ##### BaseDataを作る #####
    path_aisdata_list = glob.glob(AISDATA_FILE_PATH + '/*/*_[1-3].zip') #メッセージ番号1-3のみを抽出

    for path_aisdata in path_aisdata_list:
        with zipfile.ZipFile(path_aisdata) as zip_file:
            for path_csv_file in zip_file.namelist():
                with zip_file.open(path_csv_file, 'r') as csv_file:
                    reader = csv.reader(TextIOWrapper(csv_file, 'shift_jis'))

                    header = next(reader) #ヘッダーのスキップ

                    for row in reader:
                        mmsi = row[1]
                        date, time = utc_to_jst(row[2], row[3])
                        sog = row[9]
                        lat = row[11]
                        lon = row[12]
                        cog = row[13]
                        heading = row[14]

                        os.makedirs(BASEDATA_FILE_PATH + '/' + date, exist_ok=True)

                        with open(BASEDATA_FILE_PATH + '/' + date + '/BaseData_' + date + '_' + mmsi + '.csv', 'a', newline='') as f:
                            writer = csv.writer(f, delimiter=',')
                            writer.writerow([mmsi, date, time, sog, lat, lon, cog, heading])

    ##### BaseDataを時間でソートする #####
    path_BaseData_list = glob.glob(BASEDATA_FILE_PATH + '/' + date + '/*/BaseData_*.csv')

    for path_BaseData in path_BaseData_list:
        df = pd.read_csv(path_BaseData, header=None)
        df = df.sort_values([2])
        df.to_csv(path_BaseData, header=False, index=False)