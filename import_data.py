import pandas as pd

demand = pd.read_csv('Dataset/Demand for United States Lower 48 (region) hourly - UTC time.csv')
demand['date'] = pd.to_datetime(demand['date'])

gen_coal = pd.read_csv('Dataset/Net generation from coal for United States Lower 48 (region) hourly - UTC time.csv')
gen_coal['date'] = pd.to_datetime(gen_coal['date'])
gen_coal['Megawatthours_coal'] = gen_coal['megawatthours'].astype(float)
gen_coal = gen_coal.drop('megawatthours',axis=1)

gen_hydro = pd.read_csv('Dataset/Net generation from hydro for United States Lower 48 (region) hourly - UTC time.csv')
gen_hydro['date'] = pd.to_datetime(gen_hydro['date'])
gen_hydro['Megawatthours_hydro'] = gen_hydro['megawatthours'].astype(float)
gen_hydro = gen_hydro.drop('megawatthours',axis=1)

gen_natural_gas = pd.read_csv('Dataset/Net generation from natural gas for United States Lower 48 (region) hourly - UTC time.csv')
gen_natural_gas['date'] = pd.to_datetime(gen_natural_gas['date'])
gen_natural_gas['Megawatthours_natural_gas'] = gen_natural_gas['megawatthours'].astype(float)
gen_natural_gas = gen_natural_gas.drop('megawatthours',axis=1)

gen_nuclear = pd.read_csv('Dataset/Net generation from nuclear for United States Lower 48 (region) hourly - UTC time.csv')
gen_nuclear['date'] = pd.to_datetime(gen_nuclear['date'])
gen_nuclear['Megawatthours_nuclear'] = gen_nuclear['megawatthours'].astype(float)
gen_nuclear = gen_nuclear.drop('megawatthours',axis=1)

gen_other = pd.read_csv('Dataset/Net generation from other for United States Lower 48 (region) hourly - UTC time.csv')
gen_other['date'] = pd.to_datetime(gen_other['date'])
gen_other['Megawatthours_other'] = gen_other['megawatthours'].astype(float)
gen_other = gen_other.drop('megawatthours',axis=1)

gen_petrolium = pd.read_csv('Dataset/Net generation from petroleum for United States Lower 48 (region) hourly - UTC time.csv')
gen_petrolium['date'] = pd.to_datetime(gen_petrolium['date'])
gen_petrolium['Megawatthours_petrolium'] = gen_petrolium['megawatthours'].astype(float)
gen_petrolium = gen_petrolium.drop('megawatthours',axis=1)

gen_solar = pd.read_csv('Dataset/Net generation from solar for United States Lower 48 (region) hourly - UTC time.csv')
gen_solar['date'] = pd.to_datetime(gen_solar['date'])
gen_solar['Megawatthours_solar'] = gen_solar['megawatthours'].astype(float)
gen_solar = gen_solar.drop('megawatthours',axis=1)

gen_wind = pd.read_csv('Dataset/Net generation from wind for United States Lower 48 (region) hourly - UTC time.csv')
gen_wind['date'] = pd.to_datetime(gen_wind['date'])
gen_wind['Megawatthours_wind'] = gen_wind['megawatthours'].astype(float)
gen_wind = gen_wind.drop('megawatthours',axis=1)

dfs = [ gen_coal, gen_hydro, gen_natural_gas,
        gen_nuclear, gen_other, gen_petrolium,
          gen_solar, gen_wind]

final_df = pd.concat([df.set_index('date') for df in dfs], axis=1, join='outer')
final_df = final_df[gen_wind['date'][0]:]
demand = demand[(demand['date']>=gen_wind['date'][0]) & (demand['date']<=gen_wind['date'].values[-1])]