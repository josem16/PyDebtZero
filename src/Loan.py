import numpy as np

class Loan(object):
    """
    The Loan class object stores information regarding a source of debt.
    """

    def __init__(self, name, principal_amount, apr, min_payment=None,
                 months_to_pay=120):
        # Loan properties
        self.name = name
        self.principal_amount = principal_amount
        self.apr = apr
        self.months_to_desired_completion = months_to_pay

        # Simulation parameters
        self.amount_still_owed = None

        # Optional parameters
        self.minimum_payment_default = min_payment

    @property
    def yearly_interest_rate(self):
        # Return yearly interest rate (APR as a decimal)
        yearly_interest_rate = self.apr/100.
        return yearly_interest_rate

    @property
    def minimum_payment(self):
        # Use default payment if one is specified, otherwise compute a
        # minimum
        if self.minimum_payment_default is not None:
            payment = self.minimum_payment_default
        else:
            payment = self.compute_minimum_required_payment()
        return payment

    @property
    def minimum_payment_simulation(self):
        # Return minimum payment or amount left in loan to pay,
        # whichever comes first
        if self.amount_still_owed is None:
            payment = 0.
        elif self.amount_still_owed < self.minimum_payment:
            payment = self.amount_still_owed
        else:
            payment = self.minimum_payment
        return payment

    @property
    def monthly_interest_rate(self):
        return self.yearly_interest_rate/12.

    @property
    def monthly_interest_amp(self):
        # Returns the monthly amplification factor to be applied to the
        # principal amount to account for compounding interest.
        return 1+self.monthly_interest_rate


    def compute_minimum_required_payment(self):
        """
        Determines the minimum payment required to pay off the loan by
        the desired time in months.
        """
        # Compute based on interest rate
        if self.monthly_interest_rate == 0:
            minimum_payment = self.principal_amount/self.months_to_desired_completion
        else:
            # Interest amplification factor to reach full loan payment
            amp = (1+self.monthly_interest_rate)**self.months_to_desired_completion

            # Compute min payment
            minimum_payment = self.monthly_interest_rate*self.principal_amount*amp/(amp - 1.)

        # Return minimum payment
        return minimum_payment

    def compute_single_cycle_earned_interest(self):
        """
        Computes the interest earned in a single cycle given the current
        simulation amount still owed.
        """
        return self.principal_amount*(self.monthly_interest_amp - 1)

    def compute_single_cycle_earned_interest_simulation(self):
        """
        Computes the interest earned in a single cycle given the current
        simulation amount still owed.
        """
        if self.amount_still_owed is None:
            earned_interest = 0.
        else:
            earned_interest = self.amount_still_owed*(self.monthly_interest_amp - 1)
        return earned_interest



def main():
    print('No default behavior.')

if __name__ == "__main__":
    main()
