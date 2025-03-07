from django.test import TestCase
from django.urls import reverse 

import unittest 
from selenium import webdriver 
from selenium.webdriver.common by import By 

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    
    def tearDown(self):
        self.browser.close()

    def test_login(self):
        self.browser.get('http://127.0.0.1:8080/accounts/login/')

        name_element = self.browser.find_element(By.ID, "id_username")
        name_element.send_keys("TestUser")
        self.assertEqual(name_element.get_attribute("value"), "TestUser")
    
    def test_register(self):
        self.browser.get('http://127.0.0.1:8080/accounts/signup/')
        username_element = self.browser.find_element(By.ID, "id_username")
        username_element.send_keys("NewAccount")
        self.assertEqual(username_element.get_attribute("value"), "NewAccount")
    
    def test_forgot_password(self):
        self.browser.get('http://127.0.0.1:8080/accounts/password_reset/')
        email_element = self.browser.find_element(By.ID, "id_email")
        email_element.send_keys("newuser@hotmail.com")
        self.assertEqual(email_element.get_attribute("value"), "newuser@hotmail.com")

if __name__ == "__main__":
    unittest.main()
