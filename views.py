from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from rest_framework import status
import json
import pandas as pd
from . classes import AddDefaultData, LoadHistoricData, PrepareHistoricDataSet, RetrieveHistoricData, RetrieveForwardData, RetrieveMortalityData, LoadForwardData, PrepareForwardDataSet, PrepareReturnData, RunSimulation, AnalyseHistoricData, OptimiseAssetMix, CalcMaxBacktestedSWRs, ReverseArray, PrepareMortalityDataSet
from . serializers import UserSerializer, HistoricDataAnalysisSerializer
from django.http import HttpResponse, HttpResponseNotFound
import os
from django.views import View
from django.conf import settings
from django.http import FileResponse

@api_view(['GET'])
def get_simulation_data(request):

    # This view returns a JSON object containing three data directories - historic asset return data, forward asset return data and mortality data.  These can then be used in the 'simulation' view below.

    historic_data = RetrieveHistoricData(pd.read_csv('staticfiles/historic_dataset.csv'))
    forward_data = RetrieveForwardData(pd.read_csv('staticfiles/forward_dataset.csv'))
    mortality_data = RetrieveMortalityData(pd.read_csv('staticfiles/mortality_risk_table.csv'))
    
    return Response({
        'historic_dataset': {
        'globaleq': historic_data.globaleq,
        'useq': historic_data.useq,
        'tengilt': historic_data.tengilt,
        'ukcpi': historic_data.ukcpi,
        'gbpusd': historic_data.gbpusd,
        'year': historic_data.year,
        'tentsy': historic_data.tentsy,
        'uscpi': historic_data.uscpi,
        'usdusd': historic_data.usdusd,
        },
        'forward_dataset': {
        'gbp_index_bond_forward': forward_data.gbp_index_bond_forward,
        'gbp_bond_forward': forward_data.gbp_bond_forward,
        'usd_index_bond_forward': forward_data.usd_index_bond_forward,
        'usd_bond_forward': forward_data.usd_bond_forward,
        'update_date': forward_data.update_date,
        },
        'mortality_dataset': {
        'male': mortality_data.male,
        'female': mortality_data.female,
        'joint': mortality_data.joint,
        },
    });

