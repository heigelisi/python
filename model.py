

import os,sys,time,datetime,pymysql;
host = "localhost";
user = "root";
passwd = "";
database = "mobile";
port = 3306;
charset = 'utf8';
class Model(object):
	"""数据库操作"""
	_where = '';
	_order = '';
	_fields_ = '';
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
			self._fields = [];#字段
			self.comment = [];#注释
			self.column_key = [];#索引
			for f in fields_obj:
				self._fields.append(f[0]);
				self.comment.append(f[1]);
				self.column_key.append(f[2]);
			self._fields_ = ','.join(self._fields);
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
					if r in self._fields:
						rowdata[r] = str(row.get(r)).replace("'",'"');
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
				self.sql = sql = "insert into %s(%s) values(%s)"%(self._table,key,val);
				try:
					self.cursor.execute(sql);
					self.connect.commit();
					dataid.append(self.cursor.lastrowid);
				except Exception as e:
					self.connect.rollback();
					print(row,e);
			if len(dataid) == 1:
				return dataid[0];
			return dataid;

		except Exception as e:
			print('insert',e)
			

	def where(self,conditions=''):

		try:
			if type(conditions) == type(''):
				conditions = conditions.strip();
			else:
				self._where = '';

			if not conditions or conditions == 'all':
				self._where = '';

			else:
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
				where = 'where '+self._fields[self.column_key.index('PRI')]+'='+str(where);
			elif type(where) == type({}):
				where = list(where.items())[0];
				key = where[0];
				val = where[1];
				if key not in self._fields:
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
			self.sql = sql = "delete from %s %s"%(self._table,where);
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
			setdata = [];
			for k,v in data.items():
				setdata.append(k+"='%s'"%str(v));
			self.sql = sql = "update %s set %s %s"%(self._table,','.join(setdata),where);
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

	def fields(self,field=None):
		try:
			if not field or type(field) != type(''):
				self._fields_ = ','.join(self._fields);

			else:
				#过滤非法字段
				fieldList = field.split(',');
				_fields_ = [];
				for f in fieldList:
					if f in self._fields:
						_fields_.append(f);
				if _fields_:
					self._fields_ = ','.join(_fields_);
				else:
					self._fields_ = ','.join(self._fields);


		except Exception as e:
			pass
		return self;

	def conversionData(self,data):
		try:
			if not data:
				return None;
			#获取查询的字段
			fields = self._fields_.split(',');
			data_ = {};
			for i in data:
				data_[fields[data.index(i)]] = i;
			
			return data_;
		except Exception as e:
			pass

	def find(self):
		"""查询一条数据"""
		try:
			#获取where
			where = self._where;

			#获取排序方式
			order = self._order;

			#获取要查询的字段
			fields = self._fields_;
			if not fields:
				fields = ','.join(self._fields);

			#组建sql
			self.sql = sql = "select %s from %s %s %s limit 1"%(fields,self._table,where,order);
			self.cursor.execute(sql);
			data = self.cursor.fetchone();
			if not data:
				return None;


			return self.conversionData(data);

		except Exception as e:
			print('find',e);
			pass

	def order(self,way=''):
		"""排序"""
		try:
			if type(way) == type(''):
				way = way.strip();
			else:
				way = '';
			if not way:
				self._order = '';
			else:
				self._order = "order by %s"%(way);

		except Exception as e:
			print('order',e);
			pass
		return self;

	def limit(self,startstop=''):
		try:
			startstop = startstop.split(',');
			if len(startstop) == 1 and startstop[0].isnumeric():
				self._limit = "limit "+str(startstop[0]);
			elif len(startstop) > 1 and startstop[0].isnumeric() and startstop[1].isnumeric():
				self._limit = "limit %s,%s"%(str(startstop[0]),startstop[1]);
			else:
				self._limit = '';

		except Exception as e:
			pass
		return self;


	def count(self):
		try:

			#获取where
			where = self._where;
			self.sql = sql = "select count(1) from %s %s"%(self._table,where);
			self.cursor.execute(sql);
			count = self.cursor.fetchone()[0];
			return count;
		except Exception as e:
			print('count',e);



	def select(self):
		try:
			where = self._where;
			order = self._order;
			limit = self._limit;
			fields = self._fields_;
			self.sql = sql = "select %s from %s %s %s %s"%(fields,self._table,where,order,limit);
			self.cursor.execute(sql);
			data = self.cursor.fetchall();
			if not data:
				return [];
			#转换数据
			datas = [];
			for row in data:
				datas.append(self.conversionData(row));
			return datas;

		except Exception as e:
			pass


	def value(self,val):
		try:
			val = val.strip();
			if not val or val not in self._fields:
				print(val,'字段不存在');
				exit();
			where = self._where;
			order = self._order;
			sql = "select %s from %s %s %s limit 1"%(val,self._table,where,order);
			self.cursor.execute(sql);
			data = self.cursor.fetchone();
			if data:
				return list(self.conversionData(data).values())[0];
			return None;

		except Exception as e:
			print('val',e);


	def close(slef):
		self.cursor.close();
		self.connect.close();

	def __del__(self):
		self.cursor.close();
		self.connect.close();


# m = Model(passwd="123456",database='message',host="127.0.0.1");
# print(m.table('data').where('id=10').value('mobile'));
######增
#单条
	# data = {'mobile':'13539993040','num':1000,'msg':'ok'};
	# m.table('data').insert(data);#返回插入的主键
#多条
	# data = [{'mobile':'13539993040','num':1000,'msg':'ok'},{'mobile':'13539993040','num':1000,'msg':'ok'}];
	# m.table('data').insert(data);#返回插入的主键list

#删 成功返回影响行数 失败返回False
	# m.table('data').delete(1);#删除主键等于1的
	# m.table('data').delete('id=1');#删除id等于1的
	# m.table('data').where('id=1').delete();

#改 成功返回影响行数 失败返回False
	# data = {'mobile':'13539993040','num':10000,'msg':'修改'};
	# m.table('data').where('id=1').update(data);

#查
	# m.table('data').find();#查询一条
	# m.table('data').where('id=1').find();#按条件查询一条
	# m.table('data').where('name=zhoufei').order('id desc').find();#按条件查询一条
	# m.table('data').select();#查询多条
	# m.table('data').where('id=1').select();#按条件查询多条
	# m.table('data').where('name=zhoufei').order('id desc').select();#按条件查询多条
	# m.table('data').where('name=zhoufei').order('id desc').limit('1,5').select();#按条件查询多条分页
	# m.table('data').fields('id,name').where('name=zhoufei').order('id desc').limit('1,5').select();#按条件查询多条分页
	# m.table('data').where('name=zhoufei').count();#查询满足条件的条数
