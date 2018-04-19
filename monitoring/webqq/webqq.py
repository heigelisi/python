from selenium import webdriver
from selenium.webdriver.common.by import By #
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import time
import threading
import os
import json
import sys
import tkinter
from PIL import Image as MyImages, ImageTk
import re
import tkinter
import wmi
import requests
import pyquery
from multiprocessing import Process
import random
import queue


class WebQq(object):


	def login(self):
		browser = webdriver.Chrome()#声明一个浏览器对象

		browser.get('http://web2.qq.com/')
		