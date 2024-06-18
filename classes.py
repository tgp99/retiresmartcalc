import pandas as pd
import numpy as np
import datetime
import math

# Collects dataset from static datafile (held on server) and returns this data.  Also provides missing default data to model parameter object.
class AddDefaultData:
    def __init__(self, data_object):
        if 'historic_asset_return_data' not in data_object: 
            historic_data = RetrieveHistoricData(pd.read_csv('staticfiles/historic_dataset.csv'))
            data_object['historic_asset_return_data'] = {
            'globaleq': historic_data.globaleq,
            'useq': historic_data.useq,
            'tengilt': historic_data.tengilt,
            'ukcpi': historic_data.ukcpi,
            'gbpusd': historic_data.gbpusd,
            'year': historic_data.year,
            'tentsy': historic_data.tentsy,
            'uscpi': historic_data.uscpi,
            'usdusd': historic_data.usdusd,
            }
        if 'forward_asset_return_data' not in data_object:
            forward_data = RetrieveForwardData(pd.read_csv('staticfiles/forward_dataset.csv'))
            data_object['forward_asset_return_data'] = {
            'gbp_index_bond_forward': forward_data.gbp_index_bond_forward,
            'gbp_bond_forward': forward_data.gbp_bond_forward,
            'usd_index_bond_forward': forward_data.usd_index_bond_forward,
            'usd_bond_forward': forward_data.usd_bond_forward,
            'update_date': forward_data.update_date,
            }
        if 'mortality_data' not in data_object:
            mortality_data = RetrieveMortalityData(pd.read_csv('staticfiles/mortality_risk_table.csv'))
            data_object['mortality_data'] = {
            'male': mortality_data.male,
            'female': mortality_data.female,
            'joint': mortality_data.joint,
            }
        if 'equity_tax' not in data_object: data_object['equity_tax'] = float(0)
        if 'bond_tax' not in data_object: data_object['bond_tax'] = float(0)
        if 'draw_tax' not in data_object: data_object['draw_tax'] = float(0)
        if 'bond_coupon' not in data_object: data_object['bond_coupon'] = float(3.0)
        if 'index_bond_coupon' not in data_object: data_object['index_bond_coupon'] = float(0.5)
        if 'asset_mix_equity' not in data_object: data_object['asset_mix_equity'] = float(60)
        if 'asset_mix_bond' not in data_object: data_object['asset_mix_bond'] = float(0)
        if 'asset_mix_index_bond' not in data_object: data_object['asset_mix_index_bond'] = float(40)
        if 'annuity_percent_withdrawal' not in data_object: data_object['annuity_percent_withdrawal'] = float(0)
        if 'data_option' not in data_object: data_object['data_option'] = "forwardUSD"
        if 'data_direction' not in data_object: data_object['data_direction'] = "forward"
        if 'data_start_year' not in data_object: data_object['data_start_year'] = int(1870)
        if 'data_end_year' not in data_object: data_object['data_end_year'] = int(2023)
        if 'currency_set' not in data_object: data_object['currency_set'] = "USD"
        if 'geographic_set' not in data_object: data_object['geographic_set'] = "DOMESTIC"
        if 'start_sum' not in data_object: data_object['start_sum'] = float(1000000)
        if 'dynamic_option' not in data_object: data_object['dynamic_option'] = "constant"
        if 'withdrawal_amount' not in data_object: data_object['withdrawal_amount'] = float(40000)
        if 'bonus_target' not in data_object: data_object['bonus_target'] = float(10000)
        if 'target_withdrawal_percent' not in data_object: data_object['target_withdrawal_percent'] = float(6.0)
        if 'min_withdrawal_floor' not in data_object: data_object['min_withdrawal_floor'] = float(30000)
        if 'net_other_income' not in data_object: data_object['net_other_income'] = "0"
        if 'flex_real_decrease' not in data_object: data_object['flex_real_decrease'] = float(1.0)
        if 'flex_real_increase' not in data_object: data_object['flex_real_increase'] = float(1.0)
        if 'years_no_flex' not in data_object: data_object['years_no_flex'] = int(1)
        if 'spring_back' not in data_object: data_object['spring_back'] = "1"
        if 'annuity_option' not in data_object: data_object['annuity_option'] = "3"
        if 'annuity_increase' not in data_object: data_object['annuity_increase'] = float(3)
        if 'annuity_price' not in data_object: data_object['annuity_price'] = float(0)
        if 'annuity_tax_rate' not in data_object: data_object['annuity_tax_rate'] = float(0)
        if 'annuity_start_year' not in data_object: data_object['annuity_start_year'] = int(1)
        if 'annual_withdrawal_inc' not in data_object: data_object['annual_withdrawal_inc'] = float(0)
        if 'annuity_option2' not in data_object: data_object['annuity_option2'] = "3"
        if 'annuity_increase2' not in data_object: data_object['annuity_increase2'] = float(1)
        if 'annuity_price2' not in data_object: data_object['annuity_price2'] = float(0)
        if 'annuity_tax_rate2' not in data_object: data_object['annuity_tax_rate2'] = float(0)
        if 'annuity_start_year2' not in data_object: data_object['annuity_start_year2'] = int(1)
        if 'annual_withdrawal_inc2' not in data_object: data_object['annual_withdrawal_inc2'] = float(0)
        if 'annuity_option3' not in data_object: data_object['annuity_option3'] = "3"
        if 'annuity_increase3' not in data_object: data_object['annuity_increase3'] = float(1)
        if 'annuity_price3' not in data_object: data_object['annuity_price3'] = float(0)
        if 'annuity_tax_rate3' not in data_object: data_object['annuity_tax_rate3'] = float(0)
        if 'annuity_start_year3' not in data_object: data_object['annuity_start_year3'] = int(1)
        if 'annual_withdrawal_inc3' not in data_object: data_object['annual_withdrawal_inc3'] = float(0)
        if 'fees' not in data_object: data_object['fees'] = float(0)
        if 'start_simulation_age' not in data_object: data_object['start_simulation_age'] = int(50)
        if 'annualadjust' not in data_object: data_object['annualadjust'] = [100] * 50
        if 'years' not in data_object: data_object['years'] = int(35)
        if 'circular_simulation' not in data_object: data_object['circular_simulation'] = "1"
        if 'years_between' not in data_object: data_object['years_between'] = 0
        if 'years_contributions' not in data_object: data_object['years_contributions'] = 0
        if 'contribution' not in data_object: data_object['contribution'] = 0
        if 'contribution_increase' not in data_object: data_object['contribution_increase']  = 0
        if 'yale_weighting' not in data_object: data_object['yale_weighting']  = 70
        if 'vanguard_decrease_floor' not in data_object: data_object['vanguard_decrease_floor']  = 1.5
        if 'vanguard_increase_ceiling' not in data_object: data_object['vanguard_increase_ceiling']  = 5
        self.data_object = data_object

# these are the Boglehead Variable Percentage Withdrawal datatables
class GetVPWData:
    def __init__(self):
        self.vpwthirty = [0.034, 0.034, 0.034, 0.035, 0.035, 0.035, 0.035, 0.036, 0.036, 0.036, 0.037, 0.037, 0.037, 0.038, 0.038, 0.038, 0.039, 0.039, 0.040, 0.040, 0.041, 0.041, 0.042, 0.043, 0.043, 0.044, 0.045, 0.046, 0.047, 0.048, 0.049, 0.050, 0.051, 0.052, 0.053, 0.055, 0.056, 0.058, 0.060, 0.062, 0.064, 0.067, 0.070, 0.073, 0.076, 0.080, 0.085, 0.090, 0.097, 0.104, 0.113, 0.124, 0.138, 0.155, 0.179, 0.211, 0.261, 0.343, 0.507, 1.000]
        self.vpwforty = [0.036, 0.036, 0.037, 0.037, 0.037, 0.037, 0.038, 0.038, 0.038, 0.038, 0.039, 0.039, 0.039, 0.040, 0.040, 0.041, 0.041, 0.041, 0.042, 0.042, 0.043, 0.043, 0.044, 0.045, 0.045, 0.046, 0.047, 0.048, 0.048, 0.049, 0.050, 0.051, 0.053, 0.054, 0.055, 0.057, 0.058, 0.060, 0.062, 0.064, 0.066, 0.069, 0.071, 0.074, 0.078, 0.082, 0.087, 0.092, 0.098, 0.106, 0.114, 0.125, 0.139, 0.156, 0.180, 0.213, 0.262, 0.344, 0.508, 1.000]
        self.vpwfifty = [0.038, 0.039, 0.039, 0.039, 0.039, 0.039, 0.040, 0.040, 0.040, 0.041, 0.041, 0.041, 0.041, 0.042, 0.042, 0.043, 0.043, 0.043, 0.044, 0.044, 0.045, 0.045, 0.046, 0.047, 0.047, 0.048, 0.049, 0.050, 0.050, 0.051, 0.052, 0.053, 0.054, 0.056, 0.057, 0.058, 0.060, 0.062, 0.063, 0.065, 0.068, 0.070, 0.073, 0.076, 0.080, 0.084, 0.088, 0.094, 0.100, 0.107, 0.116, 0.127, 0.140, 0.158, 0.181, 0.214, 0.263, 0.345, 0.508, 1.000]
        self.vpwsixty = [0.041, 0.041, 0.041, 0.041, 0.041, 0.042, 0.042, 0.042, 0.042, 0.043, 0.043, 0.043, 0.044, 0.044, 0.044, 0.045, 0.045, 0.046, 0.046, 0.046, 0.047, 0.047, 0.048, 0.049, 0.049, 0.050, 0.051, 0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.057, 0.059, 0.060, 0.062, 0.063, 0.065, 0.067, 0.069, 0.072, 0.075, 0.078, 0.081, 0.085, 0.090, 0.095, 0.101, 0.109, 0.117, 0.128, 0.142, 0.159, 0.182, 0.215, 0.264, 0.346, 0.509, 1.000]
        self.vpwseventy = [0.043, 0.043, 0.043, 0.044, 0.044, 0.044, 0.044, 0.044, 0.045, 0.045, 0.045, 0.046, 0.046, 0.046, 0.047, 0.047, 0.047, 0.048, 0.048, 0.049, 0.049, 0.050, 0.050, 0.051, 0.051, 0.052, 0.053, 0.053, 0.054, 0.055, 0.056, 0.057, 0.058, 0.059, 0.061, 0.062, 0.063, 0.065, 0.067, 0.069, 0.071, 0.074, 0.076, 0.079, 0.083, 0.087, 0.091, 0.097, 0.103, 0.110, 0.119, 0.130, 0.143, 0.161, 0.184, 0.216, 0.265, 0.347, 0.510, 1.000]

# Creates age_adjusted survivorship probabilities for application to withdrawal results in simulation (provides an average of male + female)
class SurvivorshipWeightings:
    def __init__(self, years, start_age, data_set):
        weightings = []
        life_expectancy_years_male = []
        life_expectancy_years_female = []
        for a in range(years + 1):
            age = start_age + a
            if age < 65: weightings.append(1)
            elif age > 105: weightings.append(0)
            else: weightings.append((0.5 * data_set.male[age - 65] + 0.5 * data_set.female[age - 65])/ 100)
        self.result = weightings

# this is to calculate tax due on annuity payments (given the effective return of principal is tax free) which is used to scale up the amount of required annuity income and size of annuity purchased.  problem is that unless the annuity payments are fixed, the percentage that is due to be taxed is not constant, it increases with time as the annuity payments grow (i.e. with inflation)
# currently this is not used in the core simulation model
class AnnuityTax:
    def __init__(self, start_age, annuity_start_year, data_set, annuity_price):
        if start_age + annuity_start_year[0] - 1 <= 65:
            expected_years = (0.5 * data_set.male_years_left[0] + 0.5 * data_set.female_years_left[0]) + (65 - start_age)
        elif start_age + annuity_start_year[0] - 1 <= 105: 
            expected_years = (0.5 * data_set.male_years_left[start_age + annuity_start_year[0] - 1 - 65] + 0.5 * data_set.female_years_left[start_age + annuity_start_year[0] - 1 - 65])
        else:
            expected_years = (0.5 * data_set.male_years_left[start_age + 40] + 0.5 * data_set.female_years_left[start_age + 40])
        try: 
            taxable_percent = max(annuity_price[0] / 100 - 1 / expected_years, 0) / (annuity_price[0] / 100)
        except:
            taxable_percent = 0
        self.expected_years = expected_years
        self.annuity_price = annuity_price[0] / 100
        self.return_principal = 1 / expected_years
        self.taxable_percent = taxable_percent

# Takes a two dimensional data object (e.g. array of nested arrays) and transposes it
class ReverseArray:
    def __init__(self, data_set):
        new_array = []
        new_sub_array = []
        for a in range (len(data_set[0])):
            for b in range(len(data_set)):
                new_sub_array.append(data_set[b][a])
            new_array.append(new_sub_array)
            new_sub_array = []
        self.data_set = new_array

# Excel style present value caculator
class PresentValue:
    def __init__(self, rate, nper, pmt, fv):
        pv = 0
        for a in range(nper):
            pv = pv + pmt / ((1 + rate) ** (a + 1))
        pv = pv + fv / ((1 + rate) ** (nper))
        self.pv = pv

# Strips 'columns' of historic asset return data object into seperate data arrays ready to package as JSON object to send to frontend
class RetrieveHistoricData:
    def __init__(self, data_set):
        self.globaleq = data_set['GLOBALEQ'].tolist()
        self.useq = data_set['USEQ'].tolist()
        self.tengilt = data_set['10GILT'].tolist()
        self.ukcpi = data_set['UKCPI'].tolist()
        self.gbpusd = data_set['GBPUSD'].tolist()
        self.year = data_set['Year'].tolist()   
        self.tentsy = data_set['10TSY'].tolist()
        self.uscpi = data_set['USCPI'].tolist()
        self.usdusd = data_set['USDUSD'].tolist()

# Strips 'columns' of forward asset returns data object into seperate data arrays ready to package as JSON object to send to frontend
class RetrieveForwardData:
    def __init__(self, data_set):
        self.gbp_index_bond_forward = data_set['GBP_index_bond_forward'].tolist()
        self.gbp_bond_forward = data_set['GBP_bond_forward'].tolist()
        self.usd_index_bond_forward = data_set['USD_index_bond_forward'].tolist()
        self.usd_bond_forward = data_set['USD_bond_forward'].tolist()
        self.update_date = data_set['update_date'][0]

