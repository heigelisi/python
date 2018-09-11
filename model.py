

import os,sys,time,datetime,pymysql;
host = "localhost";
user = "root";
passwd = "";
database = "mobile";
port = 3306;
charset = 'utf8';
class Model(object):
	"""数据库操作"""
	_where = None;
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
			sql = "select COLUMN_NAME,column_comment,column_key from INFORMATION_SCHEMA.Columns where table_name='%s' and table_schema='%s'"%(tname,self.database);
			self.cursor.execute(sql);
			fields_obj = self.cursor.fetchall();
			self.fields = [];#字段
			self.comment = [];#注释
			self.column_key = [];#索引
			for f in fields_obj:
				self.fields.append(f[0]);
				self.comment.append(f[1]);
				self.column_key.append(f[2]);

		except Exception as e:
			print(__file__,str(sys._getframe().f_lineno)+'行','table方法:',e);
			exit();
		return self;

	

	def __filter(self,data):
		#检测数据合法性 过滤掉不合法的字段信息
		try:
			data_list = [];
			if type(data) == type({}):
				#如果是一个'dict' 添加一条
				data_list.append(data);
			elif type(data) == type([]):
				#如果传一个list 添加多条
				data_list = data;
			else:
				print('数据类型错误');
				exit();

			#过滤
			data = [];
			for row in data_list:
				row_ = row.keys();
				rowdata = {};
				for r in row_:
					#如果数据中不存在此字段去除
					if r in self.fields:
						rowdata[r] = row.get(r);
				data.append(rowdata);

			return data;

		except Exception as e:
			print('数据不合法');
			exit();

	def insert(self,data):
		try:
			data = self.__filter(data);
			if not data:
				exit();

			#组建sql
			dataid = [];
			for row in data:
				key = ','.join(row.keys());
				val = "'"+"','".join(row.values())+"'";
				sql = "insert into %s(%s) values(%s)"%(self._table,key,val);
				try:
					self.cursor.execute(sql);
					self.connect.commit();
					dataid.append(self.cursor.lastrowid);
				except Exception as e:
					self.connect.rollback();
					print(row,e);
			return dataid;

		except Exception as e:
			print(e)
			

	def where(self,conditions=None):

		try:
			if type(conditions) == type(''):
				conditions.strip();
			if conditions != None and len(conditions) == 0:
				print('条件不能为空');
				exit();

			if type(conditions) == type('') and conditions == 'all':
				self._where = '';
			elif type(conditions) == type(''):
				self._where = "where "+conditions;
			
		except Exception as e:
			print(e)
			pass
		return self;


	def delete(self,where=None):
		try:

			if type(where) == type(''):
				where.strip();
			if where != None and len(where) == 0:
				print('条件不能为空');
				exit();

			if type(where) == type('') or type(where) == type(1):
				where = 'where '+self.fields[self.column_key.index('PRI')]+'='+str(where);
			elif type(where) == type({}):
				where = list(where.items())[0];
				key = where[0];
				val = where[1];
				if key not in self.fields:
					print(key,'字段不存在');
					exit();
				where = "where "+key+"='%s'"%(str(val));
			else:
				pass
				where = self._where;

			if where == None:
				print('不能没有删除条件');
				exit();

			#执行删除
			sql = "delete from %s %s"%(self._table,where);
			res = self.cursor.execute(sql);
			if res > 0:
				self.connect.commit();
				return res;
			else:
				self.connect.rollback();
				return False;
				
		except Exception as e:
			print(e);
			return False;
		

	def update(self,data):
		try:
			data = self.__filter(data)[0];
			if not data:
				exit();

			#组建sql
			where = self._where;
			if not where:
				where = '';
			setdata = [];
			for k,v in data.items():
				setdata.append(k+"='%s'"%str(v));
			sql = "update %s set %s %s"%(self._table,','.join(setdata),where);
			res = self.cursor.execute(sql);
			if res:
				self.connect.commit();
				return res;
			else:
				self.connect.rollback();
				return False;
		except Exception as e:
			print(e);
			return False;


	def select(self):
		return ('select');

	def __del__(self):
		self.cursor.close();
		self.connect.close();



print(Model().table('linfei_images').where('id=9').update({'name':'ffff','description':'hehehe','ffff':'vvv'}))



