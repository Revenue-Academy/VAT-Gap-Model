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

def import_Excel_SUT_2014(year):

    # First prepare the Excel file by Selecting the entire sheet and unmerging any merged cells
    '''
    SUPPLY table
    '''
    supply_start_col_excel="C"
    supply_end_col_excel = "BP"
    supply_start_col = col2num(supply_start_col_excel)
    supply_end_col=col2num(supply_end_col_excel)
    supply_start_row=4
    supply_end_row=143

    supply_col_product_id_excel = "B"
    supply_col_product_id = col2num(supply_col_product_id_excel)
    supply_row_sector_id = 2

    Import_col_excel = "BX"
    Import_col = col2num(Import_col_excel)

    trade_margin_col_excel = "BZ"
    trade_margin_col = col2num(trade_margin_col_excel)

    tax_subsidies_col_excel = "BR"
    tax_subsidies_col = col2num(tax_subsidies_col_excel)

    '''
    For Latvia EU columns and non-EU columns
    '''
    Import_col_eu_excel = "BQ"
    Import_col_noneu_excel = "BT"
    Import_col_eu = col2num(Import_col_eu_excel)
    Import_col_noneu = col2num(Import_col_noneu_excel)

    '''
    USE table
    '''
    use_start_col_excel="C"
    use_end_col_excel="BO"
    use_start_col=col2num(use_start_col_excel)
    use_end_col=col2num(use_end_col_excel)
    use_start_row=6
    use_end_row=70

    use_col_product_id_excel = "A"
    use_col_product_id = col2num(use_col_product_id_excel)
    use_row_sector_id = 5

    fin_cons_hh_col_excel = "BQ"
    fin_cons_np_col_excel = "BR"
    fin_cons_gov_col_excel = "BS"

    fin_cons_hh_col = col2num(fin_cons_hh_col_excel)
    fin_cons_np_col = col2num(fin_cons_np_col_excel)
    fin_cons_gov_col = col2num(fin_cons_gov_col_excel)

    gcf_col_excel ="BY"
    gcf_col = col2num(gcf_col_excel)

    Export_col_excel = "CD"
    Export_col = col2num(Export_col_excel)

    '''
    For Latvia EU columns and non-EU columns
    '''
    Export_col_eu_excel = "BZ"
    Export_col_noneu_excel = "CC"
    Export_col_eu = col2num(Export_col_eu_excel)
    Export_col_noneu = col2num(Export_col_noneu_excel)

    df = pd.read_excel('India Supply Use Table SUT_12-13_dated_280916_working_copy.xlsx', sheet_name='supply 2012-13')
    #df1 = df.iloc[supply_start_row-2:supply_end_row-1,supply_start_col-1:supply_end_col-1]
    #df2 = df1.fillna(0)
    #

    df1 = df.iloc[:supply_end_row-1,:supply_end_col]
    df1.columns = df1.iloc[supply_row_sector_id-2,:]
    df1.index = df1.iloc[:,supply_col_product_id-1]
    df2 = df1.iloc[supply_start_row-2:,supply_start_col-1:]
    supply_plusdf = df2.fillna(0)
    supply_plus_transdf = supply_plusdf.transpose()

    sector_headers = df1.iloc[supply_row_sector_id-2,:]
    product_headers = df1.iloc[:,supply_col_product_id-1]
    sector_headers = sector_headers[2:].values
    product_headers = product_headers[4:].values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Import_col-1]
    df2 = df1.fillna(0)
    imports = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Import_col_eu-1]
    df2 = df1.fillna(0)
    imports_eu = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Import_col_noneu-1]
    df2 = df1.fillna(0)
    imports_noneu = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, trade_margin_col-1]
    df2 = df1.fillna(0)
    trade_margins = df2.values
    trade_marginsdf = pd.DataFrame(data=trade_margins, index=product_headers, columns=np.array(['Trade Margins']))

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, tax_subsidies_col-1]
    df2 = df1.fillna(0)
    tax_subsidies = df2.values
    tax_subsidiesdf = pd.DataFrame(data=tax_subsidies, index=product_headers, columns=np.array(['Tax and Subsidies']))

    df = pd.read_excel('Supply Use tables - 2014.xlsx', sheet_name='USE 2014')
#    df1 = df.iloc[use_start_row-2:use_end_row-1,use_start_col-1:use_end_col-1]
#    df2 = df1.fillna(0)
#    use = df2.values

    df1 = df.iloc[:use_end_row-1,:use_end_col]
    df1.columns  =df1.iloc[use_row_sector_id-2,:]
    df1.index = df1.iloc[:,use_col_product_id-1]
    df2 = df1.iloc[use_start_row-2:,use_start_col-1:]
    use_plusdf = df2.fillna(0)

    df1 = df.iloc[use_start_row-2:use_end_row-1, fin_cons_hh_col-1]
    df2 = df1.fillna(0)
    fin_cons_hh = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1,fin_cons_np_col-1]
    df2 = df1.fillna(0)
    fin_cons_np = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, fin_cons_gov_col-1]
    df2 = df1.fillna(0)
    fin_cons_gov = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, gcf_col-1]
    df2 = df1.fillna(0)
    gcf = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, Export_col-1]
    df2 = df1.fillna(0)
    exports = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, Export_col_eu-1]
    df2 = df1.fillna(0)
    exports_eu = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Export_col_noneu-1]
    df2 = df1.fillna(0)
    exports_noneu = df2.values

#    tot_sup_comm=supply.sum(axis=1)
#    tot_use_comm=use.sum(axis=1)

    fin_cons=fin_cons_hh+fin_cons_np+fin_cons_gov

    return (supply_plusdf, supply_plus_transdf, use_plusdf, sector_headers, product_headers, imports_eu, imports_noneu, trade_marginsdf, tax_subsidiesdf, exports_eu, exports_noneu, fin_cons, gcf)

