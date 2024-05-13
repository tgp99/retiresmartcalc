import pandas as pd
import numpy as np
import datetime

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
        if 'flex_real_decrease' not in data_object: data_object['flex_real_decrease'] = float(1.0)
        if 'flex_real_increase' not in data_object: data_object['flex_real_increase'] = float(1.0)
        if 'years_no_flex' not in data_object: data_object['years_no_flex'] = int(1)
        if 'spring_back' not in data_object: data_object['spring_back'] = "1"
        if 'annuity_option' not in data_object: data_object['annuity_option'] = "1"
        if 'annuity_increase' not in data_object: data_object['annuity_increase'] = float(3)
        if 'annuity_price' not in data_object: data_object['annuity_price'] = float(0)
        if 'annuity_tax_rate' not in data_object: data_object['annuity_tax_rate'] = float(0)
        if 'annuity_start_year' not in data_object: data_object['annuity_start_year'] = int(1)
        if 'annual_withdrawal_inc' not in data_object: data_object['annual_withdrawal_inc'] = float(0)
        if 'fees' not in data_object: data_object['fees'] = float(0)
        if 'start_simulation_age' not in data_object: data_object['start_simulation_age'] = int(50)
        if 'annualadjust' not in data_object: data_object['annualadjust'] = [100] * 50
        if 'years' not in data_object: data_object['years'] = int(30)
        if 'circular_simulation' not in data_object: data_object['circular_simulation'] = "1"
        if 'years_contributions' not in data_object: data_object['years_contributions'] = 0
        if 'years_to_withdrawals' not in data_object: data_object['years_to_withdrawals'] = 0
        if 'contribution' not in data_object: data_object['contribution']
        if 'contribution_increase' not in data_object: data_object['contribution_increase']
        self.data_object = data_object

# Creates age_adjusted survivorship probabilities for application to withdrawal results in simulation
class SurvivorshipWeightings:
    def __init__(self, years, start_age, data_set):
        weightings = []
        for a in range(years + 1):
            age = start_age + a
            if age < 65: weightings.append(1)
            elif age > 105: weightings.append(0)
            else: weightings.append((0.5 * data_set.male[age - 65] + 0.5 * data_set.female[age - 65])/ 100)
        self.result = weightings

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
    def __init__(self, withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, year, annuity_income, annuity_tax):
        self.result = ((withdrawal_amount * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax))  / (1 - draw_tax))
        self.unadjusted_result = ((withdrawal_amount * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax)) / (1 - draw_tax))

# Calculates and returns withdrawal bonus amount (from running portfolio) for specific year in back-test cycle.  Scales amount upwards for tax costs.
class CalcBonusWithdrawal:
    def __init__(self, bonus_target, draw_adjust, annual_withdrawal_inc, draw_tax, year, annuity_income, annuity_tax):
        self.result = ((bonus_target * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year))) / (1 - draw_tax))

# Calculates and returns proportional withdrawal amount (from running portfolio) for specific year in back-test cycle.  Nets off annuity income and scales amount upwards for tax costs.
class CalcProportionalWithdrawal:
    def __init__(self, target_withdrawal_percent, draw_adjust, draw_tax, year, running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax):
        result = ((running_portfolio_value * (target_withdrawal_percent / 100) * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax)) / (1 - draw_tax))
        floor = ((min_withdrawal_floor * draw_adjust[year] * ((1 + annual_withdrawal_inc) ** (year)) - annuity_income * (1 - annuity_tax)) / (1 - draw_tax))
        self.result = max(result, floor)

