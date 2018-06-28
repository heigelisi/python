	width = $('#conten').width()
	height = $('#conten').height()
	if(width < 720){
		$('#view').css('width','100%').css('height','45%').css('float','none');
		$('#msg').css('width','100%').css('float','none').css('height','40%');
		$('#input').css('width','100%').css('height','15%').css('float','none');
		$('textarea').css('width','85%');
		$('button').css('width','14%');
	}
	$('.expression').css('width',width*0.8+'px');
	$('video').click(function() {
		v = document.getElementById('myVideo1')
		if(!v.paused){
			v.pause()

		}else{
			v.play()
		}
	})

	function biaoqing(){
		display = $('.expression').css('display')
		if(display == 'none'){
			$('.expression').css('display','block');
		}else{
			$('.expression').css('display','none');
		}
	}
	$('.expression span').click(function(){
		$('textarea').val($('textarea').val()+$(this).text())
	})


// $('#send').on('click',function(){
// 	text = $('textarea[name="msg"]').val();
// 	if(text){
// 		str = '<li><div class="right" ><span class="name" style="text-align: right;">周飞</span><p class="msg">'+text+'</p></div><div class="left" style="float:right;"><i class="icon"></i></div><div class="null"></div></li>';
// 		$('#msg ul').append(str);
// 		$('textarea[name="msg"]').val('');
// 	}
// })




var showmsg;
var socket;  
   
function init(username){
  var host = "ws://localhost:8082";
  //连接服务器
  try{  
    socket = new WebSocket(host);  
    socket.onopen    = function(msg){
        log('您已经进入聊天室');
        socket.send(conversion(username));//发送用户名称给服务器端
    };
    //接受消息
    socket.onmessage = function(msg){
         msg = JSON.parse(msg.data)
         if (msg.username == sessionStorage.username){
              username = false
              $('.prompt').css('display','none');

           }else{
              username = msg.username
           }
	       log(msg.msg,username);
    };
    //断开连接时执行
    socket.onclose   = function(msg){
        log("与服务器连接断开");
    };
  }catch(ex){
      log(ex);
  }
  $(".sendInfo").focus();
}  

//发送消息给服务器 
function send(){  
	text = $('textarea[name="msg"]').val();
	if (text.length > 1000){
	    alert('不能超过1000个字符！');
	    return;
  	}
	if(text){
		str = '<li><div class="prompt"><span>发送中<img src="static/load.gif"></span></div><div class="right" ><span class="name" style="text-align: right;">我</span><p class="msg">'+text+'</p></div><div class="left" style="float:right;"><i class="icon"></i></div><div class="null"></div></li>';
		$('#msg ul').append(str);
		$('textarea[name="msg"]').val('');

		try{
        	socket.send(conversion(text));
      		$('.sayInfo').html(text)
  		} catch(ex){
      		log(ex);
  		}
	}
		
}


  



//转换中文
function conversion(msg)  
{
  message = '';
  for (var i = 0;i < msg.length; i++) {
    msg_ = msg.substr(i,1);
　　if(msg_.charCodeAt() > 255){ 
      msg_ = escape(msg_)
    }
    message += msg_
  }
  
  return message;
}


//刷新或关闭浏览器时 关闭socke
window.onbeforeunload=function(){  
    try{  
        socket.send(conversion('quit'));  
        socket.close();  
        socket=null;  
    }  
    catch(ex){  
        log(ex);  
    }  
};  

function nameok(){
	if(typeof(Storage)!=="undefined")
	{
		username = sessionStorage.username;
		if(username){
			init(username)
			$('.username').css('display','none');

		}else{
			var _name = $('input[name="username"]').val();
			if(_name){
				sessionStorage.username = _name;
				init(_name)
				$('.username').css('display','none');
			}else{
				 alert('请给自己取个名字吧');
				$('.username').css('display','block');

			}
		}
	   
	} else {
	    // 抱歉! 不支持 web 存储。
	}
 
}
nameok()
function log(msg,username='系统提醒'){
	if(username){
		msghtml = '<li><div class="left"><i class="icon"></i></div><div class="right"><span class="name">'+username+'</span><p class="msg">'+msg+'</p></div><div class="null"></div></li>';
	    $('#msg ul').append(msghtml);
	}

    //动画
    var _html = $('<div>',{'class':'showMsg'});
    _html.html(msg);
    $('.renBox').append(_html);
    _html.animate({
        'marginLeft':'-100%'
    }, 10000, function(){
        _html.remove()
    })
}
function show(obj){
    obj.fadeIn()
}
function onkey(event){ if(event.keyCode==13){ send(); } }  