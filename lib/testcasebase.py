import base64
import email
import email.header
import imaplib
import unittest
import time
import settings
import os
import sys

from datetime import datetime
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
test = []

class Extensions(object):

    def create_account_number(self, ID):
        def create_number(account):
            account_number = []
            count = 0
            while count <= account:
                account_number.append(randint(1, 9))
                count += 1
            return account_number
        def multiply_by_eleven(amount_digits):
            global account_number
            account_number = create_number(amount_digits)
            multiplied_number = 0
            multiply = amount_digits + 1
            for num in account_number:
                multiplied_number += num * multiply
                multiply -= 1
            return multiplied_number
        def sum_eleven(amount_digits):
            multiplied_number = multiply_by_eleven(amount_digits)
            eleven_modulo_outcome = multiplied_number % 11
            return eleven_modulo_outcome
        def eleven_check(amount_digits, indicator= False):
            while indicator == False:
                eleven_modulo_outcome = sum_eleven(amount_digits)
                if eleven_modulo_outcome == 0:
                    return account_number
                    break
        if ID == "rijbewijs":
            amount_digits = 9
            eleven_check(amount_digits)
            return ''.join(str(x) for x in account_number)
        elif ID == 'bankaccount':
            amount_digits = 8
            eleven_check(amount_digits)
            return ''.join(str(x) for x in account_number)

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

