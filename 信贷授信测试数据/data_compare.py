# coding:utf-8
from time import sleep
import happybase
import requests
import  pymysql


# def data_Compare():
#     with open('nameList.txt','r') as f:
#         for i in f.readlines():
#             # print(i.split(',')[0],i.split(',')[1])
#             query_mysql(i.split(',')[1].strip())
#             prod_data = queryTable("rt_loan_record1",i.split(',')[0],i.split(',')[1].strip())
#             test_data = queryTable("rt_loan_record",i.split(',')[0],i.split(',')[1].strip())
#             if test_data[10] == prod_data[10]:
#                 if test_data[15] == prod_data[15]:
#                     for j in list(test_data[22]):
#                         if j in list(prod_data[21]):
#                             print(j)
#                         else:
#                             print("{}用户在生产环境和测试环境的命中规则结果不一致，生产环境的结果为{}，测试环境的结果为{}".format(i.split(',')[1].strip(),prod_data[22], test_data[22]))
#                 else:
#                     print("{}用户在生产环境和测试环境授信额度结果不一致，生产环境的结果为{}，测试环境的结果为{}\n\n".format(i.split(',')[1].strip().strip(),prod_data[15], test_data[15]))
#             else:
#                 print("{}用户在生产环境和测试环境授信通过结果不一致，生产环境的结果为{}，测试环境的结果为{}\n\n".format(i.split(',')[1].strip().strip(),prod_data[10], test_data[10]))

thrift_url = "10.0.4.143"
connection = happybase.Connection(thrift_url, timeout=50)

def get_rowkey_data(table, rowkey,columns=None):
    content = table.row(rowkey,columns=columns,include_timestamp=False)
    return content

def get_rowkey(hbase_table,rowkey,row_start=None,row_stop=None):
    pool = happybase.ConnectionPool(size=3, host=thrift_url)
    with pool.connection() as connection:
        rts_decision_stevetao = connection.table(hbase_table)
        content = get_rowkey_data(rts_decision_stevetao, rowkey)
        # print ({'mobile':content[b'cf1:mobile'].decode('utf-8'),'responseMsg':content[b'cf1:responseMsg'].decode('utf-8')})
        return {'mobile':content[b'cf1:mobile'].decode('utf-8'),'responseMsg':content[b'cf1:responseMsg'].decode('utf-8')}


def data_Compare(filename='nameList.txt'):
    with open(filename,'r') as f:
        for i in f.readlines():
            print("\033[1;35;40m------------------开始校验{}用户比对结果----------------------\033[0m".format(i.split(',')[1].strip()))
            #发送决策引擎结果并获取rowkeyid
            rowkey = query_mysql(i.split(',')[1].strip())
            #比较生产环境的rt_loan_record表和测试环境的rt_loan_record表
            prod_data = queryTable("rt_loan_record1",i.split(',')[0],i.split(',')[1].strip())
            test_data = queryTable("rt_loan_record",i.split(',')[0],i.split(',')[1].strip())
            print("\033[1;31;46m------------------开始校验{}用户的rt_loan_record表------------\033[0m".format(i.split(',')[1].strip()))
            if prod_data == test_data:
                print("{}用户在生产环境和测试环境rt_loan_record表的命中规则结果一致".format(i.split(',')[1].strip()))
            else:
                print("{}用户在生产环境和测试环境rt_loan_record表的授信通过结果不一致，生产环境的结果为{}，测试环境的结果为{}".format(i.split(',')[1].strip().strip(),prod_data, test_data))

            #比较生产环境的rts_decision表和测试环境的rts_decision表
            print("\033[1;31;46m------------------开始校验{}用户的rts_decision表--------------\033[0m".format(i.split(',')[1].strip()))
            prod_hive = get_rowkey('rts_decision_stevetao',rowkey)
            test_hive = get_rowkey('rts_decision',rowkey)
            if prod_hive == test_hive:
                print("{}用户在生产环境和测试环境rts_decision表的结果一致".format(i.split(',')[1].strip()))
            else:
                print("{}用户在生产环境和测试环境rts_decision表的结果不一致，生产环境的结果为{}，测试环境的结果为{}\n\n".format(prod_hive,test_hive))



#发起请求
def post_requests(mobile,params):
    print("\033[1;31;46m------------------{}用户开始发起信贷授信请求------------------\033[0m".format(mobile))
    url = "http://10.0.4.149:8893/rts/invoke"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    param = {'clazz':'com.touna.rts.modules.controller.test.TestController',
             'method':'授信支用环节',
             'params':params,
             'types':'java.lang.String'
             }
    req = requests.post(url,data=param,headers=headers)
    print("{}用户的信贷授信请求结果为：{}".format(mobile,req.text))
    sleep(1)

def query_mysql(mobile):
    #连接数据库
    db = pymysql.connect('10.0.4.141','rts','m9ubQXsJ9D0p','rts',charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()
    #表名变量不能直接execute传入
    sql = "SELECT * FROM `rt_apply_ext` WHERE mobile ='{}' ORDER BY date_created DESC".format(mobile)
    cur.execute(sql)
    #发起决策引擎dubbo接口请求
    post_requests(mobile,cur.fetchone()[5])
    #获取rowkey
    return (cur.fetchone()[1]+"-"+cur.fetchone()[2])

def queryTable(table,id_no,mobile):
    #连接数据库
    db = pymysql.connect('10.0.4.141','rts','m9ubQXsJ9D0p','rts',charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()
    #表名变量不能直接execute传入
    sql = "SELECT * FROM {} WHERE id_no ='{}' AND mobile='{}' ORDER BY end_time DESC".format(table,id_no,mobile)
    cur.execute(sql)
    # print(cur.fetchall())
    arr = cur.fetchone()
    cur.scroll(0, 'absolute')
    return (arr[10],arr[15],arr[22])
    # return (cur.fetchone()[0],cur.fetchone()[10],cur.fetchone()[15],cur.fetchone()[22])


if __name__=="__main__":
    # queryTable("rt_loan_record1","4417811987050511383","18202061117")
    data_Compare()
    # get_rowkey('rts_decision_stevetao','000-11-000-0003-loan')