def import_Excel_SUT_2013(year):

    # First prepare the Excel file by Selecting the entire sheet and unmerging any merged cells
    '''
    SUPPLY table
    '''
    supply_start_col_excel="E"
    supply_end_col_excel = "BQ"
    supply_start_col = col2num(supply_start_col_excel)
    supply_end_col=col2num(supply_end_col_excel)
    supply_start_row=8
    supply_end_row=72

    supply_col_product_id_excel = "C"
    supply_col_product_id = col2num(supply_col_product_id_excel)
    supply_row_sector_id = 5

    Import_col_excel = "BW"
    Import_col = col2num(Import_col_excel)

    trade_margin_col_excel = "BY"
    trade_margin_col = col2num(trade_margin_col_excel)

    tax_subsidies_col_excel = "BZ"
    tax_subsidies_col = col2num(tax_subsidies_col_excel)

    '''
    For Latvia EU columns and non-EU columns
    '''
    Import_col_eu_excel = "BS"
    Import_col_noneu_excel = "BV"
    Import_col_eu = col2num(Import_col_eu_excel)
    Import_col_noneu = col2num(Import_col_noneu_excel)

    '''
    USE table
    '''
    use_start_col_excel="E"
    use_end_col_excel="BQ"
    use_start_col=col2num(use_start_col_excel)
    use_end_col=col2num(use_end_col_excel)
    use_start_row=8
    use_end_row=72

    use_col_product_id_excel = "C"
    use_col_product_id = col2num(use_col_product_id_excel)
    use_row_sector_id = 5

    fin_cons_hh_col_excel = "BS"
    fin_cons_np_col_excel = "BT"
    fin_cons_gov_col_excel = "BU"

    fin_cons_hh_col = col2num(fin_cons_hh_col_excel)
    fin_cons_np_col = col2num(fin_cons_np_col_excel)
    fin_cons_gov_col = col2num(fin_cons_gov_col_excel)

    gcf_col_excel ="CA"
    gcf_col = col2num(gcf_col_excel)

    Export_col_excel = "CF"
    Export_col = col2num(Export_col_excel)

    '''
    For Latvia EU columns and non-EU columns
    '''
    Export_col_eu_excel = "CB"
    Export_col_noneu_excel = "CE"
    Export_col_eu = col2num(Export_col_eu_excel)
    Export_col_noneu = col2num(Export_col_noneu_excel)


    df = pd.read_excel('Supply Use Tables - 2011-2013.xlsx', sheet_name='Supply_2013')
    #df1 = df.iloc[supply_start_row-2:supply_end_row-1,supply_start_col-1:supply_end_col-1]
    #df2 = df1.fillna(0)
    #

    df1 = df.iloc[:supply_end_row-1,:supply_end_col]
    df1.columns = df1.iloc[supply_row_sector_id-2,:]
    df1.index = df1.iloc[:,supply_col_product_id-1]
    df2 = df1.iloc[supply_start_row-2:,supply_start_col-1:]
    supply_plusdf = df2.fillna(0)
    supply_plus_transdf = supply_plusdf.transpose()

    sector_headers = df1.iloc[supply_row_sector_id-2,:]
    product_headers = df1.iloc[:,supply_col_product_id-1]
    sector_headers = sector_headers[4:].values
    product_headers = product_headers[6:].values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Import_col-1]
    df2 = df1.fillna(0)
    imports = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Import_col_eu-1]
    df2 = df1.fillna(0)
    imports_eu = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Import_col_noneu-1]
    df2 = df1.fillna(0)
    imports_noneu = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, trade_margin_col-1]
    df2 = df1.fillna(0)
    trade_margins = df2.values
    trade_marginsdf = pd.DataFrame(data=trade_margins, index=product_headers, columns=np.array(['Trade Margins']))

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, tax_subsidies_col-1]
    df2 = df1.fillna(0)
    tax_subsidies = df2.values
    tax_subsidiesdf = pd.DataFrame(data=tax_subsidies, index=product_headers, columns=np.array(['Tax and Subsidies']))

    df = pd.read_excel('Supply Use Tables - 2011-2013.xlsx', sheet_name='Use_2013')
#    df1 = df.iloc[use_start_row-2:use_end_row-1,use_start_col-1:use_end_col-1]
#    df2 = df1.fillna(0)
#    use = df2.values

    df1 = df.iloc[:use_end_row-1,:use_end_col]
    df1.columns  =df1.iloc[use_row_sector_id-2,:]
    df1.index = df1.iloc[:,use_col_product_id-1]
    df2 = df1.iloc[use_start_row-2:,use_start_col-1:]
    use_plusdf = df2.fillna(0)

    df1 = df.iloc[use_start_row-2:use_end_row-1, fin_cons_hh_col-1]
    df2 = df1.fillna(0)
    fin_cons_hh = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1,fin_cons_np_col-1]
    df2 = df1.fillna(0)
    fin_cons_np = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, fin_cons_gov_col-1]
    df2 = df1.fillna(0)
    fin_cons_gov = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, gcf_col-1]
    df2 = df1.fillna(0)
    gcf = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, Export_col-1]
    df2 = df1.fillna(0)
    exports = df2.values

    df1 = df.iloc[use_start_row-2:use_end_row-1, Export_col_eu-1]
    df2 = df1.fillna(0)
    exports_eu = df2.values

    df1 = df.iloc[supply_start_row-2:supply_end_row-1, Export_col_noneu-1]
    df2 = df1.fillna(0)
    exports_noneu = df2.values

#    tot_sup_comm=supply.sum(axis=1)
#    tot_use_comm=use.sum(axis=1)

    fin_cons=fin_cons_hh+fin_cons_np+fin_cons_gov

    return (supply_plusdf, supply_plus_transdf, use_plusdf, sector_headers, product_headers, imports_eu, imports_noneu, trade_marginsdf, tax_subsidiesdf, exports_eu, exports_noneu, fin_cons, gcf)

def import_tax_rates():
    # Import the tax rates
    df = pd.read_excel('Inputs for VAT Gap Estimation.xlsx', sheet_name='Effective Tax Rates')
    df1 = df.iloc[0:65,0:7]
    df2 = df1.fillna(0)
    #df2['Product_ID']=df2['Product_ID'].str[5:len(df2['Product_ID'])]
    tax_rates_alldf = df2
    tax_rates_alldf.set_index('Product_ID', inplace=True)
    return tax_rates_alldf

def get_tax_rates_yr(tax_rates_alldf, year):
    tax_rates_yrdf = tax_rates_alldf[['ETR_'+str(year)]]
    #tax_rates_yrdf = tax_rates_alldf.iloc[:,0:year-2011+2:year-2011+1]
#    tax_rates_yr = tax_rates_yrdf.iloc[:,1:].values
#    tax_rates_yr = tax_rates_all[:,year-2011]
#    tax_rates_yr = tax_rates.reshape(tax_rates.shape[0], 1)
#    tax_rates_vec = tax_rates_yrdf.values
    return tax_rates_yrdf

def alloc_final_cons_to_sectors(supply_mat, fin_cons):
    # Final Consumption needs to be allocated to the sectors that make the sale
    # This is needed because final consumption is shown by commodity
    # The allocation method used is that final consumptions is sold by those sectors in proportion of the commodities they produce
    tot_sup_comm_corr=np.transpose(np.array([np.sum(supply_mat,axis=1)]))
    """
    fix this 0.001 issue
    """
    tot_sup_comm_corr[tot_sup_comm_corr==0]= 0.00001
    fin_cons_alloc = fin_cons*supply_mat*(1/tot_sup_comm_corr)
    fin_cons_allocdf = pd.DataFrame(data=fin_cons_alloc, index=product_headers,columns=sector_headers)
    return (fin_cons_allocdf)

