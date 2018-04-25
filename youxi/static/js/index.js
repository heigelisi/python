
$('.login .input').hover(function(){
	// $(this).css('border','1px solid #f39800')
	$(this).find('input').focus()
},function(){
		// $(this).css('border','1px solid #454545')
		

})

$('.login input').focus(function(){
	$(this).parent().css('border','1px solid #f39800')
})
$('.login input').blur(function(){

	$(this).parent().css('border','1px solid #454545')
})

$('nav li a').click(function(){
  	// $('nav a').find('h3').eq(0).css('color','#fff');
  	h3 = $('nav a')
  	for (i =0;i < h3.length;i++){
  		$(h3[i]).find('h3').eq(0).css('color','#fff');
  	}
  	class_ = $(this).attr('r');
  	var mTop = $('.'+class_).offset().top;
    $(window).scrollTop(mTop-100);
  	$(this).find('h3').eq(0).css('color','#f00');

})



$('#top').click(function(){
	// $(window).scrollTop(0);
	$('body,html').animate({scrollTop:0},600);
})



$('.slots>div li').hover(function(){
	$(this).append('<div><a class="button" href="javascript:operation();">进入游戏</a></div>')
	$(this).find('div').css('display','block')

},function(){
	$(this).find('div').css('display','none')

})

$('.mg>div li').hover(function(){
	
	$(this).append('<div><a class="button" href="javascript:operation();">进入游戏</a></div>')
	$(this).find('div').css('display','block')

},function(){
	$(this).find('div').css('display','none')

})
$('.pt>div li').hover(function(){
	
	$(this).append('<div><a class="button" href="javascript:operation();">进入游戏</a></div>')
	$(this).find('div').css('display','block')

},function(){
	$(this).find('div').css('display','none')

})

$('.qt>div li').hover(function(){
	
	$(this).append('<div><a class="button" href="javascript:operation();">进入游戏</a></div>')
	$(this).find('div').css('display','block')

},function(){
	$(this).find('div').css('display','none')

})
$('.qipai>div li').hover(function(){
	
	$(this).append('<div><a class="button" href="javascript:operation();">进入游戏</a></div>')
	$(this).find('div').css('display','block')

},function(){
	$(this).find('div').css('display','none')

})
$('.slots>div li img').attr('src','http://678v.cc/images/logo.png')
$('.mg>div li img').attr('src','http://678v.cc/images/logo.png')
$('.pt>div li img').attr('src','http://678v.cc/images/logo.png')
$('.qt>div li img').attr('src','http://678v.cc/images/logo.png')
$('.qipai>div li img').attr('src','http://678v.cc/images/logo.png')



