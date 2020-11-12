# -*- coding:utf-8 -*-

# 若使用pymssql中文会发生乱码，请使用以下代码：
# str.encode('latin1').decode('gbk')
# str表示乱码的中文字符串

# 经测试 pymssql2.1.4+python3.5不会发生以上乱码问题

import pymssql


class Mssql:
    def __init__(self):
        # 数据库连接参数
        self.host = '127.0.0.1'
        self.user = 'sa'
        self.pwd = '123456'
        self.db = 'FaceDB'

    def getConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cursor = self.conn.cursor()
        if not cursor:
            raise (NameError, "连接数据库失败")
        else:
            return cursor

    # 查
    def Query(self, sql):
        cursor = self.getConnect()
        cursor.execute(sql)
        resList = cursor.fetchall()  # 获取查询的所有数据
        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    # 增删改查
    def Excute(self, sql):
        cursor = self.getConnect()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
