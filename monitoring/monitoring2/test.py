import shutil,os,sys
path = os.path.dirname(sys.argv[0])+'/'

shutil.copyfile( path+'cookies/www.1024vr.cn.json', path+'cookie2/www.1024vr.cn.json')