class Tele2Test(Extensions, unittest.TestCase):

    def cookiebar_accept(self):
        self.driver.switch_to_frame(self.driver.find_element_by_css_selector("#qb_cookie_consent_main"))       
        self.driver.find_element_by_css_selector('#buttonAccept').click()
        self.driver.switch_to_default_content()

    def dropdownselector(self, profile, part, selector, entry, entry_type):
        self.elementcheck(part, selector, click=True)
        self.elementcheck(entry, settings.PROFILES[profile][entry_type], click=True)

    def dropdownselector_select(self, profile, part, selector, entry):
        select = Select(self.driver.find_element_by_css_selector(settings.UI[part][selector]))
        select.select_by_value(settings.PROFILES[profile][entry])

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
                self.fail("Expected to find mandatory error on %s field but did not find it." % selector)
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
                self.fail("Expected to find mandatory popup on %s field but did not find it." % selector)
        if ('text_popup' in settings.ERROR[part][selector]):
            element = self.driver.find_element_by_css_selector(settings.ERROR[part][selector]['popup'])
            if element.text != (settings.ERROR[part][selector]['text_popup']):
                self.get_screenshot(part, selector)
                self.fail("Expected to find text popup on %s field but did not find it." % selector)
            else:
                pass

    def field_validation(self, part, selector, next_selector, entry, entry_type, error):
        for key in entry[entry_type].split(','):
            self.elementcheck(part, selector, keys=key)
            self.elementcheck(part, next_selector, click=True)
            self.errorcheck(part, error)
            self.driver.find_element_by_css_selector(settings.UI[part][selector]).clear()

    def get_screenshot(self, part, selector):
        global test
        testcase = unittest.TestCase.id(self)
        testcase = testcase.split('.')[2]
        newpath = 'H:\output\%s' % test[0]
        if not os.path.exists(newpath):
           os.mkdir('H:\output\%s' % test[0])
        newpath = 'H:\output\%s\%s' % (test[0], test[1])
        if not os.path.exists(newpath):
           os.mkdir('H:\output\%s\%s' % (test[0], test[1]))
        newpath = 'H:\output\%s\%s\%s' % (test[0], test[1], testcase)
        if not os.path.exists(newpath):
            os.mkdir('H:\output\%s\%s\%s' % (test[0], test[1], testcase))
        self.driver.get_screenshot_as_file('H:\output\%s\%s\%s\%s %s.png' % (test[0], test[1], testcase, part, selector))
        
    def go_to_configpage(self, workflow, profile='default'):
        self.cookiebar_accept()
        if len(sys.argv) > 2:
            if sys.argv[2].lower() == 'uat':
                if workflow == 'sim_only':
                    self.driver.get('http://espresso-3g-uat.tele2.nl:11111/shop/mobiel/abonnement/sim-only')
                    self.cookiebar_accept()
                elif workflow == 'handset':
                    self.driver.get('http://espresso-3g-uat.tele2.nl:11111/shop')
                    self.cookiebar_accept()
                    self.hover('overview_page', 'uat_handset')
                    self.elementcheck('overview_page', 'uat_hover_handset', click=True)
                else:
                    self.get_screenshot('configure_page', workflow)
                    # if no selector is found, spit out an error
                    self.fail('er gaat iets mis met de workflow selectie op UAT')
        else:
            self.hover('menu', 'link_mobiel')
            if workflow == 'sim_only':
                self.elementcheck('menu', 'link_sim_only',click=True)
            elif workflow == 'handset':
                self.elementcheck('menu', 'link_handset',click=True)
                handset = '.phones_wrapper.abonnement > article:nth-child(%s)' % randint(1, 9)
                self.hover_article(handset)
                handset = '%s %s' % (handset, 'a.preview-img-link')
                self.driver.find_element_by_css_selector(handset).click()
            elif workflow == 'simonly_prepaid':
                self.elementcheck('menu', 'link_prepaid',click=True)
                self.elementcheck('overview_page', 'prepaid_simonly', click=True)
            elif workflow == 'handset_prepaid':
                self.elementcheck('menu', 'link_prepaid',click=True)
                self.elementcheck('overview_page', 'prepaid_handset', click=True)
                handset = '.phones_wrapper.prepaid > article:nth-child(%s)' % randint(1, 9)
                self.hover_article(handset)
                handset = '%s %s' % (handset, 'a.preview-img-link')
                self.driver.find_element_by_css_selector(handset).click()
            else:
                self.get_screenshot('configure_page', workflow)
                # if no selector is found, spit out an error
                self.fail('er gaat iets mis met de workflow selectie')

    def go_to_step1(self, workflow, profile='default'):
        self.go_to_configpage(workflow, profile)
        #   workaround a-b testing
        if workflow == 'sim_only' or workflow == 'handset':
            try:
                self.driver.find_element_by_css_selector(settings.UI['configure_page']['button_order'])
            except NoSuchElementException:
                self.elementcheck('homepage', 'button_banner', click=True)
            #   select internet bundle
            self.dropdownselector(profile, 'configure_page', 'select_internetbundle', 'bundles', 'internetbundle')
            self.dropdownselector(profile, 'configure_page', 'select_belbundle', 'bundles', 'belbundle')
            self.get_screenshot('configure_page', 'succes')
            self.elementcheck('configure_page', 'button_order',click=True)
        elif workflow == 'simonly_prepaid' or workflow == 'handset_prepaid':
            self.get_screenshot('configure_page', 'succes')
            self.elementcheck('prepaid', 'button_order', click=True)            

    def go_to_step2(self, workflow, profile='default'):
        self.go_to_step1(workflow, profile)
        self.dropdownselector(profile, 'step_1', 'select_gender', 'gender', 'gender')
        self.elementcheck('step_1', 'input_firstname',keys=settings.PROFILES[profile]['firstname'])
        self.elementcheck('step_1', 'input_lastname',keys=settings.PROFILES[profile]['lastname'])
        self.elementcheck('step_1', 'input_initials',keys=settings.PROFILES[profile]['initials'])
        if workflow == 'sim_only' or workflow == 'handset':
            self.dropdownselector(profile, 'step_1', 'select_day', 'day', 'day')
            self.dropdownselector(profile, 'step_1', 'select_month', 'month', 'month')
            self.dropdownselector(profile, 'step_1', 'select_year', 'year', 'year')
        self.elementcheck('step_1', 'input_postcode',keys=settings.PROFILES[profile]['postcode'])
        self.elementcheck('step_1', 'input_housenumber',keys=settings.PROFILES[profile]['housenumber'])
        self.elementcheck('step_1', 'input_phonenumber',keys=settings.PROFILES[profile]['phonenumber'])
        self.elementcheck('step_1', 'input_e-mail',keys=settings.PROFILES[profile]['email'])
        self.elementcheck('step_1', 'input_repeat_email',keys=settings.PROFILES[profile]['repeat_email'])
        count = 0
        while not (self.driver.find_element_by_css_selector('#street').get_attribute("value") == settings.PROFILES[profile]['streetname']) :
            if count >= 50:
                self.get_screenshot('step_1', 'input_street')
                # if no selector is found, spit out an error
                self.fail('finding the adress took longer then 5 seconds')
            else:
                time.sleep(0.1)
                count += 1
        self.get_screenshot('step_1', 'succes')
        self.elementcheck('step_1', 'button_next_step', click=True)

    def go_to_step3(self, workflow, profile='default'):
        self.go_to_step2(workflow, profile)
        self.elementcheck('step_2', 'input_IBANnumber',keys=settings.PROFILES[profile]['IBAN_number'])
        self.dropdownselector(profile, 'step_2', 'select_document_type', 'document_type', 'document_type')              
        self.elementcheck('step_2', 'input_documentnumber',keys=settings.PROFILES[profile]['document_number'])
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        if settings.PROFILES[profile]['porting'] == 'ja':
            self.elementcheck('step_2', 'input_phonenumber',keys=settings.PROFILES[profile]['current_phonenumber'])
            self.dropdownselector(profile, 'step_2', 'select_current_subscription', 'current_subscription', 'current_subscriber')
            self.dropdownselector(profile, 'step_2', 'select_mobile_provider', 'mobile_provider', 'current_provider')
            self.elementcheck('step_2', 'input_simcard_number',keys=settings.PROFILES[profile]['current_simcardnumber'])
            self.elementcheck('step_2', 'select_date', click=True)
            self.elementcheck('step_2', 'select_day', click=True)
        self.dropdownselector(profile, 'step_2', 'select_services', 'services', 'services')              
        self.get_screenshot('step_2', 'succes')
        self.elementcheck('step_2', 'button_next_step', click=True)

    def go_to_step4(self, workflow, profile='default'):
        self.go_to_step3(workflow, profile)
        if (settings.PROFILES[profile]['delivery']):
            try:
                self.driver.find_element_by_css_selector('.request-delivery').click()
            except NoSuchElementException:
                pass
        if (settings.PROFILES[profile]['click_collect']):
            self.elementcheck('step_3', 'ratio_click_collect', click=settings.PROFILES[profile]['click_collect'])
            count = 0
            clickandcollect = self.driver.find_element_by_css_selector('.dixons-point-content')
            while not (clickandcollect.text.split()[0] == 'dixons') :
                if count >= 50:
                    if clickandcollect == 'Er':
                        self.get_screenshot('step_3', 'no dixons found')
                        # if no selector is found, spit out an error
                        self.fail('no dixons is found')
                    else:
                        self.get_screenshot('step_3', 'timeout')
                        # if no selector is found, spit out an error
                        self.fail('dixons gives timeout')
                else:
                    time.sleep(0.1)
                    clickandcollect = self.driver.find_element_by_css_selector('.shop-name')
                    count += 1
        self.elementcheck('step_3', 'terms', click=True)
        self.elementcheck('step_3', 'directdebid', click=True)
        self.get_screenshot('step_3', 'succes')
        self.elementcheck('step_3', 'button_next_step', click=True)

    def go_to_step3_prepaid(self, workflow, profile='default'):
        self.go_to_step2(workflow, profile)
        self.elementcheck('step_3', 'terms', click=True)
        self.elementcheck('step_3', 'button_next_step', click=True)

    def hover_article(self, selector):
        add = self.driver.find_element_by_css_selector(selector)
        Hover = ActionChains(self.driver).move_to_element(add)
        Hover.perform()

    def hover (self, part, selector):
        locator = settings.UI[part][selector]
        add = self.driver.find_element_by_css_selector(locator)
        Hover = ActionChains(self.driver).move_to_element(add)
        Hover.perform()

    def setUp(self):
        fp = webdriver.FirefoxProfile()
        fp.add_extension('C:\\Users\\j-rijnaars\\Documents\\python\\mobile\\addons\\Firebug.xpi')
        fp.add_extension('C:\\Users\\j-rijnaars\\Documents\\python\\mobile\\addons\\Firefinder.xpi')
        #   load up the remote driver and tell it to use Firefox
        self.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX,
            browser_profile=fp)
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1250,1000)
 
        #   navigate to URL and log in as developer (since the script creates a new instance with clean cache)
        self.driver.get('https://www.tele2.nl/')

    def tearDown(self):
        #   close the browser
        self.driver.close()

    def textcheck(self, workflow, profile='default'):
        current_text_1 = self.driver.find_element_by_css_selector('li.odd:nth-child(1) > p:nth-child(2)')
        text_1 = self.driver.find_element_by_css_selector(settings.TEXT[profile]['text_1'])
        print str(current_text_1.text)
        self.assertEqual(current_text_1.text, text_1)