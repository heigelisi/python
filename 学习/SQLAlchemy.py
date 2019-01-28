MySQL-Python
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
  
pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
  
MySQL-Connector
    pip install mysql-connector-python
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
  
cx_Oracle
    oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]
  
更多详见：http://docs.sqlalchemy.org/en/latest/dialects/index.html







常见的SQLALCHEMY列类型.配置选项和关系选项
# D:\python3\Lib\site-packages\sqlalchemy\__init__.py 字段详情
# D:\python3\Lib\site-packages\sqlalchemy\dialects\mysql\types.py mysql字段类型 导入方式： from sqlalchemy.dialects.mysql.types import TINYINT
类型名称    python类型    描述
Integer int 常规整形，通常为32位
SmallInteger    int 短整形，通常为16位
BigInteger  int或long    精度不受限整形
Float   float   浮点数
Numeric decimal.Decimal 定点数
String  str 可变长度字符串
Text    str 可变长度字符串，适合大量文本
Unicode unicode 可变长度Unicode字符串
Boolean bool    布尔型
Date    datetime.date   日期类型
Time    datetime.time   时间类型
Interval    datetime.timedelta  时间间隔
Enum    str 字符列表
PickleType  任意Python对象  自动Pickle序列化
LargeBinary str 二进制
常见的SQLALCHEMY列选项
可选参数    描述
primary_key 如果设置为True，则为该列表的主键
unique  如果设置为True，该列不允许相同值
index   如果设置为True，为该列创建索引，查询效率会更高
nullable    如果设置为True，该列允许为空。如果设置为False，该列不允许空值
default 定义该列的默认值,不在数据库中体行
server_default 定义该列的默认值,会在数据库中体行
comment 注释



from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index,CHAR,ColumnDefault,Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql.types import TINYINT
Base = declarative_base()
engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1:3306/test?charset=utf8", max_overflow=5,echo=True)#echo=True输出sql
class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(CHAR(32),server_default='f',nullable=False,index=True,comment='姓名')
	extra = Column(String(16))
	a = Column(TINYINT(1),server_default='0',nullable=False,comment='注释')
	# b = Column(String)
	__table_args__ = {
        'mysql_charset':'utf8',
        'mysql_engine':'innodb',
        "comment":'注释'
    }


# Base.metadata.create_all(engine)

Session = sessionmaker(twophase=True)
Session.configure(bind=engine)
session = Session()
User = Users(name='周飞',sex=1,age=18)
session.add(User)
session.commit()


# https://www.cnblogs.com/pycode/p/mysql-orm.html




几种常见sqlalchemy查询：
#简单查询    
print(session.query(User).all())
print(session.query(User.name, User.fullname).all())    
print(session.query(User, User.name).all())   




#带条件查询    
print(session.query(User).filter_by(name='user1').all())    
print(session.query(User).filter(User.name == "user").all())    
print(session.query(User).filter(User.name.like("user%")).all())
print(session.query(User).filter(User.name == "user")) #返回sql语句   

  
#多条件查询    
print(session.query(User).filter(and_(User.name.like("user%"), User.fullname.like("first%"))).all())    
print(session.query(User).filter(or_(User.name.like("user%"), User.password != None)).all())        


#sql过滤    
print(session.query(User).filter("id>:id").params(id=1).all())        


#关联查询     
print(session.query(User, Address).filter(User.id == Address.user_id).all())    
print(session.query(User).join(User.addresses).all())    
print(session.query(User).outerjoin(User.addresses).all())        


#聚合查询    
print(session.query(User.name, func.count('*').label("user_count")).group_by(User.name).all())    
print(session.query(User.name, func.sum(User.id).label("user_id_sum")).group_by(User.name).all())        


#子查询    
stmt = session.query(Address.user_id, func.count('*').label("address_count")).group_by(Address.user_id).subquery()    
print(session.query(User, stmt.c.address_count).outerjoin((stmt, User.id == stmt.c.user_id)).order_by(User.id).all())     

   
#exists    
print(session.query(User).filter(exists().where(Address.user_id == User.id)))    
print(session.query(User).filter(User.addresses.any()))


限制返回字段查询
person = session.query(Person.name, Person.created_at,Person.updated_at).filter_by(name="zhongwei").order_by(Person.created_at).first()


记录总数查询：
from sqlalchemy import func


# count User records, without
# using a subquery.
session.query(func.count(User.id))


# return count of user "id" grouped
# by "name"
session.query(func.count(User.id)).\
        group_by(User.name)


from sqlalchemy import distinct
# count distinct "name" values
session.query(func.count(distinct(User.name)))


#获取表结构
from sqlalchemy.engine import reflection
insp = reflection.Inspector.from_engine(engine)
colums=insp.get_columns('user_groups')#这里是写的表名
for i in colums:
        print(i)



#查询单条
session.query(User).filter(User.name=="test").first()
session.query(User).filter(User.name=="test").one()#有多条结果是会报错

#limit 
print( session.query(User).filter(User.username!='jingqi').limit(2).all())
print( session.query(User).filter(User.username!='jingqi').offset(2).all())
print( session.query(User).filter(User.username!='jingqi').slice(2,3).all())


#orderby
session.query(Users).filter(Users.userName=='test').order_by(Users.uid).order_by(Users.userName).slice(2,5).all()
from sqlalchemy import desc
session.query(Users).filter(Users.userName=='test').order_by(desc(Users.uid)).all()

#不等于
print( session.query(User).filter(User.username!='jingqi').all() )
#模糊匹配 like
print( session.query(User).filter(User.username.like('jingqi')).all() )
print( session.query(User).filter(User.username.notlike('jingqi')).all() )

#成员属于  in_
print( session.query(User).filter(User.username.in_(['jingqi','jingqi1'])).all() )

#成员不属于  notin_
print( session.query(User).filter(User.username.notin_(['jingqi','jingqi2'])).all() )

#空判断
print( session.query(User).filter(User.username==None).all() )
print( session.query(User).filter(User.username.is_(None)).all() )
print( session.query(User).filter(User.username.isnot(None)).all() )

#多条件
print( session.query(User).filter(User.username.isnot(None),User.password=='qwe123').all() )

#选择条件
from sqlalchemy import or_,and_,all_,any_
print( session.query(User).filter(or_(User.username=='jingqi',User.password=='qwe123')).all() )
print( session.query(User).filter(and_(User.username=='jingqi2',User.password=='111')).all() )


#多表联查
print( session.query(UserDetails,User).all() )  #这个是 cross join
print( session.query(UserDetails,User).filter(User.id==UserDetails.id).all() )  #这是也是cross join 但是加上了where条件
data = session.query(Users,Column_).filter(Users.uid==4).filter(Users.userName==Column_.cname).all()
print(data[0].Users.userName)
#这个是inner join
print( session.query(User.username,UserDetails.lost_login).join(UserDetails,UserDetails.id==User.id).all() )  
#这个才是左连接，sqlalchemy没有右连接
print( session.query(User.username,UserDetails.lost_login).outerjoin(UserDetails,UserDetails.id==User.id).all() )  

#这个是union关联
q1 = session.query(User.id)
q2 = session.query(UserDetails.id)
print(q1.union(q2).all())  


#原生查询 获取数据后，数据会删除
sql = "select * from users"
data = session.execute(sql)
print(data)
for i in data:
    print(i)
print( data.fetchone() )
print( data.fetchmany() )
print( data.fetchall() )