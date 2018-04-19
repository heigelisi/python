var ps0roWsid="sVuyiIsULU1h"; // n=172.68.253.160, c=124.6.35.83

// safe-monitor@gecko.js

var ps0roWiso;
try {
	ps0roWiso = (opener != null) && (typeof(opener.name) != "unknown") && (opener.ps0roWwid != null);
} catch(e) {
	ps0roWiso = false;
}
if (ps0roWiso) {
	window.ps0roWwid = opener.ps0roWwid + 1;
	ps0roWsid = ps0roWsid + "_" + window.ps0roWwid;
} else {
	window.ps0roWwid = 1;
}
function ps0roWn() {
	return (new Date()).getTime();
}
var ps0roWs = ps0roWn();
function ps0roWst(f, t) {
	if ((ps0roWn() - ps0roWs) < 7200000) {
		return setTimeout(f, t * 1000);
	} else {
		return null;
	}
}
var ps0roWil;
var ps0roWit;
function ps0roWpi() {
	var il;
	if (3 == 2) {
		il = window.pageXOffset + 50;
	} else if (3 == 3) {
		il = (window.innerWidth * 50 / 100) + window.pageXOffset;
	} else {
		il = 50;
	}
	il -= (271 / 2);
	var it;
	if (3 == 2) {
		it = window.pageYOffset + 50;
	} else if (3 == 3) {
		it = (window.innerHeight * 50 / 100) + window.pageYOffset;
	} else {
		it = 50;
	}
	it -= (191 / 2);
	if ((il != ps0roWil) || (it != ps0roWit)) {
		ps0roWil = il;
		ps0roWit = it;
		var d = document.getElementById('ci0roW');
		if (d != null) {
			d.style.left  = Math.round(ps0roWil) + "px";
			d.style.top  = Math.round(ps0roWit) + "px";
		}
	}
	setTimeout("ps0roWpi()", 100);
}
var ps0roWlc = 0;
function ps0roWsi(t) {
	window.onscroll = ps0roWpi;
	window.onresize = ps0roWpi;
	ps0roWpi();
	ps0roWlc = 0;
	var url = "http://messengers.providesupport.net/" + ((t == 2) ? "auto" : "chat") + "-invitation/0wnbj0qzkr2ks163j88h32wibn.html?ps_t=" + ps0roWn() + "&ps_vsid=" + ps0roWsid + "";
	var d = document.getElementById('ci0roW');
	if (d != null) {
		d.innerHTML = '<iframe allowtransparency="true" style="background:transparent;width:271;height:191" src="' + url + 
			'" onload="ps0roWld()" frameborder="no" width="271" height="191" scrolling="no"></iframe>';
	}
}
function ps0roWld() {
	if (ps0roWlc == 1) {
		var d = document.getElementById('ci0roW');
		if (d != null) {
			d.innerHTML = "";
		}
	}
	ps0roWlc++;
}
if (false) {
	ps0roWsi(1);
}
var ps0roWop = false;
function ps0roWco() {
	var w1 = ps0roWci.width - 1;
	ps0roWscf((w1 & 2) != 0);
	var h = ps0roWci.height;

	if (h == 1) {
		ps0roWop = false;

	// manual invitation
	} else if ((h == 2) && (!ps0roWop)) {
		ps0roWop = true;
		ps0roWsi(1);

	// auto invitation
	} else if ((h == 3) && (!ps0roWop)) {
		ps0roWop = true;
		ps0roWsi(2);
	}
}
var ps0roWci = new Image();
ps0roWci.onload = ps0roWco;
var ps0roWpm = false;
var ps0roWcp = ps0roWpm ? 30 : 60;
var ps0roWct = null;
function ps0roWscf(p) {
	if (ps0roWpm != p) {
		ps0roWpm = p;
		ps0roWcp = ps0roWpm ? 30 : 60;
		if (ps0roWct != null) {
			clearTimeout(ps0roWct);
			ps0roWct = null;
		}
		ps0roWct = ps0roWst("ps0roWrc()", ps0roWcp);
	}
}
function ps0roWrc() {
	ps0roWct = ps0roWst("ps0roWrc()", ps0roWcp);
	try {
		ps0roWci.src = "http://image.providesupport.com/cmd/0wnbj0qzkr2ks163j88h32wibn?" + "ps_t=" + ps0roWn() + "&ps_l=" + escape(document.location) + "&ps_r=" + escape(document.referrer) + "&ps_s=" + ps0roWsid + "" + "";
	} catch(e) {
	}
}
ps0roWrc();