def alloc_imports_to_sectors(imports_eu, imports_noneu, inter_use_mat_comm_ratio):
    # Imports are shown in the Supply Table by commodity needs to be allocated to the sectors that import them
    # This is needed because final consumption is shown by commodity
    # The allocation method used is that imports consumptions is sold by those sectors in proportion of the commodities
    # they use
    # exact allocation could be available from trade statistics
    #imports_tot_adj = imports_eu_adj + imports_noneu_adj

    imports_eu_alloc = inter_use_mat_comm_ratio*imports_eu
    imports_noneu_alloc = inter_use_mat_comm_ratio*imports_noneu
    imports_eu_alloc_sec =np.matmul(inter_use_mat_comm_ratio.transpose(),imports_eu)
    imports_noneu_alloc_sec =np.matmul(inter_use_mat_comm_ratio.transpose(),imports_noneu)

    return(imports_eu_alloc, imports_eu_alloc_sec, imports_noneu_alloc, imports_noneu_alloc_sec)

def adjust_imports(imports_eu, imports_noneu):
    col = np.array(['imports_eu_adj'])
    row = np.zeros(np.shape(sector_headers))
    df1 = pd.DataFrame(data=row, index=sector_headers, columns=col)
    df1 = df1.reset_index()
    df1 = df1.rename(columns={'index':'Sector_ID'})

    df2 = pd.read_excel('Inputs for VAT Gap Estimation.xlsx', sheet_name='imports_returns')
    df2 = df2[df2['year']==2011]
    df2 = df1.merge(df2, on=['Sector_ID'], how='left')
    df2 = df2.fillna(0)
    df2 = df2[['Sector_ID','Imports from EU']]
    sum = df2['Imports from EU'].sum()
    df2['Import Weights'] = df2['Imports from EU']/sum

    sum1 = imports_eu.sum()
    df2['Imports EU Adj'] = df2['Import Weights']*sum1
    imports_eu_adj = df2['Imports EU Adj'].values
    imports_eu_adj = imports_eu_adj.reshape(imports_eu_adj.shape[0],1)

    sum2 = imports_noneu.sum()
    df2['Imports non-EU Adj'] = df2['Import Weights']*sum2
    imports_noneu_adj = df2['Imports non-EU Adj'].values
    imports_noneu_adj = imports_noneu_adj.reshape(imports_noneu_adj.shape[0],1)

    return (imports_eu_adj, imports_noneu_adj)

def alloc_sec_imports_to_comm(imports_eu_alloc_sec, imports_noneu_alloc_sec, inter_use_mat_sec_ratio):
    # Imports are shown in the Supply Table by commodity needs to be allocated to the sectors that import them
    # This is needed because final consumption is shown by commodity
    # The allocation method used is that imports consumptions is sold by those sectors in proportion of the commodities
    # they use
    # exact allocation could be available from trade statistics
    #imports_tot_adj = imports_eu_adj + imports_noneu_adj


    #Assumption
    #We take the adjusted imports by sector to be that for commodities
    imports_eu_comm_adj = imports_eu_alloc_sec
    imports_noneu_comm_adj = imports_noneu_alloc_sec
    return(imports_eu_comm_adj, imports_noneu_comm_adj)


def alloc_gcf_to_sectors(use_mat, gcf):
    # Gross Capital Formation is shown in the Use Table by commodity needs to be allocated to the sectors that use them
    # This is needed because Gross Capital Formation is shown by commodity
    # The allocation method used is that use of commodities for Gross Capital Formation
    # is used by those sectors in proportion of the non-Gross Capital Formation
    # commodities they use
    tot_use_comm_corr=np.transpose(np.array([np.sum(use_mat,axis=1)]))
    tot_use_comm_corr[tot_use_comm_corr==0]= 0.00001
    gcf_alloc = gcf*use_mat*(1/tot_use_comm_corr)
    gcf_alloc_2013 = pd.DataFrame(data=gcf_alloc, index=product_headers, columns=sector_headers)
    gcf_alloc_2013.to_csv('gcf_2013.csv', index = True)
    return (gcf_alloc)

def modify_imports_for_trade_sector(use_mat, imports_eu, imports_noneu):

    df = pd.read_excel('Inputs for VAT Gap Estimation.xlsx', sheet_name='Trade_Sector_Purchases')
    df1 = pd.DataFrame(data=df.values[:,1:], index = df['Sector_ID'], columns=df.columns[1:])
    #tot_use_sector_corr=np.sum(use_plusdf,axis=0)

    tot_inter_use_sector=use_mat.sum(axis=0)
    tot_inter_use_sector.reshape(tot_inter_use_sector.shape[0],1)
    #output_tax_potential = output_tax_pot.reshape((output_tax_pot.shape[0], 1))
    #output_tax_potential = np.transpose(output_tax_potential)
    col_header = np.array(['Total Purchases'])
    tot_inter_use_sectordf = pd.DataFrame(data=tot_inter_use_sector, index = sector_headers, columns=col_header)

    tot_inter_use_sectordf.loc['V45']=df1.loc['V45','Purchases_'+str(year)]
    tot_inter_use_sectordf.loc['V46']=df1.loc['V46','Purchases_'+str(year)]
    tot_inter_use_sectordf.loc['V47']=df1.loc['V47','Purchases_'+str(year)]

    sum = tot_inter_use_sectordf['Total Purchases'].sum()
    tot_inter_use_sectordf['Total Purchases'] = tot_inter_use_sectordf['Total Purchases']/sum
    tot_inter_use_sectordf = tot_inter_use_sectordf.rename(columns={'Total Purchases':'Weight Purchase'})

    inter_use_sector_weights = tot_inter_use_sectordf.values

    tot_imports_eu = imports_eu.sum()
    tot_imports_noneu = imports_noneu.sum()

    tot_imports_eu_sec_adj = inter_use_sector_weights*tot_imports_eu
    np.savetxt('imports_eu_sec_adj'+str(year) + '.csv', tot_imports_eu_sec_adj, delimiter = ',')
    tot_imports_noneu_sec_adj = inter_use_sector_weights*tot_imports_noneu
    np.savetxt('imports_noneu_sec_adj'+str(year) + '.csv', tot_imports_noneu_sec_adj, delimiter = ',')

    return (tot_imports_eu_sec_adj, tot_imports_noneu_sec_adj)

