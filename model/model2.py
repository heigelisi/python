import os
import html
import pymysql

class Error(Exception):
    def __init__(self, e,msg):
        self.e = e
        self.msg = msg
    def __str__(self):
        try:
            print('发生错误的文件：', self.e.__traceback__.tb_frame.f_globals['__file__']);
            print('错误所在的行号：', self.e.__traceback__.tb_lineno);
            print('错误信息', self.e);
        except Exception as e:
            pass
        return self.msg+':'+repr(self.e)

class Model(object):
    config = {
    "host":'localhost',
    "user":'root',
    "passwd":'123456',
    "db":'boke',
    "port":3306,
    "charset":'utf8',
    "prefix" : ''
    }

    def __init__(self,**kwargs):
        """初始化配置"""
        try:
            if kwargs:
                for k,v in kwargs.items():
                    self.config[k] = v

            self.prefix = self.config.get('prefix')
            del self.config['prefix']

            self.connect = pymysql.connect(**self.config);
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
            self.STARTTRANS = False #默认关闭事务

        except Exception as e:
            raise Error(e,'数据库连接失败')

    def query(self,sql=''):
        """执行sql"""
        try:
            sql = sql or self.SQL
            self.cursor.execute(sql)
            fields_obj = self.cursor.fetchall()
            return fields_obj
        except Exception as e:
            raise Error(e,'查询错误sql:'+sql)

    def table(self,tableName):
        try:
            self.WHERELIST = []
            self.WHERE = ''
            self.CONNECTION = "AND" #链接符号
            self.ORDERBY = ''
            self.GROUPBY = ''
            self.LIMIT = ''
            self.SQL = ''
            self.tableName = self.prefix+tableName
            #查询表中的字段
            self.COLUMN_NAME = [] #字段
            self.COLUMN_COMMENT = [] #注释
            self.COLUMN_KEY = [] #索引
            self.SQL = "SELECT COLUMN_NAME,COLUMN_COMMENT,COLUMN_KEY from INFORMATION_SCHEMA.Columns where table_name='%s' and table_schema='%s'"%(self.tableName,self.config['db']);
            fields_obj = self.query(self.SQL)
            if not fields_obj:
                raise Error('Error','表 '+self.tableName+' 不存在')

            for row in fields_obj:
                self.COLUMN_NAME.append(row['COLUMN_NAME'])
                self.COLUMN_COMMENT.append(row['COLUMN_COMMENT'])
                self.COLUMN_KEY.append(row['COLUMN_KEY'])

            #默认查询字段
            self.FIELDS = '`'+'`,`'.join(self.COLUMN_NAME)+'`'

        except Exception as e:
            raise Error(e,'table')
        return self


    def field(self,fields=''):
        """指定查询字段"""
        if fields:
            fields = fields.split(',')
            fields_ = []
            for f in fields:
                if f in self.COLUMN_NAME:
                    fields_.append(f)
            if fields_:
                self.FIELDS = '`'+'`,`'.join(fields_)+'`'
        return self


    def where(self,conditions='',connection="AND"):
        '''
        where("id=3")
        where({"id":2,"title":'test'})
        where(['id',3])
        where(['id|cid',3])
        where(['id&cid',3])
        '''
        if not conditions:
            return self
        connection = " "+connection+" "
        WHERE = []
        if isinstance(conditions,str):#字符串
            self.WHERELIST.append(conditions)
        elif isinstance(conditions,dict):#字典
            for k,v in conditions.items():
                #只支持一层字典
                if not isinstance(v,str) and not isinstance(v,int):
                    continue
                if '|' in k:
                    field = k.split('|')
                    OR = []
                    for fd in field:
                        if fd not in self.COLUMN_NAME:
                            raise Error(fd+' 字段不存在','where')
                        OR.append('`{}` = "{}"'.format(fd,str(v)))
                    WHERE.append('('+' OR '.join(OR)+')')
                elif '&' in k:
                    field = k.split('&')
                    AND = []
                    for fd in field:
                        if fd not in self.COLUMN_NAME:
                            raise Error(fd+' 字段不存在','where')
                        AND.append('`{}` = "{}"'.format(fd,str(v)))
                    WHERE.append('( '+' AND '.join(AND)+' )')
                else:
                    if k not in self.COLUMN_NAME:
                        raise Error(k+' 字段不存在','where')
                    WHERE.append('`{}` = "{}"'.format(k,str(v)))
        elif isinstance(conditions,list):#列表
            lenght = len(conditions)
            if lenght < 2:
                return self
            elif lenght == 2:
                k = conditions[0]
                v = conditions[1]
                if '|' in k:
                    field = k.split('|')
                    OR = []
                    for fd in field:
                        if fd not in self.COLUMN_NAME:
                            raise Error(fd+' 字段不存在','where')
                        OR.append('`{}` = "{}"'.format(fd,str(v)))
                    WHERE.append('('+' OR '.join(OR)+')')
                elif '&' in k:
                    field = k.split('&')
                    AND = []
                    for fd in field:
                        if fd not in self.COLUMN_NAME:
                            raise Error(fd+' 字段不存在','where')
                        AND.append('`{}` = "{}"'.format(fd,str(v)))
                    WHERE.append('( '+' AND '.join(AND)+' )')
                else:
                    if k not in self.COLUMN_NAME:
                        raise Error(k+' 字段不存在','where')
                    WHERE.append('`{}` = "{}"'.format(k,str(v)))
            elif lenght == 3:
                k = conditions[0]
                d = conditions[1]
                v = conditions[2]
                if '|' in k:
                    field = k.split('|')
                    OR = []
                    for fd in field:
                        if fd not in self.COLUMN_NAME:
                            raise Error(fd+' 字段不存在','where')
                        OR.append('`{}` {} "{}"'.format(fd,d,str(v)))
                    WHERE.append('('+' OR '.join(OR)+')')
                elif '&' in k:
                    field = k.split('&')
                    AND = []
                    for fd in field:
                        if fd not in self.COLUMN_NAME:
                            raise Error(fd+' 字段不存在','where')
                        AND.append('`{}` {} "{}"'.format(fd,d,str(v)))
                    WHERE.append('( '+' AND '.join(AND)+' )')
                else:
                    if k not in self.COLUMN_NAME:
                        raise Error(k+' 字段不存在','where')
                    WHERE.append('`{}` {} "{}"'.format(k,d,str(v)))
        if WHERE:
            where_ = connection.join(WHERE)
            if len(WHERE) > 1:
                where_ = "( "+where_+" )"
            self.WHERELIST.append(where_)
        self.CONNECTION = " "+self.CONNECTION.strip()+" "
        self.WHERE = 'WHERE '+self.CONNECTION.join(self.WHERELIST)
        return self

    def order(self,orderby):
        """orderby的支持"""
        orderbylist = orderby.split(',')
        ORDERBY = []
        for o in orderbylist:
            olist = o.split()
            if olist[0] not in self.COLUMN_NAME:
                raise Error(olist[0]+' 字段不存在','order')
            else:
               ORDERBY.append('`{}` {}'.format(olist[0],'' if olist[0] == olist[-1] else olist[-1])) 
        self.ORDERBY = "ORDER BY "+','.join(ORDERBY)
        return self

    def group(self,groupby):
        groupbylist = groupby.split(',')
        GROUPBY = []
        for g in groupbylist:
            glist = g.split()
            if glist[0] not in self.COLUMN_NAME:
                raise Error(glist[0]+' 字段不存在','order')
            else:
               GROUPBY.append('`{}` {}'.format(glist[0],'' if glist[0] == glist[-1] else glist[-1])) 
        self.GROUPBY = "GROUP BY "+','.join(GROUPBY)
        return self

    def limit(self,limit_):
        if isinstance(limit_,list):
            self.LIMIT = "limit {0},{1}".format(limit_[0],limit_[1])
        elif isinstance(limit_,str):
            self.LIMIT = "limit "+limit_
        elif isinstance(limit_,int):
            self.LIMIT = "limit "+str(limit_)
        else:
            raise Error(limit_,'limit 不支持的格式')
        return self

    def select(self):
        """查询数据"""
        self.SQL = "SELECT {FIELDS} FROM `{tableName}` {WHERE} {GROUPBY} {ORDERBY} {LIMIT}".format(
            FIELDS=self.FIELDS,
            tableName=self.tableName,
            WHERE=self.WHERE,
            GROUPBY=self.GROUPBY,
            ORDERBY=self.ORDERBY,
            LIMIT=self.LIMIT
            )
        datas = self.query()
        return datas

    def find(self):
        self.SQL = "SELECT {FIELDS} FROM `{tableName}` {WHERE} {GROUPBY} {ORDERBY} {LIMIT}".format(
            FIELDS=self.FIELDS,
            tableName=self.tableName,
            WHERE=self.WHERE,
            GROUPBY=self.GROUPBY,
            ORDERBY=self.ORDERBY,
            LIMIT=' LIMIT 1'
            )
        data = self.query()
        if not data:
            return {}
        return data[0]

    def value(self,field=""):
        if not field:
            field = self.COLUMN_NAME[0]
        self.SQL = "SELECT {FIELDS} FROM `{tableName}` {WHERE} {GROUPBY} {ORDERBY} {LIMIT}".format(
            FIELDS=field,
            tableName=self.tableName,
            WHERE=self.WHERE,
            GROUPBY=self.GROUPBY,
            ORDERBY=self.ORDERBY,
            LIMIT=' LIMIT 1'
            )
        data = self.query()
        if not data:
            return None
        return data[0][field]

    def column(self,fields=""):
        if not fields:
            fieldsList = self.COLUMN_NAME
        else:
            fieldsList = []
            fields = fields.split(',')
        for f in fields:
            if f not in self.COLUMN_NAME:
                raise Error(f+' 字段不存在','column')
            else:
                fieldsList.append(f)
        fields = '`'+'`,`'.join(fieldsList)+'`'

        self.SQL = "SELECT {FIELDS} FROM `{tableName}` {WHERE} {GROUPBY} {ORDERBY} {LIMIT}".format(
            FIELDS=fields,
            tableName=self.tableName,
            WHERE=self.WHERE,
            GROUPBY=self.GROUPBY,
            ORDERBY=self.ORDERBY,
            LIMIT=self.LIMIT
            )
        data = []
        datas = self.query()
        if not datas:
            return {}
        if len(fieldsList) == 1:
            for v in datas:
                data.append(list(v.values())[0])
            
        elif len(fieldsList) == 2:
            for v in datas:
                data.append({v[fieldsList[0]]:v[fieldsList[1]]})
        else:
            for v in datas:
                data.append({v[fieldsList[0]]:v})
        return data


    def count(self):
        self.SQL = "SELECT count(1) as count FROM `{tableName}` {WHERE}".format(
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['count']

    def max(self,field):
        self.SQL = "SELECT max(`{FIELD}`) as max FROM `{tableName}` {WHERE}".format(
                    FIELD=field,
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['max']

    def min(self,field):
        self.SQL = "SELECT min(`{FIELD}`) as min FROM `{tableName}` {WHERE}".format(
                    FIELD=field,
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['min']

    def avg(self,field):
        self.SQL = "SELECT avg(`{FIELD}`) as avg FROM `{tableName}` {WHERE}".format(
                    FIELD=field,
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['avg']

    def sum(self,field):
        self.SQL = "SELECT sum(`{FIELD}`) as sum FROM `{tableName}` {WHERE}".format(
                    FIELD=field,
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['sum']

    def startTrans(self):
        """开启事务"""
        self.STARTTRANS = True

    def commit(self):
        """提交事务"""
        self.connect.commit()
        self.STARTTRANS = False

    def rollback(self):
        """回滚事务"""
        self.connect.rollback()
        self.STARTTRANS = False

    def execute(self,sql=''):
        """执行sql"""
        try:
            sql = sql or self.SQL
            res = self.cursor.execute(sql)
            if res:
                if not self.STARTTRANS:
                    self.connect.commit()
                insertid = self.cursor.lastrowid
                if insertid:
                    return insertid
                else:
                    return True
            else:
                self.connect.rollback()
                return False
        except Exception as e:
            raise Error(e,'column'+'sql执行错误：'+sql)

    def insert(self,datas=''):
        if not datas:
            raise Error('没有任何数据可以添加','insert')
        valuesList = []
        if isinstance(datas,dict):#添加一条
            field = list(datas.keys())
            valuesList.append(list(datas.values()))
        elif isinstance(datas,list):#添加多条
            if not isinstance(datas[0],dict):
                raise Error('数据不合法','insert') 
            field = list(datas[0].keys())
            for v in datas:
                if not isinstance(v,dict):
                    raise Error('数据不合法','insert') 
                valuesList.append(list(v.values()))
        else:
           raise Error('数据不合法','insert') 
        datas = []
        for values in valuesList:
            d = []
            for value in values:
                d.append(html.escape(str(value)))
            datas.append('("'+'","'.join(d)+'")')
        fields = '`'+'`,`'.join(field)+'`'
        self.SQL = "INSERT INTO `{tableName}`({fields}) values{values}".format(tableName=self.tableName,fields=fields,values=','.join(datas))
        return self.execute()    

    def update(self,datas):
        filed_value = []
        for k,v in datas.items():
            filed_value.append('`{k}`="{v}"'.format(k=k,v=html.escape(str(v))))
        filed_value = ','.join(filed_value)
        self.SQL = "UPDATE `{tableName}` SET {filed_value} {WHERE}".format(tableName=self.tableName,filed_value=filed_value,WHERE=self.WHERE)   
        return self.execute()

    def delete(self):
        self.SQL = "DELETE FROM {tableName}{WHERE}".format(tableName=self.tableName,WHERE=self.WHERE)
        return self.execute()


try:
    mode = Model(host="127.0.0.1").table('article')
    mode.startTrans()
    data = mode.where(['aid','=',26]).update({"title":"updatef","tag":'fff'})
    print(data)
    print(mode.SQL)
    # where('id=1')
    # where(['id','1'])
    # where(['id','=',1])
    # where({"id":1})

    pass
except Exception as e:
    print(e)








