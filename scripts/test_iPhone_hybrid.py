# -*- coding:utf-8 -*-
import os
import unittest

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class TestIosHybrid(unittest.TestCase):
    def setUp(self):
        # 步骤一：打开包含 webview 的 app
        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '8.3'
        desired_caps['deviceName'] = 'iPhone 6'
        desired_caps['app'] = PATH(
            '../app/iOSHybrid/build/Release-iphonesimulator/webViewDemo.app'
        )
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()

    def test_search(self):
        # 步骤二：输入要打开的 url （http://m.dianping.com/hangzhou） ，点击 submit 按钮打开
        self.driver.find_element_by_name("urlText").clear()
        self.driver.find_element_by_name("urlText").send_keys("http://m.dianping.com/hangzhou")
        self.driver.find_element_by_name('submit').click()
        # 隐藏软键盘（纯粹为了更好地看到效果）
        self.driver.hide_keyboard()

        # 步骤三：切换到 webview ，然后输入 '餐饮' 到搜索框
        self.driver.switch_to.context(self.driver.contexts[-1])
        try:
            self.driver.find_element_by_xpath("//a[text()='继续访问触屏版']").click()
            # 点击后页面会刷新，所以等待一会儿
            sleep(2)
        except NoSuchElementException:
            # 如果没找到 “继续访问触屏版” 按钮，直接忽略
            pass
        self.driver.find_element_by_xpath("//header/div[@class='search J_search']").click()
        self.driver.find_element_by_xpath("//div[@class='head_cnt_input']/input[@name='keyword']").send_keys(u"餐饮")

        # 步骤四：点击搜索按钮
        self.driver.find_element_by_xpath("//div[@class='head_cnt_input']/input[@type='submit']").click()

        # 步骤五：到达搜索结果页面，检查是否存在 '锅小二'
        sleep(5)
        is_displayed = self.driver.find_element_by_xpath("//h3[@class='shopname' and contains(text(),'锅小二')]")\
            .is_displayed()
        self.assertTrue(is_displayed, msg="搜索结果中没找到'锅小二'")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIosHybrid)
    unittest.TextTestRunner(verbosity=2).run(suite)
