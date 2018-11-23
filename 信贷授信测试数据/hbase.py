import happybase
import re
import requests
import json
import datetime
import logging
import sys
thrift_url = "10.0.4.143"
connection = happybase.Connection(thrift_url, timeout=50)

def get_rowkey_data(table, rowkey,columns=None):
    content = table.row(rowkey,columns=columns,include_timestamp=False)
    return content

def get_rowkey(row_start=None,row_stop=None):
    pool = happybase.ConnectionPool(size=3, host=thrift_url)
    with pool.connection() as connection:
        rts_decision_stevetao = connection.table("rts_decision_stevetao")
        # print(rts_decision_stevetao)
        # for rowKey, data in rts_decision_stevetao.scan(row_start=row_start, row_stop=row_stop,include_timestamp=True, batch_size=200):
        content = get_rowkey_data(rts_decision_stevetao, '000-11-000-0003-loan')
        print ('mobile', content[b'cf1:mobile'].decode('utf-8'))

if __name__ == '__main__':
    get_rowkey()