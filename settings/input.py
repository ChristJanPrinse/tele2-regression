BANKACCOUNT = {
    'incorrect': '12345678, 123456789, qwerty, q12324',
}

DRIVERSLICENCE = {
    'incorrect': '123456789, qwerty, nl55135135',
}

EMAIL = {
    'incorrect': 'test@test, testtest.nl, @test.nl, test@test@test.nl'
}

FIRSTNAME = {
    'incorrect': 'test1, 1234',
    'empty': '',
}

HOUSENUMBER = {
    'corrected': ' 1',
    'default': 7,
    'number_suffix': 7,
    'not_existing': 1,
    'number_in_street': 7,
    'longest_streetname': 1,
    'longest_cityname': 3,
    'incorrect': 'A, 1A',
    'empty': '',
}

IBAN = {
    'incorrect': '123456789, NL89ASNB0336589947, NL89ABNB0336589948, NL89ASN#0336589948',
    'generator_input_correct': '123456,000001,000012,000123,001234,012345,1234567,188255613',
    'generator_input_incorrect': '111111111,aaaaaaaaa,aaaa11111,a',
}

INITIALS = {
    'incorrect': '1',
    'corrected': 't1',
    'correct': 't, t t, t., t t t t t',
    'empty': '',
}

LASTNAME = {
    'incorrect': 'test1, 1234',
    'empty': '',
}

PHONENUMBER = {
    'incorrect': '1234567890, 061234567',
    'corrected': 'asdadasd, 12313adasdas, 06-12345678, 06 12345678,',
}

POSTCODE = {
    'correct': '5331XW',
    'number_suffix': '1097LW',
    'not_existing': '9999ZZ',
    'number_in_street': '4331LG',
    'longest_streetname': '1509BP',
    'longest_cityname': '9515PN',
    'incorrect': '999999, 99999Z, 9999Z',
    'empty': '',
}