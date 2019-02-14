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
    start: datetime.datetime
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
        self.bill.add_billed_minutes(call.duration)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancellation is requested.
        """
        self.start = None
        return self.bill.get_cost()


# TODO: Implement the MTMContract, TermContract, and PrepaidContract
# Sarah's ver.
class TermContract(Contract):
    """A term contract is a type of Contract with a specific start date
     and end date, and which requires a commitment until the end date.

    A term contract comes with an initial large term deposit added to the bill
    of the first month of the contract.

    === Attributes ===
    end:
        ending date for the contract

    """
    start: datetime.datetime
    bill: Optional[Bill]
    end: datetime.datetime

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """ Create a new TermContract with the <start> date, and <end> date,
        and an initial term deposit and monthly fee.
        """
        Contract.__init__(self, start)
        self.end = end
        self.bill.set_rates("TERM", TERM_MINS_COST)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Term deposit is added to the bill of the first month of the contract.
        a number of free minutes included each month, which refresh when a new
        month starts. Free minutes are used up first, so the customer only gets
        billed for minutes of voice time once the freebies have been used up.
        """
        # if first month, add term deposit to bill.
        if self.start.month == month and self.start.year == year:
            self.bill.add_fixed_cost(TERM_DEPOSIT)
            self.bill.add_free_minutes(TERM_MINS)
        elif self.end.month <= month and self.end.year <= year:
            self.bill.add_free_minutes(TERM_MINS - self.bill.free_min)
        #refresh included minutes and SMSs

        pass



class MTMContract(Contract):
    """

    === Attributes ===

    """
    start: datetime.datetime
    bill: Optional[Bill]

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        pass


class PrepaidContract(Contract):
    """
    === Attributes ===
    balance:
        the amount of money the customer owes.
    """
    start: datetime.datetime
    bill: Optional[Bill]
    balance: float

    def __init__(self, start: datetime.date, credit: float) -> None:
        """Create a new TermContract with the <start> date, and <end> date,
                and an initial term deposit and monthly fee.
        """
        Contract.__init__(self, start)
        self.balance = credit * (-1)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """



        pass
# Vic's ver.

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
