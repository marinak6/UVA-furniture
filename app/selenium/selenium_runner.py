from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


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

    def test_home_page(self):
        self.home_page = "http://web:8000"
        self.driver.get(self.home_page)
        time.sleep(10)
        assert "UVA Furniture" in self.driver.title
        # elem = self.driver.find_element_by_name("q")
        self.assertIn("UVA Furniture", self.driver.title)


if __name__ == "__main__":
    unittest.main()
