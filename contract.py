"""
CSC148, Winter 2019
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This is an abstract class. Only subclasses should be instantiated.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


# TODO: Implement the MTMContract, TermContract, and PrepaidContract

class TermContract(Contract):
    """A term contract is a type of Contract with a specific start date
     and end date, and which requires a commitment until the end date.
    A term contract comes with an initial large term deposit added to the bill
    of the first month of the contract.
    We assume that the start and end dates are at least in separate months.

    === Attributes ===
    end:
        ending date for the contract
    """
    start: datetime.date
    end: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """ Create a new TermContract with the <start> date, and <end> date,
        and an initial term deposit and monthly fee.
        """
        Contract.__init__(self, start)
        self.end = end

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Term deposit is added to the bill of the first month of the contract.
        a number of free minutes included each month, which refresh when a new
        month starts. Free minutes are used up first, so the customer only gets
        billed for minutes of voice time once the freebies have been used up.
        """
        self.bill = bill
        self.bill.set_rates("TERM", TERM_MINS_COST)
        self.bill.add_fixed_cost(TERM_MONTHLY_FEE)
        if not ((self.end.month < month and self.end.year <= year) or
                self.end.year < year):
            # refresh included minutes and SMSs
            self.bill.add_free_minutes(TERM_MINS - self.bill.free_min)
            if self.start.month == month and self.start.year == year:
                # if first month, add term deposit to bill.
                self.bill.add_fixed_cost(TERM_DEPOSIT)
        else:
            self.start = None

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill."""
        duration = ceil(call.duration / 60.0)
        if self.bill.free_min >= duration:
            self.bill.add_free_minutes(-1 * duration)
        else:
            self.bill.add_billed_minutes(duration - self.bill.free_min)
            self.bill.add_free_minutes(-1 * self.bill.free_min)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract."""
        if self.start is None:
            return self.bill.get_cost() - TERM_DEPOSIT
        return self.bill.get_cost()


class MTMContract(Contract):
    """The month-to-month contract is a Contract with no end date and
     no initial term deposit. This type of contract has higher rates
     for calls than a term contract, and comes with no free minutes included,
     but also involves no term commitment.
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ """
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        self.bill = bill
        self.bill.set_rates("MTM", MTM_MINS_COST)
        self.bill.add_fixed_cost(MTM_MONTHLY_FEE)


class PrepaidContract(Contract):
    """
    === Attributes ===
    balance:
        the amount of money the customer owes.
    """
    start: datetime.date
    bill: Optional[Bill]
    balance: float

    def __init__(self, start: datetime.date, balance: float) -> None:
        """Create a new TermContract with the <start> date, and <end> date,
                and an initial term deposit and monthly fee.
        """
        Contract.__init__(self, start)
        self.balance = balance * (-1)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        self.bill = bill
        self.bill.set_rates("PREPAID", PREPAID_MINS_COST)
        if self.balance > (-10):
            self.balance += (-25)
        self.bill.add_fixed_cost(self.balance)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill."""
        duration = ceil(call.duration / 60.0)
        self.bill.add_billed_minutes(duration)
        self.balance += (PREPAID_MINS_COST * duration)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract."""
        self.start = None
        if self.balance > 0.0:
            return self.balance
        return 0.0


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
