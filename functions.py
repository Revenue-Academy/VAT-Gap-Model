import string
import pandas as pd
import numpy as np
from babel.numbers import format_currency

# Function to convert currency into Rupee format
def in_rupees(curr):
    curr_str = format_currency(curr, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    return(remove_decimal(curr_str))

def remove_decimal(S):
    S = str(S)
    S = S[:-3]
    return S

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

# Function to reshape an array to a single colums matrix
def re_shape(input_vec):
    output_vec = input_vec.reshape(input_vec.shape[0], 1)
    return output_vec

# Function to extract data from the Supply Use Table excel file
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
            industry_header, df_product, use_mat, fin_cons_hh_vec,
            fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec, export_vec,
            gst_reg_ratio_ind_vec, industry_group_header, rate_vec, exempt_vec)

# Function to blow up the values with a blow_up factor
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

# Function to adjust supplies to taxpayers only to those who are registered
def adjusted_SUT(gst_reg_ratio_ind_vec, input_mat):
    adj_input_mat = gst_reg_ratio_ind_vec*input_mat
    return adj_input_mat
    
 # Function to compute the output tax   
def calc_output_tax(supply_mat, rate_vec):
    output_tax_mat = supply_mat * rate_vec
    return output_tax_mat

# Function to compute the ratio of ITC disallowed
def calc_itc_disallowed_ratio(supply_mat, exempt_vec):
    exempt_supply_mat = supply_mat * exempt_vec
    exempt_supply_ind_vec = calc_sum_by_industry(exempt_supply_mat)
    supply_ind_vec = calc_sum_by_industry(supply_mat)  
    itc_disallowed_ratio = np.divide(exempt_supply_ind_vec, supply_ind_vec,
                                     out=np.zeros_like(exempt_supply_ind_vec), where=supply_ind_vec!=0)
    return (itc_disallowed_ratio, exempt_supply_mat)

# Function to compute the ITC disallowed
def calc_itc_disallowed(input_tax_credit_vec, itc_disallowed_ratio):
    itc_disallowed_vec = input_tax_credit_vec * itc_disallowed_ratio
    return itc_disallowed_vec

def calc_input_tax_credit(use_mat, rate_vec):
    input_tax_credit_mat = use_mat * rate_vec
    return input_tax_credit_mat

# Function to get the industry wise total of a variable (i.e supply, use, tax etc)
def calc_sum_by_industry(input_mat):
    output_vec = input_mat.sum(axis=0)
    output_vec = output_vec.reshape(1, output_vec.shape[0])
    return output_vec

# Function to get the commodity wise total of a variable (i.e supply, use, tax etc)
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

# Function to calculate the ratio for allocating values of a product to each industry based on adjusted use matrix
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

# Function to export a vector by industry to a csv file
def make_ind_vec_df(input_vec, industry_header, output):
    input_vec = input_vec.reshape(input_vec.shape[1], 1)
    ind_df = pd.DataFrame(data=input_vec, index=industry_header, columns=np.array([output]))
    ind_df = ind_df.reset_index()
    ind_df = ind_df.rename(columns={'index':'industry_id'})
    file_name = "Output_csv\\" + output + ".csv"
    ind_df.to_csv(file_name)
    return ind_df

# Function to export a vector by product to a csv file
def make_comm_vec_df(input_vec, df_product, output):
    input_vec = input_vec.reshape(input_vec.shape[0], 1)
    ind_df = pd.DataFrame(data=input_vec, index=df_product['srl_no'], columns=np.array([output]))
    ind_df = ind_df.reset_index()
    ind_df = ind_df.rename(columns={'index':'srl_no'})
    ind_df = pd.merge(df_product, ind_df,
                            how="inner", on="srl_no")   
    file_name = "Output_csv\\" + output + ".csv"
    ind_df.to_csv(file_name, index=False)
    return ind_df

# Function to export a matrix to a csv file by converting it into vector by industry
def make_mat_ind_df(input_mat, industry_header, output):
    input_vec = calc_sum_by_industry(input_mat)
    make_ind_vec_df(input_vec, industry_header, output)

