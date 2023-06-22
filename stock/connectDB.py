import pymysql
from django.db import connection


class ConnectDB():
    # def __init__(self):
    #     import redis
    #     self.pool = redis.ConnectionPool(host='118.31.114.138', port=6379)
    #     self.r = redis.Redis(connection_pool=self.pool)
    #     self.pipe = self.r.pipeline(transaction=True)
    #
    def connectredis(self):
        import redis
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)
        pipe = r.pipeline(transaction=True)

        return (r,pipe)



    def redisClose(self,r,pipe):
        if pipe:
            pipe.close()
        if r:
            r.close()
        print("已关闭redis连接")

    def connectmysql(self):
        #118.31.114.138
        conn = pymysql.connect(host='118.31.114.138', port=3306, user='root', password='yN@5200732', \
                               database='stock', charset="utf8")
        cur=conn.cursor()
        return (conn,cur)


    def closemysql(self,conn,curror):
        if curror:
            curror.close()
        if conn:
            conn.close()
        print("已关闭mysql连接")
        conn=self.connectmysql()

    def hsetredis(self, data: list):
        '''date:"2022-01-02"\n
            data:[{"dm":"000002",
                "date":"2022-01-02"
                "ma5":"45654.22",
                "ma10":"789789.36",
                "ma20":"45646.699"},
                {"dm":"000008",
                date:"2022-01-02"
                "ma5":45654.22,
                "ma10":789789.36,
                "ma20":45646.699},
               ]
        '''
        r, pipe = self.connectredis()
        for i in data:
            dm = i["dm"]
            date = i["date"]
            ma5 = i["ma5"]
            ma10 = i["ma10"]
            ma20 = i["ma20"]
            r.hset(date,dm+'-ma5',ma5)
            r.hset(date,dm+'-ma10',ma10)
            r.hset(date,dm+'-ma20',ma20)
        pipe.execute()
        self.redisClose(r,pipe)
        print("插入成功")

    def hgetredis(self, date: str):
        ''':param:
        dm:"000002"
        :return:data:{"dm":"000002",
            "date":"2022-01-02"
            "ma5":45654.22,
            "ma10":789789.36,
            "ma20":45646.699}
        '''
        r, pipe = self.connectredis()
        stock_redis_info = r.hgetall(date)
        stock_dict={}
        for k in stock_redis_info:
            v = bytes.decode(stock_redis_info[k])
            k=bytes.decode(k)
            stock_dict[k]=v
        #print(stock_dict)
        pipe.execute()
        self.redisClose(r, pipe)
        return stock_dict

    def hdelredis(self, date: str):
        """

        :param date:hash tablename
        :return: none
        """
        r, pipe = self.connectredis()
        hallkeys = r.hkeys(date)
        for key in hallkeys:
            r.hdel(date,bytes.decode(key))
        pipe.execute()
        isdel=self.hgetredis(date)
        if len(isdel)==0:
            print("删除成功")
        else:
            print("删除失败，请查明原因")
        self.redisClose(r, pipe)

    def madata_js(self):
        conn,cur=self.connectmysql()
        cur.execute("call whiletest();")
        conn.commit()
        print("masum计算插入成功")
        self.closemysql(conn,cur)
    def bkrd_js(self):
        conn,cur=self.connectmysql()
        cur.execute("call srd2();")
        conn.commit()
        print("板块热点计算插入成功")
        self.closemysql(conn,cur)





if __name__ == '__main__':
    data=[{"dm": "000002","date": "2022-01-02","ma5":"45654.22","ma10":"789789.36","ma20": "45646.699"},
    {"dm": "000008","date": "2022-01-02","ma5": "45654.22","ma10": "789789.36","ma20": "45646.699"},
    ]
    a = ConnectDB()
    #a.madata_js()

    a.hsetredis(data)
    a.hdelredis("2022-01-02")
    c=a.hgetredis("2022-01-02")
    print(c)

