import unittest
from pytest import mark
from test_convert import test_convert
from test_balance import test_get_allbalance
from test_beneficiaries import test_get_beneficiary
from test_deposit import test_get_bank_to_deposit


class TestApi(unittest.TestCase):
    def test_convert(self):
        self.assertAlmostEqual(test_convert("USD",400,"ILS",),200,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("USD",400,"ILS",2000),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("DDD",400,"ILS"),404,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("USD",400,"NIS"),404,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("NIS",400,"NIS"),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("USD",0,"ILS"),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("False","True","ILS"),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert(None,400,"ILS"),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("USD",None,"ILS"),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("USD",400,None),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert("USD","bla",None),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert(500,900,None),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert(None,None,None),400,None,msg="FAIL")
        self.assertAlmostEqual(test_convert(None,None,None),400,None,msg="FAIL")

    # @unittest.skip('Skipped for now')
    # def test_balance(self):
    #
    #     self.assertEqual(test_get_allbalance(),200,msg="Fail")
    #
    # def test_beneficiary(self):
    #
    #     self.assertEqual(test_get_beneficiary(),200,msg="Fail: Beneficiary")
    #
    # def test_bank_to_deposit(self):

        self.assertAlmostEqual(test_get_bank_to_deposit(),200,msg="Fail")





    if __name__ == '__main__':
        unittest.main()





