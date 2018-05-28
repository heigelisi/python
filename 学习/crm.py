from selenium import webdriver
from selenium.webdriver.common.by import By #
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import time
import threading


browser = webdriver.Chrome()#声明一个浏览器对象
browser.get('https://mail.qq.com/')

#点击账号登陆按钮
wait = WebDriverWait(browser,20)
browser.switch_to.frame('login_frame')#切换到一个iframe页面
switch_btn = browser.find_element(By.CSS_SELECTOR,'#switcher_plogin')
switch_btn.click()

#输入用户名密码
user = '869688800'
password = 'zhoufei789056Yun'
password2 = 'yuan3558564'
u = browser.find_element(By.CSS_SELECTOR,'#u')
u.send_keys(user)
p = browser.find_element(By.CSS_SELECTOR,'#p')
p.send_keys(password)
#点击登陆
login_button = browser.find_element(By.CSS_SELECTOR,'#login_button')
login_button.click()
# browser.switch_to.default_content()
print(browser.current_url)
time.sleep(3)
#是否有独立密码
try:
	pp = browser.find_element(By.CSS_SELECTOR,'#pp')
	pp.send_keys(password2)
	#点击登陆
	login_button = browser.find_element(By.CSS_SELECTOR,'#btlogin')
	login_button.click()
except Exception as e:
	print(e)
	pass




time.sleep(100)
browser.quit()
