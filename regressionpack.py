import lib.testcasebase
import settings


'''
------------------------------------------------------------------------------------------------------------------------
                TEST SUMMARY
------------------------------------------------------------------------------------------------------------------------
'''


class HandsetWorkflows(lib.testcasebase.Tele2Test):
    def test_handset_postpaid_noporting_delivery(self, workflow='handset',
                                                 profile='handset_postpaid_noporting_delivery'):
        self.go_to_step4(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_handset_postpaid_noporting_delivery')

    def test_handset_postpaid_porting_delivery(self, workflow='handset', profile='handset_postpaid_porting_delivery'):
        self.go_to_step4(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_handset_postpaid_porting_delivery')

    def test_handset_postpaid_noporting_clickandcollect(self, workflow='handset',
                                                        c_c=True,
                                                        profile='handset_postpaid_noporting_clickandcollect'):
        self.go_to_step4(workflow, c_c, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_handset_postpaid_noporting_clickandcollect')

    def test_handset_postpaid_porting_clickandcollect(self, workflow='handset',
                                                      c_c=True,
                                                      profile='handset_postpaid_porting_clickandcollect'):
        self.go_to_step4(workflow, c_c, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_handset_postpaid_porting_clickandcollect')


class PrepaidWorkflows(lib.testcasebase.Tele2Test):
    def test_simonly_prepaid(self, workflow='simonly_prepaid', profile='simonly_prepaid'):
        self.go_to_step3_prepaid(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_simonly_prepaid')

    def test_handset_prepaid(self, workflow='handset_prepaid', profile='handset_prepaid'):
        self.go_to_step3_prepaid(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_simonly_prepaid')


class SimOnlyFieldCorrection(lib.testcasebase.Tele2Test):
    def test_firstletter_field_correction(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_initials', 'input_firstname', settings.INITIALS, 'corrected',
                              'check_initials')

    def test_phonenumber_field_correction(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_phonenumber', 'input_firstname', settings.PHONENUMBER, 'corrected',
                              'check_phonenumber')

    def test_housenumber_field_correction(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_housenumber', 'input_firstname', settings.HOUSENUMBER, 'corrected',
                              'check_housenumber')


class SimOnlyFieldMandatory(lib.testcasebase.Tele2Test):
    def test_gender_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'gender')

    def test_firstname_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'firstname')

    def test_lastname_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'lastname')

    def test_initials_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'initials')

    def test_DOB_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'DOB')

    def test_postcode_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'postcode')

    def test_housenumber_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'housenumber')

    def test_streetname_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'streetname')

    def test_city_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'city')

    def test_phonenumber_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'phonenumber')

    def test_email_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'e-mail')

    def test_repeat_email_mandatory(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'repeat_email')

    def test_IBAN_mandatory(self, workflow='sim_only'):
        self.go_to_step2(workflow)
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'IBANnumber')

    def test_documenttype_mandatory(self, workflow='sim_only'):
        self.go_to_step2(workflow)
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'documenttype')

    def test_documentnumber_mandatory(self, workflow='sim_only', profile='default'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_document_type', 'document_type', 'document_type')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'documentnumber')

    def test_current_subscription_mandatory(self, workflow='sim_only', profile='porting_mandatory'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'current_subscription')

    def test_current_phonenumber_mandatory(self, workflow='sim_only', profile='porting_mandatory'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'current_phonenumber')

    def test_current_mobile_provider_mandatory(self, workflow='sim_only', profile='porting_mandatory'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'mobile_provider')

    def test_current_simcard_number_mandatory(self, workflow='sim_only', profile='porting_mandatory'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'simcard_number')

    def test_current_portingdate_mandatory(self, workflow='sim_only', profile='porting_mandatory'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'porting_date')


class SimOnlyFieldValidation(lib.testcasebase.Tele2Test):
    def test_firstname_field_validation(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_firstname', 'input_lastname', settings.FIRSTNAME, 'incorrect',
                              'firstname')

    def test_lastname_field_validation(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_lastname', 'input_firstname', settings.LASTNAME, 'incorrect', 'lastname')

    def test_firstletter_field_validation(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_initials', 'input_firstname', settings.INITIALS, 'incorrect', 'initials')

    def test_postcode_field_incorrect(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_postcode', 'input_firstname', settings.POSTCODE, 'incorrect', 'postcode')

    def test_housenumber_field_incorrect(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_housenumber', 'input_firstname', settings.HOUSENUMBER, 'incorrect',
                              'housenumber')

    def test_phonenumber_field_incorrect(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_phonenumber', 'input_firstname', settings.PHONENUMBER, 'incorrect',
                              'phonenumber')

    def test_email_field_incorrect(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_e-mail', 'input_firstname', settings.EMAIL, 'incorrect', 'e-mail')

    def test_repeat_email_field_incorrect(self, workflow='sim_only'):
        self.go_to_step1(workflow)
        self.field_validation('step_1', 'input_repeat_email', 'input_firstname', settings.EMAIL, 'incorrect',
                              'repeat_email')

    def test_IBANgenerator_incorrect(self, workflow='sim_only', profile="default"):
        self.go_to_step2(workflow, profile)
        self.IBAN_generator(profile, status='incorrect')

    def test_IBANgenerator_correct(self, workflow='sim_only', profile='default'):
        self.go_to_step2(workflow, profile)
        #   self.IBAN_generator(profile, 'generator_input_incorrect', True)

    def test_IBAN_field_incorrect(self, workflow='sim_only'):
        self.go_to_step2(workflow)
        self.field_validation('step_2', 'input_IBANnumber', 'select_services', settings.IBAN, 'incorrect', 'IBANnumber')

    def test_document_number_incorrect(self, workflow='sim_only', profile='default'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_document_type', 'document_type', 'document_type')
        self.field_validation('step_2', 'input_documentnumber', 'select_document_type', settings.DRIVERSLICENCE,
                              'incorrect', 'documentnumber')

    def test_porting_phonenumber_field_incorrect(self, workflow='sim_only', profile='porting_mandatory'):
        self.go_to_step2(workflow)
        self.dropdownselector(profile, 'step_2', 'select_porting', 'porting', 'porting')
        self.field_validation('step_2', 'input_phonenumber', 'input_IBANnumber', settings.PHONENUMBER, 'incorrect',
                              'phonenumber')


class SimOnlyWorkflows(lib.testcasebase.Tele2Test):
    def test_simonly_postpaid_noporting_delivery(self, workflow='sim_only',
                                                 profile='simonly_postpaid_noporting_delivery',):
        self.go_to_step4(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_simonly_postpaid_noporting_delivery')

    def test_simonly_postpaid_porting_delivery(self, workflow='sim_only', profile='simonly_postpaid_porting_delivery'):
        self.go_to_step4(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_simonly_postpaid_porting_delivery')

    def test_simonly_postpaid_noporting_clickandcollect(self, workflow='sim_only',
                                                        profile='simonly_postpaid_noporting_clickandcollect',
                                                        c_c=True):
        self.go_to_step4(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_simonly_postpaid_noporting_clickandcollect')

    def test_simonly_postpaid_porting_clickandcollect(self, workflow='sim_only',
                                                      profile='simonly_postpaid_porting_clickandcollect',
                                                      c_c=True):
        self.go_to_step4(workflow, profile)
        self.elementcheck('step_4', 'lastpage')
        self.get_screenshot('succesfull', 'test_simonly_postpaid_porting_clickandcollect')


class SimOnlyShoppingcart(lib.testcasebase.Tele2Test):
    def test_configurepage_cart(self, workflow='sim_only'):
        self.go_to_configpage(workflow)
        self.shoppingcart_configpage()

    def test_step1_cart(self, workflow='sim_only', profile='default'):
        self.go_to_step1(workflow, profile)
        self.shoppingcart_step1()


'''
------------------------------------------------------------------------------------------------------------------------
                TEST GATHERER AND RUNNER - REPORT CREATING
------------------------------------------------------------------------------------------------------------------------
'''


if __name__ == "__main__":
    lib.testcasebase.unittest.main(verbosity=2)