"""
Converts Currrency into Rupee Format
"""

from babel.numbers import format_currency

def remove_decimal(S):
    S = str(S)
    S = S[:-3]
    return S

def in_rupees(curr):
    curr_str = format_currency(curr, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    return(remove_decimal(curr_str))
    