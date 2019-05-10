import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

np.seterr(divide='ignore', invalid='ignore')

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def re_shape(import_vec, trade_margin_vec, tax_subsidies_vec, export_vec,fin_cons_hh_vec,
             fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec, rate_vec, exempt_vec):

    import_vec = import_vec.reshape(import_vec.shape[0], 1)
    trade_margin_vec = trade_margin_vec.reshape(trade_margin_vec.shape[0], 1)
    tax_subsidies_vec = tax_subsidies_vec.reshape(tax_subsidies_vec.shape[0], 1)
    export_vec = export_vec.reshape(export_vec.shape[0], 1)
    fin_cons_hh_vec = fin_cons_hh_vec.reshape(fin_cons_hh_vec.shape[0], 1)
    fin_cons_gov_vec = fin_cons_gov_vec.reshape(fin_cons_gov_vec.shape[0], 1)
    gfcf_vec = gfcf_vec.reshape(gfcf_vec.shape[0], 1)
    vlbl_vec = vlbl_vec.reshape(vlbl_vec.shape[0], 1)
    cis_vec = cis_vec.reshape(cis_vec.shape[0], 1)
    rate_vec = rate_vec.reshape(rate_vec.shape[0], 1)
    exempt_vec = exempt_vec.reshape(exempt_vec.shape[0], 1)

    return (import_vec, trade_margin_vec, tax_subsidies_vec, export_vec,fin_cons_hh_vec,
            fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec, rate_vec, exempt_vec)


def import_Excel_SUT(filename, sheet_name_sup, sheet_name_use, sheet_name_rates,
                     sheet_name_exempt, sheet_name_reg_ratio):

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

    # Import Vector
    import_col_excel = "BX"
    import_col = col2num(import_col_excel)
    import_vec = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row,import_col-1]
    import_vec = import_vec.values

    # Trade & Transport Margin Vector
    trade_margin_col_excel = "BZ"
    trade_margin_col = col2num(trade_margin_col_excel)
    trade_margin_vec = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row,trade_margin_col-1]
    trade_margin_vec = trade_margin_vec.values

    # Product tax less subsidies Vector
    tax_subsidies_col_excel = "BR"
    tax_subsidies_col = col2num(tax_subsidies_col_excel)
    tax_subsidies_vec = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row,tax_subsidies_col-1]
    tax_subsidies_vec = tax_subsidies_vec.values

    product_header = df_supply.iloc[supply_mat_start_row-1:supply_mat_end_row, supply_col_product_id-2:supply_col_product_id]
    product_header = product_header.values
    industry_header = df_supply.iloc[supply_row_industry_id-1, supply_mat_start_col-1:supply_mat_end_col]
    industry_header = industry_header.values

    # Product Header Dataframe to ensure rates are correctly matched
    df_product = pd.DataFrame(data = product_header, columns = np.array(['srl_no', 'product_id']))
    df_product['srl_no'] = df_product['srl_no'].astype(str)
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
    
    # Public final consumption Vector
    fin_cons_hh_col_excel = "BR"
    fin_cons_hh_col = col2num(fin_cons_hh_col_excel)
    fin_cons_hh_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,
                                  fin_cons_hh_col-1]
    fin_cons_hh_vec = fin_cons_hh_vec.values
    
    # Govt. final consumption Vector
    fin_cons_gov_col_excel = "BS"
    fin_cons_gov_col = col2num(fin_cons_gov_col_excel)
    fin_cons_gov_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,
                                   fin_cons_gov_col-1]
    fin_cons_gov_vec = fin_cons_gov_vec.values

    # Gross capital formation Vector
    gfcf_col_excel ="BT"
    gfcf_col = col2num(gfcf_col_excel)
    gfcf_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,gfcf_col-1]
    gfcf_vec = gfcf_vec.values

    # Valuables Vector
    vlbl_col_excel ="BU"
    vlbl_col = col2num(vlbl_col_excel)
    vlbl_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,vlbl_col-1]
    vlbl_vec = vlbl_vec.values
    
    # Change in stocks Vector
    cis_col_excel ="BV"
    cis_col = col2num(cis_col_excel)
    cis_vec = df_use.iloc[use_mat_start_row-1:use_mat_end_row,cis_col-1]
    cis_vec = cis_vec.values
    
    # Export Vector
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
    df_rates['weighted_rates'] = df_rates['rates'] * df_rates['weight']
    df_rates = df_rates.groupby(['srl_no'])["weighted_rates"].sum()
    df_rates = df_rates.reset_index()
    df_rates = df_rates.values
    
    df_rates = pd.DataFrame(data = df_rates, columns = np.array(['srl_no', 'rates']))
    df_rates['srl_no'] = df_rates['srl_no'].astype(int)
    df_rates['srl_no'] = df_rates['srl_no'].astype(str)
    df_rates = pd.merge(df_rates, df_product,
                            how="inner", on="srl_no")        
    df_rates = df_rates[['product_id', 'rates']]    
    
    rate_vec = df_rates['rates'].values

    '''
    Exempt Supply vector
    '''
    df_exempt = pd.read_excel(filename, sheet_name_exempt, index_col=False,
                           header=0)
    df_exempt.fillna(0, inplace=True)
    df_exempt = df_exempt[['product_id', 'exempt']]
    # merge with product id to ensure that the rates are correctly matched
    df_exempt = pd.merge(df_product, df_exempt,
                            how="inner", on="product_id")
    exempt_vec = df_exempt['exempt'].values

    '''
    GST Registered Ratio by Industry
    '''
    df_gst_reg_ratio = pd.read_excel(filename, sheet_name_reg_ratio, index_col=False)
    industry_group_header = df_gst_reg_ratio['industry_group'].values
    gst_reg_ratio_ind_vec = df_gst_reg_ratio['gst_reg_ratio'].values
    
    return (supply_mat, tax_subsidies_vec, import_vec, trade_margin_vec,
            industry_header, product_header, use_mat, fin_cons_hh_vec,
            fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec, export_vec,
            gst_reg_ratio_ind_vec, industry_group_header, rate_vec, exempt_vec)


