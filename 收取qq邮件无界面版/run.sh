#!/bin/sh
ii=1
while [ 1 ]; do
  #当前时间
  send=`date '+%M'`
  let "ii+=1"
  echo $ii
  pgrep -l python3
  if [[ $send = '11' ]]; then
  	#重启python3
  	pgrep -l python3
	pkill python3
	sleep 10
	nohup python3 -u /www/wwwroot/pythonScript/getEcEmail/getEmail.py > /www/wwwroot/pythonScript/getEcEmail/getEmail.log 2>&1 &
	seltime=`date '+%Y-%m-%d %H:%M:%S'`  
	echo $seltime 
	sleep 60
  fi
  sleep 2
done

# nohup sh /www/wwwroot/pythonScript/getEcEmail/run.sh > /www/wwwroot/pythonScript/getEcEmail/run.log 2>&1 &
