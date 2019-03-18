import string
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


def re_shape(import_vec, trade_margin_vec,tax_subsidies_vec, export_vec,
             fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec, rate_vec):
             
    import_vec = import_vec.reshape(import_vec.shape[0], 1)
    trade_margin_vec = trade_margin_vec.reshape(trade_margin_vec.shape[0], 1)
    tax_subsidies_vec = tax_subsidies_vec.reshape(tax_subsidies_vec.shape[0], 1)
    export_vec = export_vec.reshape(export_vec.shape[0], 1)    
    fin_cons_hh_vec = fin_cons_hh_vec.reshape(fin_cons_hh_vec.shape[0], 1)
    fin_cons_gov_vec = fin_cons_gov_vec.reshape(fin_cons_gov_vec.shape[0], 1)
    gfcf_vec = gfcf_vec.reshape(gfcf_vec.shape[0], 1)
    rate_vec = rate_vec.reshape(rate_vec.shape[0], 1)
    
    return (import_vec, trade_margin_vec, tax_subsidies_vec, export_vec,
             fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec, rate_vec)

def import_Excel_SUT(filename, sheet_name_sup, sheet_name_use, sheet_name_rates):

    # First prepare the Excel file by Selecting the entire sheet and unmerging any merged cells
    
    '''
    SUPPLY table
    '''
    
    df_supply = pd.read_excel(filename, sheet_name_sup, index_col=False,
                              header=None)
    df_supply.fillna(0, inplace=True)
    
    supply_mat_start_col_excel="C"
    supply_mat_end_col_excel = "BP"
    supply_mat_start_col = col2num(supply_mat_start_col_excel)
    supply_mat_end_col=col2num(supply_mat_end_col_excel)
    supply_mat_start_row=4
    supply_mat_end_row=143
    supply_mat = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row,
                                supply_mat_start_col-1:supply_mat_end_col]
    supply_mat = supply_mat.values
    
    supply_col_product_id_excel = "B"
    supply_col_product_id = col2num(supply_col_product_id_excel)
    supply_row_industry_id = 2

    import_col_excel = "BX"
    import_col = col2num(import_col_excel)
    import_vec = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row,import_col-1]
    import_vec = import_vec.values

    trade_margin_col_excel = "BZ"
    trade_margin_col = col2num(trade_margin_col_excel)
    trade_margin_vec = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row,trade_margin_col-1]
    trade_margin_vec = trade_margin_vec.values

    tax_subsidies_col_excel = "BR"
    tax_subsidies_col = col2num(tax_subsidies_col_excel)
    tax_subsidies_vec = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row,tax_subsidies_col-1]
    tax_subsidies_vec = tax_subsidies_vec.values

    product_header = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row, supply_col_product_id-1]
    industry_header = df_supply.iloc[supply_row_industry_id-1, supply_mat_start_col-1:supply_mat_end_col]
    
    
    # Product Header Dataframe to ensure rates are correctly matched
    df_product = pd.DataFrame(data = product_header.values, columns = np.array(['product_id']))

    '''
    USE table
    '''
    
    df_use = pd.read_excel(filename, sheet_name_use, index_col=False,
                           header=None)
    df_use.fillna(0, inplace=True)

    
    use_mat_start_col_excel="C"
    use_mat_end_col_excel="BP"
    use_mat_start_col=col2num(use_mat_start_col_excel)
    use_mat_end_col=col2num(use_mat_end_col_excel)
    use_mat_start_row=4
    use_mat_end_row=143
    use_mat = df_use.iloc[use_mat_start_row-1:use_mat_end_row,
                                use_mat_start_col-1:use_mat_end_col]
    use_mat = use_mat.values

    fin_cons_hh_col_excel = "BR"
    fin_cons_gov_col_excel = "BS"
    fin_cons_hh_col = col2num(fin_cons_hh_col_excel)
    fin_cons_gov_col = col2num(fin_cons_gov_col_excel)
    fin_cons_hh_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,
                                  fin_cons_hh_col-1]
    fin_cons_gov_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,
                                   fin_cons_gov_col-1]
    fin_cons_hh_vec = fin_cons_hh_vec.values
    fin_cons_gov_vec = fin_cons_gov_vec.values

    gfcf_col_excel ="BT"
    gfcf_col = col2num(gfcf_col_excel)
    gfcf_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,gfcf_col-1]
    gfcf_vec = gfcf_vec.values

    export_col_excel = "BW"
    export_col = col2num(export_col_excel)
    export_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,export_col-1]
    export_vec = export_vec.values

    '''
    GST Rates table
    '''
    df_rates = pd.read_excel(filename, sheet_name_rates, index_col=False,
                           header=0)
    df_rates.fillna(0, inplace=True)
    df_rates = df_rates[['product_id', 'rates']]
    # merge with product id to ensure that the rates are correctly matched
    
    df_rates = pd.merge(df_product, df_rates,
                            how="inner", on="product_id")
    
    return (supply_mat, use_mat, product_header, industry_header,
            import_vec, trade_margin_vec, tax_subsidies_vec, export_vec,
            fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec, df_rates)

