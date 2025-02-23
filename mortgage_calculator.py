import numpy as np
from numpy_financial import rate
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_total_amortization(
        loan_amount, 
        number_of_payments, 
        monthly_interest_rate, 
        number_of_early_payments, 
        monthly_early_payments
):
    # ====================================================
    # =========         Normal payment        ============
    # ====================================================
    # Calculate the monthly payment amount
    monthly_payment = (monthly_interest_rate * loan_amount) \
                    / (1 - (1 + monthly_interest_rate) ** -number_of_payments)

    # Initialize lists to store the results
    total_interest_paid = [0]
    total_principal_paid = [0]
    total_amount_paid = [0]
    remaining_balance = [loan_amount]

    # Calculate the amortization schedule for each month
    for _ in range(number_of_payments):
        # Calculate the interest paid for the current month
        interest_payment = remaining_balance[-1] * monthly_interest_rate

        # Calculate the principal paid for the current month
        principal_payment = monthly_payment - interest_payment

        # Calculate the remaining balance after the current payment
        remaining_balance.append(remaining_balance[-1] - principal_payment)

        # Append the results to the lists
        total_interest_paid.append(interest_payment + total_interest_paid[-1])
        total_principal_paid.append(principal_payment + total_principal_paid[-1])
        total_amount_paid.append(total_interest_paid[-1] + total_principal_paid[-1])

    
    # ====================================================
    # ==========  With early principal payment  ==========
    # ====================================================
    # Initialize lists to store the results
    adjusted_total_interest_paid = [0]
    adjusted_total_principal_paid = [0]
    adjusted_total_amount_paid = [0]
    adjusted_remaining_balance = [loan_amount]

    # Calculate the amortization schedule for each month
    for i in range(number_of_payments):
        X = adjusted_remaining_balance[-1]
        if X > 0:
            interest_payment = X * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment

            if i < number_of_early_payments:
                principal_payment += monthly_early_payments
        else:
            interest_payment = 0
            principal_payment = 0

        adjusted_remaining_balance.append(X - principal_payment)
        adjusted_total_interest_paid.append(interest_payment \
                                            + adjusted_total_interest_paid[-1])
        adjusted_total_principal_paid.append(principal_payment \
                                             + adjusted_total_principal_paid[-1])
        adjusted_total_amount_paid.append(adjusted_total_interest_paid[-1] \
                                          + adjusted_total_principal_paid[-1])

    return (total_interest_paid, 
            total_principal_paid, 
            total_amount_paid, 
            remaining_balance, 
            adjusted_total_interest_paid, 
            adjusted_total_principal_paid, 
            adjusted_total_amount_paid, 
            adjusted_remaining_balance)


def calculate_monthly_amortization(
        loan_amount, 
        number_of_payments, 
        monthly_interest_rate, 
        number_of_early_payments, 
        monthly_early_payments
):
    # ====================================================
    # =========         Normal payment        ============
    # ====================================================
    # Calculate the monthly payment amount
    monthly_payment = (monthly_interest_rate * loan_amount) \
                    / (1 - (1 + monthly_interest_rate) ** -number_of_payments)

    # Initialize lists to store the results
    monthly_interest_paid = [0]
    monthly_principal_paid = [0]
    monthly_amount_paid = [0]
    remaining_balance = [loan_amount]

    # Calculate the amortization schedule for each month
    for _ in range(number_of_payments):
        # Calculate the interest paid for the current month
        interest_payment = remaining_balance[-1] * monthly_interest_rate

        # Calculate the principal paid for the current month
        principal_payment = monthly_payment - interest_payment

        # Calculate the remaining balance after the current payment
        remaining_balance.append(remaining_balance[-1] - principal_payment)

        # Append the results to the lists
        monthly_interest_paid.append(interest_payment)
        monthly_principal_paid.append(principal_payment)
        monthly_amount_paid.append(monthly_interest_paid[-1] + monthly_principal_paid[-1])

    # ====================================================
    # ==========  With early principal payment  ==========
    # ====================================================
    # Initialize lists to store the results
    adjusted_monthly_interest_paid = [0]
    adjusted_monthly_principal_paid = [0]
    adjusted_monthly_amount_paid = [0]
    adjusted_remaining_balance = [loan_amount]

    # Calculate the amortization schedule for each month
    for i in range(number_of_payments):
        X = adjusted_remaining_balance[-1]
        if X > 0:
            interest_payment = X * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment

            if i < number_of_early_payments:
                principal_payment += monthly_early_payments
        else:
            interest_payment = 0
            principal_payment = 0

        adjusted_remaining_balance.append(X - principal_payment)
        adjusted_monthly_interest_paid.append(interest_payment)
        adjusted_monthly_principal_paid.append(principal_payment)
        adjusted_monthly_amount_paid.append(principal_payment + interest_payment)

    return (monthly_interest_paid[1:], 
            monthly_principal_paid[1:], 
            monthly_amount_paid[1:],
            adjusted_monthly_interest_paid[1:], 
            adjusted_monthly_principal_paid[1:], 
            adjusted_monthly_amount_paid[1:])