def blow_up_mat(supply_mat, use_mat, import_vec, trade_margin_vec, tax_subsidies_vec,
                export_vec, fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec, vlbl_vec,
                cis_vec, blow_up_factor):

    supply_mat *= blow_up_factor
    use_mat *= blow_up_factor
    import_vec *= blow_up_factor
    trade_margin_vec *= blow_up_factor
    tax_subsidies_vec *= blow_up_factor
    export_vec *= blow_up_factor
    fin_cons_hh_vec *= blow_up_factor
    fin_cons_gov_vec *= blow_up_factor
    gfcf_vec *= blow_up_factor
    vlbl_vec *= blow_up_factor
    cis_vec *= blow_up_factor

    return (supply_mat, use_mat, import_vec, trade_margin_vec,
            tax_subsidies_vec, export_vec, fin_cons_hh_vec,
            fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec)

def calc_output_tax(supply_mat, rate_vec):
    output_tax_mat = supply_mat * rate_vec
    return output_tax_mat

def calc_itc_disallowed_ratio(supply_mat, exempt_vec):
    exempt_supply_mat = supply_mat * exempt_vec
    exempt_supply_ind_vec = calc_sum_by_industry(exempt_supply_mat)
    supply_ind_vec = calc_sum_by_industry(supply_mat)
    itc_disallowed_ratio = exempt_supply_ind_vec/supply_ind_vec
    return (itc_disallowed_ratio, exempt_supply_mat)

def calc_itc_disallowed(input_tax_credit_vec, itc_disallowed_ratio):
    itc_disallowed_vec = input_tax_credit_vec * itc_disallowed_ratio
    return itc_disallowed_vec

def calc_input_tax_credit(use_mat, rate_vec):
    input_tax_credit_mat = use_mat * rate_vec
    return input_tax_credit_mat

def calc_sum_by_industry(input_mat):
    output_vec = input_mat.sum(axis=0)
    output_vec = output_vec.reshape(1, output_vec.shape[0])
    return output_vec

def calc_sum_by_commodity(input_mat):
    output_vec = input_mat.sum(axis=1)
    output_vec = output_vec.reshape(output_vec.shape[0], 1)
    return output_vec

# Function to calculate the ratio for allocating imports/exports/taxes/subsidies of a product to each industry
def calc_allocation_ratio(input_mat):
    sum_by_prod_vec = input_mat.sum(axis=1)
    sum_by_prod_vec = sum_by_prod_vec.reshape(sum_by_prod_vec.shape[0],1)
    # dividing use_mat by iiuse_vec while avoiding zero by zero
    output_mat = np.divide(input_mat, sum_by_prod_vec,
                           out=np.zeros_like(input_mat), where=sum_by_prod_vec!=0)
    return output_mat