# Function to export a matrix to a csv file by converting it into vector by industry
def make_mat_df(input_mat, df_product, industry_header, output):
    #input_mat = input_vec.reshape(input_vec.shape[0], 1)
    ind_df = pd.DataFrame(data=input_mat, index=df_product['srl_no'], columns=np.array(industry_header))
    ind_df = ind_df.reset_index()
    #ind_df = ind_df.rename(columns={'index':'srl_no'})
    ind_df = pd.merge(df_product, ind_df,
                            how="inner", on="srl_no")   
    file_name = "Output_csv\\" + output + ".csv"
    ind_df.to_csv(file_name, index=False)
    return ind_df


# Function to extract the relevant tax data (tax payable, ITC and cash) from GSTR1 & GSTR3     
def hsn_tax_data(filename, sheet_name_cash_ratio, sheet_name_gstr1, gst_collection_full_year_dom):   
    # we have data by HSCode of a sample on the output tax and net gst paid (after inout tax credit) 
    # we use this data to calculate the ratio of net tax paid to output tax
    # we shall use this data to apply to data from
    # form gst1 which has only output tax data
    
    # calculating the net tax paid ratios   
    tax_cash_df = pd.read_excel(filename, sheet_name_cash_ratio, index_col=False)
    tax_cash_df.fillna(0, inplace=True)
    tax_cash_df['cash_tax_payable_ratio'] = tax_cash_df['tax_cash']/tax_cash_df['tax_payable']

    tax_cash_df['HSN2'] = np.where(tax_cash_df['HSN2']>9, tax_cash_df['HSN2'].astype(str),
                                ('0'+ tax_cash_df['HSN2'].astype(str)))

    # extracting the data from gstr1   
    df_gstr1 = pd.read_excel(filename, sheet_name_gstr1, index_col=False)
    df_gstr1.fillna(0, inplace=True)
    df_gstr1['HSN2'] = np.where(df_gstr1['HSN2']>9, df_gstr1['HSN2'].astype(str),
                                ('0'+ df_gstr1['HSN2'].astype(str)))
   
    # Data is for 8 months now grossedup to one year
    df_gstr1['gstr1_tax_payable'] = df_gstr1['gstr1_tax_payable'] * (12/8)
    tax_cash_df = pd.merge(tax_cash_df, df_gstr1,
                            how="inner", on="HSN2")  
    # applying the ratios calculated above to calculate the net tax paid
    # from the putput tax given in gstr1
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
    # the dataframe tax_cash explains the complete tax collected
    # and breaks it down by HS Code
    return tax_cash_df

# Function to get the unique combination for SUT srl_no and HSN-2 digit code
def hsn_sut_conc(filename, concordance_sheet):
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


