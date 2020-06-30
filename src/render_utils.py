from data_objects import Loan, UserParameters, Listing, Property, Unit


def strip(val: str):
    return val.replace('$', '').replace('%', '').replace(' ', '')


def to_num(t, val: str):
    return t(strip(val))


def get_loan(form):
    return Loan(to_num(float, form['rate']), to_num(int, form['term']))


def get_user_parameters(form):
    return UserParameters(to_num(float, form['down']), to_num(float, form['taxes']),
                          to_num(float, form['insurance']), to_num(float, form['maintenance']),
                          to_num(float, form['management']), to_num(float, form['closing_cost']))


def get_listing(form):
    units = [Unit(1, 1, 1, to_num(float, form['rent']))]
    prop = Property(units, to_num(float, form['value']))
    return Listing(prop, to_num(float, form['price']))
