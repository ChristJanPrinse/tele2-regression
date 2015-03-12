from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import settings

UI = {
    'bank': {
        'ing': '#bankSelectSelectBoxItOptions li.selectboxit-option[data-val="ing-bank"]',
        'abn_amro': '#bankSelectSelectBoxItOptions li.selectboxit-option[data-val="abn-amro"]',
    },
    'bundles': {
        '100MB': '.selectboxit-option[data-name="100"]',
        '500MB': '.selectboxit-option[data-name="500"]',
        '1000MB': '.selectboxit-option[data-name="1000"]',
        '2000MB': '.selectboxit-option[data-name="2000"]',
        '4000MB': '.selectboxit-option[data-name="4000"]',
        '150bel/sms': '.selectboxit-option[data-name="150"]',
        '300bel/sms': '.selectboxit-option[data-name="300"]',
        'onbeperktbel/sms': '.selectboxit-option[data-name="Onbeperkt"]',
    },
    'configure_page': {
        'button_order': 'a.add-cart.button',
        'cookie': '#buttonAccept',
        'select_belbundle': '#voice-subscription-listSelectBoxIt',
        'select_internetbundle': '#data-subscription-listSelectBoxIt',
        'select_simcard': '#sim-subscription-listSelectBoxIt',
    },
    'current_subscription': {
        'prepaid': '#type-of-subscriptionSelectBoxItOptions li.selectboxit-option[data-val="1"]',
        'postpaid': '#type-of-subscriptionSelectBoxItOptions li.selectboxit-option[data-val="2"]',
    },
    'day': {
        '1': '#daySelectBoxItOptions li.selectboxit-option[data-val="01"]',
    },
    'homepage': {
        'button_banner': 'a.fld_button[title="Tele2 Sim Only"]',
    },
    'month': {
        '1': '#monthSelectBoxItOptions li.selectboxit-option[data-val="01"]',
    },
    'year': {
        '1990': '#yearSelectBoxItOptions li.selectboxit-option[data-val="1990"]',
    },
    'menu': {
        'link_mobiel': 'a[data-content="mobiel"]',
        'link_sim_only':'#hover-menu a[href*="sim-only"]',
        'link_handset':'#hover-menu a[href*="smartphones"]',
        'link_prepaid': '#hover-menu a[href*="prepaid"]',
    },
    'mobile_provider': {
        'tele2': '#mobile-providerSelectBoxItOptions li.selectboxit-option[data-val="TEL2"]',
        'tele2_zakelijk':'#mobile-providerSelectBoxItOptions li.selectboxit-option[data-val="TL2Z"]',
        'KPN':'#mobile-providerSelectBoxItOptions li.selectboxit-option[data-val="SPM"]',
    },
    'overview_page': {
        'handset': '.phones_wrapper.abonnement > article:nth-child(1)',
        'hover_handset': 'a.preview-img-link',
        'uat_handset': '.phones_wrapper.abonnement > article:nth-child(1)',
        'uat_hover_handset': 'a.preview-img-link',
        'prepaid_simonly': 'a.fld_link[title*="Sim Only"]',
        'prepaid_handset': 'a.fld_link[title*="telefoons"]',
    },
    'prepaid': {
        'button_order': '.button.btn_with_icon',
        'link_handset': '.default-state img.fld_image[title*="Nokia 113"]',
        'hover_handset': 'a.preview-img-link[data-url*=nokia-113]',
    },
    'porting': {
        'ja': '#keepnumberSelectBoxItOptions li.selectboxit-option[data-val="1"]',
        'nee': '#keepnumberSelectBoxItOptions li.selectboxit-option[data-val="0"]',
    },
    'document_type': {
        'pasport': '#identificationSelectBoxItOptions li.selectboxit-option[data-val="PASSPORT"]',
        'idcart': '#identificationSelectBoxItOptions li.selectboxit-option[data-val="ID_CARD"]',
        'DRIVERS_LICENSE': '#identificationSelectBoxItOptions li.selectboxit-option[data-val="DRIVERS_LICENSE"]',
    },
    'gender': {
        'Male': '#genderSelectBoxItOptions li.selectboxit-option[data-val="Male"]',
        'Female': '#genderSelectBoxItOptions li.selectboxit-option[data-val="Female"]',
    },
    'services': {
        'standaardinstellingen': 'li.selectboxit-option[data-val="defaults"]',
        'aangepasteinstellingen': 'li.selectboxit-option[data-val="manual"]',
    },
    'step_1': {
        'button_next_step': '#btn_step_one',
        'input_e-mail':'#e-mail',
        'input_firstname': '#firstname',
        'input_housenumber': '#house',
        'input_initials': '#initials',
        'input_lastname': '#lastname',
        'input_phonenumber': '#telephone',
        'input_postcode': '#postcode',
        'input_repeat_email':'#repeat-email',
        'input_street': '#street',
        'select_gender': '#genderSelectBoxIt',
        'select_day': '#daySelectBoxIt',
        'select_month': '#monthSelectBoxIt',
        'select_year': '#yearSelectBoxIt',
    },
    'step_2': {
        'button_next_step': '#btn_step_two',
        'input_bankaccount': '#bban',
        'input_documentnumber': '#docnumber',
        'input_IBANnumber': '#rekeningnummer',
        'input_phonenumber': '#phone-number',
        'input_simcard_number': '#sim-card-number',
        'link_ibanlink': 'a.label-help',
        'select_bank': '#bankSelectSelectBoxIt',
        'select_current_subscription': '#type-of-subscriptionSelectBoxIt',
        'select_date': '#porting-date',
        'select_day': '.ui-datepicker-days-cell-over',
        'select_document_type': '#identificationSelectBoxItText',
        'select_mobile_provider': '#mobile-providerSelectBoxIt',
        'select_porting': '#keepnumberSelectBoxIt',
        'select_services': '#additional-servicesSelectBoxIt',
    },
    'step_3': {
        'button_next_step': '#btn_step_three',
        'ratio_delivery': '.request-delivery',
        'ratio_click_collect': '.pick-point',
        'terms': '#terms-one-link',
        'directdebid': '#terms-two-link',
    },
    'step_4': {
        'lastpage': '#stepFour',
        'text_1': '.odd .done ~ p',
    },
    'simcard_type': {
        'standaard': '.selectboxit-option[data-simname="Standaard- & Micro SIM"]',
        'nano': '.selectboxit-option[data-simname="Nano SIM"]',
    },
}

