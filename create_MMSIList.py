import glob
import csv
import os

def create_MMSIList(BASEDATA_FILE_PATH, MMSILIST_FILE_PATH):
    """
    BaseDataファイルのファイル名を読み込み、日付とMMSI番号を取得しMMSIListファイルを出力する。
    
    Parameters
    ----------
    BASEDATA_FILE_PATH : str
        BaseDataファイルを格納しているフォルダのパス。

    MMSILIST_FILE_PATH : str
        MMSIListファイルを出力するフォルダのパス。
    """
    print("Now : create MMSIList")

    path_BaseData_list = glob.glob(BASEDATA_FILE_PATH + '/*/BaseData_*.csv')

    for path_BaseData in path_BaseData_list:
        date = path_BaseData[-22:-14]
        mmsi = path_BaseData[-13:-4]

        os.makedirs(MMSILIST_FILE_PATH + '/' + date , exist_ok=True)

        with open(MMSILIST_FILE_PATH + '/' + date + '/MMSIList_' + date + '.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([mmsi])
    
    print("Done : create MMSIList")