def calculate_mortgage_ear(number_of_payments, total_interest, total_principal):
    """
    Calculates the effective annual interest rate (EAR) for a mortgage.

    Args:
    number_of_payments: The loan term in months.
    total_interest: The total amount of interest paid over the loan term (float).
    total_principal: The original amount of the loan (principal) (float).

    Returns:
    The effective annual interest rate (EAR) as a decimal (float).
    """

    # Calculate the monthly payment
    monthly_payment = (total_interest + total_principal) / number_of_payments

    # Use the RATE function (needs to be imported from a library like numpy_financial) 
    periodic_rate = rate(number_of_payments, -monthly_payment, total_principal, 0)

    # Calculate the APR (Annual Percentage Rate)
    apr = periodic_rate * 12

    # Calculate the EAR (Effective Annual Rate)
    ear = (1 + apr/12)**12 - 1

    return ear

def calculate_mortgage():
    """Calculates mortgage and updates GUI with results and plot."""
    try:
        loan_amount = float(loan_entry.get())
        monthly_interest_rate = float(interest_entry.get()) / 100 / 12
        number_of_payments = int(term_entry.get()) * 12
        number_of_early_payments = int(early_term_entry.get()) * 12
        monthly_early_payments = float(early_amount_entry.get())
        cap_return_rate = float(capital_return_entry.get())
        rs_return_rate = float(real_estate_return_entry.get())
        effective_rent = float(effective_rent_entry.get())
        
        # Calculate monthly payment
        monthly_payment = (monthly_interest_rate * loan_amount) \
                    / (1 - (1 + monthly_interest_rate) ** -number_of_payments)

        # Calculate amortization schedule using the function
        (total_interest_paid, 
         total_principal_paid, 
         total_amount_paid, 
         remaining_balance, 
         adjusted_total_interest_paid, 
         adjusted_total_principal_paid, 
         adjusted_total_amount_paid, 
         adjusted_remaining_balance) \
        = calculate_total_amortization(
            loan_amount, 
            number_of_payments, 
            monthly_interest_rate, 
            number_of_early_payments, 
            monthly_early_payments
        )

        # Calculate amortization schedule using the function
        (monthly_interest_paid, 
         monthly_principal_paid, 
         monthly_amount_paid,
         adjusted_monthly_interest_paid, 
         adjusted_monthly_principal_paid, 
         adjusted_monthly_amount_paid) \
        = calculate_monthly_amortization(
            loan_amount, 
            number_of_payments, 
            monthly_interest_rate, 
            number_of_early_payments, 
            monthly_early_payments
        )

        # Plotting
        figure = plt.Figure(figsize=(4, 3), dpi=400)
        ax = figure.add_subplot(111)
        ax.plot(total_interest_paid, label='Interest k($)', color='bisque')
        ax.plot(total_principal_paid, label='Principal k($)', color='lightgreen')
        ax.plot(total_amount_paid, label='Total Paid k($)', color='lightcoral')
        ax.plot(remaining_balance, label='Remain Principal k($)', color='lightskyblue')
        if number_of_early_payments > 0:
            ax.plot(adjusted_total_interest_paid, label='Adjusted Interest k($)', color='darkorange')
            ax.plot(adjusted_total_principal_paid, label='Adjusted Principal k($)', color='darkgreen')
            ax.plot(adjusted_total_amount_paid, label='Adjusted Total Paid k($)', color='firebrick')
            ax.plot(adjusted_remaining_balance, label='Adjusted Remain Principal k($)', color='darkblue')
        ax.set_xlabel("Month", fontsize="5")
        ax.set_ylabel("Amount Paid k($)", fontsize="5")
        ax.tick_params(axis='x', labelsize=5)
        ax.tick_params(axis='y', labelsize=5)

        ax.grid(True, 'both')
        ax.legend(fontsize="3", loc ="upper left")

        # Enable minor ticks
        ax.minorticks_on()

        canvas_1 = FigureCanvasTkAgg(figure, master=root)
        canvas_1.draw()
        canvas_1.get_tk_widget().grid(row=7, column=0, columnspan=2)

        figure = plt.Figure(figsize=(4, 3), dpi=400)
        ax = figure.add_subplot(111)
        ax.plot(monthly_interest_paid, label='Monthly Interest k($)', color='bisque')
        ax.plot(monthly_principal_paid, label='Monthly Principal k($)', color='lightgreen')
        ax.plot(monthly_amount_paid, label='Monthly Total k($)', color='lightcoral')
        if number_of_early_payments > 0:
            ax.plot(adjusted_monthly_interest_paid, label='Adjusted Monthly Interest k($)', color='darkorange')
            ax.plot(adjusted_monthly_principal_paid, label='Adjusted Monthly Principal k($)', color='darkgreen')
            ax.plot(adjusted_monthly_amount_paid, label='Adjusted Monthly Total k($)', color='firebrick')
        ax.set_xlabel("Month", fontsize="5")
        ax.set_ylabel("Amount Paid k($)", fontsize="5")
        ax.tick_params(axis='x', labelsize=5)
        ax.tick_params(axis='y', labelsize=5)

        ax.grid(True, 'both')
        ax.legend(fontsize="3", loc ="upper right")

        # Enable minor ticks
        ax.minorticks_on()

        canvas_2 = FigureCanvasTkAgg(figure, master=root)
        canvas_2.draw()
        canvas_2.get_tk_widget().grid(row=7, column=2, columnspan=2)

        # Calculate Effective Interest Rate
        effective_number_of_payments = np.sum(np.array(adjusted_monthly_amount_paid) > 0)
        ear = calculate_mortgage_ear(effective_number_of_payments, 
                                     1e3 * adjusted_total_interest_paid[-1], 
                                     1e3 *  loan_amount)
        if number_of_early_payments > 0:
            txt = "Original: payout after %d months, monthly payment: $ %.2fK\n" % (number_of_payments, monthly_payment) + \
                "Adjusted: payout after %d months, effective interest rate: $ %.2f%%\n" % (effective_number_of_payments, 100 * ear)
        else:
            txt = "Monthly payment: $ %.2fK, total payment amount: $ %.2fK" % (monthly_payment, total_amount_paid[-1])
        result_label.config(text=txt)

    except ValueError:
        result_label.config(text="Invalid input. Please enter numbers only.")

