# -*- coding: utf-8 -*-
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging

logging.basicConfig(
    level=logging.INFO,  # 设置日志级别，INFO及以上级别都会被记录
    format="%(asctime)s - %(levelname)s - %(message)s",  # 定义日志格式
    datefmt="%Y-%m-%d %H:%M:%S",  # 定义时间格式
)

if len(sys.argv) == 3:
    user = sys.argv[1]
    password = sys.argv[2]
else:
    quit("Usage: python autologin.py <account> <password>")

prefs = {"intl.accept_languages": "zh-CN,zh"}

options = Options()
options.add_argument("--headless")  # 启用无头模式
options.add_argument("--no-sandbox")  # 必须：绕过操作系统安全模型
options.add_argument("--disable-dev-shm-usage")  # 必须：防止/dev/shm空间不足导致的崩溃
options.add_argument("--disable-gpu")  # 禁用GPU加速（部分系统需添加）
options.add_argument("--window-size=1920,1080")  # 设置分辨率（避免元素定位问题）
options.add_experimental_option(
    "excludeSwitches", ["enable-automation"]
)  # 隐藏自动化标识
options.add_experimental_option("prefs", prefs)
options.add_argument(
    "--disable-blink-features=AutomationControlled"
)  # 禁用Blink自动化控制

logging.info("脚本启动，正在初始化WebDriver...")
try:
    driver = webdriver.Remote(
        command_executor="http://localhost:8888/wd/hub", options=options
    )
except Exception as e:
    logging.info(f"❌ 连接 WebDriver 失败，请确认 Docker 容器是否正常运行。错误: {e}")
    exit()

try:
    driver.get("https://login.bjtu.edu.cn/")
    waitDriver = WebDriverWait(driver, 10)
    logging.info("正在访问登录页面...")

    if driver.title == "上网登录页":
        logging.info("需要登录")
        form = waitDriver.until(EC.visibility_of_element_located((By.NAME, "f1")))
        waitForm = WebDriverWait(form, 10)

        account = waitForm.until(EC.visibility_of_element_located((By.NAME, "DDDDD")))
        account.send_keys(user)

        passbox = waitForm.until(EC.visibility_of_element_located((By.NAME, "upass")))
        passbox.send_keys(password)

        button = waitForm.until(EC.element_to_be_clickable((By.NAME, "0MKKey")))
        button.click()
        logging.info("登录信息已提交，等待跳转...")
    elif driver.title == "注销页":
        logging.info("已处于登录状态")
    else:
        logging.info("未知状态，当前页面标题: " + driver.title)


except Exception as e:
    logging.info(f"执行过程中发生错误: {e}")
finally:
    logging.info("脚本执行完毕，关闭 WebDriver")
    driver.quit()
