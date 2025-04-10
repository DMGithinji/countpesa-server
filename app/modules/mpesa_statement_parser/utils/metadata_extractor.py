import re


class TransactionTypes:
    TillNo = "Till Number"
    Paybill = "Paybill"
    Fuliza = "Fuliza"
    Airtime = "Airtime Purchase"
    Mshwari = "Mshwari"
    Agent = "Agent"
    SendMoney = "Send Money"
    KCBMpesa = "KCB M-Pesa"
    MoneyTransfer = "Cash Transfer"


def get_transaction_metadata(description_str):
    """
    Analyze a transaction description and return structured metadata.

    Args:
        description_str (str): The transaction description text

    Returns:
        dict: A dictionary containing account, type, and category
    """
    account = description_str
    transaction_type = ""
    category = ""

    if "Customer Transfer to" in description_str or "Customer Transfer Fuliza" in description_str:
        account = " ".join(description_str.split(" ")[-2:])
        transaction_type = TransactionTypes.SendMoney
    elif "Funds received from" in description_str:
        account = " ".join(description_str.split(" ")[-2:])
        transaction_type = TransactionTypes.SendMoney
    elif "Customer Transfer of Funds Charge" in description_str:
        account = "Safaricom Send Money"
        transaction_type = TransactionTypes.SendMoney
        category = "Transaction Cost"
    elif "Merchant Payment Online to" in description_str:
        account = "-".join(description_str.split("-")[1:])
        transaction_type = TransactionTypes.TillNo
    elif "Merchant Payment Fuliza" in description_str:
        account = "-".join(description_str.split("-")[2:])
        transaction_type = TransactionTypes.TillNo
    elif "Merchant Customer Payment from " in description_str:
        account = "-".join(description_str.split("-")[1:])
        transaction_type = TransactionTypes.MoneyTransfer
    elif (
        "Airtime Purchase" in description_str
        or "safaricom postpaid" in description_str.lower()
        or "safaricom post paid" in description_str.lower()
    ):
        account = "Safaricom Airtime"
        transaction_type = TransactionTypes.Airtime
    elif "Buy Bundles" in description_str:
        transaction_type = TransactionTypes.Airtime
    elif "Merchant Payment" in description_str:
        account = description_str.split("-")[1].strip()
        transaction_type = TransactionTypes.TillNo
    elif "Pay Bill Online to" in description_str:
        account = "-".join(description_str.split("-")[1:])
        transaction_type = TransactionTypes.Paybill
    elif (
        "Pay Bill to" in description_str
        or "Pay Bill Fuliza M-Pesa to" in description_str
        or "Pay Bill Online Fuliza M-Pesa" in description_str
    ):
        slice_index = 1 if description_str.startswith("Pay Bill to") else 2
        account = "-".join(description_str.split("-")[slice_index:])
        transaction_type = TransactionTypes.Paybill
    elif "Pay Bill Charge" in description_str:
        account = "Safaricom Paybill"
        transaction_type = TransactionTypes.Paybill
        category = "Transaction Cost"
    elif "Pay Bill Online Fuliza M-Pesa" in description_str:
        account = description_str.split("-")[2].strip()
        transaction_type = TransactionTypes.Paybill
    elif "OverDraft of Credit Party" in description_str:
        account = "Safaricom Fuliza"
        transaction_type = TransactionTypes.Fuliza
    elif "OD Loan Repayment to" in description_str:
        account = "Safaricom Fuliza"
        transaction_type = TransactionTypes.Fuliza
    elif description_str in ["M-Shwari Withdraw", "M-Shwari Deposit"]:
        account = "My M-Shwari Account"
        transaction_type = TransactionTypes.Mshwari
    elif "M-Shwari Lock" in description_str:
        account = "M-Shwari Lock Savings"
        transaction_type = TransactionTypes.Mshwari
    elif "M-Shwari Loan" in description_str:
        account = "Safaricom M-Shwari"
        transaction_type = TransactionTypes.Mshwari
    elif "Customer Withdrawal At Agent".lower() in description_str.lower():
        account = "-".join(description_str.split("-")[1:])
        account = f"Agent - {account.strip()}"
        transaction_type = TransactionTypes.Agent
    elif description_str == "Withdrawal Charge":
        account = "Safaricom Withdrawal Charge"
        transaction_type = TransactionTypes.Agent
        category = "Transaction Cost"
    elif " via API" in description_str:
        account = (
            description_str.split("-")[1].split("via API")[0]
            if "-" in description_str
            else description_str.split("via API")[0]
        )
        transaction_type = TransactionTypes.MoneyTransfer
    elif "KCB M-PESA" in description_str:
        transaction_type = TransactionTypes.KCBMpesa
    elif description_str == "Customer Send Money To Unregistered User Charge":
        transaction_type = TransactionTypes.SendMoney
        account = "Safaricom Send Money"
        category = "Transaction Cost"
    elif "unregistered user" in description_str:
        transaction_type = TransactionTypes.SendMoney
        account = "Unregistered User"
    elif description_str == "Pay Merchant Charge":
        transaction_type = TransactionTypes.TillNo
        account = "Safaricom Till No."
        category = "Transaction Cost"
    elif "Deposit of Funds at Agent".lower() in description_str.lower():
        transaction_type = TransactionTypes.Agent
        account = "-".join(description_str.split("-")[1:])
        account = f"Agent - {account.strip()}"
    elif is_international_transfer(description_str):
        metadata = get_money_transfer_metadata(description_str)
        transaction_type = metadata["type"]
        account = metadata["account"]
    elif is_small_business_tr(description_str):
        metadata = get_small_business_name(description_str)
        transaction_type = metadata["type"]
        account = f"Business - {metadata['account']}"
    elif is_reversals(description_str):
        transaction_type = TransactionTypes.MoneyTransfer

    return {"account": account.strip(), "type": transaction_type, "category": category}