# Runs back-testing cycle simulation. Takes prepared parameters and prepared return data and returns data series of results.
class RunSimulation:
    def __init__(self, equity_real, bond_real, index_bond_real, asset_mix, start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction):
        running_portfolio_value = start_sum
        end_single_cycle_portfolio_values = []
        # through_single_cycle_portfolio_values = []
        through_single_cycle_portfolio_values = [start_sum]
        all_portfolio_values_through_all_cycles = []
        through_single_cycle_withdrawals = []
        all_withdrawals_through_all_cycles = []
        all_withdrawals_through_all_cycles_mort_adjusted_discounted = []
        running_flex_withdrawal_adjustment = 1
        through_single_cycle_avg_withdrawal = []
        through_single_cycle_avg_withdrawal_mort_adjusted = []
        mortality_adjustments = SurvivorshipWeightings(years, start_simulation_age, mortality_data_pull).result
        through_single_cycle_withdrawals_mort_adjusted = []      
        through_single_cycle_withdrawals_mort_adjusted_discounted = []
        # Annuity_income_tracker_pre_purchase is scaled up to cover any tax due on the annuity income (e.g. interest income embedded in annuity return)
        annuity_income_tracker_pre_purchase = (withdrawal_amount * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
        annuity_income = 0
        simulation_fail_tag = 0
        simulation_fail_tag_through_all_cycles = []
        bonus_payment = 0
        # Below is to stop annuity option running if data_direction is 'back' (as frontend only allows annuity parameters to be changed if data_direction is 'forward').  Otherwise set annuity_percent_withdrawal to zero.
        if data_direction == "back": annuity_percent_withdrawal = 0
    
        # 'a in range' represents each back-testing cycle and 'b in range' represents each year in each cycle
        for a in range(len(equity_real) - years):
            for b in range(years):
                if annuity_start_year > (b + 1) and b > 0:
                    annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                elif annuity_start_year == (b + 1):
                    try: 
                        # The cost of the annuity which is scaled up to cover cost of deferred income tax at point of annuity purchase - this is a modelling simplification as in reality the deferred income tax will be applied to the annuity income when it is received. 
                        annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100)) / (1 - draw_tax)
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
                    min_multiple = 1 / (safest_swr_across_years[b] / 100)
                else:
                    min_multiple = 1 / (safest_swr_across_years[b - 1] / 100)

                if(dynamic_option == 'proportional'):
                    bonus = 0
                    draw = CalcProportionalWithdrawal(target_withdrawal_percent, draw_adjust, draw_tax, b, running_portfolio_value, min_withdrawal_floor, annual_withdrawal_inc, annuity_income, annuity_tax_rate).result 
                    through_single_cycle_withdrawals.append(((max(min(draw, running_portfolio_value),0)) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)))
                    
                    # Ensures simulated portfolio value can not turn negative whilst recording a fail if it would have done had the the due withdrawal been taken in full.
                    running_portfolio_value = max((running_portfolio_value - draw),0)
                    if (running_portfolio_value - draw) < 0:
                        simulation_fail_tag = 1

                    # Conditional running_portfolio_value > 0 is not whilst code stops running_portfolio_value from turning negative.
                    if data_direction == "back":
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])
                    through_single_cycle_portfolio_values.append(running_portfolio_value)
                
                else:
                    if(dynamic_option == 'constantbonus'): 
                        bonus = CalcBonusWithdrawal(bonus_target, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result
                    else:
                        bonus = 0
                    
                    # Unadjusted_draw is used for withdrawal flex and withdrawal bonus calculation.  It excludes any year by year adjustments to the withdrawal level (e.g. as % normal withdrawal level). This is used to calculate the maximum possible extra withdrawal permitted whilst remaining inside the max SWR.  The max SWR already incorporates the effect of year by year adjustments to the withdrawal level.
                    unadjusted_draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).unadjusted_result
                    if(dynamic_option == 'constantflex'):
                        if (unadjusted_draw > 0 and b >= years_no_flex):
                            # this checks whether sufficient portfolio value to flex withdrawal level upwards...
                            if(running_portfolio_value / (unadjusted_draw * running_flex_withdrawal_adjustment * (1 + flex_real_increase/100)) > min_multiple): 
                                if(spring_back == "1"):
                                    if running_flex_withdrawal_adjustment >= 1:
                                        running_flex_withdrawal_adjustment = running_flex_withdrawal_adjustment + (flex_real_increase/100)
                                        draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result * running_flex_withdrawal_adjustment
                                    else:
                                        running_flex_withdrawal_adjustment = min((running_portfolio_value / (unadjusted_draw * min_multiple)), 1)
                                        draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result * running_flex_withdrawal_adjustment
                                else:
                                    running_flex_withdrawal_adjustment = running_flex_withdrawal_adjustment + (flex_real_increase/100)
                                    draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result * running_flex_withdrawal_adjustment
                            # ...of sufficient portfolio value to maintain withdrawal level...
                            elif(running_portfolio_value / (unadjusted_draw * running_flex_withdrawal_adjustment) >= min_multiple): 
                                draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result * running_flex_withdrawal_adjustment
                            # ...otherwise this flexes withdrawal level downwards
                            else:
                                running_flex_withdrawal_adjustment = running_flex_withdrawal_adjustment - (flex_real_decrease/100)
                                draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result * running_flex_withdrawal_adjustment
                        else:
                            draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result
                    else:
                        draw = CalcConstantWithdrawal(withdrawal_amount, draw_adjust, annual_withdrawal_inc, draw_tax, b, annuity_income, annuity_tax_rate).result
                    
                    # This calculates the withdrawal recorded as part of the data output, capped by sufficient portfolio value availability to pay it.  The withdrawals are recorded net of tax, since they have been previously scaled up to include the cost of tax ('draw').
                    if(b == 0): through_single_cycle_withdrawals.append((max(min(draw, running_portfolio_value),0) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)))
                    else:
                        if(unadjusted_draw > 0):
                            if(((running_portfolio_value - draw) / unadjusted_draw) > min_multiple): 
                                bonus_payment = max(min((bonus),((running_portfolio_value - draw) - (min_multiple * unadjusted_draw))),0)
                                through_single_cycle_withdrawals.append((bonus_payment * (1 - draw_tax)) + (max(min(draw, running_portfolio_value),0) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)))
                            else: 
                                through_single_cycle_withdrawals.append((max(min(draw, running_portfolio_value),0) * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)))
                        else:
                            bonus_payment = max(min((bonus),(running_portfolio_value - draw)),0)
                            through_single_cycle_withdrawals.append((bonus_payment * (1 - draw_tax)) + (annuity_income * (1 - annuity_tax_rate)))

                    # Deduction of bonus and draw (including cost of tax) from portfolio value. Ensures simulated portfolio value can not turn negative whilst recording a fail if it would have done had the the due withdrawal been taken in full.
                    running_portfolio_value = running_portfolio_value - bonus_payment
                    running_portfolio_value = max((running_portfolio_value - draw),0)
                    if (running_portfolio_value - draw) < 0:
                        simulation_fail_tag = 1

                    # Conditional running_portfolio_value > 0 is not whilst code stops running_portfolio_value from turning negative.
                    if data_direction == "back":
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])
                    through_single_cycle_portfolio_values.append(running_portfolio_value)

                # Adjusts annuity income to keep it in real terms (e.g. if fixed type (type = "1"), then income is reduced by inflation rate)
                if annuity_option == "1":
                    annuity_income = annuity_income / (1 + cpi_change [b + a])
                elif annuity_option == "2":
                    annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_change [b + a])
                else:
                    annuity_income = annuity_income
                bonus_payment = 0

            # Survivorship adjustment (e.g. withdrawal recorded x probability of survivorship to associated age) and temporal discount (using 'real' interest rate curve)
            for a in range(years):
                through_single_cycle_withdrawals_mort_adjusted.append((through_single_cycle_withdrawals[a] * mortality_adjustments[a]))
                through_single_cycle_withdrawals_mort_adjusted_discounted.append((through_single_cycle_withdrawals[a] * mortality_adjustments[a])/((1 + ilb_spot_curve[a]) ** a))
            through_single_cycle_avg_withdrawal_mort_adjusted.append(sum(through_single_cycle_withdrawals_mort_adjusted)/len(through_single_cycle_withdrawals_mort_adjusted))
            through_single_cycle_avg_withdrawal.append(sum(through_single_cycle_withdrawals)/len(through_single_cycle_withdrawals))

            end_single_cycle_portfolio_values.append(running_portfolio_value)
            all_portfolio_values_through_all_cycles.append(through_single_cycle_portfolio_values)
            all_withdrawals_through_all_cycles.append(through_single_cycle_withdrawals)
            all_withdrawals_through_all_cycles_mort_adjusted_discounted.append(through_single_cycle_withdrawals_mort_adjusted_discounted)
            annuity_income = 0
            annuity_income_tracker_pre_purchase = (withdrawal_amount * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
            # through_single_cycle_portfolio_values = []
            through_single_cycle_portfolio_values = [start_sum]
            through_single_cycle_withdrawals = []
            through_single_cycle_withdrawals_mort_adjusted = []
            running_portfolio_value = start_sum
            running_flex_withdrawal_adjustment = 1
            simulation_fail_tag_through_all_cycles.append(simulation_fail_tag)
            simulation_fail_tag = 0

        deciles = [np.percentile(end_single_cycle_portfolio_values, i) for i in range(0, 100, 10)]
        deciles.append(max(end_single_cycle_portfolio_values))
        # deciles = []

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

        # this is just temp for testing impact of removing withdrawal distribution histogram on speed....
        # self.withdrawal_histogram_data = []
        # self.withdrawal_histogram_edges = []

        total_draw_adjusted = []
        for a in range(len(all_withdrawals_through_all_cycles_mort_adjusted_discounted)):
            total_draw_adjusted.append(sum(all_withdrawals_through_all_cycles_mort_adjusted_discounted[a]))

        self.simulation_fails = sum(simulation_fail_tag_through_all_cycles) / len(simulation_fail_tag_through_all_cycles)
        self.value_decile_data = deciles
        self.all_value_streams = all_portfolio_values_through_all_cycles
        self.all_withdrawal_streams = all_withdrawals_through_all_cycles
        self.sum_mort_adjusted_discounted_withdrawal = sum(total_draw_adjusted) / len(total_draw_adjusted)
        self.avg_withdrawal = sum(through_single_cycle_avg_withdrawal) / len(through_single_cycle_avg_withdrawal)
        self.avg_mort_adjusted_withdrawal = sum(through_single_cycle_avg_withdrawal_mort_adjusted) / len(through_single_cycle_avg_withdrawal_mort_adjusted)
        self.avg_end_value = sum(end_single_cycle_portfolio_values) / len(end_single_cycle_portfolio_values)

# Algorithm that calculates i) back-tested, zero fail safe withdrawal rate (SWR) for each seperate back-testing cycle and ii) back-tested, zero fail safe withdrawal rate (SWR) for each year through simulation (using all back-testing cycles).  Takes prepared parameters and prepared data and returns data curves.
class CalcMaxBacktestedSWRs:
    def __init__(self, equity_real, bond_real, index_bond_real, asset_mix, start_sum, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, annuity_start_year, data_direction):
                # this is to stop unwanted annuity effect happening in backward looking calc end values
        if data_direction == 'back': 
            annuity_percent_withdrawal = 0
        best_swr = []

        # Iterates through each back-testing cycle to find maximum safe withdrawal rate for each cycle.  Iterates first in 0.5% increments, then in 0.1% increments in order to accerate processing.
        for a in range(len(equity_real) - years):
            withdrawal_counter = 1.0
            while withdrawal_counter < 100:
                withdrawal = (withdrawal_counter / 100) * start_sum
                running_portfolio_value = start_sum
                annuity_income = 0
                annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
                for b in range(years):
                    if (annuity_start_year - 1) > b:
                        if b == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    elif (annuity_start_year - 1) == b:
                        try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100)) / (1 - draw_tax)
                        except: annuity_purchase_cost = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                        annuity_income = annuity_income_tracker_pre_purchase
                    if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value - (((withdrawal * draw_adjust[b] * ((1 + annual_withdrawal_inc) ** (b))) / (1 - draw_tax)) - (annuity_income * (1 + draw_tax))) 
                    if data_direction == 'back':
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])        
                    if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_change [b + a])
                    elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_change [b + a])
                    else: annuity_income = annuity_income
                if (running_portfolio_value < 0): 
                    withdrawal_counter -= 0.9
                    break
                withdrawal_counter += 1.0

            while withdrawal_counter < 100:
                withdrawal = (withdrawal_counter / 100) * start_sum
                running_portfolio_value = start_sum
                annuity_income = 0
                annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
                for b in range(years):
                    if (annuity_start_year - 1) > b:
                        if b == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                        else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    elif (annuity_start_year - 1) == b:
                        try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100)) / (1 - draw_tax)
                        except: annuity_purchase_cost = 0
                        running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                        annuity_income = annuity_income_tracker_pre_purchase
                    if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value - (((withdrawal * draw_adjust[b] * ((1 + annual_withdrawal_inc) ** (b))) / (1 - draw_tax)) - (annuity_income * (1 + draw_tax)))
                    if data_direction == 'back':
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + bond_real[b + a] * asset_mix[3] + index_bond_real[b + a] * asset_mix[4])
                    else:
                        if(running_portfolio_value > 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a] * asset_mix[0] + (bond_forward[b] - cpi[b + a]) * asset_mix[3] + index_bond_forward[b] * asset_mix[4])
                    if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_change [b + a])
                    elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_change [b + a])
                    else: annuity_income = annuity_income
                if (running_portfolio_value < 0): 
                    break
                withdrawal_counter += 0.1
            best_swr.append(withdrawal_counter - 0.1)

        safest_swr = min(best_swr)
        safest_swr_in_year = []
        safest_swr_across_years = []

        # Iterates through all back-testing cycles to find maximum safe withdrawal by year through the simulation.  Iterates in 0.1% increments until cycle fails for simulation years [max], then same again for years - 1, then years - 2 and so on.
        for c in range(years):
            for a in range(len(equity_real) - (years)):
                withdrawal_counter = 1.0
                while withdrawal_counter < 100:
                    withdrawal = (withdrawal_counter / 100) * start_sum
                    running_portfolio_value = start_sum
                    annuity_income = 0
                    annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
                    for d in range(c):
                        if d > 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    for b in range(years - c):
                        if (annuity_start_year - 1 - c) > b:
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        elif (annuity_start_year - 1 - c) == b:
                            try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100)) / (1 - draw_tax)
                            except: annuity_purchase_cost = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                            annuity_income = annuity_income_tracker_pre_purchase
                        if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - (((withdrawal * draw_adjust[b + c] * ((1 + annual_withdrawal_inc) ** (b + c))) / (1 - draw_tax)) - (annuity_income * (1 + draw_tax)))
                        if data_direction == 'back':
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + bond_real[b + a + c] * asset_mix[3] + index_bond_real[b + a + c] * asset_mix[4])
                        else:
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + (bond_forward[b + c] - cpi[b + a + c]) * asset_mix[3] + index_bond_forward[b + c] * asset_mix[4])
                        if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_change [b + a + c])
                        elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_change [b + a + c])
                        else: annuity_income = annuity_income
                    if (running_portfolio_value < 0): 
                        withdrawal_counter -= 0.9
                        break
                    withdrawal_counter += 1.0

                while withdrawal_counter < 100:
                    withdrawal = (withdrawal_counter / 100) * start_sum
                    running_portfolio_value = start_sum
                    annuity_income = 0
                    annuity_income_tracker_pre_purchase = (withdrawal * annuity_percent_withdrawal / 100) / (1 - annuity_tax_rate)
                    for d in range(c):
                        if d > 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                    for b in range(years - c):
                        if (annuity_start_year - 1 - c) > b:
                            if b == 0 and c == 0: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase
                            else: annuity_income_tracker_pre_purchase = annuity_income_tracker_pre_purchase * (1 + annual_withdrawal_inc)
                        elif (annuity_start_year - 1 - c) == b:
                            try: annuity_purchase_cost = (annuity_income_tracker_pre_purchase / (annuity_price / 100)) / (1 - draw_tax)
                            except: annuity_purchase_cost = 0
                            running_portfolio_value = running_portfolio_value - annuity_purchase_cost
                            annuity_income = annuity_income_tracker_pre_purchase
                        if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value - (((withdrawal * draw_adjust[b + c] * ((1 + annual_withdrawal_inc) ** (b + c))) / (1 - draw_tax)) - (annuity_income * (1 + draw_tax)))
                        if data_direction == 'back':
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + bond_real[b + a + c] * asset_mix[3] + index_bond_real[b + a + c] * asset_mix[4])
                        else:
                            if(running_portfolio_value >= 0): running_portfolio_value = running_portfolio_value * (1 + equity_real[b + a + c] * asset_mix[0] + (bond_forward[b + c] - cpi[b + a + c]) * asset_mix[3] + index_bond_forward[b + c] * asset_mix[4])
                        if annuity_option == "1": annuity_income = annuity_income / (1 + cpi_change [b + a + c])
                        elif annuity_option == "2": annuity_income = annuity_income * (1 + annuity_increase / 100) / (1 + cpi_change [b + a + c])
                        else: annuity_income = annuity_income
                    if (running_portfolio_value < 0): 
                        break
                    withdrawal_counter += 0.1

                safest_swr_in_year.append(withdrawal_counter - 0.1)
            safest_swr_across_years.append(min(safest_swr_in_year))
            safest_swr_in_year = []

        self.safest_swr_across_years = safest_swr_across_years
        self.best_swr = best_swr