def adjust_etr_for_trade_sectors(trade_marginsdf, tax_rates_vecdf):
    #trade_margins_vec = trade_marginsdf.values
    #trade_marginsdf = trade_marginsdf.reset_index()
    #trade_marginsdf.rename(columns = {trade_marginsdf.columns[0]: 'Product_ID'}, inplace = True)

    #trade_marginsdf = trade_marginsdf.index.names = ['Product_ID']

    df = trade_marginsdf.copy()
    #df.loc['CPA_G45':'CPA_G47'] = 0
    df = df.reset_index()
    df = df.rename(columns={'index':'Product_ID'})

    df = df.merge(tax_rates_vecdf, on=['Product_ID'], how='left')

    df['Trade Margins'] = np.where(df['Product_ID'] == 'CPA_G45', 0, df['Trade Margins'])
    df['Trade Margins'] = np.where(df['Product_ID'] == 'CPA_G46', 0, df['Trade Margins'])
    df['Trade Margins'] = np.where(df['Product_ID'] == 'CPA_G47', 0, df['Trade Margins'])

    #df = df.join(tax_rates_vecdf)

    sum = df['Trade Margins'].sum()
    df['Weighted Tax Rates'] = df['ETR']*df['Trade Margins']/sum
    etr_for_trade_sectors = df['Weighted Tax Rates'].sum()
    df['ETR'] = np.where(df['Product_ID'] == 'CPA_G45', etr_for_trade_sectors, df['ETR'])
    df['ETR'] = np.where(df['Product_ID'] == 'CPA_G46', etr_for_trade_sectors, df['ETR'])
    df['ETR'] = np.where(df['Product_ID'] == 'CPA_G47', etr_for_trade_sectors, df['ETR'])
    tax_rates_yr_adjdf = df[['Product_ID', 'ETR']].copy()

    return tax_rates_yr_adjdf

def alloc_exports_to_sectors(supply_mat, exports_eu, exports_noneu):
    # Exports needs to be allocated to the sectors that make the commodities that are exported
    # This is needed because exports are shown by commodity
    # The allocation method used is that exported commodities are made by those sectors in proportion of the commodities they produce
    # exact allocation could be available from trade statistics
    tot_sup_comm_corr=np.transpose(np.array([np.sum(supply_mat,axis=1)]))
    tot_sup_comm_corr[tot_sup_comm_corr==0]= 0.00001
    exports_eu = exports_eu.reshape((exports_eu.shape[0], 1))
    exports_eu_alloc = exports_eu*supply_mat*(1/tot_sup_comm_corr)
    exports_noneu = exports_noneu.reshape((exports_noneu.shape[0], 1))
    exports_noneu_alloc = exports_noneu*supply_mat*(1/tot_sup_comm_corr)
    return (exports_eu_alloc, exports_noneu_alloc)

def get_vat_revenues(year):
    col_dict = {'NACE_code2': str, 'Sector_ID': str}
    nace_sector_map = pd.read_excel("NACE_sector_mapping.xlsx", dtype=col_dict)
    tax_revenuedf = pd.read_excel('Tax revenues - 2013-2016.xlsx', sheet_name=str(year))
    tax_revenuedf = tax_revenuedf.groupby('NACE_code2').agg({"Revenue": "sum"})
    tax_revenuedf = tax_revenuedf.reset_index()
    tax_revenue_mergeddf = tax_revenuedf.merge(nace_sector_map, on=['NACE_code2'], how='left')
    tax_revenue_mergeddf = tax_revenue_mergeddf.iloc[:-1,1:]
    tax_revenue_mergeddf = tax_revenue_mergeddf.groupby(['Sector_ID'], sort=False).agg({"Revenue": "sum"})
    tax_revenue_mergeddf['Revenue']=tax_revenue_mergeddf['Revenue']/1e+6

    tax_revenue_mergeddf = tax_revenue_mergeddf.reset_index()
    tax_revenue_mergeddf = tax_revenue_mergeddf.rename(columns={'index':'Sector_ID'})
    col = np.array(['Revenue1'])
    row = np.zeros(np.shape(sector_headers))
    df = pd.DataFrame(data=row, index=sector_headers, columns=col)
    df = df.reset_index()
    df = df.rename(columns={'index':'Sector_ID'})
    df = df.merge(tax_revenue_mergeddf, on=['Sector_ID'], how='left')
    df = df.drop('Revenue1', axis=1)
    df = df.fillna(0)
    tax_revenue_mergeddf = df
    tax_revenue_mergeddf.to_csv('tax_revenue_' + str(year) + '.csv', index=True)
    return tax_revenue_mergeddf

def import_check_sectordf(excel_file, worksheet, param_name, year):
    col = np.array([param_name])
    row = np.zeros(np.shape(sector_headers))
    df = pd.DataFrame(data=row, index=sector_headers, columns=col)
    df = df.reset_index()
    df = df.rename(columns={'index':'Sector_ID'})
    df1 = pd.read_excel(excel_file, sheet_name=worksheet)
    df1 = df1[['Sector_ID_'+str(year), param_name+'_'+str(year)]].copy()
    df1.rename(columns = {df1.columns[0]: df1.columns[0][:-5]}, inplace = True)
    df = df.merge(df1, on=['Sector_ID'], how='left')
    df = df[['Sector_ID',param_name+'_'+str(year)]]
    df = df.fillna(0)
    df.rename(columns = {df.columns[1]: df.columns[1][:-5]}, inplace = True)
    #df = df[param_name+'_'+str(year)].fillna(0)
    return df

def import_check_productdf(excel_file, worksheet, param_name, year):
    col = np.array([param_name])
    row = np.zeros(np.shape(product_headers))
    df = pd.DataFrame(data=row, index=product_headers, columns=col)
    df = df.reset_index()
    df = df.rename(columns={'index':'Product_ID'})
    df1 = pd.read_excel(excel_file, sheet_name=worksheet)
    df1 = df1[['Product_ID_'+str(year), param_name+'_'+str(year)]].copy()
    df1.rename(columns = {df1.columns[0]: df1.columns[0][:-5]}, inplace = True)
    df = df.merge(df1, on=['Product_ID'], how='left')
    df = df[['Product_ID',param_name+'_'+str(year)]]
    df = df.fillna(0)
    df.rename(columns = {df.columns[1]: df.columns[1][:-5]}, inplace = True)
    #df = df[param_name+'_'+str(year)].fillna(0)
    return df


def import_va_non_payers(year):
    va_payersdf = import_check_sectordf('Inputs for VAT Gap Estimation.xlsx', 'va_payers', 'va_payers', year)
    va_non_payersdf = import_check_sectordf('Inputs for VAT Gap Estimation.xlsx', 'va_non_payers', 'va_non_payers', year)
    return va_payersdf, va_non_payersdf

