


def date(format_="%Y-%m-%d %H:%M:%S",timestamp=0):
	import time;
	if timestamp:
		timestamp = int(timestamp);
	else:
		timestamp = int(time.time());
	time_local = time.localtime(timestamp)
	#转换成新的时间格式(2016-05-05 20:28:54)
	return str(time.strftime(format_,time_local));


def md5(str):
	import hashlib
	return hashlib.md5(str.encode('utf-8')).hexdigest();