def blow_up_mat(supply_mat, use_mat, import_vec, trade_margin_vec,
                tax_subsidies_vec, export_vec, fin_cons_hh_vec,
                fin_cons_gov_vec, gfcf_vec, blow_up_factor):
    
    supply_mat *= blow_up_factor
    use_mat *= blow_up_factor
    import_vec *= blow_up_factor
    trade_margin_vec *= blow_up_factor
    tax_subsidies_vec *= blow_up_factor
    export_vec *= blow_up_factor
    fin_cons_hh_vec *= blow_up_factor
    fin_cons_gov_vec *= blow_up_factor
    gfcf_vec *= blow_up_factor

    return (supply_mat, use_mat, import_vec, trade_margin_vec,
            tax_subsidies_vec, export_vec, fin_cons_hh_vec,
            fin_cons_gov_vec, gfcf_vec)

def calc_output_tax(supply_mat, rate_vec):
    """
    enter the matrix operation
    """
    return output_tax_mat

def calc_input_tax_credit(use_mat, rate_vec):
    """
    enter the matrix operation
    """    
    return input_tax_credit_mat

    
filename = 'India Supply Use Table SUT_12-13.xlsx'
sheet_name_sup = 'supply 2012-13'
sheet_name_use = 'use 2012-13'
sheet_name_rates = 'rates'
supply_use_table_year = 2012
current_year = 2017

GDP_LCU = {}

GDP_LCU[2012] = 9.94401E+13
GDP_LCU[2013] = 1.12335E+14
GDP_LCU[2014] = 1.2468E+14
GDP_LCU[2015] = 1.3764E+14
GDP_LCU[2016] = 1.52537E+14
GDP_LCU[2017] = 1.67731E+14

blow_up_factor = GDP_LCU[current_year]/GDP_LCU[supply_use_table_year]

# Import the Supply Use Table and GST Rates 

(supply_mat, use_mat, sector_headers, product_headers, import_vec,
 trade_margin_vec, tax_subsidies_vec, export_vec, fin_cons_hh_vec,
 fin_cons_gov_vec, gfcf_vec, df_rates) = import_Excel_SUT(filename,
                                                          sheet_name_sup,
                                                          sheet_name_use,
                                                          sheet_name_rates)
rate_vec = df_rates['rates'].values

# reshape all vectors to column arrays
(import_vec, trade_margin_vec, tax_subsidies_vec, export_vec, fin_cons_hh_vec,
 fin_cons_gov_vec, gfcf_vec, rate_vec) = re_shape(import_vec, trade_margin_vec,
                                                  tax_subsidies_vec, 
                                                  export_vec, fin_cons_hh_vec,
                                                  fin_cons_gov_vec, gfcf_vec,
                                                  rate_vec)

 
# Blow up the Supply Use Table and Vectors to current year
(supply_mat, use_mat, imports_vec,
 trade_margins_vec, tax_subsidies_vec, export_vec, fin_cons_hh_vec,
 fin_cons_gov_vec, gfcf_vec) = blow_up_mat(supply_mat, use_mat,
                                       import_vec, trade_margin_vec,
                                       tax_subsidies_vec,
                                       export_vec, fin_cons_hh_vec,
                                       fin_cons_gov_vec, gfcf_vec,
                                       blow_up_factor)

"""
call program to estimate output tax and ITC
"""