function loadimg(){
	height = window.innerHeight;
	imgdata = $('[data-src]')
	for(i = 0;i < imgdata.length;i++){
		sTop = $(window).scrollTop();//滚动条顶部高度
		mtop = $(imgdata[i]).offset().top;//当前元素位置
		activity = mtop - sTop;
		if (activity < (height - 120) && activity > 50){
			$(imgdata[i]).attr('src',$(imgdata[i]).attr('data-src'))
		}
	}
}
loadimg()
$(function(){
window.onscroll=function(){
loadimg();


var sTop = $(window).scrollTop();
var mTop = $('.qipai')[0].offsetTop;
var qipai = mTop - sTop;
qipaiheight = $('.qipai').height()
qipaim = qipai + qipaiheight;
if (qipai < 110 && qipaim > 110){
	$('a[r="qipai"]').find('h3').eq(0).css('color','#f00')
}else{
	$('a[r="qipai"]').find('h3').eq(0).css('color','#fff')
}



var sTop = $(window).scrollTop();
var mTop = $('.shishicai')[0].offsetTop;
var shishicai = mTop - sTop;
shishicaiheight = $('.shishicai').height()
shishicaim = shishicai + shishicaiheight;
if (shishicai < 110 && shishicaim > 110){
	$('a[r="shishicai"]').find('h3').eq(0).css('color','#f00')
}else{
	$('a[r="shishicai"]').find('h3').eq(0).css('color','#fff')
}

var sTop = $(window).scrollTop();
var mTop = $('.casino')[0].offsetTop;
var casino = mTop - sTop;
casinoheight = $('.casino').height();
casinom = casino + casinoheight;
if (casino < 110 && casinom > 110){
	$('a[r="casino"]').find('h3').eq(0).css('color','#f00');
}else{
	$('a[r="casino"]').find('h3').eq(0).css('color','#fff');
}


var sTop = $(window).scrollTop();
var mTop = $('.sports')[0].offsetTop;
var sports = mTop - sTop;
sportsheight = $('.sports').height();
sportsm = sports + sportsheight;
if (sports < 110 && sportsm > 110){
	$('a[r="sports"]').find('h3').eq(0).css('color','#f00');
}else{
	$('a[r="sports"]').find('h3').eq(0).css('color','#fff');
}


var sTop = $(window).scrollTop();
var mTop = $('.slots')[0].offsetTop;
var slots = mTop - sTop;
slotsheight = $('.slots').height();
slotsm = slots + slotsheight;
if (slots < 110 && slotsm > 110){
	$('a[r="slots"]').find('h3').eq(0).css('color','#f00');
}else{
	$('a[r="slots"]').find('h3').eq(0).css('color','#fff');
}

var sTop = $(window).scrollTop();
var mTop = $('.mg')[0].offsetTop;
var mg = mTop - sTop;
mgheight = $('.mg').height();
mgm = mg + mgheight;
if (mg < 110 && mgm > 110){
	$('a[r="mg"]').find('h3').eq(0).css('color','#f00');
}else{
	$('a[r="mg"]').find('h3').eq(0).css('color','#fff');
}

var sTop = $(window).scrollTop();
var mTop = $('.pt')[0].offsetTop;
var pt = mTop - sTop;
ptheight = $('.pt').height();
ptm = pt + ptheight;
if (pt < 110 && ptm > 110){
	$('a[r="pt"]').find('h3').eq(0).css('color','#f00');
}else{
	$('a[r="pt"]').find('h3').eq(0).css('color','#fff');
}

var sTop = $(window).scrollTop();
var mTop = $('.qt')[0].offsetTop;
var qt = mTop - sTop;
qtheight = $('.qt').height();
qtm = qt + qtheight;
if (qt < 110 && qtm > 110){
	$('a[r="qt"]').find('h3').eq(0).css('color','#f00');
}else{
	$('a[r="qt"]').find('h3').eq(0).css('color','#fff');
}


// var sTop = $(window).scrollTop();
// var mTop = $('.fishing')[0].offsetTop;
// var fishing = mTop - sTop;
// fishingheight = $('.fishing').height();
// fishingm = fishing + fishingheight;
// if (fishing < 110 && fishingm > 110){
// 	$('a[r="fishing"]').find('h3').eq(0).css('color','#f00');
// }else{
// 	$('a[r="fishing"]').find('h3').eq(0).css('color','#fff');
// }

var sTop = $(window).scrollTop();
var mTop = $('.activity')[0].offsetTop;
var activity = mTop - sTop;
activityheight = $('.activity').height();
activitym = activity + activityheight;
if (activity < 110 && activitym > 110){
	$('a[r="activity"]').find('h3').eq(0).css('color','#f00');
}else{
	$('a[r="activity"]').find('h3').eq(0).css('color','#fff');
}

}
})




function reg(){
	$('.reg').css('display','block');
	height = window.innerHeight;
	thisheight = $('.reg>div').height();
	$('.reg>div').css('margin-top',(height - thisheight) / 2+'px')
}

function exit()
{
	$('.reg').css('display','none');
}

$('.exit').on('click',exit)


function app(){
	$('.app').css('display','block');
	height = window.innerHeight;
	thisheight = $('.app>div').height();
	$('.app>div').css('margin-top',(height - thisheight) / 2+'px')
}

