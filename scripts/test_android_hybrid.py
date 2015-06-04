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


class TestSendKeys(unittest.TestCase):
    def setUp(self):
        # 步骤一：打开包含 webview 的 app
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'e4d42545'
        desired_caps['unicodeKeyboard'] = 'true'
        desired_caps['resetKeyboard'] = 'true'
        desired_caps['app'] = PATH(
            '../app/androidHybrid/app/build/outputs/apk/app-debug-unaligned.apk'
        )
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()

    def test_search(self):
        # 步骤二：输入要打开的 url （http://m.dianping.com/guangzhou） ，点击 open web view 按钮打开
        self.driver.find_element_by_id('com.chjvps.hengjiechen.chjapp:id/editText').clear()
        self.driver.find_element_by_id('com.chjvps.hengjiechen.chjapp:id/editText')\
            .send_keys("http://m.dianping.com/hangzhou")
        self.driver.find_element_by_id('com.chjvps.hengjiechen.chjapp:id/web_view_btn').get_attribute("name")
        self.driver.find_element_by_id('com.chjvps.hengjiechen.chjapp:id/web_view_btn').click()

        # 步骤三：切换到 webview ，然后输入 '餐饮' 到搜索框
        print self.driver.contexts
        self.driver.switch_to.context(self.driver.contexts[-1])

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
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSendKeys)
    unittest.TextTestRunner(verbosity=2).run(suite)
