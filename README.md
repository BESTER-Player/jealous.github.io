# jealous.github.io

import tkinter as tk
from tkinter import ttk
import re
import sqlite3
import math

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('calculation_data.db')
c = conn.cursor()

# Tabellen erstellen, falls sie noch nicht existieren
c.execute('''CREATE TABLE IF NOT EXISTS BankInvestment
             (id INTEGER PRIMARY KEY, monthly_payment REAL, annual_interest_rate REAL, num_years INTEGER, future_value REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS FlatInvestment
             (id INTEGER PRIMARY KEY, monthly_rental_income REAL, annual_appreciation_rate REAL, property_price REAL,
             closing_costs REAL, loan_term_years INTEGER, loan_interest_rate REAL, future_value REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS IncomeTaxCalculation
             (id INTEGER PRIMARY KEY, income REAL, tax_class INTEGER, num_children INTEGER, income_tax REAL, tax_rate REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS MonthlyIncomeSpending
             (id INTEGER PRIMARY KEY, monthly_income REAL, additional_costs REAL, monthly_health_insurance REAL,
             monthly_car_insurance REAL, retirement_insurance REAL, occupational_disability_insurance REAL,
             household_and_homeowners_insurance REAL, monthly_car_costs REAL, financial_balance REAL)''')

def convert_to_float(value):
    if re.match(r'^\d+€$', value):  # Euro
        return float(value[:-1])
    elif re.match(r'^\d+%$', value):  # Prozent
        return float(value[:-1]) / 100
    else:
        return None


def calculate_future_value_bank():
    monthly_payment = convert_to_float(monthly_payment_var.get())
    annual_interest_rate = convert_to_float(interest_rate_var.get())
    num_years = int(num_years_var.get())

    if monthly_payment is None or annual_interest_rate is None:
        bank_result_label.config(text="Ungültige Eingabe!")
        return

    monthly_interest_rate = annual_interest_rate / 12
    num_periods = num_years * 12

    future_value = monthly_payment * (((1 + monthly_interest_rate) ** num_periods) - 1) / monthly_interest_rate

    bank_result_label.config(text="Der zukünftige Wert Ihres Bankkontos beträgt: {:.2f} Euro".format(future_value))

    c.execute(
        "INSERT INTO BankInvestment (monthly_payment, annual_interest_rate, num_years, future_value) VALUES (?, ?, ?, ?)",
        (monthly_payment, annual_interest_rate, num_years, future_value))
    conn.commit()

def calculate_future_value_flat():
    monthly_rental_income = convert_to_float(monthly_rental_income_var.get())
    annual_appreciation_rate = convert_to_float(annual_appreciation_rate_var.get())
    property_price = convert_to_float(property_price_var.get())
    loan_interest_rate = convert_to_float(loan_interest_rate_var.get())
    closing_costs = property_price * 0.02  # Annahme: 2% der Immobilienkosten für Abschlusskosten

    if None in [monthly_rental_income, annual_appreciation_rate, property_price, loan_interest_rate]:
        flat_result_label.config(text="Ungültige Eingabe!")
        return

    # Annahme: Annuität entspricht der monatlichen Miete
    monthly_payment = monthly_rental_income

    # Berechnung des Kreditbetrags (Hypothekendarlehen)
    loan_amount = property_price + closing_costs

    # Berechnung der monatlichen Zinsen
    monthly_interest_rate = loan_interest_rate / 12

    # Berechnung der Anzahl der Monate (Laufzeit), um den Kredit zurückzuzahlen
    numerator = math.log(monthly_payment / (monthly_payment - loan_amount * monthly_interest_rate))
    denominator = math.log(1 + monthly_interest_rate)
    loan_term_months = math.ceil(numerator / denominator)

    # Berechnung des zukünftigen Wertes der Investition
    future_value = 0
    remaining_loan_amount = loan_amount
    for _ in range(loan_term_months):
        remaining_loan_amount *= (1 + monthly_interest_rate)  # Zinseszins-Effekt
        monthly_principal_payment = monthly_payment - remaining_loan_amount * monthly_interest_rate
        future_value += monthly_rental_income - monthly_principal_payment
        remaining_loan_amount -= monthly_principal_payment

    # Berechnung der jährlichen Rendite
    initial_investment = property_price + closing_costs
    annual_return = (future_value - initial_investment) / initial_investment * 100

    # Ausgabe der Ergebnisse
    result_text = "Der zukünftige Wert Ihrer Investition beträgt: {:.2f} Euro.\n".format(future_value)
    result_text += "Die jährliche Rendite beträgt: {:.2f}%.".format(annual_return)

    flat_result_label.config(text=result_text)

    c.execute(
        "INSERT INTO FlatInvestment (monthly_rental_income, annual_appreciation_rate, property_price, closing_costs, loan_term_years, loan_interest_rate, future_value, annual_return) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (monthly_rental_income, annual_appreciation_rate, property_price, closing_costs, loan_term_months // 12,
         loan_interest_rate, future_value, annual_return))
    conn.commit()



