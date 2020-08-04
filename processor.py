import pandas as pd
import spreadsheets as sp
from numpy import nan
import maps


def calculate_risk(epg):
    if epg > 100:
        return 'alto'
    elif 70 < epg <= 100:
        return 'moderadoalto'
    elif 30 < epg <= 70:
        return 'moderado'
    else:
        return 'baixo'


def process_epg_data(epidemic_data:pd.DataFrame, campus, localities):
    result = pd.DataFrame()
    for city in epidemic_data.cidade.unique():
        locality_id = localities.loc[localities['cidade'] == city].iloc[0].id
        inhabitants = localities.loc[localities['cidade'] == city].iloc[0].habitantes
        city_data = epidemic_data[epidemic_data.cidade == city]
        ms_window_size = 3
        moving_sum = city_data.iloc[:, 5].rolling(ms_window_size, min_periods=1, center=True).sum()
        rho_offset = 5
        rho = pd.Series([nan] * rho_offset
                        + [moving_sum.iloc[i] / moving_sum.iloc[i - rho_offset] for i in range(rho_offset, len(moving_sum))])
        rho_t_window_size = 7
        rho_t = rho.rolling(rho_t_window_size, min_periods=1, center=True).mean()

        attack_rate_window_size = 14
        attack_rate = city_data.iloc[:, 5].rolling(attack_rate_window_size, min_periods=1).sum()

        epg = rho_t.to_numpy() * attack_rate.to_numpy() * (100000.0 / inhabitants)
        city_data.loc[:, 'mm_novos'] = city_data.iloc[:, 5].rolling(window=7, min_periods=1).mean()
        city_data.loc[:, 'epg'] = epg
        city_data.loc[:, 'risk'] = city_data.epg.apply(calculate_risk)
        city_data.loc[:, 'rho_t'] = rho_t.to_numpy()
        city_data.loc[:, 'id'] = locality_id
        result = result.append(city_data)

    result.to_excel('data/dados_' + campus + '.xlsx', index=False)


# Start processing
campi = ['garanhuns', 'salgueiro', 'arcoverde']

for campus in campi:
    localities = maps.load_cities_dataframe('data/localidades.csv')
    epidemic_data = sp.get_raw_data(campus)

    process_epg_data(epidemic_data, campus, localities)
