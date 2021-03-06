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
    print("Now : create BaseData")
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

                        if len(mmsi) != 9:
                            continue

                        if 0.0 > float(sog) or float(sog) > 50.0:
                            continue

                        if 34.685767 > float(lat) or float(lat) > 36.380717:
                            continue

                        if 139.44318 > float(lon) or float(lon) > 140.62573:
                            continue

                        if 0.0 > float(cog) or float(cog) > 360.0:
                            continue

                        if 0 > float(heading) or float(heading) > 360:
                            continue

                        os.makedirs(BASEDATA_FILE_PATH + '/' + date, exist_ok=True)

                        with open(BASEDATA_FILE_PATH + '/' + date + '/BaseData_' + date + '_' + mmsi + '.csv', 'a', newline='') as f:
                            writer = csv.writer(f, delimiter=',')
                            writer.writerow([mmsi, date, time, sog, lat, lon, cog, heading])

    print("Done : create BaseData")
    ##### BaseDataを時間でソートする #####
    print("Now : sort BaseData")
    path_BaseData_list = glob.glob(BASEDATA_FILE_PATH + '/' + date + '/*/BaseData_*.csv')

    for path_BaseData in path_BaseData_list:
        df = pd.read_csv(path_BaseData, header=None)
        df = df.sort_values([2])
        df.to_csv(path_BaseData, header=False, index=False)
    
    print("Done : sort BaseData")