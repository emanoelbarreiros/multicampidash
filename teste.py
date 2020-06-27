import spreadsheets as sp
import pandas as pd
import maps

g_localities = maps.load_cities_dataframe('data/localidades.csv')

city = 'garanhuns'
df = sp.get_epidemic_data()
df = pd.DataFrame(df)
df.columns = ['cidade', 'data', 'infectados', 'recuperados', 'obitos', 'novos']
df['infectados'] = pd.to_numeric(df['infectados'])
df['obitos'] = pd.to_numeric(df['obitos'])
df['novos'] = pd.to_numeric(df['novos'])
city_data = df[df.cidade == city]
ms_window_size = 3
moving_sum = city_data.iloc[:,5].rolling(ms_window_size, center=True).sum()
rho_offset = 5
rho = pd.Series([0]*rho_offset + [moving_sum.iloc[i]/moving_sum.iloc[i-rho_offset] for i in range(rho_offset,len(moving_sum))])
rho_t_window_size = 7
rho_t = rho.rolling(rho_t_window_size, min_periods=1, center=True).mean()

print(rho_t)
attack_rate_window_size = 14
attack_rate = city_data.iloc[:,5].rolling(attack_rate_window_size, min_periods=1).sum()
attack_rate = attack_rate.to_numpy() * 100000.0 / 139788

epg = rho_t.to_numpy() * attack_rate
print(epg)