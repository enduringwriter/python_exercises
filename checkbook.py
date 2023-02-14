"""
Keith Stateson
Project 1: checkbook
Checkbook is a command line checkbook application that allows users to track their finances.
"""

import csv
import os
import time

# variables
play_game = True

# global variables - global is generally use for static variables that don't change
cols = ['timestamp', 'transaction', 'balance', 'description']


def clear():
    os.system('clear')


def get_checkbook_status(get_choice):
    """
    Determine if the customer has an account; if not, create an account for the customer.
    :return: status of account as accessed or created
    """
    if os.path.exists('checkbook.csv'):
        if get_choice == 1:
            get_status = ''
        else:
            get_status = '\nTransaction complete!\n'
    else:
        with open('checkbook.csv', 'w') as f_gcs:
            transaction = dict(timestamp=time.ctime(), transaction='new account', balance=0,
                               description='opened new checkbook account')
            writer = csv.DictWriter(f_gcs, fieldnames=cols)
            writer.writeheader()
            writer.writerow(transaction)
        get_status = '\nCreating your new galaxy-wide checkbook account!\nWelcome to SuperNova Bank!!!\n'
    return print(get_status)


def get_checkbook_balance():
    """
    Get customer checkbook balance.
    :return: current balance
    """
    current_total = 0
    with open('checkbook.csv', 'r') as f_gcb:
        content = csv.DictReader(f_gcb, fieldnames=cols)  # output is a list [balance, 0]
        lines = [line for line in content][1:]
        for line in lines:
            current_total += int(line['balance'])
    return current_total


def get_valid_input_debit_or_credit(get_deb_cred_choice):
    """
    Prevent invalid input for debits and credits.
    :return: valid input
    """
    if get_deb_cred_choice == 2:
        choice_value = 'debit'
    else:
        choice_value = 'credit'
    while True:
        debit_or_credit_str = input(f'How much is the {choice_value}: ').lower()
        if debit_or_credit_str.isdigit() and int(debit_or_credit_str) > 0:
            valid_input_debit_or_credit = int(debit_or_credit_str)
            break
    return valid_input_debit_or_credit


def add_transaction(get_choice, get_deb_or_cred):
    """
    Add debit or credit transaction to checkbook.
    :return: no value is returned
    """
    with open('checkbook.csv', 'a') as f_trans:
        if get_choice == 3:
            transaction_type = 'credit'
        elif get_choice == 2:
            transaction_type = 'debit'
        user_description = get_user_description()
        transaction = {'timestamp': time.ctime(), 'transaction': transaction_type,
                       'balance': get_deb_or_cred, 'description': user_description}
        writer_transaction = csv.DictWriter(f_trans, fieldnames=cols)
        writer_transaction.writerow(transaction)


def get_user_description():
    while True:
        description_choice = input("Enter a description for your transaction (up to 30 characters and cannot begin with a number), or press 's' to skip: ").lower()
        if description_choice == 's':
            description_choice = ''
            break
        elif not description_choice.isdigit() and len(description_choice) <= 30:
            break
    return description_choice


def get_transaction_history():
    print("Galaxy Wide Transaction History\n".center(36, ' '))
    with open('checkbook.csv', 'r') as f_history:
        reader = csv.DictReader(f_history)
        next(reader)
        lines = [line for line in reader]

        for line in lines:  # get the max length of any tender to expand the output column
            max_length = 0
            biggie = len(line['balance'])
            if biggie > max_length:
                max_length = biggie
            max_length += 3  # accounts for two decimal places and period
        print(f"#    Timestamp                    Type       Balance, USD            Description")
        for index, line in enumerate(lines):
            print(f"{index: <4} {line['timestamp']:<28} {line['transaction']:<10}"
                  f" ${int(line['balance']):>17,.2f} {' ':<4} {line['description']}")
    print('\n')


clear()
print("\n~~~ Welcome to SuperNova's Intergalactic Terminal Checkbook! ~~~".center(64, '~'))
print("\x1B[3mWhere money grows so fast it explodes!\x1B[3m".center(72, ' '))
print("Currency is in USD, Universal Star Dollars\n".center(64, ' '))

while play_game:
    print("What would you like to do?\n")
    print("1 - view current balance")
    print("2 - record a debit (withdraw)")
    print("3 - record a credit (deposit)")
    print("4 - view intergalactic transaction history")
    print("5 - exit\n")

    while True:
        choice_str = input('Enter your choice: ').lower()
        if choice_str.isdigit() and (0 < int(choice_str) < 6):
            choice = int(choice_str)
            break

    if choice == 5:  # end game
        clear()
        print('Thank you using SuperNova, have a starbrite day!')
        play_game = False

    elif choice == 1:  # check balance
        clear()
        get_checkbook_status(get_choice=choice)    # determine if customer has an account
        current_balance = get_checkbook_balance()
        print(f'Your current galactic balance is ${current_balance:,.2f}\n')

    elif choice == 2:  # debit transaction
        clear()
        debit = -1 * get_valid_input_debit_or_credit(get_deb_cred_choice=choice)  # validation of debit
        get_checkbook_status(get_choice=choice)
        add_transaction(get_choice=choice, get_deb_or_cred=debit)  # add debit to checkbook

    elif choice == 3:  # credit transaction
        clear()
        credit = get_valid_input_debit_or_credit(get_deb_cred_choice=choice)  # validation of credit
        get_checkbook_status(get_choice=choice)
        add_transaction(get_choice=choice, get_deb_or_cred=credit)  # add credit to checkbook

    elif choice == 4:  # view transaction history
        clear()
        get_transaction_history()

    else:
        print("$omething smells fi$hy - Yo money is gaw-gaw-gone!!! Sorry, SuperNova went Nova!")
