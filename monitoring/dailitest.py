import requests


headers = {
'Cookie': 'ssuid=6837657814; SUV=00403EB33B26625256B8780974D6D975; usid=FNXmIWHPRGne0XWq; SUID=C9E88C3D1E20910A000000005A250D1A; pgv_pvi=216893440; CXID=7CCF69C14BEE9740E4CEB77B07737B68; ad=eZllllllll2zzmGSlllllV$$3jYllllltU23jyllll9lllllRCxlw@@@@@@@@@@@; SNUID=FE10B1D0A5A1C32725E66EDAA5C188DA; wuid=AAFHvJHkHgAAAAqRCGWVHQAAkwA=; FREQUENCY=1521189376881_1; ld=nyllllllll2z$c4@lllllV$rkKDlllllNxYfDlllll9lllll9llll5@@@@@@@@@@; ABTEST=0|1521310607|v1; IPLOC=CN4401; weixinIndexVisited=1; sct=3; JSESSIONID=aaas2GUzmgjDj4CVyzOiw; ppinf=5|1521310696|1522520296|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlOTElQTglRTklQTMlOUV8Y3J0OjEwOjE1MjEzMTA2OTZ8cmVmbmljazoxODolRTUlOTElQTglRTklQTMlOUV8dXNlcmlkOjQ0Om85dDJsdUtDVXNLS3hBMmFzVVNiTW1xamFoSzRAd2VpeGluLnNvaHUuY29tfA; pprdig=pL0EUW2oFcbPLon4Ih5sYTRrF2XJiiTGSHgbmiWVzRe0798o_XwM_6E4JlwShMu_WxZKtAUnJ3GXAm4beMZIoYECcVtI6kxq6JipG3am3z35uapwHVHnrVdzVxbQ3WZ-cyhHqJE2t00ZqG7nDLpK1lY6VQPPA9VaDmA4BINZJdc; sgid=12-34131385-AVqtWibgIQ5GqcJ7ianhuQIIE; ppmdig=1521310696000000cc8ca0b617511b83e34a3ef18b4cadd1',
'Host': 'weixin.sogou.com',
'Referer': 'http://weixin.sogou.com/weixin?query=%E7%BE%8E%E5%A5%B3&_sug_type_=&sut=4199&lkt=4%2C1521310654126%2C1521310658310&s_from=input&_sug_=y&type=2&sst0=1521310658413&page=18&ie=utf8&w=01019900&dr=1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.23 Safari/537.36'
}
proxies = {
	"http":"http://14.29.47.90:3128"
}

for i in range(1,100):

	try:
		html = requests.get(,allow_redirects=False,headers=headers,proxies=proxies,timeout=10)
		print(html.status_code)
	except Exception as e:


		print(e)

