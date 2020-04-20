import data_objects as do


class Input:
    def __init__(self, loan: do.Loan, parameters: do.UserParameters, listing: do.Listing):
        self.loan = loan
        self.parameters = parameters
        self.listing = listing


class Analysis:
    def __init__(self, inp: Input):
        expenses = self.calculate_monthly_expenses(inp)
        income = inp.listing.get_property().calculate_rent()
        down_payment_amount = inp.parameters.calculate_down_payment(inp.listing.selling_price())
        invest = down_payment_amount + inp.parameters.closing_costs()
        self._cash_on_cash = income - expenses
        self._apy = (self._cash_on_cash * 12) / invest
        self._cash_deal = inp.listing.get_deal()
        self._deal = self._cash_deal / inp.listing.get_property().market_value()

    @staticmethod
    def calculate_monthly_expenses(analysis_input: Input):
        price = analysis_input.listing.selling_price()
        parameters = analysis_input.parameters
        loan = analysis_input.loan
        loan_amount = price - parameters.calculate_down_payment(price)
        payment = loan.calculate_payment(loan_amount)
        expenses = payment * 12
        expenses += parameters.get_annual_taxes()
        expenses += parameters.get_annual_insurance()
        expenses += parameters.get_annual_maintenance()
        expenses += parameters.get_annual_management()
        return expenses / 12

    def get_cash_flow(self):
        return self._cash_on_cash

    def get_apy(self):
        return self._apy * 100

    def get_cash_deal(self):
        return self._cash_deal

    def get_deal(self):
        return self._deal * 100
