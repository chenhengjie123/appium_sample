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


class TestIphoneNative(unittest.TestCase):
    def setUp(self):
        # 步骤一：打开 ToDoList 应用
        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '8.3'
        desired_caps['deviceName'] = 'iPhone 5s'
        desired_caps['app'] = PATH(
            '../app/iOSNative/build/Release-iphonesimulator/ToDoList.app'
        )
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()

    def test_add_item(self):
        # 步骤二：点击右上角的 + 号
        self.driver.find_element_by_name('Add').click()

        # 步骤三：点击输入框，输入内容：学习 appium
        source =  self.driver.page_source
        to_do_item_input = self.driver.\
            find_element_by_name("item")
        to_do_item_input.clear()
        to_do_item_input.send_keys(u'学习2 appium')

        # 步骤四：点击确认按钮
        self.driver.find_element_by_name("Done").click()

        # 步骤五：回到列表页，检查待办事项是否添加成功
        sleep(5)
        try:
            self.driver.find_element_by_xpath("//UIAStaticText[@label='学习 appium']")
        except NoSuchElementException:
            self.driver.get_screenshot_as_file("test_add_item_fail.png")
            raise AssertionError("待办事项 '学习 appium' 添加不成功")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIphoneNative)
    unittest.TextTestRunner(verbosity=2).run(suite)