@api_view(['POST'])
def simulation(request):

    # 'AddDefaultData' class checks the JSON object in the body of the POST request for missing key:value pairs and adds a default pairs as required.  'UserSerializer' executes back-end validation on the JSON object and will return an error if the validation fails. 

    pre_serializer_data = AddDefaultData(json.loads(request.body))
    serializer = UserSerializer(data = pre_serializer_data.data_object)

    if serializer.is_valid():
        data = serializer.data
        historic_asset_return_data = data.get('historic_asset_return_data')
        forward_asset_return_data = data.get('forward_asset_return_data')
        mortality_data = data.get('mortality_data')
        data_start_year = data.get('data_start_year')
        data_end_year = data.get('data_end_year')
        currency_set = data.get('currency_set')
        geographic_set = data.get('geographic_set')
        data_direction = data.get('data_direction')

        historic_data_set = PrepareHistoricDataSet(historic_asset_return_data, data_start_year, data_end_year, currency_set, geographic_set)
        mortality_data_pull = PrepareMortalityDataSet(mortality_data)
        forward_data_set = PrepareForwardDataSet(forward_asset_return_data, currency_set) 

        equity_tax = float(data.get('equity_tax'))/100
        fees = float(data.get('fees'))/10000
        bond_tax = float(data.get('bond_tax'))/100
        draw_tax = float(data.get('draw_tax'))/100
        bond_coupon = float(data.get('bond_coupon'))
        index_bond_coupon = float(data.get('index_bond_coupon'))
        # asset_mix has capacity for 5 different asset classes but currently only (equity, 0, 0, conventional bonds, index linked bonds) at used
        asset_mix_sum = float(data.get('asset_mix_equity')) + float(data.get('asset_mix_bond')) + float(data.get('asset_mix_index_bond'))
        asset_mix = [float(data.get('asset_mix_equity'))/asset_mix_sum,0,0,float(data.get('asset_mix_bond'))/asset_mix_sum,float(data.get('asset_mix_index_bond'))/asset_mix_sum]
        annuity_percent_withdrawal = float(data.get('annuity_percent_withdrawal'))
        annuity_price = float(data.get('annuity_price'))
        annuity_option = data.get('annuity_option')
        annuity_increase = float(data.get('annuity_increase'))
        annuity_tax_rate = float(data.get('annuity_tax_rate')/100)
        annuity_start_year = int(data.get('annuity_start_year'))
        start_sum = float(data.get('start_sum'))
        withdrawal_amount = float(data.get('withdrawal_amount'))
        bonus_target = float(data.get('bonus_target'))
        dynamic_option = data.get('dynamic_option')
        target_withdrawal_percent = float(data.get('target_withdrawal_percent'))
        min_withdrawal_floor = float(data.get('min_withdrawal_floor'))
        flex_real_decrease = float(data.get('flex_real_decrease'))
        flex_real_increase = float(data.get('flex_real_increase'))
        years_no_flex = float(data.get('years_no_flex'))
        spring_back = data.get('spring_back')
        start_simulation_age = int(data.get('start_simulation_age'))
        annual_withdrawal_inc = float(data.get('annual_withdrawal_inc')/100)
        years = int(data.get('years'))
        annual_adjust = data.get('annualadjust')
        circular_simulation = data.get('circular_simulation')
        years_contributions = data.get('years_contributions')
        years_to_withdrawals = data.get('years_to_withdrawals')
        contribution =data.get('contribution')
        contribution_increase = data.get('contribution_increase')
        draw_adjust = []
        for a in range(len(annual_adjust)):
            draw_adjust.append(float(annual_adjust[a])/100)

        # PrepareReturnData calculates asset returns on a annual percentage basis in real terms and with net of asset return taxation ready for use in CalcMaxBacktestedSWRs and RunSimulation
        return_data_set = PrepareReturnData(historic_data_set.historic_equity, historic_data_set.historic_bond, historic_data_set.historic_index_bond, historic_data_set.historic_cpi, historic_data_set.historic_fx, equity_tax, bond_tax, bond_coupon, index_bond_coupon, forward_data_set.forward_index_bond, forward_data_set.forward_bond, fees, circular_simulation)
        
        # CalcMaxBacktestedSWRs contains an algorithm that produces a curve of max back-tested zero-failure SWRs for the portfolio through the simulation years. This is used in RunSimulation in dynamically setting the withdrawal flex and withdrawal bonus.
        backtest_swr = CalcMaxBacktestedSWRs(return_data_set.historic_equity_real, return_data_set.historic_bond_real, return_data_set.historic_index_bond_real, asset_mix, start_sum, years, annual_withdrawal_inc, draw_adjust, return_data_set.cpi_change, return_data_set.forward_index_bond_taxed, return_data_set.forward_bond_taxed, draw_tax, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, return_data_set.cpi_change, annuity_percent_withdrawal, annuity_start_year, data_direction) 
        
        # RunSimulation runs the core model simulation.  ReverseArray transposes the structure of the results to prepare for presentation in the front end.
        simulation_results = RunSimulation(return_data_set.historic_equity_real, return_data_set.historic_bond_real, return_data_set.historic_index_bond_real, asset_mix, start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, return_data_set.cpi_change, return_data_set.forward_index_bond_taxed, return_data_set.forward_bond_taxed, draw_tax, bonus_target, backtest_swr.safest_swr_across_years, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, return_data_set.cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, return_data_set.forward_index_bond_spot_curve, data_direction) 
        transposed_simulation_results = ReverseArray(simulation_results.all_withdrawal_streams)
        
        if circular_simulation == "1":
            simulation_years  = historic_data_set.years
        else:
            simulation_years = historic_data_set.years[1:-years]

        return Response({
            'simulation_fails': simulation_results.simulation_fails,
            'value_decile_data': simulation_results.value_decile_data,
            'all_value_streams': simulation_results.all_value_streams,
            'all_withdrawal_streams' : simulation_results.all_withdrawal_streams,
            'all_withdrawal_streams_transposed' : transposed_simulation_results.data_set,
            'max_zero_fail_SWR_by_cycle' : backtest_swr.best_swr,
            'max_SWR_by_simulation_year' : backtest_swr.safest_swr_across_years,
            'simulation_years' : simulation_years,
            'withdrawal_histogram_data' : simulation_results.withdrawal_histogram_data,
            'withdrawal_histogram_edges' : simulation_results.withdrawal_histogram_edges,  
            'avg_withdrawal' : simulation_results.avg_withdrawal,
            'avg_mort_adjusted_withdrawal' : simulation_results.avg_mort_adjusted_withdrawal,
            'sum_mort_adjusted_discounted_withdrawal' : simulation_results.sum_mort_adjusted_discounted_withdrawal,
            })

    else:
        errors = serializer.errors
        return Response(errors)

