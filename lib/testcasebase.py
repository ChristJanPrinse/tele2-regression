import unittest
import time
import os
import re
from datetime import datetime
from random import randint

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select

import settings


test = []


# noinspection PyBroadException
class Tele2Test(unittest.TestCase):
    def cookiebar_accept(self):
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("#qb_cookie_consent_main"))
        self.driver.find_element_by_css_selector('#buttonAccept').click()
        self.driver.switch_to.default_content()

    def click_and_collect_retrieve_adress(self, profile='default'):
        iteration_lines = []
        address = {}
        main_window = self.driver.current_window_handle
        self.servicechecker_login(profile)
        element = self.driver.find_element_by_css_selector('body').text
        for keys in element.split('Quantity'):
            iteration_lines.append(keys)
        for keys in iteration_lines:
            if keys[:6] == 'OnHand':
                amount = keys[keys.index('OnHand') +8:]
                amount = str(amount[:amount.index(",")])
                amount = int(amount)
                keys_postcode = keys[keys.index('ZipCode') +9:]
                keys_postcode = keys_postcode[:keys_postcode.index(",")]
                keys_housenumber = keys[keys.index('Address') +9:]
                keys_housenumber = keys_housenumber[:keys_housenumber.index(",")]
                #   keys_housenumber = int(re.search(r'\d+', keys_housenumber).group())
                postcode = ''
                for part in keys_postcode.split('"'):
                    postcode += part
                    postcode = str(postcode)
                    postcode = postcode.replace(" ", "")
                if amount > 0:
                    address[postcode] = keys_housenumber
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        self.driver.switch_to.window(main_window)
        return address

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
                except:
                    time.sleep(0.5)
                    count -= 0.5
            else:
                self.get_screenshot(part, selector)
                # if no selector is found, spit out an error
                self.fail("Expected to find mandatory error on %s field but did not find it." % selector)
        if ('popup' in settings.ERROR[part][selector]):
            try:
                # check for the presence of the selector
                self.driver.find_element_by_css_selector(settings.ERROR[part][selector]['popup'])
            except:
                self.get_screenshot(part, selector)
                # if no selector is found, spit out an error
                self.fail("Expected to find mandatory popup on %s field but did not find it." % selector)
        if ('text_popup' in settings.ERROR[part][selector]):
            element = self.driver.find_element_by_css_selector(settings.ERROR[part][selector]['popup'])
            element = element.text
            origin = settings.ERROR[part][selector]['text_popup']
            if element != origin:
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
        newpath = 'H:\output\%s\%s\%s' % (test[0], test[1], testcase)
        if not os.path.exists(newpath):
            os.makedirs('H:\output\%s\%s\%s' % (test[0], test[1], testcase))
        self.driver.get_screenshot_as_file(
            'H:\output\%s\%s\%s\%s %s.png' % (test[0], test[1], testcase, part, selector))

    def go_to_configpage(self, workflow, c_c=False):
        self.cookiebar_accept()
        self.hover('menu', 'link_mobiel')
        if workflow == 'sim_only':
            self.elementcheck('menu', 'link_sim_only', click=True)
        elif workflow == 'handset':
            self.elementcheck('menu', 'link_handset', click=True)
            if c_c == True:
                self.hover_article('#product-list-item-3011 .default-state')
                self.driver.find_element_by_css_selector('.preview-img-link[data-url*="-s5/"]').click()
            else:
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

    # noinspection PyArgumentList
    def go_to_step1(self, workflow, c_c=False, profile='default'):
        self.go_to_configpage(workflow, c_c)
        # workaround a-b testing
        try:
            self.driver.find_element_by_css_selector('a.fld_button[title*="Sim Only abonnement"]').click()
        except:
            pass
        if workflow == 'sim_only' or workflow == 'handset':
            # select internet bundle
            self.dropdownselector(profile, 'configure_page', 'select_internetbundle', 'bundles', 'internetbundle')
            self.dropdownselector(profile, 'configure_page', 'select_belbundle', 'bundles', 'belbundle')
            self.get_screenshot('configure_page', 'succes')
            self.elementcheck('configure_page', 'button_order', click=True)
        elif workflow == 'simonly_prepaid' or workflow == 'handset_prepaid':
            self.get_screenshot('configure_page', 'succes')
            self.elementcheck('prepaid', 'button_order', click=True)

    def go_to_step2(self, workflow, c_c=False, profile='default'):
        self.go_to_step1(workflow, c_c, profile)
        self.dropdownselector(profile, 'step_1', 'select_gender', 'gender', 'gender')
        self.elementcheck('step_1', 'input_firstname', keys=settings.PROFILES[profile]['firstname'])
        self.elementcheck('step_1', 'input_lastname', keys=settings.PROFILES[profile]['lastname'])
        self.elementcheck('step_1', 'input_initials', keys=settings.PROFILES[profile]['initials'])
        if workflow == 'sim_only' or workflow == 'handset':
            self.dropdownselector(profile, 'step_1', 'select_day', 'day', 'day')
            self.dropdownselector(profile, 'step_1', 'select_month', 'month', 'month')
            self.dropdownselector(profile, 'step_1', 'select_year', 'year', 'year')
        if c_c == True:
            address = self.click_and_collect_retrieve_adress(profile)
            housenumber = address.values()[0]
            housenumber = int(re.search(r'\d+', housenumber).group())
            c_c_streetname = address.values()[0]
            c_c_streetname = ''.join([i for i in c_c_streetname if not i.isdigit()])
            c_c_streetname = c_c_streetname.replace(" ", "")
            c_c_streetname = c_c_streetname.replace('"', '').replace("-", "")
            self.elementcheck('step_1', 'input_postcode', keys=address.keys()[0])
            self.elementcheck('step_1', 'input_housenumber', keys=housenumber)
            self.driver.find_element_by_css_selector('#street').click()
            current_streetname = self.driver.find_element_by_css_selector('#street').get_attribute("value")
            print current_streetname
            count = 0
            while not c_c_streetname in self.driver.find_element_by_css_selector('#street').get_attribute("value"):
                if count >= 50:
                    self.get_screenshot('step_1', 'input_street')
                    # if no selector is found, spit out an error
                    self.fail('finding the adress took longer then 5 seconds')
                else:
                    time.sleep(0.1)
                    count += 1
        else:
            self.elementcheck('step_1', 'input_postcode', keys=settings.PROFILES[profile]['postcode'])
            self.elementcheck('step_1', 'input_housenumber', keys=settings.PROFILES[profile]['housenumber'])
            self.driver.find_element_by_css_selector('#street').click()
            count = 0
            profile_streetname = settings.PROFILES[profile]['streetname']
            while not (self.driver.find_element_by_css_selector('#street').get_attribute("value") == profile_streetname):
                if count >= 50:
                    self.get_screenshot('step_1', 'input_street')
                    # if no selector is found, spit out an error
                    self.fail('finding the adress took longer then 5 seconds')
                else:
                    time.sleep(0.1)
                    count += 1
        self.elementcheck('step_1', 'input_phonenumber', keys=settings.PROFILES[profile]['phonenumber'])
        self.elementcheck('step_1', 'input_e-mail', keys=settings.PROFILES[profile]['email'])
        self.elementcheck('step_1', 'input_repeat_email', keys=settings.PROFILES[profile]['repeat_email'])
        self.get_screenshot('step_1', 'succes')
        self.elementcheck('step_1', 'button_next_step', click=True)

    def go_to_step3(self, workflow, c_c=False, profile='default'):
        self.go_to_step2(workflow, c_c, profile)
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
    def go_to_step4(self, workflow, c_c=False, profile='default'):
        self.go_to_step3(workflow, c_c, profile)
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
        hover = ActionChains(self.driver).move_to_element(add)
        hover.perform()

    def hover(self, part, selector):
        locator = settings.UI[part][selector]
        add = self.driver.find_element_by_css_selector(locator)
        hover = ActionChains(self.driver).move_to_element(add)
        hover.perform()

    def IBAN_generator(self, profile, status):
        keys = settings.BANKACCOUNT[status]
        for key in keys:
            self.driver.find_element_by_css_selector('a.label-help').click()
            self.dropdownselector(profile, 'step_2', 'select_bank', 'bank', 'bank')
            self.driver.find_element_by_css_selector('#bban').send_keys('key')
            actual = self.driver.find_element_by_css_selector('#ibannummer').get_attribute("value")
            self.driver.find_element_by_css_selector('#btnChooseIban').click()
            self.assertNotEqual(key, actual)

    def marketingwebchecker(self):
        self.fail('moet nog gemaakt worden')

    def servicechecker_login(self, profile):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        self.driver.get('https://tele2.nl/shop/shell/servicesChecker.php')
        # insert request url
        self.driver.find_element_by_css_selector('input[name="requesturl"]').send_keys(
            'https://wpos.basgroup.nl/servicestack/json/syncreply/')
        # insert security token
        self.driver.find_element_by_css_selector('input[name="token"]').send_keys(
            '17122D63B0628A2D77B827F3851AA94A296B8B8E1ED9AA4BA76136521216983A')
        # insert zip code
        self.driver.find_element_by_css_selector('input[name="zipcode"]').send_keys('5224AC')
        self.driver.find_element_by_css_selector('input[name="range"]').send_keys('20')
        self.driver.find_element_by_css_selector('input[name="itemnumber"]').send_keys('807066')
        self.driver.find_element_by_css_selector('input[name="send"]').click()

    def shoppingcart_configpage(self):
        try:
            self.driver.find_element_by_css_selector('a.fld_button[title*="Sim Only abonnement"]').click()
        except:
            pass
        # select price internet bundle
        internet_bundle = self.driver.find_element_by_css_selector(
            '#data-subscription-listSelectBoxItContainer .selectbox-subscription-value').text
        internet_bundle = internet_bundle[:3][1:]
        # select bel/sms bundle
        sms_bundle = self.driver.find_element_by_css_selector(
            '#voice-subscription-listSelectBoxItContainer .selectbox-subscription-value').text
        sms_bundle = sms_bundle[:3][1:]
        # select subtotal visible in page
        subtotal = self.driver.find_element_by_css_selector('.subtotals-cost').text
        subtotal = int(subtotal[:3][1:])
        # add up sms bundle and internet bundle
        bundle_total = int(internet_bundle) + int(sms_bundle)
        # assert bundle total and subtotal
        self.assertEqual(subtotal, bundle_total)

    def shoppingcart_step1(self):
        shopping_cart = self.driver.find_element_by_css_selector('.cart.block').text
        # get sms bundle from shopping cart
        sms_bundle = int(shopping_cart[shopping_cart.index('Bel/Sms') + 10:][:1])
        # get internet bundle from shopping cart
        internet_bundle = int(shopping_cart[shopping_cart.index('Internet') + 11:][:1])
        # get total cost a month
        total_cost_monthly = int(shopping_cart[shopping_cart.index('Totaal per maand') + 19:][:1])
        bundle_total = int(internet_bundle) + int(sms_bundle)
        # assert bundle total and subtotal
        self.assertEqual(total_cost_monthly, bundle_total)

    def setUp(self):
        if not test:
            now = datetime.now()
            date = '%s-%s-%s' % (now.month, now.day, now.year)
            time_tag = '%s;%s' % (now.hour, now.minute)
            test.append(date)
            test.append(time_tag)
        fp = webdriver.FirefoxProfile()
        fp.add_extension('.\\addons\\Firebug.xpi')
        fp.add_extension('.\\addons\\Firefinder.xpi')
        # load up the remote driver and tell it to use Firefox
        self.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            #   command_executor="http://PCD-1301:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX,
            browser_profile=fp)
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1280, 1024)
        # navigate to URL and log in as developer (since the script creates a new instance with clean cache)
        self.driver.get('https://www.tele2.nl/')

    def tearDown(self):
        #   Quit the browser
        self.driver.quit()