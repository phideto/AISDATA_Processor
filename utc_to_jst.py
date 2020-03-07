import datetime

def utc_to_jst(utc_date, utc_time):
    """
    UTCの日付、時刻をJSTの日付、秒で表した時刻に変換する。
    
    Patameters
    ----------
    utc_date : str
        UTCの日付を8桁(年:4桁, 月:2桁, 日:2桁)で表したもの。
    
    utc_time : str
        UTCの時刻を6桁(時:2桁, 分:2桁, 秒2桁)で表したもの。頭の0は省略されている。
    
    Returns
    ----------
    jst_date : str
        JSTの日付を8桁(年:4桁, 月:2桁, 日:2桁)で表したもの。
    
    jst_time_sec : str
        JSTの時刻を秒で表したもの。
    """
    utc_time_6digit = utc_time.zfill(6)
    utc_datetime = datetime.datetime(int(utc_date[0:4]), int(utc_date[4:6]), int(utc_date[6:8]), int(utc_time_6digit[0:2]), int(utc_time_6digit[2:4]), int(utc_time_6digit[4:6]))
    jst_datetime = utc_datetime + datetime.timedelta(hours=9)
    jst_date = str(jst_datetime.year) + str(jst_datetime.month).zfill(2) + str(jst_datetime.day).zfill(2)
    jst_time_sec = str(jst_datetime.hour * 3600 + jst_datetime.minute * 60 + jst_datetime.second)
    return jst_date, jst_time_sec