def calculate_income_tax(income, tax_class, num_children):
    global tax, tax_rate
    kindergeld = num_children * 250  # Kindergeld pro Monat
    income -= kindergeld * 12  # Jahreskindergeld vom Einkommen abziehen
    if tax_class == 1:
        if income <= 9408:
            tax = 0
            tax_rate = 0
        elif income <= 14532:
            tax = (income - 9408) * 0.14
            tax_rate = 0.14
        elif income <= 57051:
            tax = (income - 14532) * 0.42 + 717.76
            tax_rate = 0.42
        else:
            tax = (income - 57051) * 0.45 + 18002.76
            tax_rate = 0.45
    elif tax_class == 2:
        if income <= 9408:
            tax = 0
            tax_rate = 0
        elif income <= 14532:
            tax = (income - 9408) * 0.14
            tax_rate = 0.14
        elif income <= 57051:
            tax = (income - 14532) * 0.42 + 717.76
            tax_rate = 0.42
        else:
            tax = (income - 57051) * 0.45 + 18002.76
            tax_rate = 0.45
    elif tax_class == 3:
        if income <= 9408:
            tax = 0
            tax_rate = 0
        elif income <= 14532:
            tax = (income - 9408) * 0.14
            tax_rate = 0.14
        elif income <= 57051:
            tax = (income - 14532) * 0.42 + 717.76
            tax_rate = 0.42
        else:
            tax = (income - 57051) * 0.45 + 18002.76
            tax_rate = 0.45
    elif tax_class == 4:
        if income <= 9408:
            tax = 0
            tax_rate = 0
        elif income <= 14532:
            tax = (income - 9408) * 0.14
            tax_rate = 0.14
        elif income <= 57051:
            tax = (income - 14532) * 0.42 + 717.76
            tax_rate = 0.42
        else:
            tax = (income - 57051) * 0.45 + 18002.76
            tax_rate = 0.45
    elif tax_class == 5:
        tax = income * 0.6
        tax_rate = 0.6
    elif tax_class == 6:
        tax = income * 0.6
        tax_rate = 0.6
    return tax, tax_rate


def calculate_church_tax(income_tax):
    church_tax = income_tax * 0.08
    return church_tax


def calculate_social_security_contributions(income):
    pension_insurance = income * 0.093
    health_insurance = income * 0.072
    long_term_care_insurance = income * 0.015
    unemployment_insurance = income * 0.012
    return pension_insurance + health_insurance + long_term_care_insurance + unemployment_insurance


def calculate_net_income():
    income = convert_to_float(income_var.get())
    tax_class = int(tax_class_var.get())
    num_children = int(num_children_var.get())

    if income is None:
        net_income_result_label.config(text="Ungültige Eingabe!")
        return

    income_tax, tax_rate = calculate_income_tax(income, tax_class, num_children)
    church_tax = calculate_church_tax(income_tax)
    social_security_contributions = calculate_social_security_contributions(income)
    net_income = income - income_tax - church_tax - social_security_contributions

    net_income_result_label.config(text="Ihr Nettoeinkommen beträgt: {:.2f} Euro".format(net_income))
    tax_rate_label.config(text="Ihr Lohnsteuersatz beträgt: {:.2f}%".format(tax_rate * 100))
    c.execute(
        "INSERT INTO IncomeTaxCalculation (income, tax_class, num_children, income_tax, tax_rate) VALUES (?, ?, ?, ?, ?)",
        (income, tax_class, num_children, income_tax, tax_rate))
    conn.commit()

