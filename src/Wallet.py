import os
import numpy as np
import operator

class Wallet(object):
    """
    The Wallet class object stores Loan information.
    """

    def __init__(self, budget_ceiling):
        # Wallet properties
        self.loans = {}
        self.budget_ceiling = budget_ceiling

        # Simulation parameters
        self.payment_history = None
        self.balance_history = None
        self.interest_history = None
        self.method_used_name = None
        self.months_in_history = None

    @property
    def total_still_owed(self):
        total_still_owed = 0.
        for loan in self.loans.values():
            total_still_owed += loan.amount_still_owed
        return total_still_owed

    def generate_debt_snowball_plan(self):
        """
        Generates a debt-snowball debt payment strategy plan.
        """
        # Initialize start of simulation parameters
        self._initialize_simulation()

        # Perform debt-snowball until total owed is paid
        months_passed = 0
        while self.total_still_owed > 0.:
            # Record current balances
            for loan_id,loan in self.loans.iteritems():
                self.balance_history[loan_id].append(loan.amount_still_owed)

            # Compute, record, and apply debt-snowball payments
            payments = self.get_debt_snowball_payment_installment()
            for loan_id,loan in self.loans.iteritems():
                self.payment_history[loan_id].append(payments[loan_id])
                loan.amount_still_owed -= payments[loan_id]

            # Compute and record interest earned in current pay cycle,
            # then update amount owed on each loan with earned interest
            for loan_id,loan in self.loans.iteritems():
                earned_interest = loan.compute_single_cycle_earned_interest_simulation()
                self.interest_history[loan_id].append(earned_interest)
                loan.amount_still_owed += earned_interest

            # Increment month counter
            months_passed += 1

        # Update method used and total time passed
        self.method_used_name = 'Debt-Snowball'
        self.months_in_history = months_passed


    def get_debt_snowball_payment_installment(self):
        """
        Determines the amount to pay to each loan according to the
        debt-snowball procedure.
        """
        # Initialize empty payment dictionary
        payments = {}

        # Get minimum payments required on all loans
        for loan_id,loan in self.loans.iteritems():
            payments[loan_id] = loan.minimum_payment_simulation

        # Amount left after making minimum payments
        amount_left = self.budget_ceiling - np.sum(payments.values())

        # Up until remaining amount is used up, pay loans starting from
        # one with the lowest amount due
        loan_priority_ids = self.get_debt_snowball_loan_priority_ids()
        for loan_id in loan_priority_ids:
            loan_amount_still_owed = (self.loans[loan_id].amount_still_owed
                                      - payments[loan_id])
            if loan_amount_still_owed == 0.:
                continue
            elif amount_left <= loan_amount_still_owed:
                payments[loan_id] += amount_left
                break
            else:
                payments[loan_id] += loan_amount_still_owed
                amount_left -= loan_amount_still_owed

        # Return payment installment
        return payments

    def get_debt_snowball_loan_priority_ids(self):
        """
        Returns the list of loan IDs in order of lowest to greatest
        amount due.
        """
        loan_priority_dict = {loan_id:loan.amount_still_owed for (loan_id,loan) in self.loans.iteritems()}
        loan_priority_tuples = sorted(loan_priority_dict.items(), key=operator.itemgetter(1))
        loan_priority_ids = [loan_priority_tuple[0] for loan_priority_tuple in loan_priority_tuples]
        return loan_priority_ids

    def generate_debt_avalanche_plan(self):
        """
        Generates a debt-avalanche debt payment strategy plan.
        """
        # Initialize start of simulation parameters
        self._initialize_simulation()

        # Perform debt-avalanche until total owed is paid
        months_passed = 0
        while self.total_still_owed > 0.:
            # Record current balances
            for loan_id,loan in self.loans.iteritems():
                self.balance_history[loan_id].append(loan.amount_still_owed)

            # Compute, record, and apply debt-avalanche payments
            payments = self.get_debt_avalanche_payment_installment()
            for loan_id,loan in self.loans.iteritems():
                self.payment_history[loan_id].append(payments[loan_id])
                loan.amount_still_owed -= payments[loan_id]

            # Compute and record interest earned in current pay cycle,
            # then update amount owed on each loan with earned interest
            for loan_id,loan in self.loans.iteritems():
                earned_interest = loan.compute_single_cycle_earned_interest_simulation()
                self.interest_history[loan_id].append(earned_interest)
                loan.amount_still_owed += earned_interest

            # Increment month counter
            months_passed += 1

        # Update method used and total time passed
        self.method_used_name = 'Debt-Avalanche'
        self.months_in_history = months_passed

    def get_debt_avalanche_payment_installment(self):
        """
        Determines the amount to pay to each loan according to the
        debt-avalanche procedure.
        """
        # Initialize empty payment dictionary
        payments = {}

        # Get minimum payments required on all loans
        for loan_id,loan in self.loans.iteritems():
            payments[loan_id] = loan.minimum_payment_simulation

        # Amount left after making minimum payments
        amount_left = self.budget_ceiling - np.sum(payments.values())

        # Up until remaining amount is used up, pay loans starting from
        # one with the largest interest rate
        loan_priority_ids = self.get_debt_avalanche_loan_priority_ids()
        for loan_id in loan_priority_ids:
            loan_amount_still_owed = (self.loans[loan_id].amount_still_owed
                                      - payments[loan_id])
            if loan_amount_still_owed == 0.:
                continue
            elif amount_left <= loan_amount_still_owed:
                payments[loan_id] += amount_left
                break
            else:
                payments[loan_id] += loan_amount_still_owed
                amount_left -= loan_amount_still_owed

        # Return payment installment
        return payments

    def get_debt_avalanche_loan_priority_ids(self):
        """
        Returns the list of loan IDs in order of largest to smallest
        interest rate.
        """
        loan_priority_dict = {loan_id:loan.yearly_interest_rate for (loan_id,loan) in self.loans.iteritems()}
        loan_priority_tuples = sorted(loan_priority_dict.items(), key=operator.itemgetter(1))
        loan_priority_ids_s2l = [loan_priority_tuple[0] for loan_priority_tuple in loan_priority_tuples]
        loan_priority_ids_l2s = loan_priority_ids_s2l[::-1]
        return loan_priority_ids_l2s

    def generate_debt_spiral_plan(self):
        """
        Generates a debt-spiral debt payment strategy plan.
        """
        # Initialize start of simulation parameters
        self._initialize_simulation()

        # Perform debt-spiral until total owed is paid
        months_passed = 0
        while self.total_still_owed > 0.:
            # Record current balances
            for loan_id,loan in self.loans.iteritems():
                self.balance_history[loan_id].append(loan.amount_still_owed)

            # Compute, record, and apply debt-spiral payments
            payments = self.get_debt_spiral_payment_installment()
            for loan_id,loan in self.loans.iteritems():
                self.payment_history[loan_id].append(payments[loan_id])
                loan.amount_still_owed -= payments[loan_id]

            # Compute and record interest earned in current pay cycle,
            # then update amount owed on each loan with earned interest
            for loan_id,loan in self.loans.iteritems():
                earned_interest = loan.compute_single_cycle_earned_interest_simulation()
                self.interest_history[loan_id].append(earned_interest)
                loan.amount_still_owed += earned_interest

            # Increment month counter
            months_passed += 1

        # Update method used and total time passed
        self.method_used_name = 'Debt-Spiral'
        self.months_in_history = months_passed

    def get_debt_spiral_payment_installment(self):
        """
        Determines the amount to pay to each loan according to the
        debt-spiral procedure.
        """
        # Initialize empty payment dictionary
        payments = {}

        # Get minimum payments required on all loans
        for loan_id,loan in self.loans.iteritems():
            payments[loan_id] = loan.minimum_payment_simulation

        # Amount left after making minimum payments
        amount_left = self.budget_ceiling - np.sum(payments.values())

        # Up until remaining amount is used up, pay loans starting from
        # one with the largest ratio of interest rate to amount owed
        loan_priority_ids = self.get_debt_spiral_loan_priority_ids()
        for loan_id in loan_priority_ids:
            loan_amount_still_owed = (self.loans[loan_id].amount_still_owed
                                      - payments[loan_id])
            if loan_amount_still_owed == 0.:
                continue
            elif amount_left <= loan_amount_still_owed:
                payments[loan_id] += amount_left
                break
            else:
                payments[loan_id] += loan_amount_still_owed
                amount_left -= loan_amount_still_owed

        # Return payment installment
        return payments

    def get_debt_spiral_loan_priority_ids(self):
        """
        Returns the list of loan IDs in order of largest to smallest
        interest rate to amount owed ratio.
        """
        loan_priority_dict = {loan_id:loan.amount_still_owed/loan.apr for (loan_id,loan) in self.loans.iteritems()}
        loan_priority_tuples = sorted(loan_priority_dict.items(), key=operator.itemgetter(1))
        loan_priority_ids = [loan_priority_tuple[0] for loan_priority_tuple in loan_priority_tuples]
        return loan_priority_ids

    def generate_debt_optimized_plan(self):
        """
        Generates a debt-optimized debt payment strategy plan.
        """
        return

    def get_debt_optimized_payment_installment(self):
        """
        Determines the amount to pay to each loan according to the
        debt-optimized procedure.
        """
        return

    def print_plan_summary(self, dir_save=None):
        """
        Writes current stored payment plan to a text file for
        viewing/printing purposes.
        """
        # Initialize file text
        file_txt = ['pyDebtFree: %s Approach\n'%(self.method_used_name)]

        # Create column labels
        loan_names = [loan.name for loan in self.loans.values()]
        clabels_owed = ['Months'] + ['%s [Owed]'%name for name in loan_names] + ['Total Owed']
        clabels_paid = ['Months'] + ['%s [Paid]'%name for name in loan_names] + ['Total Paid']
        clabels_interest = ['Months', 'Interest Earned', 'Total Interest']

        # Initialize header row txt and plan summary containers
        header_txt_owed = ['%16s'%(label) for label in clabels_owed] + ['\n']
        header_txt_paid = ['%16s'%(label) for label in clabels_paid] + ['\n']
        header_txt_interest = ['%16s'%(label) for label in clabels_interest] + ['\n']
        history_owed_txt = ['']
        history_paid_txt = ['']
        history_interest_txt = ['']

        # Add plan simulation history
        running_total_paid = 0.
        running_total_interest = 0.
        for imonth in range(self.months_in_history):
            # Pull necessary information
            owes  = [self.balance_history[loan_id][imonth] for loan_id in self.loans.keys()]
            pays  = [self.payment_history[loan_id][imonth] for loan_id in self.loans.keys()]
            running_total_paid += np.sum(np.array(pays))
            monthly_interest = np.sum(np.array([self.interest_history[loan_id][imonth] for loan_id in self.loans.keys()]))
            running_total_interest += monthly_interest

            # Add as row
            history_owed_txt += ['%16s'%(imonth+1)] + ['%16.2f'%val for val in owes] + ['%16.2f'%(np.sum(owes))] + ['\n']
            history_paid_txt += ['%16s'%(imonth+1)] + ['%16.2f'%val for val in pays] + ['%16.2f'%(running_total_paid)] + ['\n']
            history_interest_txt += ['%16s'%(imonth+1)] + ['%16.2f'%(monthly_interest)]  + ['%16.2f'%(running_total_interest)] + ['\n']

        # Combine txt into single file
        file_txt += header_txt_owed + history_owed_txt + ['\n']*3
        file_txt += header_txt_paid + history_paid_txt + ['\n']*3
        file_txt += header_txt_interest + history_interest_txt

        # Determine file output path
        outname = '%s.txt'%(self.method_used_name)
        if dir_save is None:
            dir_save = os.getcwd()
        path_save = os.path.join(dir_save, outname)

        # Write textto file
        with open(path_save, 'w') as outfile:
            outfile.writelines(file_txt)

    def _initialize_simulation(self):
        """
        Initialize start of payment plan by setting amount due to
        principal loan amounts and resetting payment/balance history.
        """
        # Initialize amounts still owed
        # Initialize payment/balance/interest history
        self.payment_history  = {}
        self.balance_history  = {}
        self.interest_history = {}
        self.method_used_name = None
        self.months_in_history = None
        for loan_id,loan in self.loans.iteritems():
            loan.amount_still_owed = 1.*loan.principal_amount
            self.payment_history[loan_id] = []
            self.balance_history[loan_id] = []
            self.interest_history[loan_id] = []

def main():
    print('No default behavior.')

if __name__ == "__main__":
    main()
