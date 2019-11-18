from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.by import By


class TestSuite(unittest.TestCase):
    def setUp(self):
        connected = False
        while(not connected):
            try:
                self.driver = webdriver.Remote(
                    command_executor='http://selenium-chrome:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME)
                connected = True
            except:
                pass
        # time.sleep(10)
        # self.driver = webdriver.Remote(
        #     command_executor='http://selenium-chrome:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME)

    def test_home_page(self):
        self.home_page = "http://web:8000"
        self.driver.get(self.home_page)
        time.sleep(10)
        # elem = self.driver.find_element_by_name("q")
        self.assertIn("UVA Furniture", self.driver.title)
        assert "UVA Furniture" in self.driver.title

    def test_register(self):

        self.home_page = "http://web:8000"
        self.driver.get(self.home_page)
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[text() = 'Register']").click()
        time.sleep(5)
        # self.driver.find_element(
        #     By.XPATH, '//text()[contains(.,"Get started with UVA Furniture by creating an account!")]')

        # self.assertIsNotNone(element)
        self.driver.find_element_by_id(
            "id_first_name").send_keys("test_user_first")
        self.driver.find_element_by_id(
            "id_last_name").send_keys("test_user_last")
        self.driver.find_element_by_id("id_password").send_keys("password")
        self.driver.find_element_by_id("id_email").send_keys("test@test.com")
        self.driver.find_element_by_xpath("//*[@value='Submit']").click()
        time.sleep(5)
        # element = self.driver.find_element_by_class_name("wv-heading--title")
        # self.assertIsNotNone(element)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
    tester = TestSuite()
    tester.setUp()
    tester.test_home_page()
    tester.test_register()