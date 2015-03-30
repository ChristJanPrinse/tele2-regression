import unittest
import os

import datetime
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select

import settings

test = []


# noinspection PyDeprecation
class Tele2Test(unittest.TestCase):
    _multiprocess_can_split_ = True

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

    # noinspection PyRedundantParentheses
    def errorcheck(self, part, selector):
        if ('mandatory' in settings.ERROR[part][selector]):
            count = 1
            while count > 0:
                try:
                    # check for the presence of the selector
                    self.driver.find_element_by_css_selector(settings.ERROR[part][selector]['mandatory'])
                    break
                except NoSuchElementException:
                    datetime.time.sleep(0.5)
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
                except NoSuchElementException:
                    datetime.time.sleep(0.5)
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
        testcase = unittest.TestCase.id(self)
        testcase = testcase.split('.')[2]
        current = datetime.datetime.now()
        date = '%s-%s-%s' % (current.month, current.day, current.year)
        time = '%s;%s;%s' % (current.hour, current.minute, current.second)
        newpath = 'C:\Users\j-rijnaars\Documents\screenshots\%s' % date
        if not os.path.exists(newpath):
            os.mkdir('C:\Users\j-rijnaars\Documents\screenshots\%s' % date)
        newpath = 'C:\Users\j-rijnaars\Documents\screenshots\%s\%s' % (date, testcase)
        if not os.path.exists(newpath):
            os.mkdir('C:\Users\j-rijnaars\Documents\screenshots\%s\%s' % (date, testcase))
        self.driver.get_screenshot_as_file('C:\Users\j-rijnaars\Documents\screenshots\%s\%s\%s %s time=%s.png' % (
            date, testcase, part, selector, time))

    def go_to_configpage(self, workflow):
        self.cookiebar_accept()
        self.hover('menu', 'link_mobiel')
        if workflow == 'sim_only':
            self.elementcheck('menu', 'link_sim_only', click=True)
        elif workflow == 'handset':
            self.elementcheck('menu', 'link_handset', click=True)
            handset = '.phones_wrapper.abonnement > article:nth-child(%s)' % randint(1, 9)
            self.hover_article(handset)
            handset = '%s %s' % (handset, 'a.preview-img-link')
            self.driver.find_element_by_css_selector(handset).click()
        elif workflow == 'simonly_prepaid':
            self.elementcheck('menu', 'link_prepaid', click=True)
            self.elementcheck('overview_page', 'prepaid_simonly', click=True)
        elif workflow == 'handset_prepaid':
            self.elementcheck('menu', 'link_prepaid', click=True)
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
        self.go_to_configpage(workflow)
        # workaround a-b testing
        if workflow == 'sim_only' or workflow == 'handset':
            try:
                self.driver.find_element_by_css_selector(settings.UI['configure_page']['button_order'])
            except NoSuchElementException:
                self.elementcheck('homepage', 'button_banner', click=True)
            # select internet bundle
            self.dropdownselector(profile, 'configure_page', 'select_internetbundle', 'bundles', 'internetbundle')
            self.dropdownselector(profile, 'configure_page', 'select_belbundle', 'bundles', 'belbundle')
            self.get_screenshot('configure_page', 'succes')
            self.elementcheck('configure_page', 'button_order', click=True)
        elif workflow == 'simonly_prepaid' or workflow == 'handset_prepaid':
            self.get_screenshot('configure_page', 'succes')
            self.elementcheck('prepaid', 'button_order', click=True)

    def go_to_step2(self, workflow, profile='default'):
        self.go_to_step1(workflow, profile)
        self.dropdownselector(profile, 'step_1', 'select_gender', 'gender', 'gender')
        self.elementcheck('step_1', 'input_firstname', keys=settings.PROFILES[profile]['firstname'])
        self.elementcheck('step_1', 'input_lastname', keys=settings.PROFILES[profile]['lastname'])
        self.elementcheck('step_1', 'input_initials', keys=settings.PROFILES[profile]['initials'])
        if workflow == 'sim_only' or workflow == 'handset':
            self.dropdownselector(profile, 'step_1', 'select_day', 'day', 'day')
            self.dropdownselector(profile, 'step_1', 'select_month', 'month', 'month')
            self.dropdownselector(profile, 'step_1', 'select_year', 'year', 'year')
        self.elementcheck('step_1', 'input_postcode', keys=settings.PROFILES[profile]['postcode'])
        self.elementcheck('step_1', 'input_housenumber', keys=settings.PROFILES[profile]['housenumber'])
        self.elementcheck('step_1', 'input_phonenumber', keys=settings.PROFILES[profile]['phonenumber'])
        self.elementcheck('step_1', 'input_e-mail', keys=settings.PROFILES[profile]['email'])
        self.elementcheck('step_1', 'input_repeat_email', keys=settings.PROFILES[profile]['repeat_email'])
        count = 0
        while not (self.driver.find_element_by_css_selector('#street').get_attribute("value") ==
                   settings.PROFILES[profile]['streetname']):
            if count >= 50:
                self.get_screenshot('step_1', 'input_street')
                # if no selector is found, spit out an error
                self.fail('finding the adress took longer then 5 seconds')
            else:
                datetime.time.sleep(0.1)
                count += 1
        self.get_screenshot('step_1', 'succes')
        self.elementcheck('step_1', 'button_next_step', click=True)

    def go_to_step3(self, workflow, profile='default'):
        self.go_to_step2(workflow, profile)
        self.elementcheck('step_2', 'input_IBANnumber', keys=settings.PROFILES[profile]['IBAN_number'])
        self.dropdownselector(profile, 'step_2', 'select_document_type', 'document_type', 'document_type')
        self.elementcheck('step_2', 'input_documentnumber', keys=settings.PROFILES[profile]['document_number'])
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        if settings.PROFILES[profile]['porting'] == 'ja':
            self.elementcheck('step_2', 'input_phonenumber', keys=settings.PROFILES[profile]['current_phonenumber'])
            self.dropdownselector(profile, 'step_2', 'select_current_subscription', 'current_subscription',
                                  'current_subscriber')
            self.dropdownselector(profile, 'step_2', 'select_mobile_provider', 'mobile_provider', 'current_provider')
            self.elementcheck('step_2', 'input_simcard_number',
                              keys=settings.PROFILES[profile]['current_simcardnumber'])
            self.elementcheck('step_2', 'select_date', click=True)
            self.elementcheck('step_2', 'select_day', click=True)
        self.dropdownselector(profile, 'step_2', 'select_services', 'services', 'services')
        self.get_screenshot('step_2', 'succes')
        self.elementcheck('step_2', 'button_next_step', click=True)

    # noinspection PyRedundantParentheses
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
            while not (clickandcollect.text.split()[0] == 'dixons'):
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
                    datetime.time.sleep(0.1)
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
        hover = ActionChains(self.driver).move_to_element(add)
        hover.perform()

    def hover(self, part, selector):
        locator = settings.UI[part][selector]
        add = self.driver.find_element_by_css_selector(locator)
        hover = ActionChains(self.driver).move_to_element(add)
        hover.perform()

    def IBAN_generator(self, profile, entry_type, error_message):
        for keys in settings.IBAN[entry_type].split(','):
            length = 18 - len(keys)
            self.elementcheck('step_2', 'link_ibanlink', click=True)
            self.dropdownselector(profile, 'step_2', 'select_bank', 'bank', 'bank')
            self.elementcheck('step_2', 'input_bankaccount', keys=keys)
            ibanfield_entry = self.driver.find_element_by_css_selector('#ibannummer').get_attribute('value')[length:]
            if entry_type == 'backend_validation_incorrect':
                length = 19 - len(keys)
                ibanfield_entry = (self.driver.find_element_by_css_selector('#ibannummer').get_attribute('value')[
                                   length:])
                self.assertEqual(ibanfield_entry, keys)
                self.elementcheck('step_2', 'button_choose_IBAN', click=True)
            elif not error_message:
                self.assertEqual(ibanfield_entry, keys)
            elif error_message:
                self.assertEqual(ibanfield_entry, '')
            self.driver.find_element_by_css_selector('#bban').clear()

    def setUp(self):
        fp = webdriver.FirefoxProfile()
        fp.add_extension('C:\\Users\\j-rijnaars\\Documents\\python\\mobile\\addons\\Firebug.xpi')
        fp.add_extension('C:\\Users\\j-rijnaars\\Documents\\python\\mobile\\addons\\Firefinder.xpi')
        # load up the remote driver and tell it to use Firefox
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1250, 1000)
        self.driver.start_client()

        # navigate to URL and log in as developer (since the script creates a new instance with clean cache)
        self.driver.get('https://www.tele2.nl/')

    def tearDown(self):
        # close the browser
        self.driver.quit()