def va_by_reg_ratio_yr(va_payersdf, va_non_payersdf, year):
    va_by_reg_ratiodf = va_payersdf.copy()
    va_by_reg_ratiodf = va_by_reg_ratiodf.merge(va_non_payersdf, on=['Sector_ID'], how='left')
    va_by_reg_ratiodf['va_by_reg_ratio'] = va_by_reg_ratiodf['va_payers']/(va_by_reg_ratiodf['va_payers'] + va_by_reg_ratiodf['va_non_payers'])
    va_by_reg_ratiodf = va_by_reg_ratiodf.fillna(0)
    va_by_reg_ratiodf.to_csv('va_by_reg_ratio_' + str(year) + '.csv', index = True)
    va_by_reg_ratio = va_by_reg_ratiodf['va_by_reg_ratio'].values
    va_by_reg_ratio = va_by_reg_ratio.reshape(va_by_reg_ratio.shape[0], 1)
    """
    Adjusted Ratios
    """
    va_by_reg_ratiodf1 = pd.read_excel('Value Added by Registered Taxpayers - 2013.xlsx', sheet_name='va_payers')

    return (va_by_reg_ratio, va_by_reg_ratiodf1)

def get_reverse_charge_vec(supply_plusdf, year):
    col = np.array(['Reverse Charge Ratio'])
    row = np.zeros(np.shape(product_headers))
    rcdf2 = pd.DataFrame(data=row, index=product_headers, columns=col)
    rcdf2 = rcdf2.reset_index()
    rcdf2 = rcdf2.rename(columns={'index':'Product_ID'})

    rcdf1 = pd.read_excel('Inputs for VAT Gap Estimation.xlsx', sheet_name='rc')
    rcdf1 = rcdf1.iloc[:,(year-2011)*2:((year-2011)*2)+2]
    rcdf1.rename(columns = {rcdf1.columns[0]: rcdf1.columns[0][:-5]}, inplace = True)

    rcdf2 = rcdf2.merge(rcdf1, on=['Product_ID'], how='left')

    rcdf2 = rcdf2[['Product_ID','rc_'+str(year)]]
    rcdf2 = rcdf2['rc_'+str(year)].fillna(0)
    rc_vec = rcdf2.values
    return rc_vec

def get_supply_mat_param(supply_mat):
    tot_sup_comm= np.sum(supply_mat,axis=1)
    tot_sup_comm[tot_sup_comm==0]= 0.00001
    tot_sup_comm = tot_sup_comm.reshape((tot_sup_comm.shape[0], 1))
    supply_mat_comm_ratio = supply_mat/tot_sup_comm

    tot_sup_sec= np.sum(supply_mat,axis=0)
    tot_sup_sec[tot_sup_sec==0]= 0.00001
    tot_sup_sec = tot_sup_sec.reshape((tot_sup_sec.shape[0], 1))
    supply_mat_sec_ratio = supply_mat/tot_sup_sec

    return (tot_sup_comm, tot_sup_sec, supply_mat_comm_ratio, supply_mat_sec_ratio)

def adjust_supply_mat_with_margins_and_non_vat_tax(tax_rates_vec, supply_plusdf, trade_marginsdf, tax_subsidiesdf, imports_eu, imports_noneu):
    imports = imports_eu + imports_noneu
    imports[imports==0]= 0.00001
    imports = imports.reshape((imports.shape[0], 1))

    trade_margins = trade_marginsdf.values
    tax_subsidies = tax_subsidiesdf.values

    dom_supply_ratio1 = tot_sup_comm_corr/(tot_sup_comm_corr+imports)
    trade_margins_dom = trade_margins*dom_supply_ratio1
    dom_supply_ratio2 = tot_sup_comm_corr/(tot_sup_comm_corr+imports_noneu)
    tax_subsidies_dom = tax_subsidies*dom_supply_ratio2

    trade_margins_imp = trade_margins - trade_margins_dom
    tax_subsidies_imp = tax_subsidies - tax_subsidies_dom

    #trade_margins_imp_eu = trade_margins_imp*(imports_eu/imports)
    #trade_margins_imp_noneu = trade_margins_imp - trade_margins_imp_eu

    # EU imports do not face any taxes so only adjust non EU imports to include customs duty in base
    tax_subsidies_imp_noneu = tax_subsidies_imp


    #margins_alloc_supply_mat = (supply_mat/tot_sup_comm_corr)*(trade_margins_dom)

    #supply_mat_with_margins = supply_mat + margins_alloc_supply_mat
    tax_subsidies_dom = tax_subsidies_dom*(1/(1+tax_rates_vec))
    tax_subsidies_imp_noneu = tax_subsidies_imp_noneu*(1/(1+tax_rates_vec))

    supply_mat_with_tax = supply_mat + supply_mat_ratio*tax_subsidies_dom
    imp_noneu_with_tax = imports_noneu + tax_subsidies_imp_noneu

    return (supply_mat_with_tax, imp_noneu_with_tax, tax_subsidies_dom)

def get_inter_use_mat_param(use_mat):
    tot_inter_use_comm= np.sum(use_mat,axis=1)
#    tot_inter_use_comm[tot_inter_use_comm==0]= 0.00001
    tot_inter_use_comm = tot_inter_use_comm.reshape(tot_inter_use_comm.shape[0], 1)
    inter_use_mat_comm_ratio = (use_mat/tot_inter_use_comm)
    inter_use_mat_comm_ratio[np.isnan(inter_use_mat_comm_ratio)] = 0
    tot_inter_use_sec= np.sum(use_mat,axis=0)
#    tot_inter_use_sec[tot_inter_use_sec==0]= 0.00001
    tot_inter_use_sec = tot_inter_use_sec.reshape(1, tot_inter_use_sec.shape[0])
    inter_use_mat_sec_ratio = (use_mat/tot_inter_use_sec)
    inter_use_mat_sec_ratio[np.isnan(inter_use_mat_sec_ratio)] = 0
    return (tot_inter_use_comm, tot_inter_use_sec, inter_use_mat_comm_ratio, inter_use_mat_sec_ratio)

def get_use_mat_param(use_mat, tot_inter_use_comm, fin_cons, gcf):
    tot_use_comm= tot_inter_use_comm + fin_cons + gcf
    inter_use_comm_ratio = tot_inter_use_comm/tot_use_comm
    inter_use_comm_ratio[np.isnan(inter_use_comm_ratio)] = 0
    fin_cons_comm_use_ratio = fin_cons/tot_use_comm
    fin_cons_comm_use_ratio[np.isnan(fin_cons_comm_use_ratio)] = 0
    gcf_comm_use_ratio = gcf/tot_use_comm
    gcf_comm_use_ratio[np.isnan(gcf_comm_use_ratio)] = 0
    return (inter_use_comm_ratio, fin_cons_comm_use_ratio, gcf_comm_use_ratio)

