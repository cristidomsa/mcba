from datetime import datetime

def validate_json(j):

        required_fields = ['method', 'date', 'account']
        required_fields_dw = ['amt', 'ccy']
        required_fields_t = ['to_account', 'from_account']

        date_format = "%Y-%m-%d"
        currencies = ['USD', 'GBP', 'EUR', 'JPY', 'RUB']
        methods = ['deposit', 'withdrawal', 'transfer', 'get_balances']

        method = j['method']
        
        if method != 'transfer':
            if 'account' not in j:
                raise Exception('Invalid JSON! (field {} missing)'.format(field))

        if method not in methods: 
            raise Exception('Invalid JSON! (method unknown)')
        
        try: 
            datetime.strptime(j['date'], date_format)
        except Exception as e:
            raise Exception('Invalid JSON! (date format invalid)')

        if method != 'get_balances':
            if j['ccy'] not in currencies:
                raise Exception('Invalid JSON! (currencies not available)')
            
            try: 
                float(j['amt'])
            except Exception as e:
                raise Exception('Invalid JSON! (amount not number)')
            
        if method in methods[:2]:
            for field in required_fields_dw:
                if field not in j:
                    raise Exception('Invalid JSON! (field {} missing)'.format(field))
        
        if method == 'transfer':
            for field in required_fields_t:
                if field not in j:
                    raise Exception('Invalid JSON! (field {} missing)'.format(field))

        j.pop('method')
            
        return method, j