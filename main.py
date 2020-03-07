import os

from create_BaseData import create_BaseData
from create_MMSIList import create_MMSIList
from create_InterpolationData import create_InterpolationData
from create_StaticList import create_StaticList

#各ファイル名の指定
AISDATA_FILE_PATH = 'AISDATA'
BASEDATA_FILE_PATH = 'BaseData'
MMSILIST_FILE_PATH = 'MMSIList'
INTERPOLATIONDATA_FILE_PATH = 'InterpolationData'
STATICLIST_FILE_PATH = 'StaticList'

#出力するファイルの作成
os.makedirs(BASEDATA_FILE_PATH, exist_ok=True)
os.makedirs(MMSILIST_FILE_PATH, exist_ok=True)
os.makedirs(INTERPOLATIONDATA_FILE_PATH, exist_ok=True)
os.makedirs(STATICLIST_FILE_PATH, exist_ok=True)

#データ処理の実行
create_BaseData(AISDATA_FILE_PATH, BASEDATA_FILE_PATH)
create_MMSIList(BASEDATA_FILE_PATH, MMSILIST_FILE_PATH)
create_InterpolationData(BASEDATA_FILE_PATH, INTERPOLATIONDATA_FILE_PATH)
create_StaticList(AISDATA_FILE_PATH, STATICLIST_FILE_PATH)
 