def get_use_mat_tax_excl(use_mat, fin_cons, gcf, inter_use_comm_ratio, inter_use_mat_comm_ratio, fin_cons_comm_use_ratio, gcf_comm_use_ratio, tax_subsidies):
    inter_use_tax_subsidies_comm = inter_use_comm_ratio*tax_subsidies
    inter_use_tax_subsidies_mat = inter_use_mat_comm_ratio*inter_use_tax_subsidies_comm
    fin_cons_tax_subsidies_comm = fin_cons_comm_use_ratio*tax_subsidies
    gcf_tax_subsidies_comm = gcf_comm_use_ratio*tax_subsidies

    inter_use_tax_excl_mat = use_mat - inter_use_tax_subsidies_mat
    fin_cons_tax_excl = fin_cons - fin_cons_tax_subsidies_comm
    gcf_tax_excl = gcf - gcf_tax_subsidies_comm
    return (inter_use_tax_excl_mat, fin_cons_tax_excl, gcf_tax_excl)

def get_fin_cons_tax_excl(fin_cons_tax_incl, tax_rates_vecdf):
    tax_rates_vec = tax_rates_vecdf.values
    fin_cons = fin_cons_tax_incl*(1/(1+tax_rates_vec))
    return fin_cons

def get_gcf_tax_excl(gcf_tax_incl, tax_rates_vecdf):
    tax_rates_vec = tax_rates_vecdf.values
    gcf = gcf_tax_incl*(1/(1+tax_rates_vec))
    return gcf

def get_ratio_fin_cons(use_mat, fin_cons, gcf):
    inter_use = use_mat.sum(axis=1)
    inter_use = inter_use.reshape((inter_use.shape[0], 1))
    tot_use = inter_use + fin_cons + gcf
    tot_use[tot_use==0]= 0.00001
    fin_cons_ratio = fin_cons/tot_use
    gcf_ratio = gcf/tot_use
    return (fin_cons_ratio, gcf_ratio)

def alloc_dom_output_to_use(output_dom, inter_use_comm_ratio, fin_cons_comm_use_ratio, gcf_comm_use_ratio, inter_use_mat_comm_ratio):
    output_dom[output_dom<0]= 0
    output_dom_supply_comm = output_dom.sum(axis=1)
    output_dom_supply_comm = output_dom_supply_comm.reshape((output_dom_supply_comm.shape[0], 1))
    np.savetxt('output_dom_supply_comm_'+str(year) + '.csv', output_dom_supply_comm, delimiter = ',')

    inter_use_dom_sources_comm = output_dom_supply_comm*inter_use_comm_ratio
    np.savetxt('inter_use_dom_sources_comm_'+str(year) + '.csv', inter_use_dom_sources_comm, delimiter = ',')

    inter_use_dom_sources_mat = inter_use_dom_sources_comm*inter_use_mat_comm_ratio
    np.savetxt('inter_use_dom_sources_mat_'+str(year) + '.csv', inter_use_dom_sources_mat, delimiter = ',')

    fin_cons_dom_sources = output_dom_supply_comm*fin_cons_comm_use_ratio
    np.savetxt('fin_cons_dom_sources_'+str(year) + '.csv', fin_cons_dom_sources, delimiter = ',')
    gcf_dom_sources = output_dom_supply_comm*gcf_comm_use_ratio
    return (inter_use_dom_sources_mat, fin_cons_dom_sources, gcf_dom_sources)


def get_output_tax_potential(tax_rates_vec, supply_mat, supply_mat_comm_ratio, exports_alloc, rc_vec, inter_use_comm_ratio, fin_cons, fin_cons_comm_use_ratio, gcf_comm_use_ratio, inter_use_mat_comm_ratio, year):

    output_dom = supply_mat - exports_alloc
    np.savetxt('supply_mat_'+str(year) + '.csv', supply_mat, delimiter = ',')
    np.savetxt('exports_alloc_'+str(year) + '.csv', exports_alloc, delimiter = ',')
    np.savetxt('output_dom_'+str(year) + '.csv', output_dom, delimiter = ',')

    inter_use_dom_sources_mat, fin_cons_dom_sources, gcf_dom_sources = alloc_dom_output_to_use(output_dom, inter_use_comm_ratio, fin_cons_comm_use_ratio, gcf_comm_use_ratio, inter_use_mat_comm_ratio)

    fin_cons_alloc = supply_mat_comm_ratio*fin_cons

    output_tax = output_dom*tax_rates_vec

    rev_charge_supply_mat = supply_mat - fin_cons_alloc

    output_tax_rc = rc_vec*rev_charge_supply_mat

    net_output_tax = output_tax - output_tax_rc

    net_output_tax[net_output_tax<0]= 0

    np.savetxt('output_tax_'+str(year) + '.csv', output_tax, delimiter = ',')
    np.savetxt('output_tax_rc_'+str(year) + '.csv', output_tax_rc, delimiter = ',')
    np.savetxt('net_output_tax_'+str(year) + '.csv', net_output_tax, delimiter = ',')


    output_tax_pot = net_output_tax.sum(axis=0)
    output_tax_pot = output_tax_pot.reshape(output_tax_pot.shape[0],1)
    return (fin_cons_dom_sources, gcf_dom_sources, inter_use_dom_sources_mat, output_tax_pot)


def get_exempt_supply_ratio(tax_rates_vec, supply_mat, standard_vat_rate, year):
    col = np.array(['Exempt_Ratio'])
    row = np.zeros(np.shape(product_headers))
    exempt_supplydf = pd.DataFrame(data=row, index=product_headers, columns=col)
    exempt_supplydf = exempt_supplydf.reset_index()
    exempt_supplydf = exempt_supplydf.rename(columns={'index':'Product_ID'})

    df = pd.read_excel('Inputs for VAT Gap Estimation.xlsx', sheet_name='Exempt_Product')
    df = df[['Product_ID_'+str(year), 'Exempt_'+str(year)]].copy()
    df.rename(columns = {df.columns[0]: df.columns[0][:-5]}, inplace = True)

    exempt_supplydf = exempt_supplydf.merge(df, on=['Product_ID'], how='left')
    exempt_supplydf = exempt_supplydf[['Product_ID','Exempt_'+str(year)]]
    exempt_supplydf = exempt_supplydf['Exempt_'+str(year)].fillna(0)
    exempt_supply_prod_vec = exempt_supplydf.values
    exempt_supply_prod_vec = exempt_supply_prod_vec.reshape((exempt_supply_prod_vec.shape[0], 1))

    exempt_sec_alloc = exempt_supply_prod_vec*supply_mat
    exempt_sec_alloc= exempt_sec_alloc.sum(axis=0)
    exempt_sec_alloc= exempt_sec_alloc.reshape(exempt_sec_alloc.shape[0],1)
    tot_sup_sec=supply_mat.sum(axis=0)
    tot_sup_sec[tot_sup_sec==0]= 0.00001
    tot_sup_sec= tot_sup_sec.reshape(tot_sup_sec.shape[0],1)
    exempt_supply_sec_ratio = exempt_sec_alloc*(1/tot_sup_sec)
    #exempt_supply_ratio_vec = exempt_supply_ratio_vec.reshape((1, exempt_supply_ratio_vec.shape[0]))
    return exempt_supply_sec_ratio