@api_view(['POST'])
def asset_mix_optimisation(request):

    # 'AddDefaultData' class checks the JSON object in the body of the POST request for missing key:value pairs and adds a default pairs as required.  'UserSerializer' executes back-end validation on the JSON object and will return an error if the validation fails. 

    pre_serializer_data = AddDefaultData(json.loads(request.body))
    serializer = UserSerializer(data = pre_serializer_data.data_object)

    if serializer.is_valid():
        data = serializer.data
        historic_asset_return_data = data.get('historic_asset_return_data')
        forward_asset_return_data = data.get('forward_asset_return_data')
        mortality_data = data.get('mortality_data')
        data_start_year = data.get('data_start_year')
        data_end_year = data.get('data_end_year')
        currency_set = data.get('currency_set')
        geographic_set = data.get('geographic_set')
        data_direction = data.get('data_direction')

        # PrepareHistoricDataSet and PrepareForwardDataSet take the appropriate sub-datasets from the master-dataset given the desired back-testing dataset configuration

        historic_data_set = PrepareHistoricDataSet(historic_asset_return_data, data_start_year, data_end_year, currency_set, geographic_set)
        mortality_data_pull = PrepareMortalityDataSet(mortality_data)
        forward_data_set = PrepareForwardDataSet(forward_asset_return_data, currency_set)     

        equity_tax = float(data.get('equity_tax'))/100
        fees = float(data.get('fees'))/10000
        bond_tax = float(data.get('bond_tax'))/100
        draw_tax = float(data.get('draw_tax'))/100
        bond_coupon = float(data.get('bond_coupon'))
        index_bond_coupon = float(data.get('index_bond_coupon'))
        annuity_percent_withdrawal = float(data.get('annuity_percent_withdrawal'))
        annuity_price = float(data.get('annuity_price'))
        annuity_option = data.get('annuity_option')
        annuity_increase = float(data.get('annuity_increase'))
        annuity_tax_rate = float(data.get('annuity_tax_rate')/100)
        annuity_start_year = int(data.get('annuity_start_year'))
        start_sum = float(data.get('start_sum'))
        withdrawal_amount = float(data.get('withdrawal_amount'))
        dynamic_option = data.get('dynamic_option')
        target_withdrawal_percent = float(data.get('target_withdrawal_percent'))
        min_withdrawal_floor = float(data.get('min_withdrawal_floor'))
        flex_real_decrease = float(data.get('flex_real_decrease'))
        flex_real_increase = float(data.get('flex_real_increase'))
        years_no_flex = float(data.get('years_no_flex'))
        spring_back = data.get('spring_back')
        start_simulation_age = int(data.get('start_simulation_age'))
        annual_withdrawal_inc = float(data.get('annual_withdrawal_inc')/100)
        years = int(data.get('years'))
        annual_adjust = data.get('annualadjust')
        circular_simulation = data.get('circular_simulation')
        draw_adjust = []
        years_contributions = data.get('years_contributions')
        years_to_withdrawals = data.get('years_to_withdrawals')
        contribution =data.get('contribution')
        contribution_increase = data.get('contribution_increase')
        for a in range(len(annual_adjust)):
            draw_adjust.append(float(annual_adjust[a])/100)

        # PrepareReturnData calculates asset returns on a annual percentage basis in real terms and with net of asset return taxation ready for use in CalcMaxBacktestedSWRs and RunSimulation
        return_data_set = PrepareReturnData(historic_data_set.historic_equity, historic_data_set.historic_bond, historic_data_set.historic_index_bond, historic_data_set.historic_cpi, historic_data_set.historic_fx, equity_tax, bond_tax, bond_coupon, index_bond_coupon, forward_data_set.forward_index_bond, forward_data_set.forward_bond, fees, circular_simulation)
        
        # OptimiseAssetMix runs an algorithm to find the optimal asset allocation weightings given the parameterisation of the portfolio
        optimise = OptimiseAssetMix(return_data_set.historic_equity_real, return_data_set.historic_bond_real, return_data_set.historic_index_bond_real, start_sum, withdrawal_amount, years, annual_withdrawal_inc, draw_adjust, return_data_set.cpi_change, return_data_set.forward_index_bond_taxed, return_data_set.forward_bond_taxed, draw_tax, dynamic_option, target_withdrawal_percent, min_withdrawal_floor, flex_real_decrease, flex_real_increase, years_no_flex, spring_back, annuity_option, annuity_increase, annuity_price, annuity_tax_rate, return_data_set.cpi_change, annuity_percent_withdrawal, start_simulation_age, annuity_start_year, mortality_data_pull, return_data_set.forward_index_bond_spot_curve, data_direction)
        return Response({
            'optimised_bond_max' : optimise.optimised_fixedincome_max,
            'optimised_index_bond_max' : optimise.optimised_indexlinked_max,
            'optimised_equity_max' : optimise.optimised_equity_max,
            'optimised_failure_max' : optimise.optimised_failure_max,
            'optimised_bond_min' : optimise.optimised_fixedincome_min,
            'optimised_index_bond_min' : optimise.optimised_indexlinked_min,
            'optimised_equity_min' : optimise.optimised_equity_min,
            'optimised_failure_min' : optimise.optimised_failure_min,
            })

    else:
        errors = serializer.errors
        return Response(errors)

