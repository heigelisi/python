$('.nav li').hover(function(){
	$(this).css('background','#000');
	$(this).find('a').css('color','#FFD100');
},function(){
	$(this).css('background','#FFD100');
	$(this).find('a').css('color','#000');
})