def get_input_tax_potential(tax_rates_vec, use_mat, year):
    purchase_mat = use_mat
    input_tax_potential = purchase_mat*tax_rates_vec
    input_tax_potential=input_tax_potential.sum(axis=0)
    input_tax_potential = input_tax_potential.reshape(input_tax_potential.shape[0], 1)
    return input_tax_potential

def get_input_tax_disallow_potential(exempt_supply_sec_ratio, input_tax_potential, year):
    input_tax_disallow_potential = input_tax_potential*exempt_supply_sec_ratio
    return input_tax_disallow_potential

def get_rev_charge_potential(tax_rates_vec, use_mat, imports_eu_alloc, imports_noneu_alloc, rc_vec, year):
    rev_charge_purchase_mat = use_mat - imports_eu_alloc - imports_noneu_alloc
    rev_charge_potential = (rc_vec*rev_charge_purchase_mat)*tax_rates_vec
    rev_charge_potential = rev_charge_potential.sum(axis=0)
    rev_charge_potential = rev_charge_potential.reshape((rev_charge_potential.shape[0], 1))
    return rev_charge_potential

def get_import_VAT_potential(tax_rates_vec, imports_eu_alloc, imports_noneu_alloc, year):
    imports_alloc = imports_eu_alloc + imports_noneu_alloc
    import_VAT_pot = imports_alloc*tax_rates_vec
    import_VAT_pot = import_VAT_pot.sum(axis=0)
    import_VAT_pot = import_VAT_pot.reshape((import_VAT_pot.shape[0], 1))
    return import_VAT_pot

def get_VAT_potential(import_VAT_potentialdf, output_tax_potentialdf, input_tax_potentialdf, input_tax_disallow_potentialdf, rev_charge_potentialdf, va_by_reg_ratiodf, tax_revenue_mergeddf, year):
    VAT_potdf = output_tax_potentialdf.merge(rev_charge_potentialdf, on=['Sector_ID'], how='left')
    VAT_potdf = VAT_potdf.merge(import_VAT_potentialdf, on=['Sector_ID'], how='left')
    VAT_potdf = VAT_potdf.merge(input_tax_disallow_potentialdf, on=['Sector_ID'], how='left')
    VAT_potdf = VAT_potdf.merge(input_tax_potentialdf, on=['Sector_ID'], how='left')
    VAT_potdf = VAT_potdf.merge(va_by_reg_ratiodf, on=['Sector_ID'], how='left')

    VAT_potdf['VAT Potential_1'] = VAT_potdf['Output Tax'] + VAT_potdf['Import VAT'] + VAT_potdf['Reverse Charge'] + VAT_potdf['Input Tax Credit Disallowance'] - VAT_potdf['Input Tax Credit']
    VAT_potdf['VAT Potential'] = VAT_potdf['VAT Potential_1']*VAT_potdf['Value Added by Registered Ratio']
    VAT_potdf = VAT_potdf.merge(tax_revenue_mergeddf, on=['Sector_ID'], how='left')
    VAT_potdf['VAT Gap'] = VAT_potdf['VAT Potential'] - VAT_potdf['Revenue']

    df = VAT_potdf
    df['Sector Numbers'] = df.index
#    df.loc['Total'] = pd.Series(df['MyColumn'].sum(), index = ['MyColumn'])
    add_rows = ['Total']
    df.index = df.iloc[:,0]
    df = df.reindex(df.index.union(add_rows))
    df = df.sort_values(['Sector Numbers'])
    df = df.drop('Sector_ID', axis=1)
    df = df.drop('Sector Numbers', axis=1)
    df.loc['Total'] = df.sum()
    #sums = df.select_dtypes(pd.np.number).sum().rename('total')
    df = df.reset_index()
    df = df.rename(columns={'index':'Sector_ID'})
    df = df.fillna(0)
    df.to_csv('VAT_potential_' + str(year) + '.csv', index = True)
    VAT_potentialdf = df
    return VAT_potentialdf



GDP_LCU_2014 = 23618163000
GDP_LCU_2015 = 24320324000
GDP_LCU_2016 = 24925617000
GDP_LCU_2017 = 26856599000

GDP_factor_2015 = GDP_LCU_2015/GDP_LCU_2014
GDP_factor_2016 = GDP_LCU_2016/GDP_LCU_2014
#GDP_factor_2017 = GDP_LCU_2017/GDP_LCU_2014

year = 2014
if year==2013:
    supply_plusdf, supply_plus_transdf, use_plusdf, sector_headers, product_headers, imports_eu, imports_noneu, trade_marginsdf, tax_subsidiesdf, exports_eu, exports_noneu, fin_cons, gcf = import_Excel_SUT_2013(year)
if year>=2014:
    supply_plusdf, supply_plus_transdf, use_plusdf, sector_headers, product_headers, imports_eu, imports_noneu, trade_marginsdf, tax_subsidiesdf, exports_eu, exports_noneu, fin_cons, gcf = import_Excel_SUT_2014(year)

if year==2013:
    GDP_factor=1
if year==2014:
    GDP_factor=1
if year==2015:
    GDP_factor=GDP_factor_2015
if year==2016:
    GDP_factor=GDP_factor_2016

supply_mat = GDP_factor*supply_plusdf.values
use_mat = GDP_factor*use_plusdf.values
tax_subsidies = GDP_factor*tax_subsidiesdf.values
trade_margins = GDP_factor*trade_marginsdf.values
fin_cons = fin_cons.reshape(fin_cons.shape[0],1)
fin_cons = GDP_factor*fin_cons
gcf = gcf.reshape(gcf.shape[0],1)
gcf = GDP_factor*gcf
imports_eu = imports_eu.reshape(imports_eu.shape[0], 1)
imports_eu = GDP_factor*imports_eu
imports_noneu = imports_noneu.reshape(imports_noneu.shape[0], 1)
imports_noneu = GDP_factor*imports_noneu

use_mat_tax_incl = use_mat
np.savetxt('use_mat_tax_incl' + str(year)+'.csv', use_mat_tax_incl, delimiter = ',')
np.savetxt('imports_eu_' + str(year)+'.csv', imports_eu, delimiter = ',')
np.savetxt('imports_noneu_' + str(year)+'.csv', imports_noneu, delimiter = ',')