def monthly_income_spending():
    monthly_income = convert_to_float(monthly_income_var.get())
    monthly_additional_cost = convert_to_float(additional_costs_var.get())
    monthly_insurance_rate = (
            convert_to_float(monthly_helath_insurance_var.get()) +
            convert_to_float(monthly_car_insurance_var.get()) +
            convert_to_float(retirement_insurance_var.get()) +
            convert_to_float(occupational_disability_insurance_var.get()) +
            convert_to_float(household_and_homeowners_insurance_var.get())
    )
    monthly_car_costs = convert_to_float(monthly_car_costs_var.get())
    financial_balance = monthly_income - monthly_car_costs - monthly_additional_cost - monthly_insurance_rate

    monthly_income_spending_label.config(
        text="Die monatliche Finanz Balance beträgt: {:.2f} Euro".format(financial_balance))

    c.execute(
    "INSERT INTO MonthlyIncomeSpending (monthly_income, additional_costs, monthly_health_insurance, monthly_car_insurance, retirement_insurance, occupational_disability_insurance, household_and_homeowners_insurance, monthly_car_costs, financial_balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (monthly_income, monthly_additional_cost, monthly_helath_insurance_var, monthly_car_insurance_var, retirement_insurance_var, occupational_disability_insurance_var, household_and_homeowners_insurance_var, monthly_car_costs, financial_balance))
    conn.commit()

def show_income_tax_frame():
    bank_frame.grid_forget()
    flat_frame.grid_forget()
    stock_frame.grid_forget()
    monthly_income_spending_frame.grid_forget()
    income_tax_frame.grid(column=0, row=3, columnspan=2, sticky="nsew")


def show_bank_frame():
    income_tax_frame.grid_forget()
    flat_frame.grid_forget()
    monthly_income_spending_frame.grid_forget()
    bank_frame.grid(column=0, row=3, columnspan=2, sticky="nsew")


def show_flat_frame():
    income_tax_frame.grid_forget()
    bank_frame.grid_forget()
    monthly_income_spending_frame.grid_forget()
    flat_frame.grid(column=0, row=3, columnspan=2, sticky="nsew")


def show_monthly_income_spending_frame():
    income_tax_frame.grid_forget()
    bank_frame.grid_forget()
    flat_frame.grid_forget()
    monthly_income_spending_frame.grid(column=0, row=3, columnspan=2, sticky="nsew")


root = tk.Tk()
root.title("Investitions- und Einkommensrechner")
root.configure(bg="gray")
# Menüleiste erstellen
menubar = tk.Menu(root)
root.config(menu=menubar)

# Menü "Berechnungsart" erstellen
calculation_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Berechnungsart", menu=calculation_menu)

# Menüoptionen hinzufügen
calculation_menu.add_command(label="Bankinvestment", command=show_bank_frame)
calculation_menu.add_command(label="Wohnungsinvestment", command=show_flat_frame)
calculation_menu.add_command(label="Einkommenssteuerberechnung", command=show_income_tax_frame)
calculation_menu.add_command(label="Monatliche Finanzbalnce", command=show_monthly_income_spending_frame)

# Hauptfenster Layout
mainframe = ttk.Frame(root, padding="20")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Bankinvestment GUI
bank_frame = ttk.Frame(mainframe, padding="10")
bank_frame.columnconfigure(0, weight=1)
bank_frame.columnconfigure(1, weight=1)
bank_frame.rowconfigure(1, weight=1)

# Wohnungsinvestment GUI
flat_frame = ttk.Frame(mainframe, padding="10")
flat_frame.columnconfigure(0, weight=1)
flat_frame.columnconfigure(1, weight=1)
flat_frame.rowconfigure(1, weight=1)

# Einkommenssteuerberechnung GUI
income_tax_frame = ttk.Frame(mainframe, padding="10")
income_tax_frame.columnconfigure(0, weight=1)
income_tax_frame.columnconfigure(1, weight=1)
income_tax_frame.rowconfigure(1, weight=1)

# Monatliche Finanzbalance GUI
monthly_income_spending_frame = ttk.Frame(mainframe, padding="10")
monthly_income_spending_frame.columnconfigure(0, weight=1)
monthly_income_spending_frame.columnconfigure(1, weight=1)
monthly_income_spending_frame.rowconfigure(1, weight=1)

# Bankinvestment GUI-Elemente
monthly_payment_label = ttk.Label(bank_frame, text="Monatliche Einzahlung:")
monthly_payment_label.grid(column=0, row=0, sticky=tk.W)

monthly_payment_var = tk.StringVar()
monthly_payment_entry = ttk.Entry(bank_frame, textvariable=monthly_payment_var)
monthly_payment_entry.grid(column=1, row=0)

interest_rate_label = ttk.Label(bank_frame, text="Jährlicher Zinssatz:")
interest_rate_label.grid(column=0, row=1, sticky=tk.W)

interest_rate_var = tk.StringVar()
interest_rate_entry = ttk.Entry(bank_frame, textvariable=interest_rate_var)
interest_rate_entry.grid(column=1, row=1)

num_years_label = ttk.Label(bank_frame, text="Anzahl der Jahre:")
num_years_label.grid(column=0, row=2, sticky=tk.W)

num_years_var = tk.StringVar()
num_years_entry = ttk.Entry(bank_frame, textvariable=num_years_var)
num_years_entry.grid(column=1, row=2)

calculate_button = ttk.Button(bank_frame, text="Berechnen", command=calculate_future_value_bank)
calculate_button.grid(column=0, row=3, columnspan=2, pady=10)

bank_result_label = ttk.Label(bank_frame, text="")
bank_result_label.grid(column=0, row=4, columnspan=2)

# Wohnungsinvestment GUI-Elemente
monthly_rental_income_label = ttk.Label(flat_frame, text="Monatliche Mieteinnahmen:")
monthly_rental_income_label.grid(column=0, row=0, sticky=tk.W)

monthly_rental_income_var = tk.StringVar()
monthly_rental_income_entry = ttk.Entry(flat_frame, textvariable=monthly_rental_income_var)
monthly_rental_income_entry.grid(column=1, row=0)

annual_appreciation_rate_label = ttk.Label(flat_frame, text="Jährliche Wertsteigerung:")
annual_appreciation_rate_label.grid(column=0, row=1, sticky=tk.W)

annual_appreciation_rate_var = tk.StringVar()
annual_appreciation_rate_entry = ttk.Entry(flat_frame, textvariable=annual_appreciation_rate_var)
annual_appreciation_rate_entry.grid(column=1, row=1)

property_price_label = ttk.Label(flat_frame, text="Kaufpreis:")
property_price_label.grid(column=0, row=2, sticky=tk.W)

property_price_var = tk.StringVar()
property_price_entry = ttk.Entry(flat_frame, textvariable=property_price_var)
property_price_entry.grid(column=1, row=2)

loan_term_label = ttk.Label(flat_frame, text="Kreditlaufzeit (Jahre):")
loan_term_label.grid(column=0, row=3, sticky=tk.W)

loan_term_var = tk.StringVar()
loan_term_entry = ttk.Entry(flat_frame, textvariable=loan_term_var)
loan_term_entry.grid(column=1, row=3)

loan_interest_rate_label = ttk.Label(flat_frame, text="Kreditzins:")
loan_interest_rate_label.grid(column=0, row=4, sticky=tk.W)

loan_interest_rate_var = tk.StringVar()
loan_interest_rate_entry = ttk.Entry(flat_frame, textvariable=loan_interest_rate_var)
loan_interest_rate_entry.grid(column=1, row=4)

calculate_flat_button = ttk.Button(flat_frame, text="Berechnen", command=calculate_future_value_flat)
calculate_flat_button.grid(column=0, row=5, columnspan=2, pady=10)

flat_result_label = ttk.Label(flat_frame, text="")
flat_result_label.grid(column=0, row=6, columnspan=2)

# GUI-Elemente für die monatliche Einkommensberechnung
monthly_income_label = ttk.Label(monthly_income_spending_frame, text="Monatliches Einkommen:")
monthly_income_label.grid(column=0, row=0, sticky=tk.W)

monthly_income_var = tk.StringVar()
monthly_income_entry = ttk.Entry(monthly_income_spending_frame, textvariable=monthly_income_var)
monthly_income_entry.grid(column=1, row=0)

# Zusätzliche monatliche Kosten GUI-Elemente
additional_costs_label = ttk.Label(monthly_income_spending_frame, text="Zusätzliche monatliche Kosten:")
additional_costs_label.grid(column=0, row=1, sticky=tk.W)

additional_costs_var = tk.StringVar()
additional_costs_entry = ttk.Entry(monthly_income_spending_frame, textvariable=additional_costs_var)
additional_costs_entry.grid(column=1, row=1)

# Monatliche Krankenversicherung GUI-Elemente
monthly_helath_insurance_label = ttk.Label(monthly_income_spending_frame, text="Monatliche Krankenversicherung:")
monthly_helath_insurance_label.grid(column=0, row=2, sticky=tk.W)

monthly_helath_insurance_var = tk.StringVar()
monthly_helath_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=monthly_helath_insurance_var)
monthly_helath_insurance_entry.grid(column=1, row=2)