@api_view(['POST'])
def historics(request):
    serializer = HistoricDataAnalysisSerializer(data = json.loads(request.body))
    if serializer.is_valid():
        data = json.loads(request.body)
        historic_data_set = LoadHistoricData(pd.read_csv('staticfiles/historic_dataset.csv'), data.get('data_start_year'), data.get('data_end_year'), data.get('currency_set'), data.get('geographic_set'))
        forward_data_set = LoadForwardData(pd.read_csv('staticfiles/forward_dataset.csv'), 'GBP')    
        forward_data_set_us = LoadForwardData(pd.read_csv('staticfiles/forward_dataset.csv'), 'USD')

        bond_coupon = float(data.get('bond_coupon'))/100
        index_bond_coupon = float(data.get('index_bond_coupon'))/100
        period = int(data.get('period'))
        data_set = AnalyseHistoricData(historic_data_set.historic_equity, historic_data_set.historic_bond, historic_data_set.historic_index_bond, historic_data_set.historic_cpi, historic_data_set.historic_fx, bond_coupon, index_bond_coupon, period, forward_data_set.forward_index_bond, forward_data_set.forward_bond, forward_data_set_us.forward_index_bond, forward_data_set_us.forward_bond)
        return Response({
            'deciles_equity_nominal_1': data_set.deciles_equity_nominal_1,
            'deciles_bond_nominal_1' : data_set.deciles_bond_nominal_1,
            'deciles_index_bond_nominal_1' : data_set.deciles_index_bond_nominal_1,
            'deciles_cpi_change_1' : data_set.deciles_cpi_change_1,
            'avg_equity_nominal_1': data_set.avg_equity_nominal_1,
            'avg_bond_nominal_1' : data_set.avg_bond_nominal_1,
            'avg_index_bond_nominal_1' : data_set.avg_index_bond_nominal_1,
            'avg_cpi_change_1' : data_set.avg_cpi_change_1,
            'deciles_equity_real_1': data_set.deciles_equity_real_1,
            'deciles_bond_real_1' : data_set.deciles_bond_real_1,
            'deciles_index_bond_real_1' : data_set.deciles_index_bond_real_1,
            'avg_equity_real_1': data_set.avg_equity_real_1,
            'avg_bond_real_1' : data_set.avg_bond_real_1,
            'avg_index_bond_real_1' : data_set.avg_index_bond_real_1,
            'deciles_equity_nominal_5': data_set.deciles_equity_nominal_5,
            'deciles_bond_nominal_5' : data_set.deciles_bond_nominal_5,
            'deciles_index_bond_nominal_5' : data_set.deciles_index_bond_nominal_5,
            'deciles_cpi_change_5' : data_set.deciles_cpi_change_5,
            'avg_equity_nominal_5': data_set.avg_equity_nominal_5,
            'avg_bond_nominal_5' : data_set.avg_bond_nominal_5,
            'avg_index_bond_nominal_5' : data_set.avg_index_bond_nominal_5,
            'avg_cpi_change_5' : data_set.avg_cpi_change_5,
            'deciles_equity_real_5': data_set.deciles_equity_real_5,
            'deciles_bond_real_5' : data_set.deciles_bond_real_5,
            'deciles_index_bond_real_5' : data_set.deciles_index_bond_real_5,
            'avg_equity_real_5': data_set.avg_equity_real_5,
            'avg_bond_real_5' : data_set.avg_bond_real_5,
            'avg_index_bond_real_5' : data_set.avg_index_bond_real_5,
            'index_bond_forward_select' : data_set.index_bond_forward_select,
            'bond_forward_select' : data_set.bond_forward_select,
            'index_bond_forward_select_us' : data_set.index_bond_forward_select_us,
            'bond_forward_select_us' : data_set.bond_forward_select_us,
            'forward_chart_labels' : data_set.forward_chart_labels,
            'update_date' : forward_data_set.update_date,
            'years' : historic_data_set.years[1:], 
            'five' : data_set.five,
            'ten' : data_set.ten,
            'twenty' : data_set.twenty,
            'thirty' : data_set.thirty,
            'equity_chart' : data_set.equity_chart,
            'bond_chart' : data_set.bond_chart,
        })
    else:
        errors = serializer.errors
        return Response(errors)