tot_inter_use_comm, tot_inter_use_sec, inter_use_mat_comm_ratio, inter_use_mat_sec_ratio = get_inter_use_mat_param(use_mat)

inter_use_comm_ratio, fin_cons_comm_use_ratio, gcf_comm_use_ratio = get_use_mat_param(use_mat, tot_inter_use_comm, fin_cons, gcf)

use_mat_tax_incl = use_mat
use_mat, fin_cons, gcf = get_use_mat_tax_excl(use_mat, fin_cons, gcf, inter_use_comm_ratio, inter_use_mat_comm_ratio, fin_cons_comm_use_ratio, gcf_comm_use_ratio, tax_subsidies)

tot_sup_comm, tot_sup_sec, supply_mat_comm_ratio, supply_mat_sec_ratio = get_supply_mat_param(supply_mat)

#tax_rates_alldf = import_tax_rates()
standard_vat_rate = 0.21

tax_rates_vecdf = import_check_productdf('Inputs for VAT Gap Estimation.xlsx', 'effective_tax_rates', 'ETR', year)

tax_rates_vecdf = adjust_etr_for_trade_sectors(trade_marginsdf, tax_rates_vecdf)

tax_rates_vec = tax_rates_vecdf['ETR'].values
tax_rates_vec = tax_rates_vec.reshape(tax_rates_vec.shape[0],1)

imports = imports_eu + imports_noneu
imports[imports==0]=0.00001
imports_eu_ratio = imports_eu/imports

#np.savetxt('final_cons_2013.csv', final_cons_alloc, delimiter = ',')
exports_eu_alloc, exports_noneu_alloc = alloc_exports_to_sectors(supply_mat, exports_eu, exports_noneu)
exports_alloc = exports_eu_alloc + exports_noneu_alloc

gcf_alloc = alloc_gcf_to_sectors(use_mat, gcf)
va_payersdf, va_non_payersdf = import_va_non_payers(year)


#tot_imports_eu_sec_adj, tot_imports_noneu_sec_adj = modify_imports_for_trade_sector(use_mat, imports_eu, imports_noneu)

imports_eu_alloc, imports_eu_alloc_sec, imports_noneu_alloc, imports_noneu_alloc_sec  = alloc_imports_to_sectors(imports_eu, imports_noneu, inter_use_mat_comm_ratio)

imports_eu_adj, imports_noneu_adj = adjust_imports(imports_eu, imports_noneu)
imports_adj = imports_eu_adj + imports_noneu_adj
np.savetxt('imports_adj_'+ str(year)+'.csv', imports_adj, delimiter = ',')



#imports_eu_comm_adj, imports_noneu_comm_adj  = alloc_sec_imports_to_comm(tot_imports_eu_sec_adj, tot_imports_noneu_sec_adj, inter_use_mat_sec_ratio)
#np.savetxt('tax_rates_2013.csv', tax_rates_vec, delimiter = ',')
rc_vec = get_reverse_charge_vec(supply_plusdf, year)
#np.savetxt('rc_vec_2013.csv', rc_vec, delimiter = ',')
va_by_reg_ratio, va_by_reg_ratiodf  = va_by_reg_ratio_yr(va_payersdf, va_non_payersdf, year)

exempt_supply_sec_ratio = get_exempt_supply_ratio(tax_rates_vec, supply_mat, standard_vat_rate, year)

col_header = np.array(['Exempt Supply Ratio'])
exempt_supply_sec_ratiodf = pd.DataFrame(data=exempt_supply_sec_ratio, index = sector_headers, columns=col_header)
exempt_supply_sec_ratiodf.to_csv('exempt_supply_sec_ratio_' + str(year) + '.csv', index = True)

fin_cons_dom_sources, gcf_dom_sources, output_inter_cons, output_tax_pot = get_output_tax_potential(tax_rates_vec, supply_mat, supply_mat_comm_ratio, exports_alloc, rc_vec, inter_use_comm_ratio, fin_cons, fin_cons_comm_use_ratio, gcf_comm_use_ratio, inter_use_mat_comm_ratio, year)

col_header = np.array(['Output Tax'])
output_tax_potentialdf = pd.DataFrame(data=output_tax_pot, index = sector_headers, columns=col_header)
output_tax_potentialdf = output_tax_potentialdf.reset_index()
output_tax_potentialdf = output_tax_potentialdf.rename(columns={'index':'Sector_ID'})

input_tax_potential =  get_input_tax_potential(tax_rates_vec, use_mat, year)
np.savetxt('input_tax_potential_'+str(year)+'.csv', input_tax_potential, delimiter = ',')
col = np.array(['Input Tax Credit'])
input_tax_potentialdf = pd.DataFrame(data=input_tax_potential, index = sector_headers, columns=col)
input_tax_potentialdf = input_tax_potentialdf.reset_index()
input_tax_potentialdf = input_tax_potentialdf.rename(columns={'index':'Sector_ID'})

input_tax_disallow_potential = get_input_tax_disallow_potential(exempt_supply_sec_ratio, input_tax_potential, year)

col_header = np.array(['Input Tax Credit Disallowance'])
input_tax_disallow_potentialdf = pd.DataFrame(data=input_tax_disallow_potential, index = sector_headers, columns=col_header)
input_tax_disallow_potentialdf = input_tax_disallow_potentialdf.reset_index()
input_tax_disallow_potentialdf = input_tax_disallow_potentialdf.rename(columns={'index':'Sector_ID'})

rev_charge_potential = get_rev_charge_potential(tax_rates_vec, use_mat, imports_eu_alloc, imports_noneu_alloc, rc_vec, year)
col = np.array(['Reverse Charge'])
rev_charge_potentialdf = pd.DataFrame(data=rev_charge_potential, index = sector_headers, columns=col)
rev_charge_potentialdf = rev_charge_potentialdf.reset_index()
rev_charge_potentialdf = rev_charge_potentialdf.rename(columns={'index':'Sector_ID'})

import_VAT_potential = get_import_VAT_potential(tax_rates_vec, imports_eu_alloc, imports_noneu_alloc, year)
col = np.array(['Import VAT'])
import_VAT_potentialdf = pd.DataFrame(data=import_VAT_potential, index = sector_headers, columns=col)
import_VAT_potentialdf = import_VAT_potentialdf.reset_index()
import_VAT_potentialdf = import_VAT_potentialdf.rename(columns={'index':'Sector_ID'})

tax_revenue_mergeddf =  get_vat_revenues(year)

VAT_potentialdf = get_VAT_potential(import_VAT_potentialdf, output_tax_potentialdf, input_tax_potentialdf, input_tax_disallow_potentialdf, rev_charge_potentialdf, va_by_reg_ratiodf, tax_revenue_mergeddf, year)
