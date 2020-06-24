import spreadsheets as sp
import pandas as pd

# epidemic_data = sp.get_epidemic_data()
# df_epidemic = pd.DataFrame(epidemic_data)
# df_epidemic.columns = ['cidade', 'data', 'infectados', 'recuperados', 'obitos', 'novos']
# df_epidemic = df_epidemic.loc[::, ['cidade', 'data', 'infectados']]
# all_dates = df_epidemic[df_epidemic.cidade.eq('garanhuns')]['data']
# all_dates = list(all_dates)
all_dates = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17, 18,19,20,21,22,23,24,25,26,27,28,29,30,31]
selected_dates = all_dates[::len(all_dates)//5]
if all_dates[-1] not in selected_dates:
    selected_dates.append(all_dates[-1])
print(selected_dates)