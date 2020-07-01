import os
import hashlib
import numpy as np
import numpy_financial as npf


def check_and_set(lower, value, upper):
    if not (lower <= value <= upper):
        raise ValueError('Value {} is out of range.')
    return value


SALT_SIZE = 32


def _hash(data: str, salt: bytes):
    key = hashlib.pbkdf2_hmac('sha256', data.encode('utf-8'), salt, 100000)
    storage = salt + key
    return storage


class User:
    def __init__(self, name: str, email: str, score: int, down: int):
        self.name = name
        self.email = email
        self.passwd = b''
        self.score = score
        self.down = down

    def set_password(self, raw_pass: str):
        self.passwd = _hash(raw_pass, os.urandom(SALT_SIZE))

    def verify_password(self, other_passwd):
        salt = self.passwd[:SALT_SIZE]
        other_key = _hash(other_passwd, salt)
        return self.passwd[SALT_SIZE:] == other_key[SALT_SIZE:]


class Address:
    def __init__(self, street_address: str, city: str,
                 state: str, zip_code: int):
        self._street_address = street_address
        self._city = city
        self._state = state
        self._zip_code = zip_code

    def __str__(self):
        address_str = self._street_address + ', '
        address_str += self._city + ', '
        address_str += self._state + ', '
        address_str += self._zip_code + '\n'
        return address_str

    def __eq__(self, other):
        return self.__dict__.values() == other.__dict__.values()

    @classmethod
    def from_str(cls, address_str):
        address_arr = address_str.split(', ')
        return cls(address_arr[0], address_arr[1],
                   address_arr[2], address_arr[3])


class Unit:
    def __init__(self, number: int, bedrooms: int,
                 bathrooms: int, rent_estimate: float):
        self._number = check_and_set(0, number, np.inf)
        self._bedrooms = check_and_set(0, bedrooms, np.inf)
        self._bathrooms = check_and_set(0, bathrooms, np.inf)
        self._rent_estimate = check_and_set(0, rent_estimate, np.inf)

    def get_rent(self):
        return self._rent_estimate


class Property:
    def __init__(self, units: list, house_value: float):
        check_and_set(1, len(units), np.inf)
        self._units = units
        self._value = check_and_set(0, house_value, np.inf)

    def calculate_rent(self):
        rent = 0
        for unit in self._units:
            rent += unit.get_rent()
        return rent

    def market_value(self):
        return self._value


class Listing:
    def __init__(self, prop: Property, selling_price: float):
        self._property = prop
        self._selling_price = check_and_set(0, selling_price, np.inf)

    def selling_price(self):
        return self._selling_price

    def get_property(self):
        return self._property

    def get_deal(self):
        return self.get_property().market_value() - self._selling_price


class Loan:
    def __init__(self, rate: float, term: int):
        self._rate = check_and_set(0, rate / 100, 1)
        self._term = check_and_set(0, term * 12, np.inf)

    def calculate_payment(self, loan_amount: float):
        return (-1) * npf.pmt(self._rate / 12, self._term, loan_amount)


class UserParameters:
    def __init__(self, down_payment_percentage: float,
                 taxes: float, insurance: float,
                 maintenance: float, management: float,
                 closing_costs: float):
        self._down_payment_percentage = check_and_set(0, down_payment_percentage / 100, 1)
        self._taxes = check_and_set(0, taxes, np.inf)
        self._insurance = check_and_set(0, insurance, np.inf)
        self._maintenance = check_and_set(0, maintenance, np.inf)
        self._management = check_and_set(0, management, np.inf)
        self._closing = check_and_set(0, closing_costs, np.inf)

    def calculate_down_payment(self, price):
        return price * self._down_payment_percentage

    def get_annual_taxes(self):
        return self._taxes

    def get_annual_insurance(self):
        return self._insurance

    def get_annual_maintenance(self):
        return self._maintenance

    def get_annual_management(self):
        return self._management

    def closing_costs(self):
        return self._closing
