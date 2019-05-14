import string
import pandas as pd
import numpy as np
from functions import *
import matplotlib.pyplot as plt
from in_rupees import *

np.seterr(divide='ignore', invalid='ignore')

filename_tax_actuals = 'concordance_2.xlsx'
sheet_name_cash_ratio = 'tax_output_tax_ratio'
sheet_name_gstr1 = 'gstr1'
concordance_sheet = 'concordance'

gst_collection_july17_march18 = 7.41*10**5
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

tax_cash_df = hsn_tax_data(filename_tax_actuals, sheet_name_cash_ratio, sheet_name_gstr1, gst_collection_july17_june18_dom_less_trade)   

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
import_vec = re_shape(import_vec)
trade_margin_vec = re_shape(trade_margin_vec)
tax_subsidies_vec = re_shape(tax_subsidies_vec)
export_vec = re_shape(export_vec)
fin_cons_hh_vec = re_shape(fin_cons_hh_vec)
fin_cons_gov_vec = re_shape(fin_cons_gov_vec)
gfcf_vec = re_shape(gfcf_vec)
vlbl_vec = re_shape(vlbl_vec)
cis_vec = re_shape(cis_vec)
rate_vec = re_shape(rate_vec)
exempt_vec = re_shape(exempt_vec)
'''
(import_vec, trade_margin_vec, tax_subsidies_vec, export_vec,fin_cons_hh_vec, fin_cons_gov_vec,
 gfcf_vec, vlbl_vec, cis_vec, rate_vec, exempt_vec) = re_shape(import_vec, trade_margin_vec,
                                                  tax_subsidies_vec, export_vec,fin_cons_hh_vec,
                                                  fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec,
                                                  rate_vec, exempt_vec)
'''
gst_reg_ratio_ind_vec = gst_reg_ratio_ind_vec.reshape(1, gst_reg_ratio_ind_vec.shape[0])
# Blow up the Supply Use Table and Vectors to current year
(supply_mat, use_mat, import_vec, trade_margin_vec, tax_subsidies_vec, export_vec, fin_cons_hh_vec,
 fin_cons_gov_vec, gfcf_vec, vlbl_vec, cis_vec) = blow_up_mat(supply_mat, use_mat, import_vec,
                                              trade_margin_vec, tax_subsidies_vec, export_vec,
                                              fin_cons_hh_vec, fin_cons_gov_vec, gfcf_vec, vlbl_vec,
                                              cis_vec, blow_up_factor)

np.savetxt("Output_csv\\rate_vec.csv", rate_vec , delimiter=",")

supply_mat = adjusted_SUT(gst_reg_ratio_ind_vec, supply_mat)
use_mat = adjusted_SUT(gst_reg_ratio_ind_vec, use_mat)

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

'''
Calculating Actual GST By Sector
'''
# importing concrdance file
hsn_df = hsn_sut_conc(filename_SUT, concordance_sheet)
# merging concordance file HSN to Srl_no mapping with tax data which has
# collection by HSN
hsn_df = pd.merge(hsn_df, tax_cash_df,
                            how="outer", on="HSN2")
# concording output tax collection from HSN2 to Srl_no using supply table for
# weights for allocating multiple HSN2 per Srl_no
hsn_df_copy = hsn_df.copy()
tax_payable_comm_vec = concord_comm_vec(hsn_df_copy, supply_mat, 'output tax')
np.savetxt("Output_csv\\tax_payable_comm.csv", tax_payable_comm_vec , delimiter=",")
# concording input tax credit from HSN2 to Srl_no using supply table for
# weights for allocating multiple HSN2 per Srl_no
hsn_df_copy = hsn_df.copy()
tax_itc_comm_vec = concord_comm_vec(hsn_df_copy, supply_mat, 'itc')
np.savetxt("Output_csv\\itc_comm.csv", tax_itc_comm_vec , delimiter=",")
# concording net tax collection from HSN2 to Srl_no using supply table for
# weights for allocating multiple HSN2 per Srl_no
hsn_df_copy = hsn_df.copy()
tax_cash_comm_vec = concord_comm_vec(hsn_df_copy, supply_mat, 'tax')
np.savetxt("Output_csv\\tax_cash_comm.csv", tax_cash_comm_vec , delimiter=",")
# allocating tax collection to the industry using supply table for
# allocating commodity to industry as form one is reported on outward supplies
tax_cash_ind_vec = concord_ind_vec(tax_cash_comm_vec, allocation_ratio_by_supply_mat)
tax_cash_df = make_ind_vec_df(tax_cash_ind_vec, industry_header, 'GST Collection Domestic')

# calculating effective tax rate by commodity using actual output value and output tax
hsn_df_copy = hsn_df.copy()
etr_comm_vec = concord_comm_vec(hsn_df_copy, supply_mat, 'etr')
np.savetxt("Output_csv\\etr.csv", etr_comm_vec , delimiter=",")