ERROR = {
    'step_1': {
        'DOB': {
            'popup': '#yearSelectBoxItContainer ~ .popup.tooltip.error',
            'text_popup': 'Helaas ben je nog geen 18 en mag je nog geen telefoon bestellen , misschien kun je je ouders vragen om een telefoon voor je te bestellen.',
        },
        'check_initials': {
            '#initials.validation-passed',
        },
        'check_housenumber': {
            '#housenumber.validation-passed',
        },
        'check_phonenumber': {
            '#telephone.validation-passed',
        },
        'city': {
            'mandatory': '#city.validation-failed',
            'popup': '#city ~ .popup.tooltip.error',
            'text_popup': 'Woonplaats is niet ingevuld',
        },
        'e-mail': {
            'mandatory': '#e-mail.validation-failed',
            'popup': '#e-mail ~ .popup.tooltip.error',
            'text_popup': 'Zonder een correct e-mailadres kunnen we geen contact met je opnemen. Vul dus jouw correcte e-mail adres in',
        },
        'firstname': {
            'mandatory': '#firstname.validation-failed',
            'popup': '#firstname ~ .popup.tooltip.error',
            'text_popup': 'Zoals vermeld op je legitimatiebewijs',
        },
        'gender': {
            'popup': '#gender ~ .popup.tooltip.error',
            'text_popup': 'Aanhef is niet ingevuld',
        },
        'housenumber': {
            'mandatory': '#house.validation-failed',
            'popup': '#house ~ .popup.tooltip.error',
            'text_popup': 'Let op, alleen nummers zijn toegestaan.',
        },
        'initials': {
            'mandatory': '#initials.validation-failed',
            'popup': '#initials ~ .popup.tooltip.error',
            'text_popup': 'Je bent je voorletters vergeten.',
        },
        'lastname': {
            'mandatory': '#lastname.validation-failed',
            'popup': '#lastname ~ .popup.tooltip.error',
            'text_popup': 'Zoals vermeld op je legitimatiebewijs',
        },
        'phonenumber': {
            'mandatory': '#telephone.validation-failed',
            'popup': '#telephone ~ .popup.tooltip.error',
            'text_popup': 'Zonder telefoonnummer kunnen we je natuurlijk niet bereiken. Vul de tien cijfers van je telefoonnummer in',
        },
        'postcode': {
            'mandatory': '#postcode.validation-failed',
            'popup': '#postcode ~ .popup.tooltip.error',
            'text_popup': 'Typ de 4 cijfers en 2 letters van je postcode in: 1111AA',
        },
        'repeat_email': {
            'mandatory': '#repeat-email.validation-failed',
            'popup': '#repeat-email ~ .popup.tooltip.error',
            'text_popup': 'Dit e-mailadres is niet hetzelfde als dat je hierboven hebt ingevuld. Typ hier hetzelfde e-mailadres als hierboven',
        },
        'streetname': {
            'mandatory': '#street.validation-failed',
            'popup': '#street ~ .popup.tooltip.error',
            'text_popup': 'Straatnaam is niet ingevuld',
        },
    },
    'step_2': {
        'bankaccount': {
            'mandatory': '#bban.validation-failed',
            'popup': '#bban ~ .popup.tooltip.error',
            'text_popup': 'Rekeningnummer komt niet overeen met je bank',        
        },
        'current_phonenumber': {
            'mandatory': '#phone-number.validation-failed',
            'popup': '#phone-number ~ .popup.tooltip.error',
            'text_popup': 'Mobiel nummer is niet goed ingevuld (Voorbeeld: 0610000000).',
        },
        'current_subscription': {
            'mandatory': '#type-of-subscription.validation-failed',
            'popup': '#type-of-subscription ~ .popup.tooltip.error',
            'text_popup': 'Huidige belvorm is niet gekozen.',        
        },
        'documentnumber': {
            'mandatory': '#docnumber.validation-failed',
            'popup': '#docnumber ~ .popup.tooltip.error',
            'text_popup': 'Het legitimatienummer komt niet overeen met je type legitimatie.',        
        },
        'documenttype': {
            'popup': '#identificationSelectBoxItContainer ~ .popup.tooltip.error',
            'text_popup': 'Er is geen legitimatietype gekozen.',        
        },
        'IBANnumber': {
            'mandatory': '#rekeningnummer.validation-failed',
            'popup': '#rekeningnummer ~ .popup.tooltip.error',
            'text_popup': 'Rekeningnummer komt niet overeen met je bank',        
        },
        'mobile_provider': {
            'popup': '#mobile-provider ~ .popup.tooltip.error',
            'text_popup': 'Huidige provider is niet gekozen.',        
        },
        'phonenumber': {
            'mandatory': '#phone-number.validation-failed',
            'popup': '#phone-number ~ .popup.tooltip.error',
            'text_popup': 'Mobiel nummer is niet goed ingevuld (Voorbeeld: 0610000000).',
        },
        'porting_date': {
            'mandatory': '#porting-date.validation-failed',
            'popup': '#porting-date ~ .popup.tooltip.error',
            'text_popup': 'Overstapdatum is niet goed ingevuld',        
        },
        'simcard_number': {
            'mandatory': '#sim-card-number.validation-failed',
            'popup': '#sim-card-number ~ .popup.tooltip.error',
            'text_popup': 'SIM-kaartnummer komt niet overeen met uw service provider.',        
        },

    }
}