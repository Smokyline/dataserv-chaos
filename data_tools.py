import pymysql
import datetime
import numpy as np


def get_data_from_sqldb(swarm_type, from_date, to_date,):
    conn = pymysql.connect(host='imagdb.gcras.ru', port=3306,
                           user='data_reader',
                           passwd='V9e2OeroufrluwluN2u88leP9lAPhluzL7dlU67oAb5afROub9iUv7unLEhiEs9o',
                           db='intermagnet',
                           charset='utf8mb4',
                           )

    request = "SELECT date, latitude, longitude, radius, n, e, c, f FROM sat_sec_plain WHERE code='%s' " \
        "AND date BETWEEN %s AND %s" % (
            swarm_type, from_date, to_date)
    cur = conn.cursor()
    cur.execute(request)
    result = cur.fetchall()
    conn.close()
    return result


def ut_dt_to_unix(dt, out_type='str'):
    """Конвертирование UT datetime в unix time"""

    if out_type == 'str':
        unix_time = dt.strftime('%s')
    elif out_type == 'float':
        unix_time = dt.timestamp()
    else:
        print('Error input unix type')
        unix_time = None
    return unix_time  # int ot float


def unix_to_ut_dt(unix_time):
    """Конвертирование unix int time в UT datetime"""

    if not isinstance(unix_time, int):
        print('Error input unix type')
        ut_time_dt = None
    else:
        ut_time_dt = datetime.datetime.fromtimestamp(unix_time)
    return ut_time_dt  # dt


def data_reduction(respond, delta):
    N, M = respond.shape
    redu_resp = np.empty((0, M))
    st_idx = 0
    while st_idx < N:
        delta_resp = respond[st_idx:st_idx + delta]
        dt, y, x, r = delta_resp[-1, (0, 1, 2, 3)]
        n = np.mean(delta_resp[:, 4])
        e = np.mean(delta_resp[:, 5])
        c = np.mean(delta_resp[:, 6])
        f = np.mean(delta_resp[:, 7])
        redu_resp = np.append(redu_resp, [[dt, y, x, r, n, e, c, f]], axis=0)
        st_idx += delta
    return redu_resp
