from unittest import TestCase
import data_objects as do


class TestLoan(TestCase):
    def test_calculate_payment_1(self):
        loan = do.Loan(4.75, 30)
        self.assertAlmostEqual(1251.95, loan.calculate_payment(240000), 2)

    def test_calculate_payment_2(self):
        loan = do.Loan(3.5, 30)
        self.assertAlmostEqual(1077.71, loan.calculate_payment(240000), 2)

    def test_calculate_payment_3(self):
        loan = do.Loan(4.75, 15)
        self.assertAlmostEqual(1866.80, loan.calculate_payment(240000), 2)

