def is_otm(option_type, stock_price, strike_price):

    if option_type == 'Call':

        if strike_price <= stock_price:

            return False 

        else:

            return True 

    elif option_type == 'Put':

        if strike_price >= stock_price:

            return False 

        else:

            return True 

    else:

        raise ValueError(f'Option type "{option_type}" not recognized.')

def is_itm(option_type, stock_price, strike_price):

    if option_type == 'Call':

        if strike_price < stock_price:

            return True 

        else:

            return False 

    elif option_type == 'Put':

        if strike_price > stock_price:

            return True 

        else:

            return False 

    else:

        raise ValueError(f'Option type "{option_type}" not recognized.')

def is_atm(option_type, stock_price, strike_price, delta=None):

    if option_type == 'Call' or option_type == 'Put':
        if delta is None:
            if strike_price == stock_price:

                return True 

            else:

                return False 
        else:
            
            if strike_price >= stock_price - delta and strike_price <= stock_price + delta:

                return True 

            else:

                return False 

    else:

        raise ValueError(f'Option type "{option_type}" not recognized.')
