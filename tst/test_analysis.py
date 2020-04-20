from unittest import TestCase
import data_objects as do
import estimator


def create_single_family():
    loan = do.Loan(4.75, 30)
    parameters = do.UserParameters(20, 343.75 * 12, 100 * 12, 100 * 12, 200 * 12, 9000)
    offer = do.Listing(do.Property([do.Unit(1, 2, 1, 2000)], 330000), 300000)
    return estimator.Input(loan, parameters, offer)


def create_multi_family():
    loan = do.Loan(4.75, 30)
    parameters = do.UserParameters(20, 343.75 * 12, 100 * 12, 100 * 12, 480 * 12, 9000)
    units = [do.Unit(1, 2, 1, 2000), do.Unit(1, 2, 1, 1500), do.Unit(1, 2, 1, 1300)]
    offer = do.Listing(do.Property(units, 330000), 300000)
    return estimator.Input(loan, parameters, offer)


class TestAnalysis(TestCase):

    def test_calculate_monthly_expenses(self):
        inp = create_single_family()
        exp = estimator.Analysis.calculate_monthly_expenses(inp)
        self.assertAlmostEqual(1995.70, exp, 2)

    def test_get_cash_flow_single_family(self):
        inp = create_single_family()
        res = estimator.Analysis(inp)
        self.assertAlmostEqual(4.30, res.get_cash_flow(), 2)
        self.assertAlmostEqual(0.0745, res.get_apy(), 2)

    def test_get_deal_single_family(self):
        inp = create_single_family()
        res = estimator.Analysis(inp)
        self.assertAlmostEqual(9.09, res.get_deal(), 2)
        self.assertAlmostEqual(30000, res.get_cash_deal(), 2)

    def test_get_cash_flow_multi_family(self):
        inp = create_multi_family()
        res = estimator.Analysis(inp)
        self.assertAlmostEqual(2524.30, res.get_cash_flow(), 2)
        self.assertAlmostEqual(43.90, res.get_apy(), 2)