def get_money_transfer_metadata(description_str):
    """Extract account and type from international money transfer description"""
    # account is text between '- ' and '.'
    account = description_str.split("- ")[1].split(".")[0]
    transaction_type = TransactionTypes.MoneyTransfer
    return {"account": account, "type": transaction_type}


def is_international_transfer(description_str):
    """Check if the transaction is an international transfer"""
    # follows a regex pattern of 'Receive International <xxxx> Transfer From
    # <xxxx> - </xxxx>. Original conversation ID is <xxxx>.'
    regex = r"Receive International( Zero Rated)? Transfer From \d+ - "
    return bool(re.search(regex, description_str))


def is_small_business_tr(description_str):
    """Check if the transaction is with a small business"""
    # Customer Payment to Small Business to - 2547******779 ISAIAH ACUMBIKA
    # Customer Send Money to Micro SME Business with Fuliza MPesa to - 2547******521 FREDRICK
    regex = r"Customer (Payment|Send Money) to (Small Business|Micro SME Business)\
        ( with Fuliza MPesa)? to - \d{2,4}\*+\d{3} [A-Za-z ]+"
    return bool(re.search(regex, description_str))


def get_small_business_name(description_str):
    """Extract business account from small business transaction description"""
    # Customer Payment to Small Business to - 2547******521 ALFRED
    # Customer Send Money to Micro SME Business with Fuliza MPesa to - 2547******521 FREDRICK
    account = description_str.split("-")[1].strip()
    account = " ".join(account.split(" ")[1:])
    transaction_type = TransactionTypes.TillNo
    return {"account": account, "type": transaction_type}


def is_reversals(description_str):
    """Check if the transaction is a reversal"""
    # Send Money Expire Reversal
    # GlobalPay reversal from 903470 - M-PESA GlobalPay Acc. 0303196436895935
    # Pay Utility Reversal by C2B Standard Chartered Bank\Initiator
    # Pay Merchant Reversal by M- PESA - Jkiema
    return "reversal" in description_str.lower()
