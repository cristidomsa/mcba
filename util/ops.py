from db import get_session
from db.models import Account, Transaction
from util.rates import convert

from datetime import datetime, timedelta

session = get_session()

CODES = {100: 'ARPOVED',
         200: 'INSUFICIENT FUNDS',
         300: 'MONEY LAUDERING LIMIT EXEEDED',
         500: 'BALANCES: EUR: {0}; USD: {1}; GBP: {2}; JPY: {3}; RUB: {4};',
         700: 'UNKNOWN ACCOUNT {}',
         800: 'JSON ERROR: {}',
         900: 'SERVER ERROR: {}',}

MAX_LIMIT = 10000
MAX_CCY = 'EUR'

currencies = ['EUR', 'USD', 'GBP', 'JPY', 'RUB']

class Operations():

    get_user = lambda self, x: session.query(Account).filter(Account.name == x).one_or_none()

    @staticmethod
    def deposit(account, amt, ccy, date):
        try:
            acc = Operations().get_user(account)
            
            if acc is None: return (0, CODES[700].format(account))

            acc.balance += convert(amt, ccy, acc.ccy)
            op = Transaction(name_id=acc.id, op_type='deposit',
                             amount=amt, ccy=ccy, date=datetime.strptime(date, "%Y-%m-%d"), op_details='')
            acc.ops.append(op)

            session.commit()

        except Exception as err:

            return (0, CODES[900].format(err))

        return (1, CODES[100])

    @staticmethod
    def withdrawal(account, amt, ccy, date):

        def _validate_op():
            start_date = date - timedelta(days=5)

            ops = session.query(Transaction).filter(
            Transaction.op_type == 'withdrawal',
            Transaction.name_id == acc.id,
            Transaction.date >= start_date,
            Transaction.date <= date).all()
            
            sum = 0

            for op in ops:
                sum += float(op.op_details)
                print(op.op_type, op.amount, op.date)

            if sum > MAX_LIMIT:
                return False
            else:
                return True

        try:
            acc = Operations().get_user(account)
            if acc is None: return (0, CODES[700].format(account))

            sum = convert(amt, ccy, acc.ccy)
            date = datetime.strptime(date, "%Y-%m-%d")
            valid_money = _validate_op()
            if acc.balance - sum >= 0 and valid_money:
                acc.balance -= sum
            else:
                if not valid_money:
                    return (0, CODES[300])
                else:
                    return (0, CODES[200])


            op = Transaction(name_id=acc.id, op_type='withdrawal',
                             amount=amt, ccy=ccy, date=date, op_details=str(convert(amt, ccy, MAX_CCY)))
            acc.ops.append(op)
            print(op.op_type, op.amount, op.date)

            session.commit()

        except Exception as err:
            return (0, CODES[900].format(err))

        return (1, CODES[100])

    @staticmethod
    def transfer(from_account, to_account, amt, ccy, date):
        try:
            acc_from = Operations().get_user(from_account)
            
            if acc_from is None: return (0, CODES[700].format(from_account))

            acc_to = Operations().get_user(to_account)
            
            if acc_from is None: return (0, CODES[700].format(to_account))

            sum_from = convert(amt, ccy, acc_from.ccy)
            sum_to = convert(amt, ccy, acc_to.ccy)
            if acc_from.balance - sum_from >= 0:
                acc_from.balance -= sum_from
                acc_to.balance += sum_to
            else:
                return (0, CODES[200])

            op = Transaction(name_id=acc_from.id, op_type='transfer',
                             amount=sum_from, ccy=ccy, date=datetime.strptime(date, "%Y-%m-%d"), op_details=to_account)
            acc_from.ops.append(op)
            session.commit()

        except Exception as err:
            return (0, CODES[900].format(err))

        return (1, CODES[100])

    @staticmethod
    def balance(account, date):
        acc = Operations().get_user(account)

        if acc is None: return (0, CODES[700].format(account))

        return (1, CODES[500].format(*[convert(acc.balance, acc.ccy, k) for k in currencies]))