# Strips 'columns' of mortality data object into seperate data arrays ready to package as JSON object to send to frontend
class RetrieveMortalityData:
    def __init__(self, data_set):
        self.male = data_set['Male'].tolist()
        self.female = data_set['Female'].tolist()
        self.joint = data_set['Joint'].tolist()
        self.male_years_left = data_set['MaleYearsLeft'].tolist()
        self.female_years_left = data_set['FemaleYearsLeft'].tolist()

# Strips 'columns' of historic data object and forms sub-set returned as seperate data arrays (for historic returns analysis, dataset is fed in directly from csv file in static files)
class LoadHistoricData:
    def __init__(self, data_set, start_year, end_year, currency_set, geographic_set):
        years = data_set['Year'].tolist()
        start_list = years.index(start_year)
        end_list = years.index(end_year)
        if (currency_set == 'GBP' and geographic_set == 'GLOBAL'):
            self.historic_equity = data_set['GLOBALEQ'].tolist()[start_list:(end_list + 1)]
            self.historic_bond = data_set['10GILT'].tolist()[start_list:(end_list + 1)]
            self.historic_index_bond = data_set['10GILT'].tolist()[start_list:(end_list + 1)]
            self.historic_cpi = data_set['UKCPI'].tolist()[start_list:(end_list + 1)]
            self.historic_fx = data_set['GBPUSD'].tolist()[start_list:(end_list + 1)]
            self.years = data_set['Year'].tolist()[start_list:(end_list + 1)]
        elif (currency_set == 'USD' and geographic_set == 'DOMESTIC'):
            self.historic_equity = data_set['USEQ'].tolist()[start_list:(end_list + 1)]
            self.historic_bond = data_set['10TSY'].tolist()[start_list:(end_list + 1)]
            self.historic_index_bond = data_set['10TSY'].tolist()[start_list:(end_list + 1)]
            self.historic_cpi = data_set['USCPI'].tolist()[start_list:(end_list + 1)]
            self.historic_fx = data_set['USDUSD'].tolist()[start_list:(end_list + 1)]
            self.years = data_set['Year'].tolist()[start_list:(end_list + 1)]
        else: 
            self.historic_equity = data_set['GLOBALEQ'].tolist()[start_list:(end_list + 1)]
            self.historic_bond = data_set['10TSY'].tolist()[start_list:(end_list + 1)]
            self.historic_index_bond = data_set['10TSY'].tolist()[start_list:(end_list + 1)]
            self.historic_cpi = data_set['USCPI'].tolist()[start_list:(end_list + 1)]
            self.historic_fx = data_set['USDUSD'].tolist()[start_list:(end_list + 1)]
            self.years = data_set['Year'].tolist()[start_list:(end_list + 1)]

# Creates sub-set of historic asset return data out of full set (for simulation class, dataset is a JSON object)
class PrepareHistoricDataSet:
    def __init__(self, data_set, start_year, end_year, currency_set, geographic_set):
        years = data_set['year']
        start_list = years.index(start_year)
        end_list = years.index(end_year)
        if (currency_set == 'GBP' and geographic_set == 'GLOBAL'):
            self.historic_equity = data_set['globaleq'][start_list:(end_list + 1)]
            self.historic_bond = data_set['tengilt'][start_list:(end_list + 1)]
            self.historic_index_bond = data_set['tengilt'][start_list:(end_list + 1)]
            self.historic_cpi = data_set['ukcpi'][start_list:(end_list + 1)]
            self.historic_fx = data_set['gbpusd'][start_list:(end_list + 1)]
            self.years = data_set['year'][start_list:(end_list + 1)]
        elif (currency_set == 'USD' and geographic_set == 'DOMESTIC'):
            self.historic_equity = data_set['useq'][start_list:(end_list + 1)]
            self.historic_bond = data_set['tentsy'][start_list:(end_list + 1)]
            self.historic_index_bond = data_set['tentsy'][start_list:(end_list + 1)]
            self.historic_cpi = data_set['uscpi'][start_list:(end_list + 1)]
            self.historic_fx = data_set['usdusd'][start_list:(end_list + 1)]
            self.years = data_set['year'][start_list:(end_list + 1)]
        else: 
            self.historic_equity = data_set['globaleq'][start_list:(end_list + 1)]
            self.historic_bond = data_set['tentsy'][start_list:(end_list + 1)]
            self.historic_index_bond = data_set['tentsy'][start_list:(end_list + 1)]
            self.historic_cpi = data_set['uscpi'][start_list:(end_list + 1)]
            self.historic_fx = data_set['usdusd'][start_list:(end_list + 1)]
            self.years = data_set['year'][start_list:(end_list + 1)]

# Strips 'columns' of forward data object and forms sub-set returned as seperate data arrays
class LoadForwardData:
    def __init__(self, data_set, currency_set):
        update_date = data_set['update_date'].tolist()
        if currency_set == 'GBP':
            self.forward_index_bond = data_set['GBP_index_bond_forward'].tolist()
            self.forward_bond = data_set['GBP_bond_forward'].tolist()
        else:
            self.forward_index_bond = data_set['USD_index_bond_forward'].tolist()
            self.forward_bond = data_set['USD_bond_forward'].tolist()
        self.update_date = datetime.datetime(1899, 12, 30) + datetime.timedelta(days = update_date[0])


# Creates sub-set of forward asset return data out of full set
class PrepareForwardDataSet:
    def __init__(self, data_set, currency_set):
        update_date = data_set['update_date']
        if currency_set == 'GBP':
            self.forward_index_bond = data_set['gbp_index_bond_forward']
            self.forward_bond = data_set['gbp_bond_forward']
        else:
            self.forward_index_bond = data_set['usd_index_bond_forward']
            self.forward_bond = data_set['usd_bond_forward']
        self.update_date = datetime.datetime(1899, 12, 30) + datetime.timedelta(days = update_date)

# Creates sub-set of mortality data out of full set (currently does not change anything)
class PrepareMortalityDataSet:
    def __init__(self, data_set):
        self.male = data_set['male']
        self.female = data_set['female']
        self.joint = data_set['joint']
        self.male_years_left = data_set['male_years_left']
        self.female_years_left = data_set['female_years_left']

# Takes historic asset return data, converts into real terms and applies tax parameters and returns prepared data
class PrepareReturnData:
    def __init__(self, equity, historic_bond, historic_index_bond, cpi, historic_fx, equity_tax, bond_tax, bond_coupon, index_bond_coupon, forward_index_bond, forward_bond, fees, circular_simulation):
        historic_equity_real = []
        historic_bond_real = []
        historic_index_bond_real = []
        cpi_change = []
        forward_index_bond_taxed = []
        forward_bond_taxed = []
        forward_index_bond_spot_curve = []

        for a in range(len(equity) - 1):
            num = float(equity[a + 1]) / float(historic_fx [a + 1])
            denom = float(equity[a]) / float(historic_fx [a])
            num_cpi = float(cpi[a + 1])
            denom_cpi = float(cpi[a])
            change = (((num / denom) - 1 - fees) * (1 - equity_tax)) - ((num_cpi / denom_cpi) - 1) 
            historic_equity_real.append(change)
        for a in range(len(historic_bond) - 1):
            num = PresentValue(float(historic_bond[a + 1]) / 100, 10, bond_coupon, 100).pv
            denom = PresentValue(float(historic_bond[a]) / 100, 10, bond_coupon, 100).pv
            num_cpi = float(cpi[a + 1])
            denom_cpi = float(cpi[a])
            change = ((num / denom) - 1 - fees) * (1 - bond_tax) + (float(historic_bond[a]) / 100) * (1 - bond_tax) - ((num_cpi / denom_cpi) - 1)
            historic_bond_real.append(change)
        for a in range(len(historic_index_bond) - 1):
            num = PresentValue(float(historic_index_bond[a + 1]) / 100, 10, index_bond_coupon, 100).pv
            denom = PresentValue(float(historic_index_bond[a]) / 100, 10, index_bond_coupon, 100).pv
            change = ((num / denom) - 1 - fees) * (1 - bond_tax) + (float(historic_index_bond[a]) / 100) * (1 - bond_tax) 
            historic_index_bond_real.append(change)    
        for a in range(len(cpi) - 1):
            num_cpi = float(cpi[a + 1])
            denom_cpi = float(cpi[a])
            change = ((num_cpi / denom_cpi) - 1) 
            cpi_change.append(change)
        for a in range(len(forward_index_bond)):
            tax_adjust = ((forward_index_bond[a] / 100) - fees) * (1 - bond_tax)
            forward_index_bond_taxed.append(tax_adjust)
        for a in range(len(forward_bond)):
            tax_adjust = ((forward_bond[a] / 100) - fees) * (1 - bond_tax)
            forward_bond_taxed.append(tax_adjust)
        for a in range(len(forward_index_bond)):
            if a == 0: forward_index_bond_spot_curve.append(forward_index_bond[0] / 100)
            else:
                forward_index_bond_spot_curve.append(((((1 + forward_index_bond_spot_curve[-1]) ** a) * (1 + forward_index_bond[a] / 100)) ** (1 / (a + 1))) - 1)

 
        self.forward_index_bond_taxed = forward_index_bond_taxed
        self.forward_bond_taxed = forward_bond_taxed
        # forward_index_bond_spot_curve is used in calculation of sum of discounted future withdrawals
        self.forward_index_bond_spot_curve = forward_index_bond_spot_curve

        # introduce circular bootstrapping...
        if circular_simulation == "1":
            historic_equity_real_extended = historic_equity_real
            historic_bond_real_extended = historic_bond_real
            historic_index_bond_real_extended = historic_index_bond_real
            cpi_change_extended = cpi_change
            for a in range(len(historic_equity_real) - 1):
                historic_equity_real_extended.append(historic_equity_real[a])
                historic_bond_real_extended.append(historic_bond_real[a])
                historic_index_bond_real_extended.append(historic_index_bond_real[a])
                cpi_change_extended.append(cpi_change[a])
            self.historic_equity_real = historic_equity_real_extended
            self.historic_bond_real = historic_bond_real_extended
            self.historic_index_bond_real = historic_index_bond_real_extended
            self.cpi_change = cpi_change_extended

        else: 
            self.historic_equity_real = historic_equity_real
            self.historic_bond_real = historic_bond_real
            self.historic_index_bond_real = historic_index_bond_real
            self.cpi_change = cpi_change

# Calculates and returns withdrawal amount (from running portfolio) for specific year in back-test cycle.  Nets off annuity income and scales amount upwards for tax costs.
class CalcConstantWithdrawal:
    def __init__(self, withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, year, annuity_income, annuity_tax, annuity_income2, annuity_tax2, annuity_income3, annuity_tax3):
        self.result = ((withdrawal_amount * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3))  / (1 - draw_tax))
        self.unadjusted_result = ((withdrawal_amount * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))

# Calculates and returns withdrawal bonus amount (from running portfolio) for specific year in back-test cycle.  Scales amount upwards for tax costs.
class CalcBonusWithdrawal:
    def __init__(self, bonus_target, draw_adjust, annual_withdrawal_inc, draw_tax, year, annuity_income, annuity_tax, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax3):
        self.result = ((bonus_target * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))

# Calculates and returns proportional withdrawal amount (from running portfolio) for specific year in back-test cycle.  Nets off annuity income and scales amount upwards for tax costs.
class CalcProportionalWithdrawal:
    def __init__(self, target_withdrawal_percent, draw_adjust, draw_tax, year, running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax, annuity_income2, annuity_tax2, annuity_income3, annuity_tax3, net_other_income):
        if net_other_income == "0":
            result = ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
            floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
            self.result = max(result, floor)
        else:
            result = ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
            floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
            self.result = max(result, floor)