# Monatliche Kfz-Versicherung GUI-Elemente
monthly_car_insurance_label = ttk.Label(monthly_income_spending_frame, text="Monatliche Kfz-Versicherung:")
monthly_car_insurance_label.grid(column=0, row=3, sticky=tk.W)

monthly_car_insurance_var = tk.StringVar()
monthly_car_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=monthly_car_insurance_var)
monthly_car_insurance_entry.grid(column=1, row=3)

# Monatliche Rentenversicherung GUI-Elemente
retirement_insurance_label = ttk.Label(monthly_income_spending_frame, text="Monatliche Rentenversicherung:")
retirement_insurance_label.grid(column=0, row=4, sticky=tk.W)

retirement_insurance_var = tk.StringVar()
retirement_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=retirement_insurance_var)
retirement_insurance_entry.grid(column=1, row=4)

# Berufsunfähigkeitsversicherung GUI-Elemente
occupational_disability_insurance_label = ttk.Label(monthly_income_spending_frame, text="Berufsunfähigkeitsversicherung:")
occupational_disability_insurance_label.grid(column=0, row=5, sticky=tk.W)

occupational_disability_insurance_var = tk.StringVar()
occupational_disability_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=occupational_disability_insurance_var)
occupational_disability_insurance_entry.grid(column=1, row=5)