def concord_comm_vec(hsn_df_copy, alloc_mat, alloc_var):
    # concording the srl_no data and allocating to industry
    # allocation is based on the distribution by srl_no
    # as per alloc_mat - Supply or Use
    # we first create a dataframe with the totals of supply by commodity 
    # i.e. by Srl_no
    alloc_comm_vec = calc_sum_by_commodity(alloc_mat)
    alloc_comm_vec_df = pd.DataFrame(data=alloc_comm_vec, columns=np.array([alloc_var]))
    alloc_comm_vec_df = alloc_comm_vec_df.reset_index()
    alloc_comm_vec_df = alloc_comm_vec_df.rename(columns={'index':'srl_no'})
    alloc_comm_vec_df['srl_no'] = alloc_comm_vec_df['srl_no'] + 1
    alloc_comm_vec_df['srl_no'] = alloc_comm_vec_df['srl_no'].astype(str)
    # we then merge this onto the the srl_no HSN concordance file
    # to allocate a HSN for each serial number
    hsn_df_copy = pd.merge(hsn_df_copy, alloc_comm_vec_df,
                                how="outer", on="srl_no")
    # we then group the alloc_var eg. output by HSN 
    alloc_hsn2 = hsn_df_copy.groupby('HSN2')[alloc_var].sum()
    alloc_hsn2 = alloc_hsn2.values
    alloc_hsn2_df = pd.DataFrame(data=alloc_hsn2, columns=np.array([alloc_var+'_hsn2']))
    alloc_hsn2_df = alloc_hsn2_df.reset_index()
    alloc_hsn2_df = alloc_hsn2_df.rename(columns={'index':'HSN2'})
    alloc_hsn2_df['HSN2'] = np.where(alloc_hsn2_df['HSN2']>9, alloc_hsn2_df['HSN2'].astype(str),
                                    ('0'+ alloc_hsn2_df['HSN2'].astype(str)))
    # we merge the alloc_var eg. output by HSN back to the srl_no HSN 
    # concordance we now have the HSN wise total of alloc_var eg. output
    # mapped to every srl_no
    hsn_df_copy = pd.merge(hsn_df_copy, alloc_hsn2_df,
                                how="outer", on="HSN2")
    hsn_df_copy = hsn_df_copy.dropna()
    # we calculate the weight of each output (alloc_var) by commodity for 
    # srl_no over the output per commodity by HSN
    # This gives what proportion of HSN output (alloc_var) is one particular 
    # srl_no
    hsn_df_copy['srl_HSN_wt'] = hsn_df_copy[alloc_var]/hsn_df_copy[alloc_var+'_hsn2']
    hsn_df_copy = hsn_df_copy.sort_values('HSN2')
    # we then use these weights to allocate the parameter we are trying to
    # apportion by srl_no
    if alloc_var=='output tax':
        hsn_df_copy['alloc_var_srl_no'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['tax_payable_bu']
    else:
        if alloc_var=='itc':
            hsn_df_copy['alloc_var_srl_no'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['tax_itc_bu']
        else: 
            if alloc_var=='tax':
                hsn_df_copy['alloc_var_srl_no'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['tax_cash_bu']            
            else:
                if alloc_var=='etr':
                    hsn_df_copy['alloc_var_srl_no1'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['tax_payable']
                    hsn_df_copy['alloc_var_srl_no2'] = hsn_df_copy['srl_HSN_wt'] * hsn_df_copy['taxable_value']
    hsn_df_copy['srl_no'] = hsn_df_copy['srl_no'].astype(int)
    hsn_df_copy = hsn_df_copy.sort_values('srl_no')
    # grouping by serial number as multiple entries are there
    if alloc_var=='etr':
        srl_no_alloc_var1 = hsn_df_copy.groupby('srl_no')['alloc_var_srl_no1'].sum()
        srl_no_alloc_var2 = hsn_df_copy.groupby('srl_no')['alloc_var_srl_no2'].sum()
        srl_no_alloc_var = np.where(srl_no_alloc_var2==0, 0, srl_no_alloc_var1/srl_no_alloc_var2)
        srl_no_alloc_var_vec = srl_no_alloc_var.reshape(srl_no_alloc_var.shape[0], 1)
    else:
        srl_no_alloc_var = hsn_df_copy.groupby('srl_no')['alloc_var_srl_no'].sum()
        # hsn_df[['srl_no', 'HSN2', 'tax_cash_bu', 'srl_HSN_wt', 'tax_cash_bu_srl_no']]
        srl_no_alloc_var_df = srl_no_alloc_var.reset_index()
        srl_no_alloc_var_df['srl_no'] = srl_no_alloc_var_df['srl_no'].astype(int)
        srl_no_alloc_var_df = srl_no_alloc_var_df.sort_values('srl_no')
        # srl_no_alloc_var_df.to_csv('srl_no_tax_cash.csv')   
        srl_no_alloc_var_vec = srl_no_alloc_var_df['alloc_var_srl_no'].values
        srl_no_alloc_var_vec = srl_no_alloc_var_vec.reshape(srl_no_alloc_var_vec.shape[0], 1)
    return srl_no_alloc_var_vec

def concord_ind_vec(srl_no_alloc_var_vec, allocation_ratio):
    alloc_var_mat = calc_allocation_to_industry(allocation_ratio, srl_no_alloc_var_vec)
    # np.savetxt("Output_csv\\alloc_sec.csv", alloc_var_mat , delimiter=",")
    alloc_var_ind_vec = calc_sum_by_industry(alloc_var_mat)
    return alloc_var_ind_vec