# Calculates and returns Yale formula proportional withdrawal amount (from running portfolio) for specific year in back-test cycle.  Nets off annuity income and scales amount upwards for tax costs.
class CalcProportionalWithdrawalYale:
    def __init__(self, target_withdrawal_percent, draw_adjust, draw_tax, year, running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax, annuity_income2, annuity_tax2, annuity_income3, annuity_tax3, b, previous_draw, yale_weighting, net_other_income):
        weight = yale_weighting / 100
        if net_other_income == "0":
            if b == 0: 
                result = ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                result_unadjusted = ((running_portfolio_value * (target_withdrawal_percent / 100) * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
            else:    
                result = ((((1 - weight) * (running_portfolio_value * (target_withdrawal_percent / 100)) + weight * previous_draw) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                result_unadjusted = ((((1 - weight) * (running_portfolio_value * (target_withdrawal_percent / 100)) + weight * previous_draw) * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
            floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
            self.result = max(result, floor)
            self.result_unadjusted = result_unadjusted
        else:
            if b == 0: 
                result = ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                result_unadjusted = ((running_portfolio_value * (target_withdrawal_percent / 100) * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
            else:    
                result = ((((1 - weight) * (running_portfolio_value * (target_withdrawal_percent / 100)) + weight * previous_draw) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                result_unadjusted = ((((1 - weight) * (running_portfolio_value * (target_withdrawal_percent / 100)) + weight * previous_draw) * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
            floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
            self.result = max(result, floor)
            self.result_unadjusted = result_unadjusted
       
# Calculates and returns Vanguard Dynamic Withdrawal formula proportional withdrawal amount (from running portfolio) for specific year in back-test cycle.  Nets off annuity income and scales amount upwards for tax costs.
class CalcProportionalWithdrawalVanguard:
    def __init__(self, target_withdrawal_percent, draw_adjust, draw_tax, year, running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax, annuity_income2, annuity_tax2, annuity_income3, annuity_tax3, b, previous_draw, vanguard_decrease_floor, vanguard_increase_ceiling, net_other_income):
        if net_other_income == "0":
            if b == 0:
                self.result_unadjusted = ((running_portfolio_value * (target_withdrawal_percent / 100) * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                result_adjusted = ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                self.result = max(result_adjusted, floor)
            else:
                result_before_cap_floor = ((running_portfolio_value * (target_withdrawal_percent / 100) * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                result_capped = min(previous_draw * (1 + vanguard_increase_ceiling / 100), result_before_cap_floor)
                result_floored_capped = max(previous_draw * (1 - vanguard_decrease_floor / 100), result_capped)
                self.result_unadjusted = result_floored_capped
                try: 
                    result_adjusted = (result_floored_capped / result_before_cap_floor) * ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                except:
                    result_adjusted = result_before_cap_floor
                floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))
                self.result = max(result_adjusted, floor)
        else: 
            if b == 0:
                self.result_unadjusted = ((running_portfolio_value * (target_withdrawal_percent / 100) * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                result_adjusted = ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                self.result = max(result_adjusted, floor)
            else:
                result_before_cap_floor = ((running_portfolio_value * (target_withdrawal_percent / 100) * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                result_capped = min(previous_draw * (1 + vanguard_increase_ceiling / 100), result_before_cap_floor)
                result_floored_capped = max(previous_draw * (1 - vanguard_decrease_floor / 100), result_capped)
                self.result_unadjusted = result_floored_capped
                try: 
                    result_adjusted = (result_floored_capped / result_before_cap_floor) * ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                except:
                    result_adjusted = result_before_cap_floor
                floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax) - annuity_income2 * (1 - annuity_tax2) - annuity_income3 * (1 - annuity_tax3)) / (1 - draw_tax))
                self.result = max(result_adjusted, floor)

# Calculates and returns Bogleheads variable percentage withdrawal formula withdrawal amount (from running portfolio) for specific year in back-test cycle.  Nets off annuity income and scales amount upwards for tax costs.
class CalcVPW:
    def __init__(self, draw_adjust, draw_tax, running_portfolio_value, annual_withdrawal_inc, annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3, vpw_data, asset_mix, start_simulation_age, b, years_to_withdrawal, years):
        start = max(start_simulation_age - 40, 0)
        offset = max(years - 60, 0)        
        row = min(max(start + years_to_withdrawal + b - offset, 0), 59)

        if asset_mix[0] < 0.4:
            draw_percents = vpw_data.vpwthirty[row]
        elif asset_mix[0] < 0.5:
            draw_percents = vpw_data.vpwforty[row]
        elif asset_mix[0] < 0.6:
            draw_percents = vpw_data.vpwfifty[row]
        elif asset_mix[0] < 0.7:
            draw_percents = vpw_data.vpwsixty[row]
        else: 
            draw_percents = vpw_data.vpwseventy[row]

        self.result = running_portfolio_value * draw_percents * draw_adjust[b] / (1 - draw_tax)
        self.result_unadjusted = running_portfolio_value * draw_percents / (1 - draw_tax)
        self.draw_percents = draw_percents

# Runs back-testing cycle simulation. Takes prepared parameters and prepared return data and returns data series of results.
class RunSimulation:
    def __init__(self, equity_real, bond_real, index_bond_real, asset_mix, start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option_list, annuity_increase_list, annuity_price_list, annuity_tax_rate_list, cpi_change, annuity_percent_withdrawal_list, start_simulation_age, annuity_start_year_list, mortality_data_pull, ilb_spot_curve, data_direction, years_contributions, contribution, contribution_increase, years_between, yale_weighting, vanguard_decrease_floor, vanguard_increase_ceiling, vpw_data, net_other_income):
                
        annuity_option = annuity_option_list[0]
        annuity_increase = annuity_increase_list[0]
        annuity_price = annuity_price_list[0]
        annuity_tax_rate = annuity_tax_rate_list[0]
        annuity_percent_withdrawal = annuity_percent_withdrawal_list[0]
        annuity_start_year = annuity_start_year_list[0]

        annuity_option2 = annuity_option_list[1]
        annuity_increase2 = annuity_increase_list[1]
        annuity_price2 = annuity_price_list[1]
        annuity_tax_rate2 = annuity_tax_rate_list[1]
        annuity_percent_withdrawal2 = annuity_percent_withdrawal_list[1]
        annuity_start_year2 = annuity_start_year_list[1]

        annuity_option3 = annuity_option_list[2]
        annuity_increase3 = annuity_increase_list[2]
        annuity_price3 = annuity_price_list[2]
        annuity_tax_rate3 = annuity_tax_rate_list[2]
        annuity_percent_withdrawal3 = annuity_percent_withdrawal_list[2]
        annuity_start_year3 = annuity_start_year_list[2]

        # self.occupational_pension_check = [annuity_option3, annuity_increase3, annuity_price3, annuity_tax_rate3, annuity_percent_withdrawal3, annuity_start_year3]

        if annuity_option2 == "4": annual_annuity2_inc = annuity_increase2 / 100
        else: annual_annuity2_inc = 0
        if annuity_option3 == "4": annual_annuity3_inc = annuity_increase3 / 100
        else: annual_annuity3_inc = 0

        running_portfolio_value = start_sum
        end_single_cycle_portfolio_values = []
        through_single_cycle_portfolio_values = [start_sum]
        all_portfolio_values_through_all_cycles = []
        through_single_cycle_withdrawals = []
        through_single_cycle_annuity_income = []
        through_single_cycle_annuity_income2 = []
        through_single_cycle_annuity_income3 = []
        through_single_cycle_withdrawal_net_annuity = []
        all_withdrawals_through_all_cycles = []
        all_withdrawals_through_all_cycles_mort_adjusted_discounted = []
        all_withdrawals_through_all_cycles_all_periods = []
        annuity_income_through_all_cycles = []
        annuity_income2_through_all_cycles = []
        annuity_income3_through_all_cycles = []
        withdrawal_net_annuity_through_all_cycles = []        
        running_flex_withdrawal_adjustment = 1
        through_single_cycle_avg_withdrawal = []
        through_single_cycle_avg_withdrawal_mort_adjusted = []
        mortality_adjustments = SurvivorshipWeightings(years, start_simulation_age, mortality_data_pull).result
        through_single_cycle_withdrawals_mort_adjusted = []      
        through_single_cycle_withdrawals_mort_adjusted_discounted = []
        annuity_income_tracker_pre_purchase = (withdrawal_amount * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
        annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
        annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)
        annuity_income = 0
        annuity_income2 = 0
        annuity_income3 = 0
        simulation_fail_tag = 0
        simulation_fail_tag_through_all_cycles = []
        bonus_payment = 0
        # Below is to stop annuity option running if data_direction is 'back' (as frontend only allows annuity parameters to be changed if data_direction is 'forward').  Otherwise set annuity_percent_withdrawal to zero.
        # if data_direction == "back": annuity_percent_withdrawal = 0
        data_tracker = []
        data_tracker_parent = []
        running_contribution = contribution
        years_to_withdrawal = years_contributions + years_between
        unadjusted_draw_tracker = []
        annuity_purchase_cost = 0
        annuity_purchase_cost2 = 0
        annuity_purchase_cost3 = 0
        annuity_purchase_cost_tracker = []

        # 'a in range' represents each back-testing cycle and 'b in range' represents each year in each cycle
        for a in range(len(equity_real) - years):
            for b in range(years_to_withdrawal):
                if b < years_contributions:
                    running_portfolio_value += running_contribution
                    running_contribution = running_contribution * (1 + contribution_increase / 100)
                if data_direction == "back":
                    if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                else:
                    if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])
                through_single_cycle_portfolio_values.append(running_portfolio_value)
                if(a == 0): unadjusted_draw_tracker.append(0)

                if b == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)   

                if b == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc) 

                if b == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase3
                else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc) 

                through_single_cycle_annuity_income.append(0)
                through_single_cycle_annuity_income2.append(0)
                through_single_cycle_annuity_income3.append(0)
                through_single_cycle_withdrawal_net_annuity.append(0)               

            for b in range(years - years_to_withdrawal):
                if b < (annuity_start_year2 - 1 - years_to_withdrawal):
                    if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                    else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)
                elif b == (annuity_start_year2 - 1 - years_to_withdrawal):
                    if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                    else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)
                    try: 
                        annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100))
                    except: 
                        annuity_purchase_cost2 = 0
                    if running_portfolio_value >= annuity_purchase_cost2:
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost2
                        annuity_income2 = annuity_income_tracker_pre_purchase2
                    else: 
                        # This scales back the size of the annuity income that can be purchased if there are insufficient funds to purchase the entire target annuity
                        annuity_income2 = annuity_income_tracker_pre_purchase2 * (running_portfolio_value / annuity_purchase_cost2)
                        running_portfolio_value = 0

                if b < (annuity_start_year3 - 1 - years_to_withdrawal):
                    if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                    else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)
                elif b == (annuity_start_year3 - 1 - years_to_withdrawal):
                    if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                    else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)
                    try: 
                        annuity_purchase_cost3 = (annuity_income_tracker_pre_purchase3 / (annuity_price3 / 100))
                    except: 
                        annuity_purchase_cost3 = 0
                    if running_portfolio_value >= annuity_purchase_cost3:
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost3
                        annuity_income3 = annuity_income_tracker_pre_purchase3
                    else: 
                        # This scales back the size of the annuity income that can be purchased if there are insufficient funds to purchase the entire target annuity
                        annuity_income3 = annuity_income_tracker_pre_purchase3 * (running_portfolio_value / annuity_purchase_cost3)
                        running_portfolio_value = 0

                if b < (annuity_start_year - 1 - years_to_withdrawal):
                    if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                    else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                elif b == (annuity_start_year - 1 - years_to_withdrawal):
                    if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                    else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    # This nets the state and occupational pensions off what is required to achieved annuity withdrawal coverage
                    if annuity_start_year2 and annuity_start_year3 <= annuity_start_year: 
                        annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2) - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                    elif annuity_start_year2 <= annuity_start_year: 
                        annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2)), 0) 
                    elif annuity_start_year3 <= annuity_start_year: 
                        annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                    else: 
                        annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase 
                    try: 
                        annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100))
                    except: 
                        annuity_purchase_cost = 0
                    if running_portfolio_value >= annuity_purchase_cost:
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                        annuity_income = annuity_income_tracker_pre_purchase
                    else: 
                        # This scales back the size of the annuity income that can be purchased if there are insufficient funds to purchase the entire target annuity
                        annuity_income = annuity_income_tracker_pre_purchase * (running_portfolio_value / annuity_purchase_cost)
                        running_portfolio_value = 0                        

                # Below calculates withdrawal amount (draw) according to withdrawal option (dynamic_option) selected. The three classes above (Calc ConstantWithdrawal, CalcProportionalWithdrawal, CalcBonusWithdrawal) calculate the withdrawal amounts for each cycle. Withdrawal amounts are calculated net of any annuity income. Net withdrawal amounts are scaled up to cover cost of any deferred income tax - this is applied only to the net as cost of deferred income tax already applied to annuity purchase amount. 
                # This reads the maximum SWR by simulation year for use in withdrawal bonus and withdrawal flex calculations.  It reads the value for the preceding year to add assurance the bonus or flexed withdrawal is not too large.
                if b == 0:
                    min_multiple = 1 / (safest_swr_across_years[b + years_to_withdrawal] / 100)
                else:
                    min_multiple = 1 / (safest_swr_across_years[b - 1 + years_to_withdrawal] / 100)

                if(dynamic_option == 'proportional' or dynamic_option == 'yale' or dynamic_option == 'vanguard' or dynamic_option == 'vpw'):
                    bonus = 0
                    if b == 0: previous_draw = 0
                    if(dynamic_option == 'yale'):
                        calc = CalcProportionalWithdrawalYale(target_withdrawal_percent, draw_adjust, draw_tax, (b + years_to_withdrawal), running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3, b, previous_draw, yale_weighting, net_other_income)
                        draw = calc.result
                        previous_draw = calc.result_unadjusted
                    elif(dynamic_option == 'vanguard'):
                        calc = CalcProportionalWithdrawalVanguard(target_withdrawal_percent, draw_adjust, draw_tax, (b + years_to_withdrawal), running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3, b, previous_draw, vanguard_decrease_floor, vanguard_increase_ceiling, net_other_income)
                        draw = calc.result
                        previous_draw = calc.result_unadjusted
                    elif(dynamic_option == 'vpw'):
                        calc = CalcVPW(draw_adjust, draw_tax, running_portfolio_value, annual_withdrawal_inc, annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3, vpw_data, asset_mix, start_simulation_age, b, years_to_withdrawal, years)
                        draw = calc.result
                        previous_draw = calc.result_unadjusted
                        # data_tracker.append(calc.draw_percents)
                    else:
                        draw = CalcProportionalWithdrawal(target_withdrawal_percent, draw_adjust, draw_tax, (b + years_to_withdrawal), running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3, net_other_income).result 
                    single_withdrawal = ((max(min(draw, running_portfolio_value),0)) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)) + (annuity_income2 * (1 - annuity_tax_rate2) ) + (annuity_income3 * (1 - annuity_tax_rate3))
                    through_single_cycle_withdrawals.append(single_withdrawal)
        
                    through_single_cycle_annuity_income.append(annuity_income * (1 - annuity_tax_rate))
                    through_single_cycle_annuity_income2.append(annuity_income2 * (1 - annuity_tax_rate2))
                    through_single_cycle_annuity_income3.append(annuity_income3 * (1 - annuity_tax_rate3))
                    through_single_cycle_withdrawal_net_annuity.append(single_withdrawal - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3))

                    # Ensures simulated portfolio value can not turn negative whilst recording a fail if it would have done had the the due withdrawal been taken in full.
                    if (running_portfolio_value - draw) < 0:
                        simulation_fail_tag = 1
                    running_portfolio_value = max((running_portfolio_value - draw),0)

                    if(a == 0): unadjusted_draw_tracker.append(draw)  

                    # Conditional running_portfolio_value > 0 is not whilst code stops running_portfolio_value from turning negative.
                    if data_direction == "back":
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + bond_real[b + a + years_to_withdrawal] * asset_mix[3] + index_bond_real[b + a + years_to_withdrawal] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + (bond_forward[b + years_to_withdrawal] - cpi[b + a + years_to_withdrawal]) * asset_mix[3] + index_bond_forward[b + years_to_withdrawal] * asset_mix[4])
                    through_single_cycle_portfolio_values.append(running_portfolio_value)
                
                else:
                    if(dynamic_option == 'constantbonus'): 
                        bonus = CalcBonusWithdrawal(bonus_target, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate,  annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result
                    else:
                        bonus = 0
                    
                    # Unadjusted_draw is used for withdrawal flex and withdrawal bonus calculation.  It excludes any year by year adjustments to the withdrawal level (e.g. as % normal withdrawal level). This is used to calculate the maximum possible extra withdrawal permitted whilst remaining inside the max SWR.  The max SWR already incorporates the effect of year by year adjustments to the withdrawal level.
                    unadjusted_draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate,  annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).unadjusted_result
                    if(dynamic_option == 'constantflex' and annuity_option == '3') or (dynamic_option == 'constantflex' and annuity_percent_withdrawal == 0):
                        if (unadjusted_draw > 0 and b >= years_no_flex):
                            # this checks whether sufficient portfolio value to flex withdrawal level upwards...
                            if(running_portfolio_value / (unadjusted_draw * running_flex_withdrawal_adjustment * (1 + flex_real_increase/100)) > min_multiple): 
                                if(spring_back == "1"):
                                    if running_flex_withdrawal_adjustment >= 1:
                                        running_flex_withdrawal_adjustment = running_flex_withdrawal_adjustment + (flex_real_increase/100)
                                        draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result * running_flex_withdrawal_adjustment
                                    else:
                                        running_flex_withdrawal_adjustment = min((running_portfolio_value / (unadjusted_draw * min_multiple)), 1)
                                        draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result * running_flex_withdrawal_adjustment
                                else:
                                    running_flex_withdrawal_adjustment = running_flex_withdrawal_adjustment + (flex_real_increase/100)
                                    draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate,  annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result * running_flex_withdrawal_adjustment
                            # ...of sufficient portfolio value to maintain withdrawal level...
                            elif(running_portfolio_value / (unadjusted_draw * running_flex_withdrawal_adjustment) >= min_multiple): 
                                draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result * running_flex_withdrawal_adjustment
                            # ...otherwise this flexes withdrawal level downwards
                            else:
                                running_flex_withdrawal_adjustment = running_flex_withdrawal_adjustment - (flex_real_decrease/100)
                                draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate,  annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result * running_flex_withdrawal_adjustment
                        else:
                            draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result
                    else:
                        draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, (b + years_to_withdrawal), annuity_income, annuity_tax_rate, annuity_income2, annuity_tax_rate2, annuity_income3, annuity_tax_rate3).result
                    
                    if(a == 0): unadjusted_draw_tracker.append(unadjusted_draw)  

                    # This calculates the withdrawal recorded as part of the data output, capped by sufficient portfolio value availability to pay it.  The withdrawals are recorded net of tax, since they have been previously scaled up to include the cost of tax ('draw').
                    if(b == 0): 
                        single_withdrawal = (max(min(draw, running_portfolio_value),0) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)) + (annuity_income2 * (1 - annuity_tax_rate2)) + (annuity_income3 * (1 - annuity_tax_rate3))
                        through_single_cycle_withdrawals.append(single_withdrawal)
                    
                    else:
                        if(unadjusted_draw > 0):
                            # this is to stop negative draw (e.g. state pension > withdrawal) screwing up the min funding multiple check...
                            if(((running_portfolio_value - max(draw,0)) / max(unadjusted_draw,0)) > min_multiple):
                                # bonus_payment = max(min((bonus),((running_portfolio_value - draw) - (min_multiple * unadjusted_draw))),0)
                                bonus_payment = max(min((bonus),((running_portfolio_value - max(draw,0)) - (min_multiple * max(unadjusted_draw,0)))),0)
                                single_withdrawal = ((bonus_payment * (1 - draw_tax)) + (max(min(draw, running_portfolio_value),0) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)) + (annuity_income2 * (1 - annuity_tax_rate2)) + (annuity_income3 * (1 - annuity_tax_rate3)))
                                through_single_cycle_withdrawals.append(single_withdrawal)
                            else: 
                                single_withdrawal = ((max(min(draw, running_portfolio_value),0) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)) + (annuity_income2 * (1 - annuity_tax_rate2)) + (annuity_income3 * (1 - annuity_tax_rate3)))
                                through_single_cycle_withdrawals.append(single_withdrawal)
                        else:
                            bonus_payment = max(min((bonus),(running_portfolio_value - max(draw,0))),0)
                            single_withdrawal = ((bonus_payment * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)) + (annuity_income2 * (1 - annuity_tax_rate2)) + (annuity_income3 * (1 - annuity_tax_rate3)))
                            through_single_cycle_withdrawals.append(single_withdrawal)

                    through_single_cycle_annuity_income.append(annuity_income * (1 - annuity_tax_rate))
                    through_single_cycle_annuity_income2.append(annuity_income2 * (1 - annuity_tax_rate2))
                    through_single_cycle_annuity_income3.append(annuity_income3 * (1 - annuity_tax_rate3))
                    through_single_cycle_withdrawal_net_annuity.append(single_withdrawal - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3))

                    # Deduction of bonus and draw (including cost of tax) from portfolio value. Ensures simulated portfolio value can not turn negative whilst recording a fail if it would have done had the the due withdrawal been taken in full.
                    if (running_portfolio_value - draw) < 0:
                        simulation_fail_tag = 1
                    running_portfolio_value = max((running_portfolio_value - draw - bonus_payment),0)

                    # Conditional running_portfolio_value > 0 is to stop running_portfolio_value from turning negative.
                    if data_direction == "back":
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + bond_real[b + a + years_to_withdrawal] * asset_mix[3] + index_bond_real[b + a + years_to_withdrawal] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + (bond_forward[b + years_to_withdrawal] - cpi[b + a + years_to_withdrawal]) * asset_mix[3] + index_bond_forward[b + years_to_withdrawal] * asset_mix[4])
                    through_single_cycle_portfolio_values.append(running_portfolio_value)

                # Adjusts annuity income to keep it in real terms (e.g. if fixed type (type = "1"), then income is reduced by inflation rate)
                if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_change [b + a + years_to_withdrawal])
                elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                else: annuity_income = annuity_income

                if annuity_option2 == "1": annuity_income2 = annuity_income2 / (1 + cpi_change [b + a + years_to_withdrawal])
                elif annuity_option2 == "2": annuity_income2 = annuity_income2 * (1 + annuity_increase2 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                elif annuity_option2 == "3": annuity_income2 = annuity_income2
                else: annuity_income2 = annuity_income2 * (1 + annual_annuity2_inc)

                if annuity_option3 == "1": annuity_income3 = annuity_income3 / (1 + cpi_change [b + a + years_to_withdrawal])
                elif annuity_option3 == "2": annuity_income3 = annuity_income3 * (1 + annuity_increase3 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                elif annuity_option3 == "3": annuity_income3 = annuity_income3
                else: annuity_income3 = annuity_income3 * (1 + annual_annuity3_inc)                   
                
                bonus_payment = 0

            # Survivorship adjustment (e.g. withdrawal recorded x probability of survivorship to associated age) and temporal discount (using 'real' interest rate curve)
            for a in range(years - years_to_withdrawal):
                through_single_cycle_withdrawals_mort_adjusted.append((through_single_cycle_withdrawals[a] * mortality_adjustments[a + years_to_withdrawal]))
                through_single_cycle_withdrawals_mort_adjusted_discounted.append((through_single_cycle_withdrawals[a] * mortality_adjustments[a + years_to_withdrawal])/((1 + ilb_spot_curve[a + years_to_withdrawal]) ** (a + years_to_withdrawal)))
            through_single_cycle_avg_withdrawal_mort_adjusted.append(sum(through_single_cycle_withdrawals_mort_adjusted)/len(through_single_cycle_withdrawals_mort_adjusted))
            through_single_cycle_avg_withdrawal.append(sum(through_single_cycle_withdrawals)/len(through_single_cycle_withdrawals))

            end_single_cycle_portfolio_values.append(running_portfolio_value)
            all_portfolio_values_through_all_cycles.append(through_single_cycle_portfolio_values)
            
            annuity_income_through_all_cycles.append(through_single_cycle_annuity_income)
            annuity_income2_through_all_cycles.append(through_single_cycle_annuity_income2)
            annuity_income3_through_all_cycles.append(through_single_cycle_annuity_income3)
            withdrawal_net_annuity_through_all_cycles.append(through_single_cycle_withdrawal_net_annuity)  
            through_single_cycle_annuity_income = []
            through_single_cycle_annuity_income2 = []
            through_single_cycle_annuity_income3 = []
            through_single_cycle_withdrawal_net_annuity = []

            all_withdrawals_through_all_cycles.append(through_single_cycle_withdrawals)
            all_withdrawals_through_all_cycles_mort_adjusted_discounted.append(through_single_cycle_withdrawals_mort_adjusted_discounted)
            through_single_cycle_withdrawal_all_periods = [0] * years_to_withdrawal + through_single_cycle_withdrawals
            all_withdrawals_through_all_cycles_all_periods.append(through_single_cycle_withdrawal_all_periods)

            annuity_income = 0
            annuity_income_tracker_pre_purchase = (withdrawal_amount * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
            annuity_income2 = 0
            annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
            annuity_income3 = 0
            annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)            
            through_single_cycle_portfolio_values = [start_sum]
            through_single_cycle_withdrawals = []
            through_single_cycle_withdrawals_mort_adjusted = []
            through_single_cycle_withdrawals_mort_adjusted_discounted = []
            through_single_cycle_withdrawal_all_periods = []
            running_portfolio_value = start_sum
            running_flex_withdrawal_adjustment = 1
            simulation_fail_tag_through_all_cycles.append(simulation_fail_tag)
            simulation_fail_tag = 0
            running_contribution = contribution
            data_tracker_parent.append(data_tracker)
            data_tracker = []
            annuity_purchase_cost_tracker.append([annuity_purchase_cost, annuity_purchase_cost2])

        # sorts out data for percentile chart for portfolio values
        porfolio_value_dec0 = []
        porfolio_value_dec10 = []
        porfolio_value_dec25 = []
        porfolio_value_dec50 = []
        porfolio_value_dec75 = []
        porfolio_value_dec90 = []
        porfolio_value_dec100 = []
        portfolio_value_fan_chart_data = []
        vertical = []
        for a in range(len(all_portfolio_values_through_all_cycles[0])):
            for b in range(len(all_portfolio_values_through_all_cycles)):
                vertical.append(all_portfolio_values_through_all_cycles[b][a])
            porfolio_value_dec0.append(np.percentile(vertical, 0))
            porfolio_value_dec10.append(np.percentile(vertical, 10))
            porfolio_value_dec25.append(np.percentile(vertical, 25))
            porfolio_value_dec50.append(np.percentile(vertical, 50))
            porfolio_value_dec75.append(np.percentile(vertical, 75))
            porfolio_value_dec90.append(np.percentile(vertical, 90))
            porfolio_value_dec100.append(np.percentile(vertical, 100))
            vertical = []
        portfolio_value_fan_chart_data.append(porfolio_value_dec0)
        portfolio_value_fan_chart_data.append(porfolio_value_dec10)
        portfolio_value_fan_chart_data.append(porfolio_value_dec25)
        portfolio_value_fan_chart_data.append(porfolio_value_dec50)
        portfolio_value_fan_chart_data.append(porfolio_value_dec75)
        portfolio_value_fan_chart_data.append(porfolio_value_dec90)
        portfolio_value_fan_chart_data.append(porfolio_value_dec100)

        # sorts out data for percentile chart for income / withdrawal
        income_value_dec0 = []
        income_value_dec10 = []
        income_value_dec25 = []
        income_value_dec50 = []
        income_value_dec75 = []
        income_value_dec90 = []
        income_value_dec100 = []
        income_value_fan_chart_data = []
        vertical = []
        for a in range(len(all_withdrawals_through_all_cycles_all_periods[0])):
            for b in range(len(all_withdrawals_through_all_cycles_all_periods)):
                vertical.append(all_withdrawals_through_all_cycles_all_periods[b][a])
            income_value_dec0.append(np.percentile(vertical, 0))
            income_value_dec10.append(np.percentile(vertical, 10))
            income_value_dec25.append(np.percentile(vertical, 25))
            income_value_dec50.append(np.percentile(vertical, 50))
            income_value_dec75.append(np.percentile(vertical, 75))
            income_value_dec90.append(np.percentile(vertical, 90))
            income_value_dec100.append(np.percentile(vertical, 100))
            vertical = []
        income_value_fan_chart_data.append(income_value_dec0)
        income_value_fan_chart_data.append(income_value_dec10)
        income_value_fan_chart_data.append(income_value_dec25)
        income_value_fan_chart_data.append(income_value_dec50)
        income_value_fan_chart_data.append(income_value_dec75)
        income_value_fan_chart_data.append(income_value_dec90)
        income_value_fan_chart_data.append(income_value_dec100)

        # sorts out data for median income by type through simulation chart
        annuity_income_through_all_cycles_median = []
        annuity_income2_through_all_cycles_median = []
        annuity_income3_through_all_cycles_median = []
        withdrawal_net_annuity_all_cycles_median = []
        median_withdraw_by_type_all_cycles = []
        vertical = []
        for a in range(len(annuity_income2_through_all_cycles[0])):
            for b in range(len(annuity_income2_through_all_cycles)):    
                vertical.append(annuity_income2_through_all_cycles[b][a])
            annuity_income2_through_all_cycles_median.append(np.median(vertical))
            vertical = []
        vertical = []
        for a in range(len(annuity_income3_through_all_cycles[0])):
            for b in range(len(annuity_income3_through_all_cycles)):    
                vertical.append(annuity_income3_through_all_cycles[b][a])
            annuity_income3_through_all_cycles_median.append(np.median(vertical))
            vertical = []
        vertical = []
        for a in range(len(annuity_income_through_all_cycles[0])):
            for b in range(len(annuity_income_through_all_cycles)):    
                vertical.append(annuity_income_through_all_cycles[b][a])
            annuity_income_through_all_cycles_median.append(np.median(vertical))
            vertical = []            
        vertical = []  
        for a in range(len(withdrawal_net_annuity_through_all_cycles[0])):
            for b in range(len(withdrawal_net_annuity_through_all_cycles)):    
                vertical.append(withdrawal_net_annuity_through_all_cycles[b][a])
            withdrawal_net_annuity_all_cycles_median.append(np.median(vertical))
            vertical = []
        
        median_withdraw_by_type_all_cycles.append(annuity_income2_through_all_cycles_median)
        median_withdraw_by_type_all_cycles.append(annuity_income3_through_all_cycles_median)         
        median_withdraw_by_type_all_cycles.append(annuity_income_through_all_cycles_median)        
        median_withdraw_by_type_all_cycles.append(withdrawal_net_annuity_all_cycles_median)

        deciles = [np.percentile(end_single_cycle_portfolio_values, i) for i in range(0, 100, 10)]
        deciles.append(max(end_single_cycle_portfolio_values))

        #Calculate of withdrawal histogram output...
        draw_hist_data = []
        for a in range(len(all_withdrawals_through_all_cycles)):
            for b in range(len(all_withdrawals_through_all_cycles[a])):
                draw_hist_data.append(all_withdrawals_through_all_cycles[a][b])
        if (np.max(draw_hist_data) - np.min(draw_hist_data)) > 100000: interval = 10000
        elif np.max(np.max(draw_hist_data) - np.min(draw_hist_data)) > 50000: interval = 5000
        elif np.max(np.max(draw_hist_data) - np.min(draw_hist_data)) > 20000: interval = 2000
        else: interval = 1000
        rounded_max = np.ceil(np.max(draw_hist_data)/ interval) * interval
        rounded_min = np.floor(np.min(draw_hist_data)/ interval) * interval
        hist, bin_edges = np.histogram(draw_hist_data, bins=range(int(rounded_min), (int(rounded_max) + interval + 1), interval))
        draw_hist_data_count = hist.tolist()
        draw_hist_data_edges = bin_edges.tolist()
        draw_hist_data_percent = []
        for a in range(len(draw_hist_data_count)):
            draw_hist_data_percent.append(draw_hist_data_count[a] / len(draw_hist_data))
        self.withdrawal_histogram_data = draw_hist_data_percent
        self.withdrawal_histogram_edges = draw_hist_data_edges

        total_draw_adjusted = []
        for a in range(len(all_withdrawals_through_all_cycles_mort_adjusted_discounted)):
            total_draw_adjusted.append(sum(all_withdrawals_through_all_cycles_mort_adjusted_discounted[a]))

        self.simulation_fails = sum(simulation_fail_tag_through_all_cycles) / len(simulation_fail_tag_through_all_cycles)
        self.value_decile_data = deciles
        self.all_value_streams = all_portfolio_values_through_all_cycles
        self.all_withdrawal_streams = all_withdrawals_through_all_cycles_all_periods
        self.sum_mort_adjusted_discounted_withdrawal = sum(total_draw_adjusted) / len(total_draw_adjusted)
        self.avg_mort_adjusted_withdrawal = sum(through_single_cycle_avg_withdrawal_mort_adjusted) / len(through_single_cycle_avg_withdrawal_mort_adjusted)
        self.avg_withdrawal = sum(through_single_cycle_avg_withdrawal) / len(through_single_cycle_avg_withdrawal)
        self.avg_mort_adjusted_withdrawal = sum(through_single_cycle_avg_withdrawal_mort_adjusted) / len(through_single_cycle_avg_withdrawal_mort_adjusted)
        self.avg_end_value = sum(end_single_cycle_portfolio_values) / len(end_single_cycle_portfolio_values)
        self.unadjusted_draw_tracker = unadjusted_draw_tracker
        self.data_tracker_parent = data_tracker_parent
        self.annuity_purchase_cost_tracker = annuity_purchase_cost_tracker
        self.median_withdraw_by_type_all_cycles = median_withdraw_by_type_all_cycles
        self.portfolio_value_fan_chart_data = portfolio_value_fan_chart_data
        self.income_value_fan_chart_data = income_value_fan_chart_data

# Algorithm that calculates i) back-tested, zero fail safe withdrawal rate (SWR) for each seperate back-testing cycle and ii) back-tested, zero fail safe withdrawal rate (SWR) for each year through simulation (using all back-testing cycles).  Takes prepared parameters and prepared data and returns data curves.
class CalcMaxBacktestedSWRs:
    def __init__(self, equity_real, bond_real, index_bond_real, asset_mix, start_sum, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, annuity_option_list, annuity_increase_list, annuity_price_list, annuity_tax_rate_list, cpi_change, annuity_percent_withdrawal_list, annuity_start_year_list, data_direction, years_contributions, contribution, contribution_increase, years_between):
        
        annuity_option = annuity_option_list[0]
        annuity_increase = annuity_increase_list[0]
        annuity_price = annuity_price_list[0]
        annuity_tax_rate = annuity_tax_rate_list[0]
        annuity_percent_withdrawal = annuity_percent_withdrawal_list[0]
        annuity_start_year = annuity_start_year_list[0]

        annuity_option2 = annuity_option_list[1]
        annuity_increase2 = annuity_increase_list[1]
        annuity_price2 = annuity_price_list[1]
        annuity_tax_rate2 = annuity_tax_rate_list[1]
        annuity_percent_withdrawal2 = annuity_percent_withdrawal_list[1]
        annuity_start_year2 = annuity_start_year_list[1]

        annuity_option3 = annuity_option_list[2]
        annuity_increase3 = annuity_increase_list[2]
        annuity_price3 = annuity_price_list[2]
        annuity_tax_rate3 = annuity_tax_rate_list[2]
        annuity_percent_withdrawal3 = annuity_percent_withdrawal_list[2]
        annuity_start_year3 = annuity_start_year_list[2]
        

        # this sets the value increase for state pension through simulation years 
        if annuity_option2 == "4": annual_annuity2_inc = annuity_increase2 / 100
        else: annual_annuity2_inc = 0
        if annuity_option3 == "4": annual_annuity3_inc = annuity_increase3 / 100
        else: annual_annuity3_inc = 0

        # this is to stop unwanted annuity effect happening in backward looking calc end values
        # if data_direction == 'back': 
        #     annuity_percent_withdrawal = 0

        safe_withdrawal = []
        years_to_withdrawal = years_contributions + years_between

        for a in range(len(equity_real) - years):
            withdrawal_unit = start_sum / 100
            withdrawal_counter = 1.0
            while withdrawal_counter < 100:
                withdrawal = withdrawal_unit * withdrawal_counter
                running_portfolio_value = start_sum
                running_contribution = contribution

                annuity_income = 0
                annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)                
                annuity_income2 = 0                    
                annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
                annuity_income3 = 0                    
                annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)

                for b in range(years_to_withdrawal):
                    if b < years_contributions:
                        running_portfolio_value += running_contribution
                        running_contribution = running_contribution * (1 + contribution_increase / 100)
                    if data_direction == "back":
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])
                    if b == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                    else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)   
                    if b == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                    else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc) 

                for b in range(years - years_to_withdrawal):      
                    if b < (annuity_start_year2 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                        else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)         
                    elif b == (annuity_start_year2 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                        else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)                        
                        try: annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100))
                        except: annuity_purchase_cost2 = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost2
                        annuity_income2 = annuity_income_tracker_pre_purchase2

                    if b < (annuity_start_year3 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                        else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)         
                    elif b == (annuity_start_year3 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                        else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)                        
                        try: annuity_purchase_cost3 = (annuity_income_tracker_pre_purchase3 / (annuity_price3 / 100))
                        except: annuity_purchase_cost3 = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost3
                        annuity_income3 = annuity_income_tracker_pre_purchase3

                    if b < (annuity_start_year - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    elif b == (annuity_start_year - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        if annuity_start_year2 and annuity_start_year3 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2) - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                        elif annuity_start_year2 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2)), 0) 
                        elif annuity_start_year3 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                        else: 
                            annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        
                        try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100))
                        except: annuity_purchase_cost = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                        annuity_income = annuity_income_tracker_pre_purchase

                    if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - (withdrawal * draw_adjust[b + years_to_withdrawal] * ((1 + annual_withdrawal_inc) ** (b + years_to_withdrawal)) - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3)) / (1 - draw_tax)
                    if data_direction == 'back':
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + bond_real[b + a + years_to_withdrawal] * asset_mix[3] + index_bond_real[b + a + years_to_withdrawal] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + (bond_forward[b + years_to_withdrawal] - cpi[b + a + years_to_withdrawal]) * asset_mix[3] + index_bond_forward[b + years_to_withdrawal] * asset_mix[4])        

                    if annuity_option == "1": annuity_income = annuity_income / (1 + cpi[b + a + years_to_withdrawal])
                    elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi[b + a + years_to_withdrawal])
                    else: annuity_income = annuity_income

                    if annuity_option2 == "1": annuity_income2 = annuity_income2 / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option2 == "2": annuity_income2 = annuity_income2 * (1 + annuity_increase2 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option2 == "3": annuity_income2 = annuity_income2
                    else: annuity_income2 = annuity_income2 * (1 + annual_annuity2_inc)

                    if annuity_option3 == "1": annuity_income3 = annuity_income3 / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option3 == "2": annuity_income3 = annuity_income3 * (1 + annuity_increase3 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option3 == "3": annuity_income3 = annuity_income3
                    else: annuity_income3 = annuity_income3 * (1 + annual_annuity3_inc)

                if (running_portfolio_value < 0): 
                    withdrawal_counter -= 0.9
                    break
                withdrawal_counter += 1

            while withdrawal_counter < 100:
                withdrawal = withdrawal_unit * withdrawal_counter
                running_portfolio_value = start_sum
                running_contribution = contribution

                annuity_income = 0
                annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)                
                annuity_income2 = 0                    
                annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
                annuity_income3 = 0                    
                annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)

                for b in range(years_to_withdrawal):
                    if b < years_contributions:
                        running_portfolio_value += running_contribution
                        running_contribution = running_contribution * (1 + contribution_increase / 100)
                    if data_direction == "back":
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])
                    if b == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                    else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)   
                    if b == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                    else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc) 

                for b in range(years - years_to_withdrawal):      
                    if b < (annuity_start_year2 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                        else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)         
                    elif b == (annuity_start_year2 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                        else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)                        
                        try: annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100))
                        except: annuity_purchase_cost2 = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost2
                        annuity_income2 = annuity_income_tracker_pre_purchase2

                    if b < (annuity_start_year3 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                        else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)         
                    elif b == (annuity_start_year3 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                        else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)                        
                        try: annuity_purchase_cost3 = (annuity_income_tracker_pre_purchase3 / (annuity_price3 / 100))
                        except: annuity_purchase_cost3 = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost3
                        annuity_income3 = annuity_income_tracker_pre_purchase3

                    if b < (annuity_start_year - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    elif b == (annuity_start_year - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        if annuity_start_year2 and annuity_start_year3 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2) - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                        elif annuity_start_year2 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2)), 0) 
                        elif annuity_start_year3 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                        else: 
                            annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase            
                        try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100))
                        except: annuity_purchase_cost = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                        annuity_income = annuity_income_tracker_pre_purchase

                    if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - (withdrawal * draw_adjust[b + years_to_withdrawal] * ((1 + annual_withdrawal_inc) ** (b + years_to_withdrawal)) - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3)) / (1 - draw_tax)
                    if data_direction == 'back':
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + bond_real[b + a + years_to_withdrawal] * asset_mix[3] + index_bond_real[b + a + years_to_withdrawal] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + (bond_forward[b + years_to_withdrawal] - cpi[b + a + years_to_withdrawal]) * asset_mix[3] + index_bond_forward[b + years_to_withdrawal] * asset_mix[4])        

                    if annuity_option == "1": annuity_income = annuity_income / (1 + cpi[b + a + years_to_withdrawal])
                    elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi[b + a + years_to_withdrawal])
                    else: annuity_income = annuity_income

                    if annuity_option2 == "1": annuity_income2 = annuity_income2 / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option2 == "2": annuity_income2 = annuity_income2 * (1 + annuity_increase2 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option2 == "3": annuity_income2 = annuity_income2
                    else: annuity_income2 = annuity_income2 * (1 + annual_annuity2_inc)

                    if annuity_option3 == "1": annuity_income3 = annuity_income3 / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option3 == "2": annuity_income3 = annuity_income3 * (1 + annuity_increase3 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option3 == "3": annuity_income3 = annuity_income3
                    else: annuity_income3 = annuity_income3 * (1 + annual_annuity3_inc)

                if (running_portfolio_value < 0): 
                    withdrawal_counter -= 0.09
                    break
                withdrawal_counter += 0.1

            while withdrawal_counter < 100:
                withdrawal = withdrawal_unit * withdrawal_counter
                running_portfolio_value = start_sum
                running_contribution = contribution

                annuity_income = 0
                annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)                
                annuity_income2 = 0                    
                annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
                annuity_income3 = 0                    
                annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)

                for b in range(years_to_withdrawal):
                    if b < years_contributions:
                        running_portfolio_value += running_contribution
                        running_contribution = running_contribution * (1 + contribution_increase / 100)
                    if data_direction == "back":
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])
                    if b == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                    else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)   
                    if b == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                    else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc) 

                for b in range(years - years_to_withdrawal):      
                    if b < (annuity_start_year2 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                        else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)         
                    elif b == (annuity_start_year2 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                        else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)                        
                        # try: annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100)) / (1 - draw_tax)
                        try: annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100))
                        except: annuity_purchase_cost2 = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost2
                        annuity_income2 = annuity_income_tracker_pre_purchase2

                    if b < (annuity_start_year3 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                        else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)         
                    elif b == (annuity_start_year3 - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                        else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)                        
                        try: annuity_purchase_cost3 = (annuity_income_tracker_pre_purchase3 / (annuity_price3 / 100))
                        except: annuity_purchase_cost3 = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost3
                        annuity_income3 = annuity_income_tracker_pre_purchase3

                    if b < (annuity_start_year - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    elif b == (annuity_start_year - 1 - years_to_withdrawal):
                        if b == 0 and years_to_withdrawal == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        if annuity_start_year2 and annuity_start_year3 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2) - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                        elif annuity_start_year2 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2)), 0)
                        elif annuity_start_year3 <= annuity_start_year: 
                            annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0)
                        else: 
                            annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100))
                        except: annuity_purchase_cost = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                        annuity_income = annuity_income_tracker_pre_purchase

                    if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - (withdrawal * draw_adjust[b + years_to_withdrawal] * ((1 + annual_withdrawal_inc) ** (b + years_to_withdrawal)) - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3)) / (1 - draw_tax)
                    if data_direction == 'back':
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + bond_real[b + a + years_to_withdrawal] * asset_mix[3] + index_bond_real[b + a + years_to_withdrawal] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + years_to_withdrawal] * asset_mix[0] + (bond_forward[b + years_to_withdrawal] - cpi[b + a + years_to_withdrawal]) * asset_mix[3] + index_bond_forward[b + years_to_withdrawal] * asset_mix[4])        

                    if annuity_option == "1": annuity_income = annuity_income / (1 + cpi[b + a + years_to_withdrawal])
                    elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi[b + a + years_to_withdrawal])
                    else: annuity_income = annuity_income

                    if annuity_option2 == "1": annuity_income2 = annuity_income2 / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option2 == "2": annuity_income2 = annuity_income2 * (1 + annuity_increase2 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option2 == "3": annuity_income2 = annuity_income2
                    else: annuity_income2 = annuity_income2 * (1 + annual_annuity2_inc)

                    if annuity_option3 == "1": annuity_income3 = annuity_income3 / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option3 == "2": annuity_income3 = annuity_income3 * (1 + annuity_increase3 / 100) / (1 + cpi_change [b + a + years_to_withdrawal])
                    elif annuity_option3 == "3": annuity_income3 = annuity_income3
                    else: annuity_income3 = annuity_income3 * (1 + annual_annuity3_inc)

                if (running_portfolio_value < 0): 
                    break
                withdrawal_counter += 0.01
            safe_withdrawal.append((withdrawal_counter - 0.01) * (withdrawal_unit))
        safest_swr_in_year = []
        safest_swr_across_years = []
        minimum_funding_level_across_years = []

        # this option gives the max running portfolio value at the beginning of the year sub-set (to calc swr with contribution at their smallest as % of running portfolio value)
        for c in range(years):
            start_running_portfolio_value = start_sum
            running_contribution = contribution
            range_start_running_portfolio_values = []
            for d in range(len(equity_real) - (years)):
                for e in range(c):
                    if e < (years_contributions):
                        start_running_portfolio_value += running_contribution
                        running_contribution = running_contribution * (1 + contribution_increase / 100)
                    if data_direction == 'back':
                        if(start_running_portfolio_value >= 0): start_running_portfolio_value = start_running_portfolio_value * (1 + equity_real[e + d] * asset_mix[0] + bond_real[e + d] * asset_mix[3] + index_bond_real[e + d] * asset_mix[4])
                    else:
                        if(start_running_portfolio_value >= 0): start_running_portfolio_value = start_running_portfolio_value * (1 + equity_real[e + d] * asset_mix[0] + (bond_forward[e] - cpi[e + d]) * asset_mix[3] + index_bond_forward[e] * asset_mix[4])
                range_start_running_portfolio_values.append(start_running_portfolio_value)
                start_running_portfolio_value = start_sum
                running_contribution = contribution
            mid_simulation_running_portfolio_value = max(range_start_running_portfolio_values)
            mid_simulation_running_contribution = running_contribution
            for a in range(len(equity_real) - (years)):
               
                withdrawal_counter = 1.0
                while withdrawal_counter < 100:
                    running_portfolio_value = mid_simulation_running_portfolio_value
                    withdrawal_unit = running_portfolio_value / 100
                    withdrawal = withdrawal_counter * withdrawal_unit
                    running_contribution = mid_simulation_running_contribution

                    annuity_income = 0
                    annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
                    annuity_income2 = 0                    
                    annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
                    annuity_income3 = 0                    
                    annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)

                    for b in range(years - c):
                        if b < (years_contributions - c):
                            running_portfolio_value += running_contribution
                            running_contribution = running_contribution * (1 + contribution_increase / 100)
                        if b < (annuity_start_year2 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                            else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)
                        elif b == (annuity_start_year2 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                            else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)                            
                            try: annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100))
                            except: annuity_purchase_cost2 = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost2
                            annuity_income2 = annuity_income_tracker_pre_purchase2

                        if b < (years_contributions - c):
                            running_portfolio_value += running_contribution
                            running_contribution = running_contribution * (1 + contribution_increase / 100)
                        if b < (annuity_start_year3 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                            else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)
                        elif b == (annuity_start_year3 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                            else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)                            
                            try: annuity_purchase_cost3 = (annuity_income_tracker_pre_purchase3 / (annuity_price3 / 100))
                            except: annuity_purchase_cost3 = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost3
                            annuity_income3 = annuity_income_tracker_pre_purchase3

                        if b < (annuity_start_year - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        elif b == (annuity_start_year - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                            if annuity_start_year2 and annuity_start_year3 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2) - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                            elif annuity_start_year2 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2)), 0)
                            elif annuity_start_year3 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0)
                            else: 
                                annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100))
                            except: annuity_purchase_cost = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                            annuity_income = annuity_income_tracker_pre_purchase

                        net_withdrawal = (withdrawal * draw_adjust[b + c] * ((1 + annual_withdrawal_inc) ** (b)) - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3)) / (1 - draw_tax)
                        if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - net_withdrawal
                        if data_direction == 'back':
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + bond_real[b + a + c] * asset_mix[3] + index_bond_real[b + a + c] * asset_mix[4])
                        else:
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + (bond_forward[b + c] - cpi[b + a + c]) * asset_mix[3] + index_bond_forward[b + c] * asset_mix[4])
                        
                        cpi_delta = cpi[b + a + c]
                        if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_delta)
                        elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_delta)
                        else: annuity_income = annuity_income

                        if annuity_option2 == "1": annuity_income2 = annuity_income2 / (1 + cpi_delta)
                        elif annuity_option2 == "2": annuity_income2 = annuity_income2 * (1 + annuity_increase2 / 100) / (1 + cpi_delta)
                        elif annuity_option2 == "3": annuity_income2 = annuity_income2
                        else: annuity_income2 = annuity_income2 * (1 + annual_annuity2_inc)

                        if annuity_option3 == "1": annuity_income3 = annuity_income3 / (1 + cpi_delta)
                        elif annuity_option3 == "2": annuity_income3 = annuity_income3 * (1 + annuity_increase3 / 100) / (1 + cpi_delta)
                        elif annuity_option3 == "3": annuity_income3 = annuity_income3
                        else: annuity_income3 = annuity_income3 * (1 + annual_annuity3_inc)                    

                    if (running_portfolio_value < 0): 
                        withdrawal_counter -= 0.9
                        break
                    withdrawal_counter += 1.0
                    
                while withdrawal_counter < 100:
                    running_portfolio_value = mid_simulation_running_portfolio_value
                    withdrawal_unit = running_portfolio_value / 100
                    withdrawal = withdrawal_counter * withdrawal_unit
                    running_contribution = mid_simulation_running_contribution

                    annuity_income = 0
                    annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
                    annuity_income2 = 0                    
                    annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
                    annuity_income3 = 0                    
                    annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)

                    for b in range(years - c):
                        if b < (years_contributions - c):
                            running_portfolio_value += running_contribution
                            running_contribution = running_contribution * (1 + contribution_increase / 100)
                        if b < (annuity_start_year2 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                            else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)
                        elif b == (annuity_start_year2 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                            else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)                            
                            try: annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100))
                            except: annuity_purchase_cost2 = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost2
                            annuity_income2 = annuity_income_tracker_pre_purchase2

                        if b < (years_contributions - c):
                            running_portfolio_value += running_contribution
                            running_contribution = running_contribution * (1 + contribution_increase / 100)
                        if b < (annuity_start_year3 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                            else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)
                        elif b == (annuity_start_year3 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                            else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)                            
                            try: annuity_purchase_cost3 = (annuity_income_tracker_pre_purchase3 / (annuity_price3 / 100))
                            except: annuity_purchase_cost3 = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost3
                            annuity_income3 = annuity_income_tracker_pre_purchase3

                        if b < (annuity_start_year - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        elif b == (annuity_start_year - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                            if annuity_start_year2 and annuity_start_year3 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2) - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                            elif annuity_start_year2 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2)), 0) 
                            elif annuity_start_year3 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                            else: 
                                annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase 
                            try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100))
                            except: annuity_purchase_cost = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                            annuity_income = annuity_income_tracker_pre_purchase

                        net_withdrawal = (withdrawal * draw_adjust[b + c] * ((1 + annual_withdrawal_inc) ** (b)) - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3)) / (1 - draw_tax)
                        if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - net_withdrawal
                        if data_direction == 'back':
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + bond_real[b + a + c] * asset_mix[3] + index_bond_real[b + a + c] * asset_mix[4])
                        else:
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + (bond_forward[b + c] - cpi[b + a + c]) * asset_mix[3] + index_bond_forward[b + c] * asset_mix[4])
                        
                        cpi_delta = cpi[b + a + c]
                        if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_delta)
                        elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_delta)
                        else: annuity_income = annuity_income

                        if annuity_option2 == "1": annuity_income2 = annuity_income2 / (1 + cpi_delta)
                        elif annuity_option2 == "2": annuity_income2 = annuity_income2 * (1 + annuity_increase2 / 100) / (1 + cpi_delta)
                        elif annuity_option2 == "3": annuity_income2 = annuity_income2
                        else: annuity_income2 = annuity_income2 * (1 + annual_annuity2_inc)

                        if annuity_option3 == "1": annuity_income3 = annuity_income3 / (1 + cpi_delta)
                        elif annuity_option3 == "2": annuity_income3 = annuity_income3 * (1 + annuity_increase3 / 100) / (1 + cpi_delta)
                        elif annuity_option3 == "3": annuity_income3 = annuity_income3
                        else: annuity_income3 = annuity_income3 * (1 + annual_annuity3_inc)                    

                    if (running_portfolio_value < 0): 
                        withdrawal_counter -= 0.09
                        break
                    withdrawal_counter += 0.1

                while withdrawal_counter < 100:
                    running_portfolio_value = mid_simulation_running_portfolio_value
                    withdrawal_unit = running_portfolio_value / 100
                    withdrawal = withdrawal_counter * withdrawal_unit
                    running_contribution = mid_simulation_running_contribution

                    annuity_income = 0
                    annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
                    annuity_income2 = 0                    
                    annuity_income_tracker_pre_purchase2 = (annuity_percent_withdrawal2)
                    annuity_income3 = 0                    
                    annuity_income_tracker_pre_purchase3 = (annuity_percent_withdrawal3)

                    for b in range(years - c):
                        if b < (years_contributions - c):
                            running_portfolio_value += running_contribution
                            running_contribution = running_contribution * (1 + contribution_increase / 100)
                        if b < (annuity_start_year2 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                            else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)
                        elif b == (annuity_start_year2 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2
                            else: annuity_income_tracker_pre_purchase2 = annuity_income_tracker_pre_purchase2 * (1 + annual_annuity2_inc)                            
                            try: annuity_purchase_cost2 = (annuity_income_tracker_pre_purchase2 / (annuity_price2 / 100))
                            except: annuity_purchase_cost2 = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost2
                            annuity_income2 = annuity_income_tracker_pre_purchase2

                        if b < (years_contributions - c):
                            running_portfolio_value += running_contribution
                            running_contribution = running_contribution * (1 + contribution_increase / 100)
                        if b < (annuity_start_year3 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                            else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)
                        elif b == (annuity_start_year3 - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3
                            else: annuity_income_tracker_pre_purchase3 = annuity_income_tracker_pre_purchase3 * (1 + annual_annuity3_inc)                            
                            try: annuity_purchase_cost3 = (annuity_income_tracker_pre_purchase3 / (annuity_price3 / 100))
                            except: annuity_purchase_cost3 = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost3
                            annuity_income3 = annuity_income_tracker_pre_purchase3

                        if b < (annuity_start_year - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        elif b == (annuity_start_year - 1 - c):
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                            if annuity_start_year2 and annuity_start_year3 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2) - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                            elif annuity_start_year2 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase2 * (1 - annuity_tax_rate2)), 0)
                            elif annuity_start_year3 <= annuity_start_year: 
                                annuity_income_tracker_pre_purchase = max((annuity_income_tracker_pre_purchase - annuity_income_tracker_pre_purchase3 * (1 - annuity_tax_rate3)), 0) 
                            else: 
                                annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100))
                            except: annuity_purchase_cost = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                            annuity_income = annuity_income_tracker_pre_purchase

                        net_withdrawal = (withdrawal * draw_adjust[b + c] * ((1 + annual_withdrawal_inc) ** (b)) - annuity_income * (1 - annuity_tax_rate) - annuity_income2 * (1 - annuity_tax_rate2) - annuity_income3 * (1 - annuity_tax_rate3)) / (1 - draw_tax)
                        if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - net_withdrawal
                        if data_direction == 'back':
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + bond_real[b + a + c] * asset_mix[3] + index_bond_real[b + a + c] * asset_mix[4])
                        else:
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + (bond_forward[b + c] - cpi[b + a + c]) * asset_mix[3] + index_bond_forward[b + c] * asset_mix[4])
                        
                        cpi_delta = cpi[b + a + c]
                        if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_delta)
                        elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_delta)
                        else: annuity_income = annuity_income

                        if annuity_option2 == "1": annuity_income2 = annuity_income2 / (1 + cpi_delta)
                        elif annuity_option2 == "2": annuity_income2 = annuity_income2 * (1 + annuity_increase2 / 100) / (1 + cpi_delta)
                        elif annuity_option2 == "3": annuity_income2 = annuity_income2
                        else: annuity_income2 = annuity_income2 * (1 + annual_annuity2_inc)

                        if annuity_option3 == "1": annuity_income3 = annuity_income3 / (1 + cpi_delta)
                        elif annuity_option3 == "2": annuity_income3 = annuity_income3 * (1 + annuity_increase3 / 100) / (1 + cpi_delta)
                        elif annuity_option3 == "3": annuity_income3 = annuity_income3
                        else: annuity_income3 = annuity_income3 * (1 + annual_annuity3_inc)                    

                    if (running_portfolio_value < 0): 
                        break
                    withdrawal_counter += 0.01

                safest_swr_in_year.append((withdrawal_counter - 0.01))
            safest_swr_across_years.append(min(safest_swr_in_year))
            safest_swr_in_year = []

        self.safest_swr_across_years = safest_swr_across_years
        self.safe_withdrawal = safe_withdrawal
        self.minimum_funding_level_across_years = minimum_funding_level_across_years

