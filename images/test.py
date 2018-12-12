from PIL import Image,ImageDraw

def zoom(filepath,width,height):
	#图片缩放
	from PIL import Image
	newImg = Image.new('RGBA',(width,height),(255,255,255))#创建一个新图片
	img = Image.open(filepath)#要缩放的图片
	w,h = img.size#获取原大小
	#w/h谁大按照谁缩放，目标大小width/height除以要缩放的图片w/h得出要缩放的比率
	if w > h:
		x = width / w
	else:
		x = height / h
	#按照x比率计算缩放大小
	ww = int(w*x)
	hh = int(h*x)
	img2 = img.resize((ww,hh),Image.ANTIALIAS)#缩放
	left = int((width - ww) / 2)#得出粘贴位置的left
	top = int((height - hh) / 2)#得出粘贴位置的top
	newImg.paste(img2,(left,top))#合并图片
	newImg.save('4.png','png')#保存图片

# zoom('1.jpg',800,800)

def circular(filepath):
	"""图片转换层圆形"""
	ima = Image.open(filepath).convert("RGBA")#打开要处理的图片
	# 获取最小半径
	size = ima.size
	r2 = min(size[0], size[1])
	#如果不是正方向 转换成正方形
	if size[0] != size[1]:
		ima = ima.resize((r2, r2), Image.ANTIALIAS)

	#创建透明图
	circle = Image.new('L', (r2, r2), 0)
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, r2, r2), fill=255)
	alpha = Image.new('L', (r2, r2), 255)
	alpha.paste(circle, (0, 0))
	ima.putalpha(alpha)#给图片添加透明度
	ima.save('test_circle.png')



circular('1.jpg')