# Create the main window
root = tk.Tk()
root.title("Mortgage Calculator")

# Loan amount input
loan_label = ttk.Label(root, text="Loan Amount k ($):")
loan_label.grid(row=0, column=0, padx=10, pady=10)
loan_entry = ttk.Entry(root)
loan_entry.insert(0, "1400")
loan_entry.grid(row=0, column=1, padx=10, pady=10)

# Interest rate input
interest_label = ttk.Label(root, text="Annual interest Rate (%):")
interest_label.grid(row=1, column=0, padx=10, pady=10)
interest_entry = ttk.Entry(root)
interest_entry.insert(0, "5.5")
interest_entry.grid(row=1, column=1, padx=10, pady=10)

# Loan term input
term_label = ttk.Label(root, text="Loan Term (Years):")
term_label.grid(row=2, column=0, padx=10, pady=10)
term_entry = ttk.Entry(root)
term_entry.insert(0, "30")
term_entry.grid(row=2, column=1, padx=10, pady=10)

# Early payment term input
early_term_label = ttk.Label(root, text="Early Payment Term (Years):")
early_term_label.grid(row=3, column=0, padx=10, pady=10)
early_term_entry = ttk.Entry(root)
early_term_entry.insert(0, "5")
early_term_entry.grid(row=3, column=1, padx=10, pady=10)

# Early payment amount input
early_amount_label = ttk.Label(root, text="Early Payment Amount k($):")
early_amount_label.grid(row=4, column=0, padx=10, pady=10)
early_amount_entry = ttk.Entry(root)
early_amount_entry.insert(0, "4")
early_amount_entry.grid(row=4, column=1, padx=10, pady=10)


# capital investment return rate input
capital_return_label = ttk.Label(root, text="Capital investment return rate %:")
capital_return_label.grid(row=0, column=2, padx=10, pady=10)
capital_return_entry = ttk.Entry(root)
capital_return_entry.insert(0, "3.5")
capital_return_entry.grid(row=0, column=3, padx=10, pady=10)

# real estate return rate input
real_estate_return_label = ttk.Label(root, text="Real estate return rate %:")
real_estate_return_label.grid(row=1, column=2, padx=10, pady=10)
real_estate_return_entry = ttk.Entry(root)
real_estate_return_entry.insert(0, "3.5")
real_estate_return_entry.grid(row=1, column=3, padx=10, pady=10)

# Effective rent input
effective_rent_label = ttk.Label(root, text="Effective rent k($):")
effective_rent_label.grid(row=2, column=2, padx=10, pady=10)
effective_rent_entry = ttk.Entry(root)
effective_rent_entry.insert(0, "4")
effective_rent_entry.grid(row=2, column=3, padx=10, pady=10)


# Calculate button
calculate_button = ttk.Button(root, text="Calculate", command=calculate_mortgage)
calculate_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

# Result label
result_label = ttk.Label(root, text="")
result_label.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

root.mainloop()
