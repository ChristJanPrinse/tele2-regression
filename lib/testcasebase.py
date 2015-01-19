import base64
import email
import email.header
import imaplib
import unittest
import time
import settings
import os

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Tele2Test(unittest.TestCase):

    def cookiebar_accept(self):
        self.driver.switch_to_frame(self.driver.find_element_by_css_selector("#qb_cookie_consent_main"))       
        self.driver.find_element_by_css_selector('#buttonAccept').click()
        self.driver.switch_to_default_content()

    def dropdownselector(self, part, selector, entry, entry_type):
        self.elementcheck(part, selector, click=True)
        self.elementcheck(entry, entry_type, click=True)

    def dropdownselector_workflow(self, profile, part, selector, entry, entry_type):
        self.elementcheck(part, selector, click=True)
        self.elementcheck(entry, settings.PROFILES[profile][entry_type], click=True)

    def elementcheck(self, part, selector, keys='', click=False):
        if keys:
            try:
                # check for the presence of the selector
                self.driver.find_element_by_css_selector(settings.UI[part][selector]).send_keys(keys)
            except NoSuchElementException:
                self.get_screenshot(part, selector)
                # if no selector is found, spit out an error
                self.fail("Tried to send %s into element %s but did not find it." % (keys, selector))
        elif click:
            try:
                # check for the presence of the selector
                self.driver.find_element_by_css_selector(settings.UI[part][selector]).click()
            except NoSuchElementException:
                self.get_screenshot(part, selector)
                # if no selector is found, spit out an error
                self.fail("Tried to click element %s but did not find it." % selector)
        else:
            try:
                # check for the presence of the selector
                self.driver.find_element_by_css_selector(settings.UI[part][selector])
            except NoSuchElementException:
                self.get_screenshot(part, selector)
                # if no selector is found, spit out an error
                self.fail("Expected to find element %s but did not find it." % selector)

    def errorcheck(self, part, selector):
        if ('mandatory' in settings.ERROR[part][selector]):
            count = 1
            while count > 0:
                try:
                    # check for the presence of the selector
                    self.driver.find_element_by_css_selector(settings.ERROR[part][selector]['mandatory'])
                    break
                except:
                    time.sleep(0.5)
                    count -= 0.5
            else:
                self.get_screenshot(part, selector)
                # if no selector is found, spit out an error
                self.fail("Expected to find mandatory error on  %s field but did not find it." % selector)
        if ('popup' in settings.ERROR[part][selector]):
            count = 1
            while count > 0:
                try:
                    # check for the presence of the selector
                    self.driver.find_element_by_css_selector(settings.ERROR[part][selector]['popup'])
                    break
                except:
                    time.sleep(0.5)
                    count -= 0.5
            else:
                self.get_screenshot(part, selector)
                # if no selector is found, spit out an error
                self.fail("Expected to find mandatory popup on  %s field but did not find it." % selector)
        if ('text_popup' in settings.ERROR[part][selector]):
            element = self.driver.find_element_by_css_selector(settings.ERROR[part][selector]['popup'])
            if element.text != (settings.ERROR[part][selector]['text_popup']):
                self.get_screenshot(part, selector)
                self.fail("Expected to find text popup on  %s field but did not find it." % selector)
            else:
                pass

    def field_validation(self, part, selector, next_selector, entry, entry_type, error):
        for key in entry[entry_type].split(','):
            self.elementcheck(part, selector, keys=key)
            self.elementcheck(part, next_selector, click=True)
            self.errorcheck(part, error)
            self.driver.find_element_by_css_selector(settings.UI[part][selector]).clear()

    def get_screenshot(self, part, selector):
        testcase = unittest.TestCase.id(self)
        testcase = testcase.split('.')[2]
        now = datetime.now()
        date = '%s-%s-%s' % (now.month, now.day, now.year)
        time = '%s;%s;%s' % (now.hour, now.minute, now.second)
        newpath = 'C:\Users\j-rijnaars\Documents\screenshots\%s' % date
        if not os.path.exists(newpath):
           os.mkdir('C:\Users\j-rijnaars\Documents\screenshots\%s' % date)
        newpath = 'C:\Users\j-rijnaars\Documents\screenshots\%s\%s' % (date, testcase)
        if not os.path.exists(newpath):
            os.mkdir('C:\Users\j-rijnaars\Documents\screenshots\%s\%s' % (date, testcase))
        self.driver.get_screenshot_as_file('C:\Users\j-rijnaars\Documents\screenshots\%s\%s\%s %s time=%s.png' % (date, testcase, part, selector, time))

    def getactivationcode(email_account="automatedmailbox@gmail.com", email_password="Selenium123", email_folder="inbox"):
        def skipline(base, i=1):
            return '\n'.join(base.split('\n')[i:])
        M = imaplib.IMAP4_SSL('imap.gmail.com')
        rv, data = M.login(email_account, email_password)
        rv, mailboxes = M.list()
        rv, data = M.select(email_folder) 
        rv, data = M.search(None, "ALL")
        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')
            msg = email.message_from_string(data[0][1])
            for part in email.iterators.typed_subpart_iterator(msg, 'text', 'html'): 
                html = base64.b64decode(skipline(str(part), 4))
                html = html[html.index("activate=")+9:]
                return html[:html.index('\"')]
        M.close()
        M.logout()

    def go_to_sim_only_configpage(self):
        self.cookiebar_accept()
        self.hover('menu', 'link_mobiel')
        self.elementcheck('menu', 'link_sim_only',click=True)

    def go_to_sim_only_step1(self, profile='default'):
        self.go_to_sim_only_configpage()
        #   workaround a-b testing
        try:
            self.driver.find_element_by_css_selector(settings.UI['configure_page']['button_order'])
        except NoSuchElementException:
            self.elementcheck('homepage', 'button_banner', click=True)
        #   select internet bundle
        self.dropdownselector_workflow(profile, 'configure_page', 'select_internetbundle', 'bundles', 'internetbundle')
        #   self.driver.find_element_by_css_selector('.cart-container-title').click()
        self.dropdownselector_workflow(profile, 'configure_page', 'select_belbundle', 'bundles', 'belbundle')
        self.dropdownselector_workflow(profile, 'configure_page', 'select_simcard', 'simcard_type', 'simcard')
        self.elementcheck('configure_page', 'button_order',click=True)

    '''def go_to_sim_only_step1(self):
        self.go_to_sim_only_configpage()
        self.elementcheck('configure_page', 'button_order',click=True)'''

    def go_to_sim_only_step2(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'input_lastname',keys='test')
        self.elementcheck('step_1', 'input_initials',keys='t')
        self.dropdownselector('step_1', 'select_day', 'day', '1')
        self.dropdownselector('step_1', 'select_month', 'month', '1')
        self.dropdownselector('step_1', 'select_year', 'year', '1990')
        self.elementcheck('step_1', 'input_postcode',keys='5331XW')
        self.elementcheck('step_1', 'input_housenumber',keys='7')
        self.elementcheck('step_1', 'input_phonenumber',keys='0612345678')
        self.elementcheck('step_1', 'input_e-mail',keys='test@test.nl')
        self.elementcheck('step_1', 'input_repeat_email',keys='test@test.nl')
        time.sleep(5)
        self.elementcheck('step_1', 'button_next_step', click=True)

    def hover (self, part, selector):
        locator = settings.UI[part][selector]
        add = self.driver.find_element_by_css_selector(locator)
        Hover = ActionChains(self.driver).move_to_element(add)
        Hover.perform()

    def setUp(self):
        #   load up the remote driver and tell it to use Firefox
        self.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1250,1000)
 
        #   navigate to URL and log in as developer (since the script creates a new instance with clean cache)
        self.driver.get('https://www.tele2.nl/')

    def tearDown(self):
        #   close the browser
        self.driver.close()