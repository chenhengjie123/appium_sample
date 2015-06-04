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
        # 步骤一：打开大众点评android版本app
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'e4d42545'
        # desired_caps['udid'] = '750ACKS3LSE4'
        # desired_caps['automationName'] = 'Selendroid'
        desired_caps['unicodeKeyboard'] = 'true'
        desired_caps['resetKeyboard'] = 'true'
        desired_caps['app'] = PATH(
            '../app/Dianping_dianping-web_7.1.1.apk'
        )
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait("15")

    def tearDown(self):
        # end the session
        self.driver.quit()

    def test_search(self):
        # 步骤二：点击左上角的城市，选择杭州
        sleep(25)
        self.driver.find_element_by_xpath('//android.widget.TextView[@text="杭州"]').click()

        # 步骤三：点击搜索框，输入关键词：餐饮
        self.driver.find_element_by_id("com.dianping.v1:id/start_search").click()
        search_input = self.driver.find_element_by_id("com.dianping.v1:id/search_edit")
        search_input.get_attribute("content-desc")
        # search_input.clear()
        search_input.send_keys(u"餐饮")

        # 步骤四：点击搜索按钮
        self.driver.find_element_by_id("com.dianping.v1:id/notify").click()

        # 步骤五：到达搜索结果页面，查询到锅小二的餐饮店铺
        sleep(5)
        # TODO: refactor this to using scrollTo function
        list_view_id="android:id/list"
        element_class = "android.widget.TextView"
        element_text = "锅小二"

        list_view_locator = 'new UiScrollable(new UiSelector().resourceId("{}"))'.format(list_view_id)
        element_locator = 'new UiSelector().className("{}"), "{}"'.format(element_class, element_text)
        uiautomator_string = '{}.getChildByText({});'.format(list_view_locator, element_locator)
        self.driver.find_element_by_android_uiautomator(uiautomator_string)

        # 步骤六：判断搜索结果页面达到，正确
        # 下面的找元素
        try:
            self.driver.find_element_by_xpath('//android.widget.TextView[@text="锅小二"]')
        except NoSuchElementException, e:
            raise self.failureException("搜索结果中没找到'锅小二'")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSendKeys)
    unittest.TextTestRunner(verbosity=2).run(suite)