# Haftpflicht- und Hausratversicherung GUI-Elemente
household_and_homeowners_insurance_label = ttk.Label(monthly_income_spending_frame, text="Haftpflicht- und Hausratversicherung:")
household_and_homeowners_insurance_label.grid(column=0, row=6, sticky=tk.W)

household_and_homeowners_insurance_var = tk.StringVar()
household_and_homeowners_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=household_and_homeowners_insurance_var)
household_and_homeowners_insurance_entry.grid(column=1, row=6)

# Zusätzliche monatliche Kosten GUI-Elemente
additional_costs_label = ttk.Label(monthly_income_spending_frame, text="Zusätzliche monatliche Kosten:")
additional_costs_label.grid(column=0, row=1, sticky=tk.W)

additional_costs_var = tk.StringVar()
additional_costs_entry = ttk.Entry(monthly_income_spending_frame, textvariable=additional_costs_var)
additional_costs_entry.grid(column=1, row=1)

# Monatliche Krankenversicherung GUI-Elemente
monthly_helath_insurance_label = ttk.Label(monthly_income_spending_frame, text="Monatliche Krankenversicherung:")
monthly_helath_insurance_label.grid(column=0, row=2, sticky=tk.W)

monthly_helath_insurance_var = tk.StringVar()
monthly_helath_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=monthly_helath_insurance_var)
monthly_helath_insurance_entry.grid(column=1, row=2)

# Monatliche Kfz-Versicherung GUI-Elemente
monthly_car_insurance_label = ttk.Label(monthly_income_spending_frame, text="Monatliche Kfz-Versicherung:")
monthly_car_insurance_label.grid(column=0, row=3, sticky=tk.W)

monthly_car_insurance_var = tk.StringVar()
monthly_car_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=monthly_car_insurance_var)
monthly_car_insurance_entry.grid(column=1, row=3)

