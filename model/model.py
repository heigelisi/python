import os
import html
import pymysql

class Error(Exception):
    def __init__(self, e,msg):
        self.e = e
        self.msg = msg
    def __str__(self):
        return self.msg+':'+repr(self.e)

class Model(object):
    """
    python3 pymysql 操作MySQL数据库
    """
    config = {
    "host":'localhost',
    "user":'root',
    "passwd":'123456',
    "db":'boke',
    "port":3306,
    "charset":'utf8',
    "prefix" : '',
    "printSql":False
    }
    new = False
    init = False
    def __new__(cls,*args,**wkargs):
        if not cls.new:
            cls.new = super().__new__(cls)
        return cls.new

    def __init__(self,**kwargs):
        """初始化配置"""
        if self.init:
            return
        try:
            if kwargs:
                for k,v in kwargs.items():
                    self.config[k] = v

            self.config2 = self.config.copy()
            del self.config2['prefix']
            del self.config2['printSql']

            self.connect = pymysql.connect(**self.config2);
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
            self.STARTTRANS = False #默认关闭事务
            self.init = True

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

    def __table_as(self,tableName):
        """分离表面和别名"""
        tableName = tableName
        AS = tableName
        if ' as ' in tableName:
            table_as = tableName.split(' as ')
            tableName = table_as[0].strip()
            AS = table_as[1].strip()
        elif ' AS ' in tableName:
            table_as = tableName.split(' AS ')
            tableName = table_as[0].strip()
            AS = table_as[1].strip()
        return [tableName,AS]
        

    def table(self,tableName):
        """初始化表信息及查询条件"""
        try:
            self.WHERELIST = [] #存储多次wehre条件语句
            self.WHERE = '' #存储完整的where条件语句
            self.CONNECTION = "AND" #多条where条件连接符号(AND,OR)
            self.ORDERBY = '' #存储order by 语句
            self.GROUPBY = '' #存储goup by 语句
            self.LIMIT = '' #存储limit 语句
            self.SQL = '' #完整SQL语句
            tableName_as = self.__table_as(tableName)
            self.AS = self.config['prefix']+tableName_as[1] #表别名
            self.tableName = self.config['prefix']+tableName_as[0] #表明
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
            self.FIELDS = '`'+'`,`'.join(self.COLUMN_NAME)+'`' #默认查询字段(所有字段)

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

    def connection(self,CONNECTION="AND"):
        """修改连接符号"""
        if CONNECTION.upper() == 'OR':
            self.CONNECTION == "OR"

    def where(self,conditions='',connection="AND"):
        '''
        where条件
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
        self.WHERE = ' WHERE '+self.CONNECTION.join(self.WHERELIST)
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
        self.ORDERBY = " ORDER BY "+','.join(ORDERBY)
        return self

    def group(self,groupby):
        """groupby的支持"""
        groupbylist = groupby.split(',')
        GROUPBY = []
        for g in groupbylist:
            glist = g.split()
            if glist[0] not in self.COLUMN_NAME:
                raise Error(glist[0]+' 字段不存在','order')
            else:
               GROUPBY.append('`{}` {}'.format(glist[0],'' if glist[0] == glist[-1] else glist[-1])) 
        self.GROUPBY = " GROUP BY "+','.join(GROUPBY)
        return self

    def limit(self,limit_):
        if isinstance(limit_,list):
            self.LIMIT = " limit {0},{1}".format(limit_[0],limit_[1])
        elif isinstance(limit_,str):
            self.LIMIT = " limit "+limit_
        elif isinstance(limit_,int):
            self.LIMIT = " limit "+str(limit_)
        else:
            raise Error(limit_,'limit 不支持的格式')
        return self

    def select(self):
        """查询数据"""
        self.SQL = "SELECT {FIELDS} FROM `{tableName}`{WHERE}{GROUPBY}{ORDERBY}{LIMIT}".format(
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
        """查询单条数据"""
        self.SQL = "SELECT {FIELDS} FROM `{tableName}`{WHERE}{GROUPBY}{ORDERBY}{LIMIT}".format(
            FIELDS=self.FIELDS,
            tableName=self.tableName,
            WHERE=self.WHERE,
            GROUPBY=self.GROUPBY,
            ORDERBY=self.ORDERBY,
            LIMIT='LIMIT 1'
            )
        data = self.query()
        if not data:
            return {}
        return data[0]

    def value(self,field=""):
        """获取指定字段的值"""
        if not field:
            field = self.COLUMN_NAME[0]
        self.SQL = "SELECT {FIELDS} FROM `{tableName}`{WHERE}{GROUPBY}{ORDERBY}{LIMIT}".format(
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
        """返回数据中的指定列"""
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

        self.SQL = "SELECT {FIELDS} FROM `{tableName}`{WHERE}{GROUPBY}{ORDERBY}{LIMIT}".format(
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
        self.SQL = "SELECT count(1) as count FROM `{tableName}`{WHERE}".format(
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['count']

    def max(self,field):
        self.SQL = "SELECT max(`{FIELD}`) as max FROM `{tableName}`{WHERE}".format(
                    FIELD=field,
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['max']

    def min(self,field):
        self.SQL = "SELECT min(`{FIELD}`) as min FROM `{tableName}`{WHERE}".format(
                    FIELD=field,
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['min']

    def avg(self,field):
        self.SQL = "SELECT avg(`{FIELD}`) as avg FROM `{tableName}`{WHERE}".format(
                    FIELD=field,
                    tableName=self.tableName,
                    WHERE=self.WHERE,
                    )      
        data = self.query()
        return data[0]['avg']

    def sum(self,field):
        self.SQL = "SELECT sum(`{FIELD}`) as sum FROM `{tableName}`{WHERE}".format(
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

    def getAutoID(self):
        """获取自增ID"""
        self.SQL = "SELECT auto_increment FROM INFORMATION_SCHEMA.tables where table_name = '{tableName}' and table_schema = '{db}'".format(tableName=self.tableName,db=self.config['db'])
        return self.query()[0]['auto_increment']

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
        """添加数据"""
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
        """修改数据"""
        filed_value = []
        for k,v in datas.items():
            filed_value.append('`{k}`="{v}"'.format(k=k,v=html.escape(str(v))))
        filed_value = ','.join(filed_value)
        self.SQL = "UPDATE `{tableName}` SET {filed_value}{WHERE}".format(tableName=self.tableName,filed_value=filed_value,WHERE=self.WHERE)   
        return self.execute()

    def delete(self,primarykey=""):
        """删除数据"""
        if primarykey:
            index = self.COLUMN_KEY.index('PRI')
            if isinstance(primarykey,list):
                values = ','.join([str(i) for i in primarykey])
            elif isinstance(primarykey,str):
                values = primarykey
            self.WHERE = "WHERE {PRI} in({values})".format(PRI=self.COLUMN_NAME[index],values=values)
        self.SQL = "DELETE FROM `{tableName}`{WHERE}".format(tableName=self.tableName,WHERE=self.WHERE)
        return self.execute()

    def on(self,where):
        """on条件"""
        self.ON = where

    def ljoin(self):
        """left join"""

    def rjoin(self):
        """right join"""

    def join(self,tableName):
        """inner join"""
        tableName_as = self.__table_as(tableName)
        tableName = tableName_as[0]
        AS = tableName_as[1]
        self.SQL = "SELECT {FIELDS} FROM `{tableName}` AS {AS} INNER JOIN `{tableName2}` AS {AS2} ON {ON}{WHERE}{GROUPBY}{ORDERBY}{LIMIT}".format(
            FIELDS=self.FIELDS,
            tableName=self.tableName,
            tableName2=tableName,
            AS=self.AS,
            AS2=AS,
            ON=self.ON,
            WHERE=self.WHERE,
            GROUPBY=self.GROUPBY,
            ORDERBY=self.ORDERBY,
            LIMIT=self.LIMIT
            )
        # datas = self.query()
        # return datas
        print(self.SQL)

    def __del__(self):
        try:
            if self.config['printSql']:
                print(self.SQL)
            self.cursor.colse()
            self.connect.colse()
        except Exception as e:
            pass


model = Model().table('column as c').join('article as a').on('a.cid = c.cid')
print(model)