# Below views support front end functionality and are not part of the simulation model code

@api_view(['GET', 'POST'])
def testapi(request):
    
    headers = request.headers
    if request.method == 'GET':
        return Response({
            'message': 'GET',
            'headers': headers
            })

    if request.method == 'POST':
        return Response({
            'message': 'POST',
            'headers': headers
            })

def sitemap(request):
    with open('sitemap.xml', 'r') as f:
        content = f.read()
    return HttpResponse(content, content_type='application/xml')

def logo(request):
    logo_path = os.path.join(settings.BASE_DIR, 'staticfiles/', 'logo.png')
    if os.path.exists(logo_path):
        response = HttpResponse(open(logo_path, 'rb').read(), content_type='image/png')
        return response
    else:
        return HttpResponse(status=404)

def excel_download(request):
    excel_file_path = os.path.join(settings.BASE_DIR, 'staticfiles/', 'RetireSmartCalc_DataFile.xlsx')
    if os.path.exists(excel_file_path):
        return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        return FileResponse(status=404)


def historic_csv_download(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'staticfiles/', 'historic_dataset.csv')
    if os.path.exists(csv_file_path):
        return FileResponse(open(csv_file_path, 'rb'), content_type='text/csv')
    else:
        return FileResponse(status=404)

def forward_csv_download(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'staticfiles/', 'forward_dataset.csv')
    if os.path.exists(csv_file_path):
        return FileResponse(open(csv_file_path, 'rb'), content_type='text/csv')
    else:
        return FileResponse(status=404)

def mortality_csv_download(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'staticfiles/', 'mortality_risk_table.csv')
    if os.path.exists(csv_file_path):
        return FileResponse(open(csv_file_path, 'rb'), content_type='text/csv')
    else:
        return FileResponse(status=404)

def documentation_download(request):
    pdf_file_path = os.path.join(settings.BASE_DIR, 'staticfiles/', 'RetireSmartCalc_Methodology_Document.pdf')
    if os.path.exists(pdf_file_path):
        return FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
    else:
        return FileResponse(status=404)

class Assets(View):
    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'static', filename)
        if os.path.isfile(path):
            with open(path, 'rb') as file:
                return HttpResponse(file.read(), content_type='application/javascript')
        else:
            return HttpResponseNotFound()
