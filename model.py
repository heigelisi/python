

import os,sys,time,datetime,pymysql;
host = "localhost";
user = "root";
passwd = "";
database = "mobile";
port = 3306;
charset = 'utf8';
class Model(object):
	"""数据库操作"""
	def __init__(self,host=host,user=user,passwd=passwd,database=database,port=port,charset=charset):
		try:
			self.host=host;
			self.user=user;
			self.passwd=passwd;
			self.database=database;
			self.port=port;
			self.charset=charset;
			self.connect = pymysql.connect(host=host,user=user,passwd=passwd,db=database,charset=charset,port=port);
			self.cursor = self.connect.cursor();
		except Exception as e:
			print('数据库连接失败',e);
			exit();

	def error(self):
		return __file__,sys._getframe().f_lineno;

	#
	#tname 数据表名称 str
	#
	def table(self,tname):
		
		try:
			if not tname:
				print('数据表不能为空');
				exit();

			if type(tname) != type(''):
				print('table方法应该传入字符串');
				exit();

			self._table = tname;

			#查询表中的字段
			sql = "select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name='%s' and table_schema='%s'"%(tname,self.database);
			self.cursor.execute(sql);
			fields_obj = self.cursor.fetchall();
			self.fields = [];
			
			print(fields)



		except Exception as e:
			print(__file__,str(sys._getframe().f_lineno)+'行','table方法:',e);
			exit();
		return self;

	



	def insert(self,data):
		print('insert')

	def select(self):
		return ('select');





print(Model().table('linfei_images').insert('fff'))



