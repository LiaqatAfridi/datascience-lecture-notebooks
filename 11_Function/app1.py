import streamlit as st
import random

# ---------------------------------------------
# Initialize Accounts in Session State
# ---------------------------------------------
if "all_accounts" not in st.session_state:
    st.session_state.all_accounts = []

# ---------------------------------------------
# Backend Functions
# ---------------------------------------------

def open_account(cnic, account_title, initial_deposit):
    account = {
        'cnic': cnic,
        'title': account_title,
        'balance': initial_deposit,
        'account_number': random.randint(1000, 9999),
        'pin': random.randint(1000, 9999)
    }
    st.session_state.all_accounts.append(account)
    return account


def show_balance(account_number, pin):
    for acc in st.session_state.all_accounts:
        if acc['account_number'] == account_number:
            if acc['pin'] == pin:
                return acc['balance'], None
            else:
                return None, "Invalid PIN"
    return None, "Account Not Found"


def deposit_amt(account_number, amount):
    for acc in st.session_state.all_accounts:
        if acc['account_number'] == account_number:
            acc['balance'] += amount
            return acc['balance'], None
    return None, "Account Not Found"


def withdraw_amt(account_number, pin, amount):
    for acc in st.session_state.all_accounts:
        if acc['account_number'] == account_number:

            if acc['pin'] != pin:
                return None, "Invalid PIN"

            if amount > acc['balance']:
                return None, "Insufficient Balance"

            acc['balance'] -= amount
            return acc['balance'], None

    return None, "Account Not Found"


def transfer_amt(account_number, pin, amount, beneficiary_acc):
    for acc in st.session_state.all_accounts:
        if acc['account_number'] == account_number:

            if acc['pin'] != pin:
                return None, "Invalid PIN"

            if acc['balance'] < amount:
                return None, "Insufficient Balance"

            # beneficiary
            for bacc in st.session_state.all_accounts:
                if bacc['account_number'] == beneficiary_acc:
                    acc['balance'] -= amount
                    bacc['balance'] += amount
                    return acc['balance'], None

            return None, "Beneficiary Account Not Found"

    return None, "Account Not Found"


# ---------------------------------------------
# Streamlit UI
# ---------------------------------------------

st.title("🏦 Simple Banking System - Streamlit Interface")

menu = st.sidebar.selectbox(
    "Select Action",
    ["Open Account", "Check Balance", "Deposit", "Withdraw", "Transfer", "Show All Accounts"]
)

# ---------------------------------------------
# Open Account
# ---------------------------------------------
if menu == "Open Account":
    st.header("➕ Open a New Account")

    cnic = st.text_input("Enter CNIC")
    title = st.text_input("Account Title")
    deposit = st.number_input("Initial Deposit", min_value=0)

    if st.button("Create Account"):
        acc = open_account(cnic, title, deposit)
        st.success("🎉 Account Created Successfully!")
        st.write(f"**Account Number:** `{acc['account_number']}`")
        st.write(f"**PIN:** `{acc['pin']}` (Save this!)")

# ---------------------------------------------
# Check Balance
# ---------------------------------------------
elif menu == "Check Balance":
    st.header("💰 Check Balance")

    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)

    if st.button("Show Balance"):
        bal, err = show_balance(acc_no, pin)
        if err:
            st.error(err)
        else:
            st.success(f"Your Current Balance is: **Rs {bal}**")

# ---------------------------------------------
# Deposit
# ---------------------------------------------
elif menu == "Deposit":
    st.header("📥 Deposit Amount")

    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    amt = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        bal, err = deposit_amt(acc_no, amt)
        if err:
            st.error(err)
        else:
            st.success(f"Amount Deposited! New Balance: **Rs {bal}**")

# ---------------------------------------------
# Withdraw
# ---------------------------------------------
elif menu == "Withdraw":
    st.header("📤 Withdraw Amount")

    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)
    amt = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        bal, err = withdraw_amt(acc_no, pin, amt)
        if err:
            st.error(err)
        else:
            st.success(f"Withdrawal Successful! New Balance: **Rs {bal}**")

# ---------------------------------------------
# Transfer
# ---------------------------------------------
elif menu == "Transfer":
    st.header("💸 Transfer Amount")

    acc_no = st.number_input("Your Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("Your PIN", min_value=1000, max_value=9999)
    amt = st.number_input("Amount", min_value=1)
    ben = st.number_input("Beneficiary Account Number", min_value=1000, max_value=9999)

    if st.button("Transfer"):
        bal, err = transfer_amt(acc_no, pin, amt, ben)
        if err:
            st.error(err)
        else:
            st.success(f"Transfer Successful! Remaining Balance: **Rs {bal}**")

# ---------------------------------------------
# Show All Accounts (debug screen)
# ---------------------------------------------
elif menu == "Show All Accounts":
    st.header("📋 All Accounts (Debug View)")
    st.write(st.session_state.all_accounts)