# calculating output tax to the industry using supply table for
# allocating commodity to industry
tax_payable_ind_vec = concord_ind_vec(tax_payable_comm_vec, allocation_ratio_by_supply_mat)
# calculating input tax credit to the industry using use table for
# allocating commodity to industry
tax_itc_ind_vec = concord_ind_vec(tax_itc_comm_vec, allocation_ratio_by_use_mat)
# alternative way to allocate net tax collection to the industry by taking the 
# difference of output tax and itc
tax_cash_ind_vec_alt = tax_payable_ind_vec - tax_itc_ind_vec
make_ind_vec_df(tax_payable_ind_vec, industry_header, 'tax_payable_ind')
make_ind_vec_df(tax_itc_ind_vec, industry_header, 'tax_itc_ind')
make_ind_vec_df(tax_cash_ind_vec_alt, industry_header, 'tax_cash_ind_2')

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

# converting to crores
GST_on_imports_ind_vec_cr = GST_on_imports_ind_vec/100
tot_GST_on_imports_cr = tot_GST_on_imports/100

gst_potential_less_import_vec_reg_cr = (gst_reg_ratio_ind_vec * gst_potential_less_import_vec)/100
gst_potential_less_import_total_cr = gst_potential_less_import_vec_reg_cr.sum()
gst_potential_ind_vec_cr = gst_potential_less_import_vec_reg_cr + GST_on_imports_ind_vec_cr
gst_potential_total_cr = gst_potential_ind_vec_cr.sum()

# Calculate the GST Gap for Domestic Taxes - tax cash is in crores
gst_gap_ind_vec_cr = gst_potential_less_import_vec_reg_cr - tax_cash_ind_vec 

gst_gap_dom_total_cr = gst_gap_ind_vec_cr.sum()
gst_collection = tax_cash_ind_vec.sum()


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
make_ind_vec_df(gst_potential_ind_vec_cr, industry_header, "gst_potential")
gst_less_import_pot_df = make_ind_vec_df(gst_potential_less_import_vec_reg_cr, industry_header, 'gst_potential_less_imports')
gst_gap_dom_df = make_ind_vec_df(gst_gap_ind_vec_cr, industry_header, "gst_gap_domestic")

# Grouping industries into broader classes for charts
industry_group_df = pd.DataFrame(data=industry_group_header, index=industry_header, columns=np.array(['Industry Group']))
industry_group_df = industry_group_df.reset_index()
industry_group_df = industry_group_df.rename(columns={'index':'industry_id'})
industry_group_df.to_csv('Output_csv\\industry.csv')

gst_pot_cr = gst_potential_less_import_vec_reg_cr.reshape(gst_potential_less_import_vec_reg_cr.shape[1], 1)
gst_pot_ind_df = pd.DataFrame(data=gst_pot_cr, index=industry_header, columns=np.array(['GST Potential']))
gst_pot_ind_df = gst_pot_ind_df.reset_index()
gst_pot_ind_df = gst_pot_ind_df.rename(columns={'index':'industry_id'})
gst_pot_ind_df.to_csv('Output_csv\\gst_coll.csv')
gst_pot_ind_group_df = pd.merge(gst_pot_ind_df, industry_group_df,
                            how="inner", on="industry_id")
gst_pot_ind_group_df = pd.merge(gst_pot_ind_group_df, tax_cash_df,
                            how="inner", on="industry_id")
gst_ind_group_df = gst_pot_ind_group_df.groupby(['Industry Group']).sum()
gst_ind_group_df = gst_ind_group_df[['GST Potential', 'GST Collection Domestic']]
 
gst_ind_group_df = gst_ind_group_df.sort_values('GST Potential', ascending=False)

# Print Results in Rs Crores
print(f'GST Potential less imports (Rs Cr.): {in_rupees(gst_potential_less_import_total_cr)}')
print(f'GST Potential on imports (Rs Cr.)  : {in_rupees(tot_GST_on_imports_cr)}')
print(f'Total GST Potential (Rs Cr.) : {in_rupees(gst_potential_total_cr)}')
print(f'Total GST Collection (Rs Cr.): {in_rupees(gst_collection)}')
print(f'Total GST Gap on Domestic Production (Rs Cr.): {in_rupees(gst_gap_dom_total_cr)}')

'''
Draw charts for displaying outputs
'''
plt.rcdefaults()
#fig, ax = plt.subplots(figsize=(8, 8))
# Example data
ax = gst_ind_group_df.plot.bar(legend=False)
ax.legend(loc='best')
ax.set_ylabel('Rupees crores')
ax.set_xlabel('Industry')
ax.set_title('India - GST Potential and Actual Collection by Industry - 2017')
plt.savefig('GST Potential.png', bbox_inches = "tight")
plt.show()