def calc_allocation_by_use(use_mat, fin_cons_hh_vec ,fin_cons_gov_vec , gfcf_vec, vlbl_vec, cis_vec):
    use_comm_vec = calc_sum_by_commodity(use_mat)
    dom_use_vec =  use_comm_vec + fin_cons_hh_vec + fin_cons_gov_vec + gfcf_vec + vlbl_vec + cis_vec
    use_vec_ratio = use_comm_vec / dom_use_vec
    fin_cons_hh_vec_ratio = fin_cons_hh_vec/ dom_use_vec
    fin_cons_gov_vec_ratio = fin_cons_gov_vec/ dom_use_vec
    gfcf_vec_ratio = gfcf_vec/ dom_use_vec
    vlbl_vec_ratio = vlbl_vec/dom_use_vec
    cis_vec_ratio = cis_vec/dom_use_vec
    return (use_vec_ratio, fin_cons_hh_vec_ratio, fin_cons_gov_vec_ratio, gfcf_vec_ratio, vlbl_vec_ratio,
            cis_vec_ratio)

# Function to allocate imports/exports/taxes/subsidies of a product to each industry proportionately
def calc_allocation_to_industry(allocation_mat, input_vec):
    output_mat = allocation_mat * input_vec
    return output_mat

# Function to calculate GST on imports
def calc_GST_on_imports(use_mat, import_vec, rate_vec):
    allocation_ratio_by_use_mat = calc_allocation_ratio(use_mat)
    import_mat = calc_allocation_to_industry(allocation_ratio_by_use_mat, import_vec)
    GST_on_imports_mat = import_mat * rate_vec
    GST_on_imports_ind_vec = calc_sum_by_industry(GST_on_imports_mat)
    tot_GST_on_imports =  GST_on_imports_ind_vec.sum()
    return (GST_on_imports_ind_vec, tot_GST_on_imports)

# Function to export a Vector by industry to a csv file
def make_ind_vec_df(input_vec, industry_header, output):
    input_vec = input_vec.reshape(input_vec.shape[1], 1)
    industry_header = industry_header.reshape(industry_header.shape[0], 1)
    ind_df = pd.DataFrame(data=input_vec, index=industry_header, columns=np.array([output]))
    ind_df = ind_df.reset_index()
    ind_df = ind_df.rename(columns={'index':'industry_id'})
    file_name = "Output_csv\\" + output + ".csv"
    ind_df.to_csv(file_name)

# Function to export a matrix to a csv file vy converting it into vector by industry
def make_mat_df(input_mat, industry_header, output):
    input_vec = calc_sum_by_industry(input_mat)
    make_ind_vec_df(input_vec, industry_header, output)
    
def hsn_tax_ratio(filename, sheet_name_cash_ratio, sheet_name_gstr1, gst_collection_full_year_dom):   
    tax_cash_df = pd.read_excel(filename, sheet_name_cash_ratio, index_col=False)
    tax_cash_df.fillna(0, inplace=True)
    tax_cash_df['cash_tax_payable_ratio'] = tax_cash_df['tax_cash']/tax_cash_df['tax_payable']

    tax_cash_df['HSN2'] = np.where(tax_cash_df['HSN2']>9, tax_cash_df['HSN2'].astype(str),
                                ('0'+ tax_cash_df['HSN2'].astype(str)))
    
    df_gstr1 = pd.read_excel(filename, sheet_name_gstr1, index_col=False)
    df_gstr1.fillna(0, inplace=True)
    df_gstr1['HSN2'] = np.where(df_gstr1['HSN2']>9, df_gstr1['HSN2'].astype(str),
                                ('0'+ df_gstr1['HSN2'].astype(str)))
   
    # Data is for 8 months now grossedup to one year
    df_gstr1['gstr1_tax_payable'] = df_gstr1['gstr1_tax_payable'] * (12/8)
    tax_cash_df = pd.merge(tax_cash_df, df_gstr1,
                            how="inner", on="HSN2")    
    tax_cash_df['tax_cash'] = (tax_cash_df['cash_tax_payable_ratio'] * 
                                 tax_cash_df['gstr1_tax_payable'])
    tax_collection_gstr1 = tax_cash_df['tax_cash'].sum()
    # GSTR1 does not explain all the tax so blow up
    blow_up_factor = (gst_collection_full_year_dom/tax_collection_gstr1)
    tax_cash_df['tax_payable_bu'] = df_gstr1['gstr1_tax_payable']*blow_up_factor
    tax_cash_df['tax_cash_bu'] = tax_cash_df['tax_cash']*blow_up_factor
    tax_cash_df['tax_itc_bu'] = (tax_cash_df['tax_payable_bu'] - 
                                         tax_cash_df['tax_cash_bu'])
    #tax_cash_dom_less_trade = tax_cash_df['tax_cash_bu'].sum()
    return tax_cash_df


