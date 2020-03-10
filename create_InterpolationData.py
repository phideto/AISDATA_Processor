import csv
import glob
import os
import pandas as pd


def create_InterpolationData(BASEDATA_FILE_PATH, INTERPOLATIONDATA_FILE_PATH):
    """
    BaseDataファイルを読み込み、1秒おきに線形補間したInterpolationDataファイルを出力する。
    時間を補間したInterpolationファイルを出力後、出力したInterpolationDataファイルを読み込み線形補間する。
    
    Parameters
    ----------
    BASEDATA_FILE_PATH : str
        BaseDataファイルを格納しているフォルダのパス。

    INTERPOLATIONDATA_FILE_PATH : str
        InterpolationDataファイルを出力するフォルダのパス。
    """
    print("Now : create InterpolationData")

    path_BaseData_list = glob.glob(BASEDATA_FILE_PATH + '/*/BaseData_*.csv')

    ##### 時間を補完したデータを作成 #####
    for path_BaseData in path_BaseData_list:
        mmsi = path_BaseData[-13:-4]
        date = path_BaseData[-22:-14]

        with open(path_BaseData, 'r') as basedata:
            reader = csv.reader(basedata)

            os.makedirs(INTERPOLATIONDATA_FILE_PATH + '/' + date, exist_ok=True)

            with open(INTERPOLATIONDATA_FILE_PATH + '/' + date + '/InterpolationData_' + date + '_' + mmsi + '.csv', 'w', newline='') as f:
                writer = csv.writer(f)

                #最初の行の処理
                first_row = next(reader)
                pre_time = int(first_row[2])
                writer.writerow(first_row)

                #2行目以降の処理
                for row in reader:
                    time = int(row[2])

                    while True:
                        if time - pre_time > 1:
                            write_time = pre_time + 1
                            writer.writerow([mmsi, date, write_time, '', '', '', '', ''])
                            pre_time = write_time
                        else:
                            break

                    writer.writerow(row)
                    pre_time = time
                
    print("Done : create InterpolationData")
    ##### 線形補間の処理 #####
    print("Now : interpolate data")
    path_InterpolationData_list = glob.glob(INTERPOLATIONDATA_FILE_PATH + '/*/InterpolationData_*.csv')

    for path_InterpolationData in path_InterpolationData_list:
        df = pd.read_csv(path_InterpolationData, header=None)
        df = df.interpolate()
        df.to_csv(path_InterpolationData, header=False, index=False)
    
    print("Done : interpolate data")
