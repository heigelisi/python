function objview78_000(url){ 
    var obj = new Object; 
    //obj.imgurl = _embed_v3_.stat;
    //obj.arrivalurl = _embed_v3_.arrivalstat;
    obj.expires = _pushshowjs_.expires ? _pushshowjs_.expires : 10;
    obj.param = _pushshowjs_.param;
    obj.iWidth = 320;
    obj.iHeight = 240;
    obj.iPosition = 1;
    obj.iBorder = 1;
    obj.iShowType = 1;
    //obj.iStartTime = 1;
    //obj.iCloseTime = 0;    
    obj.bHadShow = false;
    obj.sInterval = 5;
    obj.bNeedShow = false;
    obj.bShowing = false;
    obj.hHandle; // the handle of scroll timer;
    obj.hCheckAD;  // the handle of adchecker timer;
    obj.arralreadysend = false; //
    obj.iPid = 0; 
    obj.base_url = _pushshowjs_.baseurl;
    obj.url = url;
    obj.elmHeight = 0;
    obj.policyParam = '';
	obj.closeispush = _pushshowjs_.closeispush;
	obj.feedbackurl = _pushshowjs_.feedurl;
	
	obj.isAutoClose = _pushshowjs_.isAutoClose != null && typeof(_pushshowjs_.isAutoClose) != "undefined" && !isNaN(_pushshowjs_.isAutoClose) ? _pushshowjs_.isAutoClose : 1;
	obj.closeTimes = _pushshowjs_.closeTimes != null && typeof(_pushshowjs_.closeTimes) != "undefined" && !isNaN(_pushshowjs_.closeTimes) ? _pushshowjs_.closeTimes : 0;
	
    obj.GetViewHtml = function(){
        var str = '';
        str = str + '<div id="_embed_v3_dc" style="overflow:hidden; margin:0; float:left; z-index:9998; position:fixed;bottom:0;right:0;display:none;">';
		str = str + '  <div id="_embed_v3_hd_r" style="overflow:hidden; z-index:2147483647; width:100%; height:18px; position:relative;" onclick="clickCloseFeedback('+obj.closeispush+')"><span id="_embed_v3_btnc" alt="Close"><img src="http://183.59.53.202:3535/pushjs/close.gif" style="height:14px; width:43px; float:right;" /></span>';
		    str = str + '  <div id="_embed_v3_hd">';
		    str = str + '    <div id="_embed_v3_hd_l"></div>';
		    str = str + '    <div id="_embed_v3_hd_c"></div>';
		    str = str + '    </div>';
        str = str + '  </div>';
        str = str + '  <div id="_embed_v3_main"  style="z-index:2147483646;height:100%; top:15px;"><iframe id="_embed_v3_frmc" style="border:0px;width:100%;height:100%;" scrolling="no" name="_embed_v3_frmc" src="'+obj.url+'"></iframe></div>';
        str = str + '  <div id="_embed_v3_ft"></div>';
        str = str + '</div>';
        
        return str;
    };
	
	obj.autoClose = function(){
		//alert(obj.isAutoClose + "|" + obj.closeTimes);
		if(obj.isAutoClose == 0){
			var cTimes = obj.closeTimes * 1000;
			//document.getElementById('_embed_v3_dc').style.display='none'; 
			//document.getElementById('_embed_v3_frmc').src='';
			setTimeout("document.getElementById('_embed_v3_dc').style.display='none';document.getElementById('_embed_v3_frmc').src='';",cTimes);
			if(obj.closeispush == 1){
				var URL = _pushshowjs_.feedurl;
				var path = _pushshowjs_.eparam;

				path=decodeURIComponent(path);
				path=path.replace(' ','+');
				
				if (path != "") {
					path = URL + path + "&stype=5";
				} else {
					path = URL;
				}

				var xhr;
				if (window.XMLHttpRequest) {
					xhr = new XMLHttpRequest();
				} else {
					xhr = new ActiveXObject("Microsoft.XMLHTTP");
				}

				xhr.open("get", path, true);

				xhr.onreadystatechange = function(data) {
					if (xhr.readyState == 4) {
						if (xhr.status == 200) {
							/*if(stype==0){
								//实名推送获取内容替换占位符
								replaceContent(xhr.responseText);
							}else if(stype==3){
								closePage();
							}*/
						}
					}
				}
				
				xhr.send();
			}
		}
	};
	
    obj.getParams = function() {
        var paramarray = obj.param.split("|");
        obj.SetCookie(obj.policyParam,obj.policyParam, { expires: obj.expires, path: '/' });
        try {
            obj.iWidth = parseInt(paramarray[1], 10);
            obj.iHeight = parseInt(paramarray[2], 10);
            obj.iPosition = parseInt(paramarray[3], 10);
            obj.iBorder = parseInt(paramarray[4], 10);
            obj.iShowType = parseInt(paramarray[5], 10);
            //obj.iStartTime = parseInt(paramarray[5], 10);
            //obj.iCloseTime = parseInt(paramarray[6], 10);
        } catch (e) {
            obj.iWidth = 320;
            obj.iHeight = 240;
            obj.iPosition = 1;
            obj.iBorder = 1;
            obj.iShowType = 1;
            //obj.iStartTime = 1;
            //obj.iCloseTime = 0;
        }
    };
    obj.getPolicyParam = function(){
				//var c_start = obj.arrivalurl.indexOf("=") + 1;
				//return obj.arrivalurl.substring(c_start); 
				return obj.param;
     };
    obj.getStyle = function(el, style) {
        if (!document.getElementById) return;
        var value = el.style[obj.toCamelCase(style)];

        if (!value) if (document.defaultView) value = document.defaultView.getComputedStyle(el, "").getPropertyValue(style);

        else if (el.currentStyle) value = el.currentStyle[obj.toCamelCase(style)];

        return value;
    };
    obj.setStyle = function(objId, style, value) {
        document.getElementById(objId).style[style] = value;
    };
    obj.toCamelCase = function(sInput) {
        var oStringList = sInput.split('-');
        if (oStringList.length == 1) return oStringList[0];
        var ret = sInput.indexOf("-") == 0 ? oStringList[0].charAt(0).toUpperCase() + oStringList[0].substring(1) : oStringList[0];
        for (var i = 1,len = oStringList.length; i < len; i++) {
            var s = oStringList[i];
            ret += s.charAt(0).toUpperCase() + s.substring(1);
        }
        return ret;
    };
    obj.add_css = function(str_css) {
        var style;
        if (document.createStyleSheet) {
            style = document.createStyleSheet();
            style.cssText = str_css;
        } else {
            style = document.createElement("style");
            style.type = "text/css";
            style.textContent = str_css;
            document.getElementsByTagName("head")[0].appendChild(style);
        }
    };
    obj.DrawAdDiv = function(iStyle) {
        //iStyle: 1:no border; 2:qq style;3:sina style
        //no border
        if (iStyle == 1) {
            obj.setStyle('_embed_v3_frmc', "height", obj.iHeight + "px");
            obj.setStyle('_embed_v3_frmc', "width", obj.iWidth + "px");
            obj.setStyle('_embed_v3_dc', "height", obj.iHeight + "px");
            obj.setStyle('_embed_v3_dc', "width", obj.iWidth + "px");
            obj.setStyle('_embed_v3_dc', "position", "fixed");
            obj.setStyle('_embed_v3_hd_l', "text-indent", "-9999px");
            document.getElementById("_embed_v3_hd_c").innerHTML = "&nbsp;";
			//document.getElementById("_embed_v3_btnc").style.cssText = "width:20px; height:14px; float:right; background-color:Silver; font-size:12px; cursor:pointer; text-align:center; position:relative; z-index:9999; margin:-14px 5px 0 0;";
            document.getElementById("_embed_v3_main").style.cssText = "position:absolute; top:15; left:0; z-index:9997;overflow:hidden;";
            obj.setStyle('_embed_v3_main', "width", obj.iWidth + "px");
        }
        //2:qq style;
        if (iStyle == 2) {
            obj.setStyle('_embed_v3_frmc', "height", obj.iHeight + "px");
            obj.setStyle('_embed_v3_frmc', "width", obj.iWidth + "px");
            obj.setStyle('_embed_v3_dc', "height", obj.iHeight + 24 + 5 + "px");
            obj.setStyle('_embed_v3_dc', "width", obj.iWidth + 3 + 3 + "px");
            obj.setStyle('_embed_v3_dc', "position", "fixed");
            document.getElementById("_embed_v3_hd").style.cssText = 'height:24px; overflow:hidden;';
            obj.setStyle('_embed_v3_hd', "width", obj.iWidth + 3 + 3 + "px");
            //document.getElementById("_embed_v3_hd_l").style.cssText = 'width:3px; height:24px;background:url("'+obj.base_url+'images/qqstyle_01.gif") no-repeat; text-indent:-9999px; float:left;';
            document.getElementById("_embed_v3_hd_l").style.cssText = 'width:3px; height:24px; text-indent:-9999px; float:left;';
            //document.getElementById("_embed_v3_hd_c").style.cssText = 'height:24px; background:url("'+obj.base_url+'images/qqstyle_02.gif") repeat-x; float:left;';
            document.getElementById("_embed_v3_hd_c").style.cssText = 'height:24px; float:left;';
            obj.setStyle('_embed_v3_hd_c', "width", obj.iWidth + 3 + 3 - 3 - 20 + "px");
            document.getElementById("_embed_v3_hd_r").style.cssText =  'width:20px; height:24px; float:left;';
            //document.getElementById("_embed_v3_btnc").style.cssText = 'width:20px;height:24px;float:right; background:url("'+obj.base_url+'images/qqstyle_06.gif") no-repeat; position:relative; z-index:9999; text-indent:-9999px;cursor:pointer;';
            document.getElementById("_embed_v3_btnc").style.cssText = 'width:43px;height:30px;float:right; background:url("'+obj.base_url+'close.gif") no-repeat; position:relative; z-index:9999; text-indent:-9999px;cursor:pointer;';
            //document.getElementById("_embed_v3_main").style.cssText = 'background:#bddefd; text-align:center; padding:0 3px;';
            document.getElementById("_embed_v3_main").style.cssText = 'text-align:center; padding:0 0px;';
            obj.setStyle('_embed_v3_main', "width", obj.iWidth + "px");
            //document.getElementById("_embed_v3_ft").style.cssText = 'height:5px; background:#bddefd;';
            document.getElementById("_embed_v3_ft").style.cssText = 'height:5px;';
            obj.setStyle('_embed_v3_ft', "width", obj.iWidth + 3 + 3 + "px");
        }
        //3:sina style	
        if (iStyle == 3) {
            obj.setStyle('_embed_v3_frmc', "height", obj.iHeight + "px");
            obj.setStyle('_embed_v3_frmc', "width", obj.iWidth + "px");
            obj.setStyle('_embed_v3_dc', "height", obj.iHeight + 27 + 5 + "px");
            obj.setStyle('_embed_v3_dc', "width", obj.iWidth + 3 + 3 + "px");
            obj.setStyle('_embed_v3_dc', "position", "fixed");
            document.getElementById("_embed_v3_hd").style.cssText = 'height:27px; overflow:hidden;';
            obj.setStyle('_embed_v3_hd', "width", obj.iWidth + 3 + 3 + "px");
            document.getElementById("_embed_v3_hd_l").style.cssText = 'width:3px; height:27px;background:url("'+obj.base_url+'images/sinastyle_01.gif") no-repeat; text-indent:-9999px; float:left;';
            document.getElementById("_embed_v3_hd_c").style.cssText = 'height:27px; background:url("'+obj.base_url+'images/sinastyle_02.gif") repeat-x; float:left;';
            obj.setStyle('_embed_v3_hd_c', "width", obj.iWidth + 3 + 3 - 3 - 65 + "px");
            document.getElementById("_embed_v3_hd_r").style.cssText ='width:65px; height:27px; float:left;cursor:pointer;';
            document.getElementById("_embed_v3_btnc").style.cssText ='width:65px;height:27px; float:right; background:url("'+obj.base_url+'images/sinastyle_06.gif") no-repeat; position:relative; z-index:9999; text-indent:-9999px;';
            document.getElementById("_embed_v3_main").style.cssText = 'background:#bddefd; text-align:center; padding:0 3px;';
            obj.setStyle('_embed_v3_main', "width", obj.iWidth + "px");
            document.getElementById("_embed_v3_ft").style.cssText ='height:5px; background:#bddefd;';
            obj.setStyle('_embed_v3_ft', "width", obj.iWidth + 3 + 3 + "px");
        }
    };
    obj.ShowIt = function(elmHeight) {       
        if (obj.bHadShow || obj.bShowing) return;        
        //obj.SendArrive();
        obj.bShowing = true;       
        obj.setStyle('_embed_v3_dc', 'display', '');
        if (obj.iShowType == 1) {
           obj.setStyle('_embed_v3_dc', 'height', elmHeight + "px");
           obj.bHadShow = true;
           obj.bShowing = false;           
        } else {
           obj.elmHeight = elmHeight;
           obj.hHandle = setInterval(obj.scrollit, obj.sInterval);
        }
    };
    //obj.SendArrive = function() {
   //     if (!obj.arralreadysend){
		//			obj.arralreadysend = true;
		//			var img1 = new Image();
		 //   	img1.src = obj.imgurl;
		//			var img2 = new Image();
		//			img2.src = obj.arrivalurl;
     //   }
    //};
    obj.scrollit = function() {
        var currh = parseInt(obj.getStyle(document.getElementById("_embed_v3_dc"), "height"));
        currh++;
        obj.setStyle('_embed_v3_dc', 'height', currh + "px");
        if (currh >= obj.elmHeight) {
           obj.bHadShow = true;
           obj.bShowing = false;
           clearInterval(obj.hHandle);
        }
    };
    obj.Get_scroll_70e=(document.compatMode=="CSS1Compat")?document.documentElement:document.body;
    obj.PositionIE = function(){
	    if (/msie (\d+\.\d)/i.test(navigator.userAgent)) {
		    var q=parseFloat(RegExp.$1);
		    return (q>=7&&document.compatMode!="BackCompat");
	    }else return true;
    };
    obj.xcy_move = function(){
	    if(obj.Get_scroll_70e==null){
		    obj.Get_scroll_70e=(document.compatMode=="CSS1Compat")?document.documentElement:document.body;
		}		    
		var dcWidth = parseInt(obj.getStyle(document.getElementById('_embed_v3_dc'), "width"));
        var dcHeight = parseInt(obj.getStyle(document.getElementById('_embed_v3_dc'), "height"));  
        //alert("top="+obj.Get_scroll_70e.scrollTop + obj.Get_scroll_70e.clientHeight - dcHeight);
        //alert("left="+obj.Get_scroll_70e.scrollLeft + obj.Get_scroll_70e.clientWidth - dcWidth);
        obj.setStyle('_embed_v3_dc', "left", parseInt(obj.Get_scroll_70e.scrollLeft + obj.Get_scroll_70e.clientWidth - dcWidth) + "px");
        obj.setStyle('_embed_v3_dc', "top", (obj.Get_scroll_70e.scrollTop + obj.Get_scroll_70e.clientHeight - dcHeight) + "px");
    };
    obj.locatead = function(showad){ 		
		var posLeft = 0;
		var posTop = 0;
		//FixDomain();
		var docWidth = obj.Get_scroll_70e.scrollLeft + obj.Get_scroll_70e.clientWidth;
		var docHeight = obj.Get_scroll_70e.scrollTop + obj.Get_scroll_70e.clientHeight;   
		var dcWidth = parseInt(obj.getStyle(document.getElementById('_embed_v3_dc'), "width"));
        var dcHeight = parseInt(obj.getStyle(document.getElementById('_embed_v3_dc'), "height"));  
		switch (obj.iPosition) {
			case 1:
				obj.setStyle('_embed_v3_dc', "top", "0px");
				obj.setStyle('_embed_v3_dc', "left", "0px");
				break;
			case 2:
				obj.setStyle('_embed_v3_dc', "left", "0px");
				obj.setStyle('_embed_v3_dc', "top", parseInt((docHeight - dcHeight) / 2) + "px");
				break;
			case 3:
				obj.setStyle('_embed_v3_dc', "left", "0px");
				obj.setStyle('_embed_v3_dc', "top", (docHeight - dcHeight) + "px");
				break;
			case 4:
				obj.setStyle('_embed_v3_dc', "top", "0px");
				obj.setStyle('_embed_v3_dc', "left", parseInt((docWidth - dcWidth) / 2) + "px");
				break;
			case 5:
				obj.setStyle('_embed_v3_dc', "left", parseInt((docWidth - dcWidth) / 2) + "px");
				obj.setStyle('_embed_v3_dc', "top", parseInt((docHeight - dcHeight) / 2) + "px");
				break;
			case 6:
				obj.setStyle('_embed_v3_dc', "left", parseInt((docWidth - dcWidth) / 2) + "px");
				obj.setStyle('_embed_v3_dc', "top", (docHeight - dcHeight) + "px");
				break;
			case 7:
				obj.setStyle('_embed_v3_dc', "left", parseInt(docWidth - dcWidth) + "px");
				obj.setStyle('_embed_v3_dc', "top", "0px");
				break;
			case 8:
				obj.setStyle('_embed_v3_dc', "left", parseInt(docWidth - dcWidth) + "px");
				obj.setStyle('_embed_v3_dc', "top", parseInt((docHeight - dcHeight) / 2) + "px");
				break;
			case 9:
				obj.setStyle('_embed_v3_dc', "left", parseInt(docWidth - dcWidth) + "px");
				obj.setStyle('_embed_v3_dc', "top", (docHeight - dcHeight) + "px");
				break;
		}
		//CheckScreenSize();
		//if (obj.bHadShow == false && showad && !obj.bShowing) {
		//	obj.setStyle('_embed_v3_dc', "height", "0px");  
		//	if (parseInt(getStyle($('dc'), 'top')) + dcHeight == docHeight) {
		//		setStyle('dc', "top", "");
		//		setStyle('dc', "bottom", "0px");
		//	}        
		//	ShowIt(dcHeight);
		//}
         
        if (obj.bHadShow == false && showad && !obj.bShowing) {
            //var dcHeight = parseInt(obj.getStyle(document.getElementById('_embed_v3_dc'), "height"));             
            obj.setStyle('_embed_v3_dc', "height", "0px");                  
            obj.ShowIt(dcHeight);
			window.setInterval(obj.resize,100);
			//obj.iframecontent();
        }	      
    };
	obj.resize = function(){
		obj.locatead(false);
	};
	obj.iframecontent = function(){
	try{
	    var aa =document.getElementById("_embed_v3_frmc").contentWindow.document.body.innerHTML;
	    }catch(e){}
	};
    obj.view = function(){
		if(obj.adcheck()) return;

        obj.getParams();
        //document.writeln(obj.GetViewHtml());    
				var a=document.createElement("div");
				a.innerHTML= obj.GetViewHtml(); 
				document.body.appendChild(a);
        obj.setStyle("_embed_v3_dc", "display", "none");
                       
        obj.bNeedShow = true;
        if (!obj.bShowing && !obj.bHadShow){ 
            obj.dispad();
        }
		obj.autoClose();
    };
    obj.adcheck = function() {

        if(location.href.indexOf("gd.189.cn")>=0) return true;
        var isIf = false;		
		try{
			if(self != top){
				isIf = true;
		}}catch(e){
			//如果是在和父页面不同域
			isIf = true;
		}		
		return isIf;
    };
    obj.dispad = function() {
        if (obj.bShowing == false && obj.bNeedShow) {
            obj.DrawAdDiv(obj.iBorder); 
            obj.locatead(true);
        }
    };
    obj.trim = function(text){  
     return (text || "").replace(/^\s+|\s+$/g, ""); 
    };
    obj.GetCookie = function(name){
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = obj.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    obj.SetCookie = function(name, value, options) {    
        options = options || {};
        if (value === null) {
            value = '';
            options.expires = -1;
        }        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires  * 1000));
            } else {
                date = options.expires;
            }   
            expires = '; expires=' + date.toUTCString();
        }        
        var path = options.path ? '; path=' + (options.path) : '';
        var domain = options.domain ? '; domain=' + (options.domain) : '';
        var secure = options.secure ? '; secure' : '';
        document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
    };
    return obj; 
}
function clickCloseFeedback(closeispush){
	document.getElementById('_embed_v3_dc').style.display='none'; 
	document.getElementById('_embed_v3_frmc').src='';
	if(closeispush == 1){
		var URL = _pushshowjs_.feedurl;
		var path = _pushshowjs_.eparam;

		path=decodeURIComponent(path);
		path=path.replace(' ','+');
		
		if (path != "") {
			path = URL + path + "&stype=5";
		} else {
			path = URL;
		}

		var xhr;
		if (window.XMLHttpRequest) {
			xhr = new XMLHttpRequest();
		} else {
			xhr = new ActiveXObject("Microsoft.XMLHTTP");
		}

		xhr.open("get", path, true);

		xhr.onreadystatechange = function(data) {
			if (xhr.readyState == 4) {
				if (xhr.status == 200) {
					/*if(stype==0){
						//实名推送获取内容替换占位符
						replaceContent(xhr.responseText);
					}else if(stype==3){
						closePage();
					}*/
				}
			}
		}
		
		xhr.send();
	}
};
var _oP78_000=objview78_000(_pushshowjs_.url); 
try{
    _oP78_000.policyParam =  _oP78_000.getPolicyParam();
    if (_oP78_000.GetCookie(_oP78_000.policyParam) == null){       
			_oP78_000.view();
    }
}catch (err) {}