def calc_hsn_sut_conc(filename, concordance_sheet):
    concordance_df = pd.read_excel(filename, concordance_sheet, index_col=False)
    hsn_df = concordance_df.sort_values(['HSN2', 'srl_no'])
    hsn_df['HSN2'] = np.where(hsn_df['HSN2']>9, hsn_df['HSN2'].astype(str),
                                ('0'+ hsn_df['HSN2'].astype(str)))
    hsn_df['key'] = hsn_df['srl_no'].astype(str) + '_' + hsn_df['HSN2']
    hsn_df = hsn_df.drop_duplicates(subset='key', keep='first')
    hsn_df = hsn_df.reset_index()
    hsn_df = hsn_df.drop(['index', 'key', 'HSN', 'product_id'], axis=1)
    hsn_df['srl_no'] = hsn_df['srl_no'].astype(str)
    return hsn_df


def concord_comm_vec(hsn_df_copy, alloc_mat, alloc_var ):
    alloc_comm_vec = calc_sum_by_commodity(alloc_mat)
    alloc_comm_vec_df = pd.DataFrame(data=alloc_comm_vec, columns=np.array([alloc_var]))
    alloc_comm_vec_df = alloc_comm_vec_df.reset_index()
    alloc_comm_vec_df = alloc_comm_vec_df.rename(columns={'index':'srl_no'})
    alloc_comm_vec_df['srl_no'] = alloc_comm_vec_df['srl_no'] + 1
    alloc_comm_vec_df['srl_no'] = alloc_comm_vec_df['srl_no'].astype(str)  
    hsn_df_copy = pd.merge(hsn_df_copy, alloc_comm_vec_df,
                                how="outer", on="srl_no")   
    alloc_hsn2 = hsn_df_copy.groupby('HSN2')[alloc_var].sum()
    alloc_hsn2 = alloc_hsn2.values
    alloc_hsn2_df = pd.DataFrame(data=alloc_hsn2, columns=np.array([alloc_var+'_hsn2']))
    alloc_hsn2_df = alloc_hsn2_df.reset_index()
    alloc_hsn2_df = alloc_hsn2_df.rename(columns={'index':'HSN2'})
    alloc_hsn2_df['HSN2'] = np.where(alloc_hsn2_df['HSN2']>9, alloc_hsn2_df['HSN2'].astype(str),
                                    ('0'+ alloc_hsn2_df['HSN2'].astype(str)))
    hsn_df_copy = pd.merge(hsn_df_copy, alloc_hsn2_df,
                                how="outer", on="HSN2")
    #hsn_df.groupby('HSN2')['tax_cash_bu'].mean().sum()
    hsn_df_copy = hsn_df_copy.dropna()
    #hsn_df.groupby('HSN2')['tax_cash_bu'].mean().sum()
    hsn_df_copy['srl_HSN_wt'] = hsn_df_copy[alloc_var]/hsn_df_copy[alloc_var+'_hsn2']
    #hsn_df.groupby('HSN2')['tax_cash_bu'].mean().sum()
    hsn_df_copy = hsn_df_copy.sort_values('HSN2')
    #hsn_df[['srl_no', 'HSN2', 'tax_cash_bu', 'srl_HSN_wt']]
    if alloc_var=='supply':
        hsn_df_copy['alloc_var_srl_no'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['tax_payable_bu']
    else:
        if alloc_var=='use':
            hsn_df_copy['alloc_var_srl_no'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['tax_itc_bu']
        else:
            if alloc_var=='etr':
                hsn_df_copy['alloc_var_srl_no1'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['taxable_value']
                hsn_df_copy['alloc_var_srl_no2'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['tax_cash']            
    hsn_df_copy = hsn_df_copy.sort_values('srl_no')
    #grouping by serial number as multiple entries are there
    if alloc_var=='etr':
        srl_no_alloc_var1 = hsn_df_copy.groupby('srl_no')['alloc_var_srl_no1'].sum()
        srl_no_alloc_var2 = hsn_df_copy.groupby('srl_no')['alloc_var_srl_no2'].sum()       
        hsn_df_copy['alloc_var_srl_no'] = srl_no_alloc_var1/srl_no_alloc_var2
    
    srl_no_alloc_var = hsn_df_copy.groupby('srl_no')['alloc_var_srl_no'].sum()
    #hsn_df[['srl_no', 'HSN2', 'tax_cash_bu', 'srl_HSN_wt', 'tax_cash_bu_srl_no']]
    srl_no_alloc_var_df = srl_no_alloc_var.reset_index()
    srl_no_alloc_var_df['srl_no'] = srl_no_alloc_var_df['srl_no'].astype(int)
    srl_no_alloc_var_df = srl_no_alloc_var_df.sort_values('srl_no')
    #srl_no_alloc_var_df.to_csv('srl_no_tax_cash.csv')   
    srl_no_alloc_var_vec = srl_no_alloc_var_df['alloc_var_srl_no'].values
    srl_no_alloc_var_vec = srl_no_alloc_var_vec.reshape(srl_no_alloc_var_vec.shape[0], 1)
    return srl_no_alloc_var_vec

def concord_ind_vec(srl_no_alloc_var_vec, allocation_ratio):
    alloc_var_mat = calc_allocation_to_industry(allocation_ratio, srl_no_alloc_var_vec)
    alloc_var_ind_vec = calc_sum_by_industry(alloc_var_mat)
    return alloc_var_ind_vec
    



filename_concordance = 'concordance_2.xlsx'
sheet_name_cash_ratio = 'tax_output_tax_ratio'
sheet_name_gstr1 = 'gstr1'
concordance_sheet = 'concordance'

gst_collection_july17_march18 = 7.41*10**5
igst_import_july17_march18 = 1.73 * 10**5
gst_collection_july17_june18 = gst_collection_july17_march18 * (12/8)
igst_import_july17_june18 = igst_import_july17_march18 * (12/8)
gst_collection_july17_june18_dom = (gst_collection_july17_june18 - 
                                    igst_import_july17_june18)

SUT_trade_margin = 138695029/100
#assuming average rate of 10%
avg_gst_rate_trade = 0.1
gst_trade = SUT_trade_margin*avg_gst_rate_trade

gst_collection_july17_june18_dom_less_trade = (gst_collection_july17_june18_dom -
                                               gst_trade)

gst_collection_full_year_dom = gst_collection_july17_june18_dom_less_trade

tax_cash_df = hsn_tax_ratio(filename_concordance, sheet_name_cash_ratio, sheet_name_gstr1, gst_collection_july17_june18_dom_less_trade)   

filename_SUT = 'India Supply Use Table SUT_12-13.xlsx'
sheet_name_sup = 'supply 2012-13'
sheet_name_use = 'use 2012-13'
sheet_name_rates = 'detailed_rates'
sheet_name_exempt = 'exempt'
sheet_name_reg_ratio = 'gst_reg_ratio'
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
(supply_mat, tax_subsidies_vec, import_vec, trade_margin_vec, industry_header,
 product_header, use_mat, fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec,
 vlbl_vec, cis_vec, export_vec, gst_reg_ratio_ind_vec, industry_group_header,
 rate_vec, exempt_vec) = import_Excel_SUT(filename_SUT, sheet_name_sup, sheet_name_use, 
                     sheet_name_rates, sheet_name_exempt, sheet_name_reg_ratio)

# reshape all vectors to column arrays
(import_vec, trade_margin_vec, tax_subsidies_vec, export_vec,fin_cons_hh_vec, fin_cons_gov_vec,
 gfcf_vec, vlbl_vec, cis_vec, rate_vec, exempt_vec) = re_shape(import_vec, trade_margin_vec,
                                                  tax_subsidies_vec, export_vec,fin_cons_hh_vec,
                                                  fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec,
                                                  rate_vec, exempt_vec)

gst_reg_ratio_ind_vec = gst_reg_ratio_ind_vec.reshape(1, gst_reg_ratio_ind_vec.shape[0])
# Blow up the Supply Use Table and Vectors to current year
(supply_mat, use_mat, import_vec, trade_margin_vec, tax_subsidies_vec, export_vec, fin_cons_hh_vec,
 fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec) = blow_up_mat(supply_mat, use_mat, import_vec,
                                              trade_margin_vec, tax_subsidies_vec, export_vec,
                                              fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec, vlbl_vec,
                                              cis_vec, blow_up_factor)

# Call function to find the ratio of allocation to be used for imports and tax & subsidies
allocation_ratio_by_use_mat = calc_allocation_ratio(use_mat)

# Call function to allocate imports across industries
# import_mat is the matrix containing imports by products & industries
import_mat = calc_allocation_to_industry(allocation_ratio_by_use_mat, import_vec)

# Call function to allocate tax & sunsidies across industries
# tax_subsidy_mat is the matrix containing taxes & sunsidies by products & industries
(use_vec_ratio, fin_cons_hh_vec_ratio, fin_cons_gov_vec_ratio, gfcf_vec_ratio, vlbl_vec_ratio,
 cis_vec_ratio) = calc_allocation_by_use(use_mat, fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec)
tax_subsidies_vec_iiuse = tax_subsidies_vec * (use_vec_ratio)   
tax_subsidy_mat = calc_allocation_to_industry(allocation_ratio_by_use_mat, tax_subsidies_vec_iiuse)

# Call function to allocate gross capital formation across industries
# gfcf_mat is the matrix containing gross capital formation by products & industries
tax_subsidies_vec_gfcf = tax_subsidies_vec * (gfcf_vec_ratio) 
gfcf_less_tax_vec = gfcf_vec - tax_subsidies_vec_gfcf  
gfcf_less_tax_mat = calc_allocation_to_industry(allocation_ratio_by_use_mat, gfcf_less_tax_vec)

# Removing Tax and subsidies from use matrix to reduce tax base
use_less_tax_mat = use_mat - tax_subsidy_mat
# Add gross capital formation to the use_less_tax_mat
use_for_ITC_mat = use_less_tax_mat + gfcf_less_tax_mat

# Call function to allocate exports across industries
# export_mat is the matrix containing exports by products & industries
allocation_ratio_by_supply_mat = calc_allocation_ratio(supply_mat)
export_mat = calc_allocation_to_industry(allocation_ratio_by_supply_mat, export_vec)

# Reducing the exports from supply to get domestic comsumption
supply_less_exports_mat = supply_mat - export_mat

# Calculating Actual GST By Sector
# importing concrdance file
hsn_df = calc_hsn_sut_conc(filename_concordance, concordance_sheet)
# merging concordance file with tax data
hsn_df = pd.merge(hsn_df, tax_cash_df,
                            how="outer", on="HSN2")
hsn_df_copy = hsn_df.copy()
tax_payable_comm_vec = concord_comm_vec(hsn_df_copy, supply_mat, 'supply')
hsn_df_copy = hsn_df.copy()
tax_itc_comm_vec = concord_comm_vec(hsn_df_copy, use_mat, 'use')
hsn_df_copy = hsn_df.copy()
etr_comm_vec = concord_comm_vec(hsn_df_copy, supply_mat, 'etr')

np.savetxt("etr.csv", etr_comm_vec , delimiter=",")

tax_payable_ind_vec = concord_ind_vec(tax_payable_comm_vec, allocation_ratio_by_supply_mat)
tax_itc_ind_vec = concord_ind_vec(tax_itc_comm_vec, allocation_ratio_by_use_mat)
tax_cash_ind_vec = tax_payable_ind_vec - tax_itc_ind_vec
make_ind_vec_df(tax_payable_ind_vec, industry_header, 'tax_payable_ind')
make_ind_vec_df(tax_itc_ind_vec, industry_header, 'tax_itc_ind')
make_ind_vec_df(tax_cash_ind_vec, industry_header, 'tax_cash_ind')

# call functions to calculate output tax and Input tax credit
output_tax_mat = calc_output_tax(supply_less_exports_mat, rate_vec)
input_tax_credit_mat = calc_input_tax_credit(use_for_ITC_mat, rate_vec)
output_tax_ind_vec = calc_sum_by_industry(output_tax_mat)
itc_ind_vec = calc_sum_by_industry(input_tax_credit_mat)

# Calculate ITC disallowed which is based on the ratio of exempt sales to total sales
(itc_disallowed_ratio, exempt_supply_mat) = calc_itc_disallowed_ratio(supply_less_exports_mat, exempt_vec)
itc_disallowed_ind_vec = calc_itc_disallowed(itc_ind_vec, itc_disallowed_ratio)

# Calculate the net ITC available
itc_available_ind_vec = itc_ind_vec - itc_disallowed_ind_vec

# Call function to calculate GST on imports
(GST_on_imports_ind_vec, tot_GST_on_imports) = calc_GST_on_imports(use_mat, import_vec, rate_vec)

# Calculate the GST Potential
gst_potential_less_import_vec = output_tax_ind_vec - itc_available_ind_vec
gst_potential_less_import_vec_reg = gst_reg_ratio_ind_vec * gst_potential_less_import_vec
gst_potential_less_import_total = gst_potential_less_import_vec_reg.sum()
gst_potential_ind_vec = gst_potential_less_import_vec_reg + GST_on_imports_ind_vec
gst_potential_total = gst_potential_ind_vec.sum()

# Print GST Potential in Rs Crores
print(f'GST Potential less imports (Rs Cr.): {gst_potential_less_import_total * 1e-2:.2f}')
print(f'GST Potential on imports (Rs Cr.): {tot_GST_on_imports * 1e-2:.2f}')
print(f'Total GST Potential (Rs Cr.): {gst_potential_total * 1e-2:.2f}')

# Export the importatnt vectors for comparison
make_mat_df(export_mat, industry_header, "export_ind")
make_mat_df(supply_mat, industry_header, "supply_ind")
make_mat_df(import_mat, industry_header, "import_ind")
make_mat_df(supply_less_exports_mat, industry_header, "dom_supply")
make_mat_df(output_tax_mat, industry_header, "output_tax")
make_mat_df(exempt_supply_mat, industry_header, "exempt_ind")
make_mat_df(input_tax_credit_mat, industry_header, "itc_ind")
make_ind_vec_df(itc_disallowed_ind_vec, industry_header, "itc_disall")
make_ind_vec_df(GST_on_imports_ind_vec, industry_header, "GST_imports")
make_ind_vec_df(gst_potential_ind_vec, industry_header, "gst_potential")

# Grouping industries into broader classes for charts
industry_group_df = pd.DataFrame(data=industry_group_header, index=industry_header, columns=np.array(['industry_group']))
industry_group_df = industry_group_df.reset_index()
industry_group_df = industry_group_df.rename(columns={'index':'industry_id'})
industry_group_df.to_csv('Output_csv\industry.csv')

gst_pot_less_import_crores = gst_potential_less_import_vec/100
gst_pot_ind_crores = gst_potential_ind_vec/100
gst_pot_crores = gst_pot_ind_crores.reshape(gst_pot_ind_crores.shape[1], 1)
gst_coll_industry_df = pd.DataFrame(data=gst_pot_crores, index=industry_header, columns=np.array(['GST potential']))
gst_coll_industry_df = gst_coll_industry_df.reset_index()
gst_coll_industry_df = gst_coll_industry_df.rename(columns={'index':'industry_id'})
gst_coll_industry_df.to_csv('Output_csv\gst_coll.csv')
gst_coll_industry_group_df = pd.merge(gst_coll_industry_df, industry_group_df,
                            how="inner", on="industry_id")
gst_coll_industry_group_df = gst_coll_industry_group_df[['industry_group', 'GST potential']]
gst_coll_group_df = gst_coll_industry_group_df.groupby(['industry_group']).sum()
gst_coll_group_df = gst_coll_group_df.reset_index()

industry_group = gst_coll_group_df['industry_group'].values
gst_industry_group = gst_coll_group_df['GST potential'].values



'''
Draw charts for displaying outputs
'''
plt.rcdefaults()
fig, ax = plt.subplots(figsize=(8, 8))
# Example data
x_pos = np.arange(len(industry_group))
ax.bar(x_pos, gst_industry_group, 
        color='green')
ax.set_xticks(x_pos)
ax.set_xticklabels(industry_group, rotation=90)

ax.set_ylabel('Rupees crores')
ax.set_xlabel('Industry')
ax.set_title('GST Potential for India by Industry - 2017')
plt.savefig('GST Potential.png', bbox_inches = "tight")
plt.show()
