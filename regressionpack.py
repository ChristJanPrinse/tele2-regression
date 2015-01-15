from lib.testcasebase import Tele2Test, unittest, settings

class SimOnlyFieldCorrection(Tele2Test):

    def test_firstletter_field_correction(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_initials', 'input_firstname', settings.INITIALS, 'corrected', 'check_initials')

    def test_phonenumber_field_correction(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_phonenumber', 'input_firstname', settings.PHONENUMBER, 'corrected', 'check_phonenumber')

    def test_housenumber_field_correction(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_housenumber', 'input_firstname', settings.HOUSENUMBER, 'corrected', 'check_housenumber')

class SimOnlyFieldMandatory(Tele2Test):

    def test_gender_mandatory(self):
        self.go_to_sim_only_step1()
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'gender')

    def test_firstname_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'firstname')

    def test_lastname_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'lastname')

    def test_initials_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'input_lastname',keys='test')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'initials')

    def test_DOB_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'input_lastname',keys='test')
        self.elementcheck('step_1', 'input_initials',keys='t')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'DOB')

    def test_postcode_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'input_lastname',keys='test')
        self.elementcheck('step_1', 'input_initials',keys='t')
        self.dropdownselector('step_1', 'select_day', 'day', '1')
        self.dropdownselector('step_1', 'select_month', 'month', '1')
        self.dropdownselector('step_1', 'select_year', 'year', '1990')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'postcode')

    def test_housenumber_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'input_lastname',keys='test')
        self.elementcheck('step_1', 'input_initials',keys='t')
        self.dropdownselector('step_1', 'select_day', 'day', '1')
        self.dropdownselector('step_1', 'select_month', 'month', '1')
        self.dropdownselector('step_1', 'select_year', 'year', '1990')
        self.elementcheck('step_1', 'input_postcode',keys='5331XW')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'housenumber')

    def test_streetname_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'input_lastname',keys='test')
        self.elementcheck('step_1', 'input_initials',keys='t')
        self.dropdownselector('step_1', 'select_day', 'day', '1')
        self.dropdownselector('step_1', 'select_month', 'month', '1')
        self.dropdownselector('step_1', 'select_year', 'year', '1990')
        self.elementcheck('step_1', 'input_postcode',keys='5331XW')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'streetname')

    def test_city_mandatory(self):
        self.go_to_sim_only_step1()
        self.dropdownselector('step_1', 'select_gender', 'gender', 'male')
        self.elementcheck('step_1', 'input_firstname',keys='test')
        self.elementcheck('step_1', 'input_lastname',keys='test')
        self.elementcheck('step_1', 'input_initials',keys='t')
        self.dropdownselector('step_1', 'select_day', 'day', '1')
        self.dropdownselector('step_1', 'select_month', 'month', '1')
        self.dropdownselector('step_1', 'select_year', 'year', '1990')
        self.elementcheck('step_1', 'input_postcode',keys='5331XW')
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'city')

    def test_phonenumber_mandatory(self):
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
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'phonenumber')

    def test_email_mandatory(self):
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
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'e-mail')

    def test_repeat_email_mandatory(self):
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
        self.elementcheck('step_1', 'button_next_step', click=True)
        self.errorcheck('step_1', 'repeat_email')

    def test_IBAN_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'IBANnumber')

    def test_documenttype_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'documenttype')

    def test_documentnumber_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.dropdownselector('step_2', 'select_idtype', 'idtype', 'drivers_licence')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'documentnumber')

    def test_current_subscription_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.dropdownselector('step_2', 'select_idtype', 'idtype', 'drivers_licence')
        self.elementcheck('step_2', 'input_documentnumber', keys="1234567890")
        self.dropdownselector('step_2', 'select_porting', 'porting', 'ja')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'current_subscription')

    def test_current_phonenumber_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.dropdownselector('step_2', 'select_idtype', 'idtype', 'drivers_licence')
        self.elementcheck('step_2', 'input_documentnumber', keys="1234567890")
        self.dropdownselector('step_2', 'select_porting', 'porting', 'ja')
        self.dropdownselector('step_2', 'select_current_subscription', 'current_subscription', 'prepaid')
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'current_phonenumber')

    def test_current_mobile_provider_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.dropdownselector('step_2', 'select_idtype', 'idtype', 'pasport')
        self.elementcheck('step_2', 'input_documentnumber', keys="1234567890")
        self.dropdownselector('step_2', 'select_porting', 'porting', 'ja')
        self.dropdownselector('step_2', 'select_current_subscription', 'current_subscription', 'prepaid')
        self.elementcheck('step_2', 'input_phonenumber', keys="0636253786")
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'mobile_provider')

    def test_current_simcard_number_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.dropdownselector('step_2', 'select_idtype', 'idtype', 'pasport')
        self.elementcheck('step_2', 'input_documentnumber', keys="1234567890")
        self.dropdownselector('step_2', 'select_porting', 'porting', 'ja')
        self.dropdownselector('step_2', 'select_current_subscription', 'current_subscription', 'prepaid')
        self.elementcheck('step_2', 'input_phonenumber', keys="0636253786")
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'simcard_number')

    def test_current_portingdate_mandatory(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.dropdownselector('step_2', 'select_idtype', 'idtype', 'drivers_licence')
        self.elementcheck('step_2', 'input_documentnumber', keys="1234567890")
        self.dropdownselector('step_2', 'select_porting', 'porting', 'ja')
        self.dropdownselector('step_2', 'select_current_subscription', 'current_subscription', 'prepaid')
        self.elementcheck('step_2', 'input_phonenumber', keys="0636253786")
        self.elementcheck('step_2', 'button_next_step', click=True)
        self.errorcheck('step_2', 'porting_date')

class SimOnlyFieldValidation(Tele2Test):

    def test_firstname_field_validation(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_firstname', 'input_lastname', settings.FIRSTNAME, 'incorrect', 'firstname')

    def test_lastname_field_validation(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_lastname', 'input_firstname', settings.LASTNAME, 'incorrect', 'lastname')

    def test_firstletter_field_validation(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_initials', 'input_firstname', settings.INITIALS, 'incorrect', 'initials')

    def test_postcode_field_incorrect(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_postcode', 'input_firstname', settings.POSTCODE, 'incorrect', 'postcode')

    def test_housenumber_field_incorrect(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_housenumber', 'input_firstname', settings.HOUSENUMBER, 'incorrect', 'housenumber')

    def test_phonenumber_field_incorrect(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_phonenumber', 'input_firstname', settings.PHONENUMBER, 'incorrect', 'phonenumber')

    def test_email_field_incorrect(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_e-mail', 'input_firstname', settings.EMAIL, 'incorrect', 'e-mail')

    def test_repeat_email_field_incorrect(self):
        self.go_to_sim_only_step1()
        self.field_validation('step_1', 'input_repeat_email', 'input_firstname', settings.EMAIL, 'incorrect', 'repeat_email')

    def test_IBAN_field_incorrect(self):
        self.go_to_sim_only_step2()
        self.field_validation('step_2', 'input_IBANnumber', 'select_services', settings.IBAN, 'incorrect', 'IBANnumber')

    def test_document_number_incorrect(self):
        self.go_to_sim_only_step2()
        self.elementcheck('step_2', 'input_IBANnumber', keys='NL20INGB0000546546')
        self.dropdownselector('step_2', 'select_idtype', 'idtype', 'drivers_licence')
        self.field_validation('step_2', 'input_documentnumber', 'select_idtype', settings.DRIVERSLICENCE, 'incorrect', 'documentnumber')

class Workflows(Tele2Test):

    def test_simonly_postpaid_noporting_delivery(self):
        testcase = unittest.TestCase.id(self)
        testcase = testcase.split('.')[2]
        self.go_to_sim_only_step1()

# collect the tests and run them
if __name__ == "__main__":
    unittest.main(verbosity=2)