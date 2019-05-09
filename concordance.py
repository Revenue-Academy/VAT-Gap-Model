# -*- coding: utf-8 -*-
"""
Created on Thu May  9 03:11:08 2019

@author: wb305167
"""
import pandas as pd

def hsn_tax_ratio(gst_collection_full_year_dom):
    
    df_cash_ratio = pd.read_excel(filename, sheet_name_cash_ratio, index_col=False)
    df_cash_ratio.fillna(0, inplace=True)
    df_cash_ratio['cash_tax_payable_ratio'] = df_cash_ratio['tax_cash']/df_cash_ratio['tax_payable']
    df_cash_ratio['HSN2'] = df_cash_ratio['HSN2'].astype(str)
    """
    if df_cash_ratio['HSN2'].map(len)<2:
        df_cash_ratio['HSN2'] = "0" + df_cash_ratio['HSN2']
    """
    df_gstr1 = pd.read_excel(filename, sheet_name_gstr1, index_col=False)
    df_gstr1.fillna(0, inplace=True)
    df_gstr1['HSN2'] = df_gstr1['HSN2'].astype(str)
    # Data is for 9 months now groosedup to one year
    df_gstr1['gstr1_tax_payable'] = df_gstr1['gstr1_tax_payable'] * (12/9)
    df_cash_ratio = pd.merge(df_cash_ratio, df_gstr1,
                            how="inner", on="HSN2")    
    df_cash_ratio['tax_cash'] = (df_cash_ratio['cash_tax_payable_ratio'] * 
                                 df_cash_ratio['gstr1_tax_payable'])
    tax_collection_gstr1 = df_cash_ratio['tax_cash'].sum()
    blow_up_factor = (gst_collection_full_year_dom/tax_collection_gstr1)
    df_cash_ratio['tax_cash_bu'] = df_cash_ratio['tax_cash']*blow_up_factor
    tax_cash_dom_less_trade = df_cash_ratio['tax_cash_bu'].sum()


filename = 'concordance_2.xlsx'
sheet_name_cash_ratio = 'tax_output_tax_ratio'
sheet_name_gstr1 = 'gstr1'

gst_collection_july17_march18 = 8.41*10**5
igst_import_july17_march18 = 1.73 * 10**5
gst_collection_july17_june18 = gst_collection_july17_march18 * (12/9)
igst_import_july17_june18 = igst_import_july17_march18 * (12/9)
gst_collection_july17_june18_dom = (gst_collection_july17_june18 - 
                                    igst_import_july17_june18)

SUT_trade_margin = 138695029/100
#assuming average rate of 10%
avg_gst_rate_trade = 0.1
gst_trade = SUT_trade_margin*avg_gst_rate_trade

gst_collection_july17_june18_dom_less_trade = (gst_collection_july17_june18_dom -
                                               gst_trade)

gst_collection_full_year_dom = gst_collection_july17_june18_dom_less_trade

#hsn_tax_ratio(gst_collection_july17_june18_dom_less_trade)
