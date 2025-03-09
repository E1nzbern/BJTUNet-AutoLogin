import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if len(sys.argv) == 3:
    user = sys.argv[1]
    password = sys.argv[2]
else:
    quit("Usage: python autologin.py <account> <password>")

options = Options()
options.add_argument("--headless")  # 启用无头模式
options.add_argument("--disable-gpu")  # 禁用GPU加速（部分系统需添加）
options.add_argument("--window-size=1920,1080")  # 设置分辨率（避免元素定位问题）
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 隐藏自动化标识
options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用Blink自动化控制

driver = webdriver.Chrome(options=options)
driver.get("https://login.bjtu.edu.cn/")
waitDriver = WebDriverWait(driver, 10)

if driver.title == "上网登录页":
    form = waitDriver.until(
        EC.visibility_of_element_located((By.NAME, "f1"))
    )
    waitForm = WebDriverWait(form, 10)

    account = waitForm.until(
        EC.visibility_of_element_located((By.NAME, "DDDDD"))
    )
    account.send_keys(user)

    passbox = waitForm.until(
        EC.visibility_of_element_located((By.NAME, "upass"))
    )
    passbox.send_keys(password)

    button = waitForm.until(
        EC.element_to_be_clickable((By.NAME, "0MKKey"))
    )
    button.click()

driver.quit()