# Algorithm that finds optimal asset mix combination for taking prepared parameter & return data set and by iterating through possible combinations (in 10% increments) and using the RunSimulation () class to test each iteration.  Returns two asset mix combinations ('max' and 'min' respectively) i) mix that returns highest expected end simulation value (for zero or lowest possible failure rate) ii) mix that has lowest real-term value volatility (for zero or lowest possible failure rate).
class OptimiseAssetMix:
    def __init__(self, equity_real, bond_real, index_bond_real, start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction):
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
        # below is here as instances of RunSimulation() in this class require it (but don't use it)
        if withdrawal_amount > 0: 
            safest_swr_across_years = [(withdrawal_amount / start_sum) * 100] * years
        else:
            safest_swr_across_years = [3] * years

        result = RunSimulation(equity_real, bond_real, index_bond_real, [equity,0,0,fixed_income_bond, inflation_linked_bond], start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction)
        best_result_max = {'equity' : equity * 100, 'fixed_income_bond' : fixed_income_bond * 100, 'inflation_linked_bond' : inflation_linked_bond * 100, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
        best_result_min = {'equity' : equity * 100, 'fixed_income_bond' : fixed_income_bond * 100, 'inflation_linked_bond' : inflation_linked_bond * 100, 'fail' : result.simulation_fails, 'avg_value' : result.avg_end_value}
        equity_weights = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for a in equity_weights:
            equity = a
            fixed_income = 100 - equity
            if data_direction == "back":
                fixed_income_bond = fixed_income
                inflation_linked_bond = 0
                result = RunSimulation(equity_real, bond_real, index_bond_real, [equity/100,0,0,fixed_income_bond/100, inflation_linked_bond/100], start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction)
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
                    result = RunSimulation(equity_real, bond_real, index_bond_real, [equity/100,0,0,fixed_income_bond/100, inflation_linked_bond/100], start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, cpi, index_bond_forward, bond_forward, draw_tax, bonus_target, safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, ilb_spot_curve, data_direction)
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