# Monatliche Rentenversicherung GUI-Elemente
retirement_insurance_label = ttk.Label(monthly_income_spending_frame, text="Monatliche Rentenversicherung:")
retirement_insurance_label.grid(column=0, row=4, sticky=tk.W)

retirement_insurance_var = tk.StringVar()
retirement_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=retirement_insurance_var)
retirement_insurance_entry.grid(column=1, row=4)

# Berufsunfähigkeitsversicherung GUI-Elemente
occupational_disability_insurance_label = ttk.Label(monthly_income_spending_frame, text="Berufsunfähigkeitsversicherung:")
occupational_disability_insurance_label.grid(column=0, row=5, sticky=tk.W)

occupational_disability_insurance_var = tk.StringVar()
occupational_disability_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=occupational_disability_insurance_var)
occupational_disability_insurance_entry.grid(column=1, row=5)

# Haftpflicht- und Hausratversicherung GUI-Elemente
household_and_homeowners_insurance_label = ttk.Label(monthly_income_spending_frame, text="Haftpflicht- und Hausratversicherung:")
household_and_homeowners_insurance_label.grid(column=0, row=6, sticky=tk.W)

household_and_homeowners_insurance_var = tk.StringVar()
household_and_homeowners_insurance_entry = ttk.Entry(monthly_income_spending_frame, textvariable=household_and_homeowners_insurance_var)
household_and_homeowners_insurance_entry.grid(column=1, row=6)

# Monatliche Autokosten GUI-Elemente
monthly_car_costs_label = ttk.Label(monthly_income_spending_frame, text="Monatliche Autokosten:")
monthly_car_costs_label.grid(column=0, row=7, sticky=tk.W)

monthly_car_costs_var = tk.StringVar()
monthly_car_costs_entry = ttk.Entry(monthly_income_spending_frame, textvariable=monthly_car_costs_var)
monthly_car_costs_entry.grid(column=1, row=7)

# Berechnen-Button für monatliche Finanzbalance
calculate_monthly_balance_button = ttk.Button(monthly_income_spending_frame, text="Berechnen", command=monthly_income_spending)
calculate_monthly_balance_button.grid(column=0, row=8, columnspan=2, pady=10)

# Label für monatliche Finanzbalance
monthly_income_spending_label = ttk.Label(monthly_income_spending_frame, text="")
monthly_income_spending_label.grid(column=0, row=9, columnspan=2)

# Einkommenssteuerberechnung GUI-Elemente
income_label = ttk.Label(income_tax_frame, text="Einkommen:")
income_label.grid(column=0, row=0, sticky=tk.W)

income_var = tk.StringVar()
income_entry = ttk.Entry(income_tax_frame, textvariable=income_var)
income_entry.grid(column=1, row=0)

tax_class_label = ttk.Label(income_tax_frame, text="Steuerklasse:")
tax_class_label.grid(column=0, row=1, sticky=tk.W)

tax_class_var = tk.StringVar()
tax_class_entry = ttk.Entry(income_tax_frame, textvariable=tax_class_var)
tax_class_entry.grid(column=1, row=1)

num_children_label = ttk.Label(income_tax_frame, text="Anzahl der Kinder:")
num_children_label.grid(column=0, row=2, sticky=tk.W)

num_children_var = tk.StringVar()
num_children_entry = ttk.Entry(income_tax_frame, textvariable=num_children_var)
num_children_entry.grid(column=1, row=2)

calculate_tax_button = ttk.Button(income_tax_frame, text="Berechnen", command=calculate_net_income)
calculate_tax_button.grid(column=0, row=3, columnspan=2, pady=10)

net_income_result_label = ttk.Label(income_tax_frame, text="")
net_income_result_label.grid(column=0, row=4, columnspan=2)

tax_rate_label = ttk.Label(income_tax_frame, text="")
tax_rate_label.grid(column=0, row=5, columnspan=2)
# Stockinvestment GUI
stock_frame = ttk.Frame(mainframe, padding="10")
stock_frame.columnconfigure(0, weight=1)
stock_frame.columnconfigure(1, weight=1)
stock_frame.rowconfigure(1, weight=1)
# GUI-Elemente anzeigen
bank_frame.grid(column=0, row=3, columnspan=2, sticky="nsew")


root.mainloop()