class CalcSafeFundingLevel:
    def __init__(self, swr, draw, years):
        min_funding_level = []
        max_withdrawal_rate = []
        for a in range(len(swr)):
            result = (draw[a] / (swr[a] / 100))
            if a < years: 
                min_funding_level.append(None)
                max_withdrawal_rate.append(None)
            else: 
                min_funding_level.append(result)
                max_withdrawal_rate.append(swr[a])
        self.min_funding_level = min_funding_level
        self.max_withdrawal_rate = max_withdrawal_rate


# Algorithm that finds optimal asset mix combination for taking prepared parameter & return data set and by iterating through possible combinations (in 10% increments) and using the RunSimulation () class to test each iteration.  Returns two asset mix combinations ('max' and 'min' respectively) i) mix that returns highest expected end simulation value (for zero or lowest possible failure rate) ii) mix that has lowest real-term value volatility (for zero or lowest possible failure rate).
class OptimiseAssetMix:
    def __init__(self, equity_real, bond_real, index_bond_real, start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction, years_contributions, contribution, contribution_increase, years_between, yale_weighting, vanguard_decrease_floor, vanguard_increase_ceiling, vpw_data, net_other_income):
        # this sets the 'starting portfolio' against which the iteration tries to find an improvement.
        if data_direction == "back":
            equity = 0
            fixed_income_bond = 1
            inflation_linked_bond = 0
        else: 
            equity = 0
            fixed_income_bond = 0
            inflation_linked_bond = 1
        bonus_target = 0

        # below is here as instances of RunSimulation() in this class require it (for flex and bonus withdrawal strategic calculations).  Ideally would call CalcMaxBacktestedSWRs for each asset mix iteration but it is too time consuming.  Putting safest_swr_across_years to 3 is suitably conservative fix.  
        safest_swr_across_years = [3] * years

        result = RunSimulation(equity_real, bond_real, index_bond_real, [equity,0,0,fixed_income_bond, inflation_linked_bond], start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction, years_contributions, contribution, contribution_increase, years_between, yale_weighting, vanguard_decrease_floor, vanguard_increase_ceiling, vpw_data, net_other_income)
        best_result_max = {'equity' : equity * 100, 'fixed_income_bond' : fixed_income_bond * 100, 'inflation_linked_bond' : inflation_linked_bond * 100, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
        best_result_min = {'equity' : equity * 100, 'fixed_income_bond' : fixed_income_bond * 100, 'inflation_linked_bond' : inflation_linked_bond * 100, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
        equity_weights = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for a in equity_weights:
            equity = a
            fixed_income = 100 - equity
            if data_direction == "back":
                fixed_income_bond = fixed_income
                inflation_linked_bond = 0
                result = RunSimulation(equity_real, bond_real, index_bond_real, [equity/100,0,0,fixed_income_bond/100, inflation_linked_bond/100], start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction, years_contributions, contribution, contribution_increase, years_between, yale_weighting, vanguard_decrease_floor, vanguard_increase_ceiling, vpw_data, net_other_income)
                if result.simulation_fails < best_result_min['fail']:
                    best_result_min = {'equity' : equity, 'fixed_income_bond' : fixed_income_bond, 'inflation_linked_bond' : inflation_linked_bond, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
                if result.simulation_fails < best_result_max['fail']:
                    best_result_max = {'equity' : equity, 'fixed_income_bond' : fixed_income_bond, 'inflation_linked_bond' : inflation_linked_bond, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
                if result.simulation_fails == best_result_max['fail'] and result.avg_end_value > best_result_max['avg_value']:
                    best_result_max = {'equity' : equity, 'fixed_income_bond' : fixed_income_bond, 'inflation_linked_bond' : inflation_linked_bond, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}

            else:
                for b in range(0, fixed_income + 1, 10):
                    fixed_income_bond = b
                    inflation_linked_bond = fixed_income - b
                    result = RunSimulation(equity_real, bond_real, index_bond_real, [equity/100,0,0,fixed_income_bond/100, inflation_linked_bond/100], start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction, years_contributions, contribution, contribution_increase, years_between, yale_weighting, vanguard_decrease_floor, vanguard_increase_ceiling, vpw_data, net_other_income)
                    if result.simulation_fails < best_result_min['fail']:
                        best_result_min = {'equity' : equity, 'fixed_income_bond' : fixed_income_bond, 'inflation_linked_bond' : inflation_linked_bond, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
                    if result.simulation_fails < best_result_max['fail']:
                        best_result_max = {'equity' : equity, 'fixed_income_bond' : fixed_income_bond, 'inflation_linked_bond' : inflation_linked_bond, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
                    if result.simulation_fails == best_result_max['fail'] and result.avg_end_value > best_result_max['avg_value']:
                        best_result_max = {'equity' : equity, 'fixed_income_bond' : fixed_income_bond, 'inflation_linked_bond' : inflation_linked_bond, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
            
            self.optimised_equity_max = best_result_max['equity']
            self.optimised_indexlinked_max = best_result_max['inflation_linked_bond']
            self.optimised_fixedincome_max = best_result_max['fixed_income_bond']
            self.optimised_failure_max = best_result_max['fail']
            self.optimised_equity_min = best_result_min['equity']
            self.optimised_indexlinked_min = best_result_min['inflation_linked_bond']
            self.optimised_fixedincome_min = best_result_min['fixed_income_bond']
            self.optimised_failure_min = best_result_min['fail']

# Class is independent of other classes and calculates different analytical cuts of historic return data.  Serves the 'historics' view.
class AnalyseHistoricData:
    def __init__(self, equity, historic_bond, historic_index_bond, cpi, gbpusd, bond_coupon, index_bond_coupon, period, index_bond_forward, bond_forward, index_bond_forward_us, bond_forward_us):
        
        equity_nominal_1 = []
        bond_nominal_1 = []
        index_bond_nominal_1 = []
        cpi_change_1 = []
        equity_real_1 = []
        bond_real_1 = []
        index_bond_real_1 = [] 

        equity_nominal_5 = []
        bond_nominal_5 = []
        index_bond_nominal_5 = []
        cpi_change_5 = []
        equity_real_5 = []
        bond_real_5 = []
        index_bond_real_5 = []
        index_bond_forward_select = []

        # guessing this is for the forward looking bond market yields (code takes forward rates and constructs 5, 10, 20 and 30 year yields)
        for a in range(len(index_bond_forward) - 13):
            index_bond_forward_select.append(index_bond_forward[a + 3])
        bond_forward_select = []
        for a in range(len(bond_forward) - 13):
            bond_forward_select.append(bond_forward[a + 3])
        index_bond_forward_select_us = []
        for a in range(len(index_bond_forward_us) - 13):
            index_bond_forward_select_us.append(index_bond_forward_us[a + 3])
        bond_forward_select_us = []
        for a in range(len(bond_forward_us) - 13):
            bond_forward_select_us.append(bond_forward_us[a + 3])

        bond_gbp = [0, 0, 0, 0]
        ilb_gbp = [0, 0, 0, 0]
        bond_usd = [0, 0, 0, 0]
        ilb_usd = [0, 0, 0, 0]
        result = 1

        y = [5, 10, 20, 30]
        for a in range(len(y)):
            for b in range(y[a]):
                result = result * (1 + float(bond_forward[b]) / 100)
            result = ((result ** (1 / y[a])) - 1) * 100
            bond_gbp[a] = result
            result = 1
            for b in range(y[a]):
                result = result * (1 + float(index_bond_forward[b]) / 100)
            result = ((result ** (1 / y[a])) - 1) * 100
            ilb_gbp[a] = result
            result = 1
            for b in range(y[a]):
                result = result * (1 + float(bond_forward_us[b]) / 100)
            result = ((result ** (1 / y[a])) - 1) * 100
            bond_usd[a] = result
            result = 1
            for b in range(y[a]):
                result = result * (1 + float(index_bond_forward_us[b]) / 100)
            result = ((result ** (1 / y[a])) - 1) * 100
            ilb_usd[a] = result
            result = 1

        five = [bond_gbp[0], ilb_gbp[0], bond_usd[0], ilb_usd[0]]
        ten = [bond_gbp[1], ilb_gbp[1], bond_usd[1], ilb_usd[1]]
        twenty = [bond_gbp[2], ilb_gbp[2], bond_usd[2], ilb_usd[2]]
        thirty = [bond_gbp[3], ilb_gbp[3], bond_usd[3], ilb_usd[3]]

        forward_chart_labels = []
        for a in range(len(index_bond_forward_select)):
            forward_chart_labels.append(a + 3)

        # below calculates lists of historic returns
        for a in range(len(equity) - 1):
            num = float(equity[a + 1]) / float(gbpusd [a + 1])
            denom = float(equity[a]) / float(gbpusd [a])
            change = ((num / denom) - 1)
            equity_nominal_1.append(change)
        for a in range(len(historic_bond) - 1):
            num = PresentValue(float(historic_bond[a + 1]) / 100, 10, bond_coupon, 100).pv
            denom = PresentValue(float(historic_bond[a]) / 100, 10, bond_coupon, 100).pv
            change = ((num / denom) - 1) + (float(historic_bond[a]) / 100)
            bond_nominal_1.append(change)
        for a in range(len(historic_index_bond) - 1):
            num = PresentValue(float(historic_index_bond[a + 1]) / 100, 10, index_bond_coupon, 100).pv
            denom = PresentValue(float(historic_index_bond[a]) / 100, 10, index_bond_coupon, 100).pv
            num_cpi = float(cpi[a + 1])
            denom_cpi = float(cpi[a])
            change = ((num / denom) - 1) + (float(historic_index_bond[a]) / 100) + ((num_cpi / denom_cpi) - 1)
            index_bond_nominal_1.append(change)    
        for a in range(len(cpi) - 1):
            num_cpi = float(cpi[a + 1])
            denom_cpi = float(cpi[a])
            change = ((num_cpi / denom_cpi) - 1)
            cpi_change_1.append(change)
        for a in range(len(equity) - 1):
            num = float(equity[a + 1]) / float(gbpusd [a + 1])
            denom = float(equity[a]) / float(gbpusd [a])
            num_cpi = float(cpi[a + 1])
            denom_cpi = float(cpi[a])            
            change = ((num / denom) - 1) - ((num_cpi / denom_cpi) - 1)
            equity_real_1.append(change)
        for a in range(len(historic_bond) - 1):
            num = PresentValue(float(historic_bond[a + 1]) / 100, 10, bond_coupon, 100).pv
            denom = PresentValue(float(historic_bond[a]) / 100, 10, bond_coupon, 100).pv
            num_cpi = float(cpi[a + 1])
            denom_cpi = float(cpi[a]) 
            change = ((num / denom) - 1) + (float(historic_bond[a]) / 100) - ((num_cpi / denom_cpi) - 1)
            bond_real_1.append(change)
        for a in range(len(historic_index_bond) - 1):
            num = PresentValue(float(historic_index_bond[a + 1]) / 100, 10, index_bond_coupon, 100).pv
            denom = PresentValue(float(historic_index_bond[a]) / 100, 10, index_bond_coupon, 100).pv
            change = ((num / denom) - 1) + (float(historic_index_bond[a]) / 100)
            index_bond_real_1.append(change)

        # below is for avg return / variance analysis
        equity100nominal = []
        equity80nominal = []
        equity60nominal = []
        equity40nominal = []
        equity20nominal = []
        equity0nominal = []
        equity100real = []
        equity90real = []
        equity80real = []
        equity70real = []
        equity60real = []
        equity50real = []
        equity40real = []
        equity30real = []
        equity20real = []
        equity10real = []
        equity0real = []
        
        for a in range(len(equity_nominal_1)):
            equity100nominal.append(equity_nominal_1[a] * 1 + bond_nominal_1[a] * 0)
            equity80nominal.append(equity_nominal_1[a] * 0.8 + bond_nominal_1[a] * 0.2)
            equity60nominal.append(equity_nominal_1[a] * 0.6 + bond_nominal_1[a] * 0.4)
            equity40nominal.append(equity_nominal_1[a] * 0.4 + bond_nominal_1[a] * 0.6)
            equity20nominal.append(equity_nominal_1[a] * 0.2 + bond_nominal_1[a] * 0.8)
            equity0nominal.append(equity_nominal_1[a] * 0 + bond_nominal_1[a] * 1)
            equity100real.append(equity_real_1[a] * 1 + bond_real_1[a] * 0)
            equity90real.append(equity_real_1[a] * 0.9 + bond_real_1[a] * 0.1)
            equity80real.append(equity_real_1[a] * 0.8 + bond_real_1[a] * 0.2)
            equity70real.append(equity_real_1[a] * 0.7 + bond_real_1[a] * 0.3)
            equity60real.append(equity_real_1[a] * 0.6 + bond_real_1[a] * 0.4)
            equity50real.append(equity_real_1[a] * 0.5 + bond_real_1[a] * 0.5)
            equity40real.append(equity_real_1[a] * 0.4 + bond_real_1[a] * 0.6)
            equity30real.append(equity_real_1[a] * 0.3 + bond_real_1[a] * 0.7)
            equity20real.append(equity_real_1[a] * 0.2 + bond_real_1[a] * 0.8)
            equity10real.append(equity_real_1[a] * 0.1 + bond_real_1[a] * 0.9)
            equity0real.append(equity_real_1[a] * 0 + bond_real_1[a] * 1)

        p = 3
        equity100real_three, equity90real_three, equity80real_three, equity70real_three, equity60real_three, equity50real_three, equity40real_three, equity30real_three, equity20real_three, equity10real_three, equity0real_three  = [], [], [], [], [], [], [], [], [], [], []
        start100, start90, start80, start70, start60, start50, start40, start30, start20, start10, start0 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        for a in range(len(equity100nominal) - p):
            for b in range(p):
                start100 = start100 * (1 + equity100real[a + b])
                start90 = start90 * (1 + equity90real[a + b])
                start80 = start80 * (1 + equity80real[a + b])
                start70 = start70 * (1 + equity70real[a + b])
                start60 = start60 * (1 + equity60real[a + b])
                start50 = start50 * (1 + equity50real[a + b])
                start40 = start40 * (1 + equity40real[a + b])
                start30 = start30 * (1 + equity30real[a + b])
                start20 = start20 * (1 + equity20real[a + b])
                start10 = start10 * (1 + equity10real[a + b])
                start0 = start0 * (1 + equity0real[a + b])
            equity100real_three.append((start100 ** (1 / p)) - 1)
            equity90real_three.append((start90 ** (1 / p)) - 1)
            equity80real_three.append((start80 ** (1 / p)) - 1)
            equity70real_three.append((start70 ** (1 / p)) - 1)
            equity60real_three.append((start60 ** (1 / p)) - 1)
            equity50real_three.append((start50 ** (1 / p)) - 1)
            equity40real_three.append((start40 ** (1 / p)) - 1)
            equity30real_three.append((start30 ** (1 / p)) - 1)
            equity20real_three.append((start20 ** (1 / p)) - 1)
            equity10real_three.append((start10 ** (1 / p)) - 1)
            equity0real_three.append((start0 ** (1 / p)) - 1)
            start100, start90, start80, start70, start60, start50, start40, start30, start20, start10, start0 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1

        p = 10
        equity100real_ten, equity90real_ten, equity80real_ten, equity70real_ten, equity60real_ten, equity50real_ten, equity40real_ten, equity30real_ten, equity20real_ten, equity10real_ten, equity0real_ten  = [], [], [], [], [], [], [], [], [], [], []
        start100, start90, start80, start70, start60, start50, start40, start30, start20, start10, start0 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        for a in range(len(equity100nominal) - p):
            for b in range(p):
                start100 = start100 * (1 + equity100real[a + b])
                start90 = start90 * (1 + equity90real[a + b])
                start80 = start80 * (1 + equity80real[a + b])
                start70 = start70 * (1 + equity70real[a + b])
                start60 = start60 * (1 + equity60real[a + b])
                start50 = start50 * (1 + equity50real[a + b])
                start40 = start40 * (1 + equity40real[a + b])
                start30 = start30 * (1 + equity30real[a + b])
                start20 = start20 * (1 + equity20real[a + b])
                start10 = start10 * (1 + equity10real[a + b])
                start0 = start0 * (1 + equity0real[a + b])
            equity100real_ten.append((start100 ** (1 / p)) - 1)
            equity90real_ten.append((start90 ** (1 / p)) - 1)
            equity80real_ten.append((start80 ** (1 / p)) - 1)
            equity70real_ten.append((start70 ** (1 / p)) - 1)
            equity60real_ten.append((start60 ** (1 / p)) - 1)
            equity50real_ten.append((start50 ** (1 / p)) - 1)
            equity40real_ten.append((start40 ** (1 / p)) - 1)
            equity30real_ten.append((start30 ** (1 / p)) - 1)
            equity20real_ten.append((start20 ** (1 / p)) - 1)
            equity10real_ten.append((start10 ** (1 / p)) - 1)
            equity0real_ten.append((start0 ** (1 / p)) - 1)
            start100, start90, start80, start70, start60, start50, start40, start30, start20, start10, start0 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1

        p = 20
        equity100real_twenty, equity90real_twenty, equity80real_twenty, equity70real_twenty, equity60real_twenty, equity50real_twenty, equity40real_twenty, equity30real_twenty, equity20real_twenty, equity10real_twenty, equity0real_twenty  = [], [], [], [], [], [], [], [], [], [], []
        start100, start90, start80, start70, start60, start50, start40, start30, start20, start10, start0 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        for a in range(len(equity100nominal) - p):
            for b in range(p):
                start100 = start100 * (1 + equity100real[a + b])
                start90 = start90 * (1 + equity90real[a + b])
                start80 = start80 * (1 + equity80real[a + b])
                start70 = start70 * (1 + equity70real[a + b])
                start60 = start60 * (1 + equity60real[a + b])
                start50 = start50 * (1 + equity50real[a + b])
                start40 = start40 * (1 + equity40real[a + b])
                start30 = start30 * (1 + equity30real[a + b])
                start20 = start20 * (1 + equity20real[a + b])
                start10 = start10 * (1 + equity10real[a + b])
                start0 = start0 * (1 + equity0real[a + b])
            equity100real_twenty.append((start100 ** (1 / p)) - 1)
            equity90real_twenty.append((start90 ** (1 / p)) - 1)
            equity80real_twenty.append((start80 ** (1 / p)) - 1)
            equity70real_twenty.append((start70 ** (1 / p)) - 1)
            equity60real_twenty.append((start60 ** (1 / p)) - 1)
            equity50real_twenty.append((start50 ** (1 / p)) - 1)
            equity40real_twenty.append((start40 ** (1 / p)) - 1)
            equity30real_twenty.append((start30 ** (1 / p)) - 1)
            equity20real_twenty.append((start20 ** (1 / p)) - 1)
            equity10real_twenty.append((start10 ** (1 / p)) - 1)
            equity0real_twenty.append((start0 ** (1 / p)) - 1)
            start100, start90, start80, start70, start60, start50, start40, start30, start20, start10, start0 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1

        self.returnvariance = {
        'one' : [
            {'x': np.std(equity100real_three) * 100, 'y': np.mean(equity100real_three) * 100},
            {'x': np.std(equity90real_three) * 100, 'y': np.mean(equity90real_three) * 100},
            {'x': np.std(equity80real_three) * 100, 'y': np.mean(equity80real_three) * 100},
            {'x': np.std(equity70real_three) * 100, 'y': np.mean(equity70real_three) * 100},
            {'x': np.std(equity60real_three) * 100, 'y': np.mean(equity60real_three) * 100},
            {'x': np.std(equity50real_three) * 100, 'y': np.mean(equity50real_three) * 100},
            {'x': np.std(equity40real_three) * 100, 'y': np.mean(equity40real_three) * 100},
            {'x': np.std(equity30real_three) * 100, 'y': np.mean(equity30real_three) * 100},
            {'x': np.std(equity20real_three) * 100, 'y': np.mean(equity20real_three) * 100},
            {'x': np.std(equity10real_three) * 100, 'y': np.mean(equity10real_three) * 100},
            {'x': np.std(equity0real_three) * 100, 'y': np.mean(equity0real_three) * 100},
        ],           
        'ten' : [
            {'x': np.std(equity100real_ten) * 100, 'y': np.mean(equity100real_ten) * 100},
            {'x': np.std(equity90real_ten) * 100, 'y': np.mean(equity90real_ten) * 100},
            {'x': np.std(equity80real_ten) * 100, 'y': np.mean(equity80real_ten) * 100},
            {'x': np.std(equity70real_ten) * 100, 'y': np.mean(equity70real_ten) * 100},
            {'x': np.std(equity60real_ten) * 100, 'y': np.mean(equity60real_ten) * 100},
            {'x': np.std(equity50real_ten) * 100, 'y': np.mean(equity50real_ten) * 100},
            {'x': np.std(equity40real_ten) * 100, 'y': np.mean(equity40real_ten) * 100},
            {'x': np.std(equity30real_ten) * 100, 'y': np.mean(equity30real_ten) * 100},
            {'x': np.std(equity20real_ten) * 100, 'y': np.mean(equity20real_ten) * 100},
            {'x': np.std(equity10real_ten) * 100, 'y': np.mean(equity10real_ten) * 100},
            {'x': np.std(equity0real_ten) * 100, 'y': np.mean(equity0real_ten) * 100},
        ],
        'twenty' : [
            {'x': np.std(equity100real_twenty) * 100, 'y': np.mean(equity100real_twenty) * 100},
            {'x': np.std(equity90real_twenty) * 100, 'y': np.mean(equity90real_twenty) * 100},
            {'x': np.std(equity80real_twenty) * 100, 'y': np.mean(equity80real_twenty) * 100},
            {'x': np.std(equity70real_twenty) * 100, 'y': np.mean(equity70real_twenty) * 100},
            {'x': np.std(equity60real_twenty) * 100, 'y': np.mean(equity60real_twenty) * 100},
            {'x': np.std(equity50real_twenty) * 100, 'y': np.mean(equity50real_twenty) * 100},
            {'x': np.std(equity40real_twenty) * 100, 'y': np.mean(equity40real_twenty) * 100},
            {'x': np.std(equity30real_twenty) * 100, 'y': np.mean(equity30real_twenty) * 100},
            {'x': np.std(equity20real_twenty) * 100, 'y': np.mean(equity20real_twenty) * 100},
            {'x': np.std(equity10real_twenty) * 100, 'y': np.mean(equity10real_twenty) * 100},
            {'x': np.std(equity0real_twenty) * 100, 'y': np.mean(equity0real_twenty) * 100},
        ],
        }

        # this is the historic index chart
        equity_chart = [1]
        bond_chart = [1]
        equity_index_running = 1
        bond_index_running = 1
        for a in range(len(equity_real_1)):
            equity_index_running = equity_index_running * (1 + equity_real_1[a])
            equity_chart.append(equity_index_running)
        for a in range(len(bond_real_1)):
            bond_index_running = bond_index_running * (1 + bond_real_1[a])
            bond_chart.append(bond_index_running)        


        # this is working out the 5/10/15/20/25 year rolling returns (as given by period)
        start = 1
        for a in range(len(equity_nominal_1) - period):
            for b in range(period):       
                start = start * (1 + equity_nominal_1[a + b])
            equity_nominal_5.append((start ** (1 / period)) - 1)
            start = 1

        start = 1
        for a in range(len(bond_nominal_1) - period):
            for b in range(period):       
                start = start * (1 + bond_nominal_1[a + b])
            bond_nominal_5.append((start ** (1 / period)) - 1)
            start = 1

        start = 1
        for a in range(len(index_bond_nominal_1) - period):
            for b in range(period):       
                start = start * (1 + index_bond_nominal_1[a + b])
            index_bond_nominal_5.append((start ** (1 / period)) - 1)
            start = 1

        start = 1
        for a in range(len(cpi_change_1) - period):
            for b in range(period):       
                start = start * (1 + cpi_change_1[a + b])
            cpi_change_5.append((start ** (1 / period)) - 1)
            start = 1

        start = 1
        for a in range(len(equity_real_1) - period):
            for b in range(period):       
                start = start * (1 + equity_real_1[a + b])
            equity_real_5.append((start ** (1 / period)) - 1)
            start = 1

        start = 1
        for a in range(len(bond_real_1) - period):
            for b in range(period):       
                start = start * (1 + bond_real_1[a + b])
            bond_real_5.append((start ** (1 / period)) - 1)
            start = 1

        start = 1
        for a in range(len(index_bond_real_1) - period):
            for b in range(period):       
                start = start * (1 + index_bond_real_1[a + b])
            index_bond_real_5.append((start ** (1 / period)) - 1)
            start = 1   

        start = 1   
        for a in (equity_nominal_1):
            start = start * (1 + a)
        avg_equity_nominal_1 = start ** (1 / len(equity_nominal_1)) - 1
        start = 1   
        for a in (bond_nominal_1):
            start = start * (1 + a)
        avg_bond_nominal_1 = start ** (1 / len(bond_nominal_1)) - 1
        start = 1   
        for a in (index_bond_nominal_1):
            start = start * (1 + a)
        avg_index_bond_nominal_1 = start ** (1 / len(index_bond_nominal_1)) - 1
        start = 1   
        for a in (cpi_change_1):
            start = start * (1 + a)
        avg_cpi_change_1 = start ** (1 / len(cpi_change_1)) - 1
        start = 1   
        for a in (equity_real_1):
            start = start * (1 + a)
        avg_equity_real_1 = start ** (1 / len(equity_real_1)) - 1
        start = 1   
        for a in (bond_real_1):
            start = start * (1 + a)
        avg_bond_real_1 = start ** (1 / len(bond_real_1)) - 1
        start = 1   
        for a in (index_bond_real_1):
            start = start * (1 + a)
        avg_index_bond_real_1 = start ** (1 / len(index_bond_real_1)) - 1
 
        start = 1   
        for a in (equity_nominal_5):
            start = start * (1 + a)
        avg_equity_nominal_5 = start ** (1 / len(equity_nominal_5)) - 1
        start = 1   
        for a in (bond_nominal_5):
            start = start * (1 + a)
        avg_bond_nominal_5 = start ** (1 / len(bond_nominal_5)) - 1
        start = 1   
        for a in (index_bond_nominal_5):
            start = start * (1 + a)
        avg_index_bond_nominal_5 = start ** (1 / len(index_bond_nominal_5)) - 1
        start = 1   
        for a in (cpi_change_5):
            start = start * (1 + a)
        avg_cpi_change_5 = start ** (1 / len(cpi_change_5)) - 1
        start = 1   
        for a in (equity_real_5):
            start = start * (1 + a)
        avg_equity_real_5 = start ** (1 / len(equity_real_5)) - 1
        start = 1   
        for a in (bond_real_5):
            start = start * (1 + a)
        avg_bond_real_5 = start ** (1 / len(bond_real_5)) - 1
        start = 1   
        for a in (index_bond_real_5):
            start = start * (1 + a)
        avg_index_bond_real_5 = start ** (1 / len(index_bond_real_5)) - 1

        # lastly the rolling returns are put into precentiles (0, 25th, 50th, 75th, 100th)
        self.deciles_equity_nominal_1 = [np.percentile(equity_nominal_1, i) for i in range(0, 125, 25)]
        self.deciles_bond_nominal_1 = [np.percentile(bond_nominal_1, i) for i in range(0, 125, 25)]
        self.deciles_index_bond_nominal_1 = [np.percentile(index_bond_nominal_1, i) for i in range(0, 125, 25)]
        self.deciles_cpi_change_1 = [np.percentile(cpi_change_1, i) for i in range(0, 125, 25)]
        self.avg_equity_nominal_1 = avg_equity_nominal_1
        self.avg_bond_nominal_1 = avg_bond_nominal_1
        self.avg_index_bond_nominal_1 = avg_index_bond_nominal_1
        self.avg_cpi_change_1 = avg_cpi_change_1
        self.deciles_equity_real_1 = [np.percentile(equity_real_1, i) for i in range(0, 125, 25)]
        self.deciles_bond_real_1 = [np.percentile(bond_real_1, i) for i in range(0, 125, 25)]
        self.deciles_index_bond_real_1 = [np.percentile(index_bond_real_1, i) for i in range(0, 125, 25)]
        self.avg_equity_real_1 = avg_equity_real_1
        self.avg_bond_real_1 = avg_bond_real_1
        self.avg_index_bond_real_1 = avg_index_bond_real_1

        self.deciles_equity_nominal_5 = [np.percentile(equity_nominal_5, i) for i in range(0, 125, 25)]
        self.deciles_bond_nominal_5 = [np.percentile(bond_nominal_5, i) for i in range(0, 125, 25)]
        self.deciles_index_bond_nominal_5 = [np.percentile(index_bond_nominal_5, i) for i in range(0, 125, 25)]
        self.deciles_cpi_change_5 = [np.percentile(cpi_change_5, i) for i in range(0, 125, 25)]
        self.avg_equity_nominal_5 = avg_equity_nominal_5
        self.avg_bond_nominal_5 = avg_bond_nominal_5
        self.avg_index_bond_nominal_5 = avg_index_bond_nominal_5
        self.avg_cpi_change_5 = avg_cpi_change_5
        self.deciles_equity_real_5 = [np.percentile(equity_real_5, i) for i in range(0, 125, 25)]
        self.deciles_bond_real_5 = [np.percentile(bond_real_5, i) for i in range(0, 125, 25)]
        self.deciles_index_bond_real_5 = [np.percentile(index_bond_real_5, i) for i in range(0, 125, 25)]
        self.avg_equity_real_5 = avg_equity_real_5
        self.avg_bond_real_5 = avg_bond_real_5
        self.avg_index_bond_real_5 = avg_index_bond_real_5

        self.index_bond_forward_select = index_bond_forward_select
        self.bond_forward_select = bond_forward_select
        self.index_bond_forward_select_us = index_bond_forward_select_us
        self.bond_forward_select_us = bond_forward_select_us

        self.forward_chart_labels = forward_chart_labels

        self.five = five
        self.ten = ten
        self.twenty = twenty
        self.thirty = thirty

        self.equity_chart = equity_chart
        self.bond_chart = bond_chart

