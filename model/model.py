import sys,os,time,json,pymysql
#数据库配置
host = "localhost"
user = "root"
passwd = ""
database = "mobile"
port = 3306
charset = 'utf8'
prefix = ''#表前缀

#用配置文件指定配置
try:
    from .database import *#当前目录下的database.py
except Exception as e:
    from database import *#当前目录下的database.py
    pass


class Model(object):
    """基于pymysql的MySQL操作类"""
    new = False
    init = False

    def __new__(self,*args,**wkargs):
        if not self.new:
            self.new = super().__new__(self)

        return self.new



    def __init__(self,host=host,user=user,passwd=passwd,database=database,port=port,charset=charset,prefix=prefix):
        """初始化配置"""
        try:
            if self.init:
                return
            self._startTrans = False#事务
            #链接信息
            self.host=host
            self.user=user
            self.passwd=passwd
            self.database=database
            self.port=port
            self.charset=charset
            self.prefix = prefix
            self.connect = pymysql.connect(host=host,user=user,passwd=passwd,db=database,charset=charset,port=port);
            self.cursor = self.connect.cursor()
            self.init = True
        except Exception as e:
            self.error(e)
            exit()


    def error(self,e):
        """错误信息"""
        try:
            print('发生错误的文件：', e.__traceback__.tb_frame.f_globals['__file__']);
            print('错误所在的行号：', e.__traceback__.tb_lineno);
            print('错误信息', e);
        except Exception as e:
            print(e)

    def query(self,sql=''):
        """执行sql"""
        try:
            sql = sql or self.sql
            self.cursor.execute(sql)
            fields_obj = self.cursor.fetchall()
            return fields_obj
        except Exception as e:
            self.error(e)

    def startTrans(self):
        """开启事务"""
        self._startTrans = True

    def commit(self):
        """提交事务"""
        try:
            self.connect.commit()
            self._startTrans = False
        except Exception as e:
            self.error(e)

    def rollback(self):
        """回滚事务"""
        try:
            self.connect.rollback()
            self._startTrans = False
        except Exception as e:
            self.error(e)        

    def execute(self,sql=''):
        """执行sql"""
        try:
            sql = sql or self.sql
            res = self.cursor.execute(sql)
            if res:
                if not self._startTrans:
                    self.connect.commit()
                insertid = self.cursor.lastrowid
                if insertid:
                    return insertid
                    # rollback
                else:
                    return True
            else:
                self.connect.rollback()
                return False
        except Exception as e:
            self.error(e)


    def table(self,tbname):
        """设置表"""
        try:
            #条件
            self._connection = " AND "#连接符号
            self._where = ''#wehre条件
            self._where_ = []#wehre条件
            self._order_ = ''#order条件
            self._group_ = ''#group条件
            self._limit_ = ''#limit条件
            self.sql = ''#sql语句
            self._fetchSQL_ = False
            #表信息
            self._tbname = self.prefix+tbname
            self._fields = [];#字段
            self._comment = [];#注释
            self._index = [];#索引
            #查询表中的字段
            self.sql = "select COLUMN_NAME,column_comment,column_key from INFORMATION_SCHEMA.Columns where table_name='%s' and table_schema='%s'"%(self._tbname,self.database);
            fields_obj = self.query(self.sql)
            for row in fields_obj:
                filed = row[0]#字段
                self._fields.append(filed)
                comment = row[1]#注释
                self._comment.append(comment)
                index = row[2]#索引
                self._index.append(index)

            self._fields_ = '`'+'`,`'.join(self._fields)+'`'#fields方法传入的字段信息初始化

        except Exception as e:
            self.error(e)
        return self;

    def filterField(self,fields):
        """过滤字段"""
        try:
            fields_ = []
            for r in fields.split(','):
                if r in self._fields:
                    fields_.append(r)
        except Exception as e:
            self.error(e)
        return fields_

    def field(self,fileds=''):
        """要查询的字段"""
        try:
            fileds = fileds.strip()
            filedlist = []
            if fileds:
                # fileds = self.filterField(fileds)#过滤非法字段
                fileds = fileds.split(',')
                for filed in fileds:
                    if filed in self._fields_:
                        filedlist.append('`'+filed+'`')
                    else:
                        
                        filedlist.append(filed)
                if fileds:
                    self._fields_ = ','.join(filedlist)
        except Exception as e:
            self.error(e)
        return self

    def connection(self,symbol="ADN"):
        """多个表达式连接符号"""
        try:
            self._connection = ' '+symbol.strip()+' '
        except Exception as e:
            self.error(e)
        return self


    def where(self,*conditions):
        """条件处理"""
        try:
            if not conditions:
                return self
            len_ = len(conditions)
            if len_ == 1:
                where_ = conditions[0]
                if isinstance(where_,str):
                    self._where_.append(where_)
                    # where('id=2')

                elif isinstance(where_,list):
                    if len(where_) < 3:
                        return self
                    #处理val
                    value = where_[2]
                    if isinstance(where_,tuple):
                        value = str(value)
                    else:
                        value = "'"+str(value)+"'"

                    #处理字段
                    filed = where_[0]
                    fileds = []
                    WHERE = []
                    #支持or
                    if '|' in filed:
                        fileds = filed.split('|')
                        connection = " OR "
                    #支持and
                    if '&' in filed:
                        connection = " AND "
                        fileds = filed.split('&')
                    if len(fileds) > 1 and isinstance(fileds,list):
                        for row in fileds:
                            WHERE.append('`'+row+'` '+where_[1]+" "+str(value)+"")
                    else:
                        fileds.append(filed)

                    #过滤非法字段
                    for r in fileds:
                        if r not in self._fields:
                            return self
                    if WHERE:
                        self._where_.append('('+connection.join(WHERE)+')')
                    else:
                        self._where_.append('`'+filed+'` '+where_[1]+" "+value+"")
                    # where(['id','=',2])

                #处理字典传惨
                elif isinstance(conditions[0],dict):
                    wheres = conditions[0]
                    for k,v in wheres.items():
                        self._where_.append('`'+k+'` = '+"'"+str(v)+"'")
    


        except Exception as e:
            self.error(e)
        if self._where_:
            self._where = ' WHERE '+self._connection.join(self._where_)

        return self


    def order(self,orderby):
        """orderby的支持"""
        try:
            orderbylist = orderby.split()
            if orderbylist[0] not in self._fields:
                return self
            self._order_ = " ORDER BY "+orderby.strip()
        except Exception as e:
            self.error(e)
        return self

    def group(self,groupby):
        try:
            groupbylist = groupby.split()
            if groupbylist[0] not in self._fields:
                return self
            self._group_ = " GROUP BY "+groupby.strip()
        except Exception as e:
            self.error(e)
        return self

    def limit(self,limit_):
        try:
            if isinstance(limit_,list):
                self._limit_ = " limit {0},{1}".format(limit_[0],limit_[1])
            else:
                self._limit_ = " limit "+str(limit_)
        except Exception as e:
            self.error(e)
        return self


    def fetchData(self,data):
        try:
            if not data:
                return None
            data = list(data)
            keydata = list(range(len(data)))
            data = dict(zip(keydata,data))
            #获取查询的字段
            fields = self._fields_.split(',')
            fieldslist = []
            for field in fields:
                filed_list = field.split(' as ')
                if len(filed_list) == 2:
                    field = filed_list[1]
                fieldslist.append(field)
            data_ = {}
            for i in data.keys():
                fields_ = fieldslist[i].strip('`')
                data_[fields_] = data[i]

            return data_
        except Exception as e:
            self.error(e)
    def fetchSQL(self,b=False):
        if b:
            self._fetchSQL_ = True
        return self

    def printSQL(self):
        if self._fetchSQL_:
            print(self.sql)

    def select(self):
        """查询全部"""
        try:
            self.sql = "SELECT {0} FROM {1}{2}{3}{4}{5}".format(self._fields_,self._tbname,self._where,self._group_,self._order_,self._limit_)
            self.printSQL()
            datas = []
            data = self.query()
            if data:
                for row in data:
                    datas.append(self.fetchData(row))
        except Exception as e:
            self.error(e)
        return datas

    def find(self):
        """查询单条记录"""
        try:
            self.sql = "SELECT {0} FROM {1}{2}{3}{4} limit 1".format(self._fields_,self._tbname,self._where,self._group_,self._order_)
            self.printSQL() 
            data = self.query()
            if data:
                return self.fetchData(data[0])
            else:
                return None
        except Exception as e:
            self.error(e)

    def value(self,filed):
        try:
            self.sql = "SELECT `{0}` FROM {1}{2}{3}{4} limit 1".format(filed,self._tbname,self._where,self._group_,self._order_)
            self.printSQL() 
            data = self.query()
            if data:
                return data[0][0]
            else:
                return None
        except Exception as e:
            self.error(e)

    def column(self,filed=''):
        try:
            if not filed:
                self._fields_ = self._fields[0]
            else:
                filed = filed.split(',')
                self._fields_ = '`'+'`,`'.join(filed)+'`'
            self.sql = "SELECT {0} FROM {1}{2}{3}{4}{5}".format(self._fields_,self._tbname,self._where,self._group_,self._order_,self._limit_)
            self.printSQL()
            datas = {}
            data = self.query()
            if not data:
                return {}
            if len(filed) > 1:
                for row in data:
                    key = row[0]
                    value = list(row)[1:]
                    if len(value) == 1:
                        value = value[0]
                    datas[key] = value
            else:
                datas = []
                for row in data:
                    datas.append(str(row[0]))
                    
        except Exception as e:
            self.error(e)
        
        return datas



    def count(self):
        try:
            self.sql = "SELECT count(1) FROM {0}{1}{2}{3}{4}".format(self._tbname,self._where,self._group_,self._order_,self._limit_)
            self.printSQL()
            data = self.query()
            if data:
                return data[0][0]
            else:
                return None
        except Exception as e:
            self.error(e)


    def max(self,filed):
        try:
            self.sql = "SELECT max({0}) FROM {1}{2}{3}{4}{5}".format(filed,self._tbname,self._where,self._group_,self._order_,self._limit_)
            self.printSQL()
            data = self.query()
            if data:
                return data[0][0]
            else:
                return None
        except Exception as e:
            self.error(e)

    def min(self,filed):
        try:
            self.sql = "SELECT min({0}) FROM {1}{2}{3}{4}{5}".format(filed,self._tbname,self._where,self._group_,self._order_,self._limit_)
            self.printSQL()
            data = self.query()
            if data:
                return data[0][0]
            else:
                return None
        except Exception as e:
            self.error(e)

    def avg(self,filed):
        try:
            self.sql = "SELECT avg({0}) FROM {1}{2}{3}{4}{5}".format(filed,self._tbname,self._where,self._group_,self._order_,self._limit_)
            self.printSQL()
            data = self.query()
            if data:
                return data[0][0]
            else:
                return None
        except Exception as e:
            self.error(e)

    def sum(self,filed):
        try:
            self.sql = "SELECT sum({0}) FROM {1}{2}{3}{4}{5}".format(filed,self._tbname,self._where,self._group_,self._order_,self._limit_)
            self.printSQL()
            data = self.query()
            if data:
                return data[0][0]
            else:
                return None
        except Exception as e:
            self.error(e)

    def insert(self,datas):
        try:
            datas_ = {}
            if not datas:
                return
            datas_ = []
            #处理key
            if isinstance(datas,dict):
                fileds = ','.join(datas.keys())
                datas_.append(datas)

            elif isinstance(datas,list):
                fileds = ','.join(datas[0].keys())
                datas_ = datas

            else:
                print('数据不合法')
                exit()
            #字段过滤
            fileds_ = self.filterField(fileds)
            fileds = '`'+'`,`'.join(fileds_)+'`'

            import html
            #处理val
            valuelist = []
            for val in datas_:
                values = []
                for filed in fileds_:
                    value_ = str(val.get(filed))
                    values.append('"'+html.escape(value_)+'"')
                valuelist.append('('+','.join(values)+')')
            
            value = ','.join(valuelist)
            self.sql = "INSERT INTO {0}({1}) VALUES{2}".format(self._tbname,fileds,value)
            self.printSQL()
            return self.execute()

        except Exception as e:
            self.error(e)


    def update(self,data):
        try:
            fileds = ','.join(data.keys())
            #字段过滤
            fileds_ = self.filterField(fileds)
            fileds = '`'+'`,`'.join(fileds_)+'`'
            import html
            values = []
            for filed in fileds_:
                values.append('`'+filed+'`='+'"'+html.escape(str(data.get(filed)))+'"')

            value = ','.join(values)
            self.sql = "UPDATE `{0}` SET {1}{2}".format(self._tbname,value,self._where)
            self.printSQL()
            return self.execute()

        except Exception as e:
            self.error(e)

    def delete(self):
        try:
            self.sql = "DELETE FROM {0}{1}".format(self._tbname,self._where)
            self.printSQL()
            return self.execute()

        except Exception as e:
            self.error(e)

    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
        except Exception as e:
            self.error(e)




