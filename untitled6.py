# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:16:05 2024

@author: IGNAOLSZ
"""


#calculate distribution of snowpack and reservoir levels

def quantify_res_water_levels(countries):
    ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
    secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
    session = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)
    
    date_min = dt.date(day = 1, month = 1, year = 2013)
    date_max = dt.date.today() 
    data = {}
    
    for country in countries:
        
        if country == 'Switzerland':
            frcst_area = 'ch'
        if country == 'France':
            frcst_area = 'fr'
        if country == 'Italy':
            frcst_area = 'it-nord'
        if country == 'Austria':
            frcst_area = 'at'
        if country == 'Nordics':
            frcst_area = 'np'
        
        #normal levels
        curve_sgw_name = 'res '+ frcst_area +' hydro wtr gwh cet h n'
        curve_reserv_norm = session.get_curve(name=curve_sgw_name)
        wap_reserv_norm = curve_reserv_norm.get_data(data_from=date_min, data_to=date_max, function='AVERAGE', frequency='D')
        df_reserv_norm = wap_reserv_norm.to_pandas()
        
        
        #actual levels
        curve_reserv_name = 'res '+ frcst_area +' hydro wtr gwh cet h sa'
        curve_reserv = session.get_curve(name=curve_reserv_name)
        wap_reserv = curve_reserv.get_data(data_from=date_min, data_to=date_max, function='AVERAGE', frequency='D')
        df_reserv = wap_reserv.to_pandas()
        
        reserv_anom = df_reserv - df_reserv_norm
        # reserv_anom.dropna(inplace = True)
        
        df = pd.concat({'production': df_reserv,
                            'norm': df_reserv_norm,
                            'anomaly': reserv_anom},
                               axis=1).tz_localize(None)
        
        df.index.name = 'Original Date'
        df['Year'] = df.index.year
        df['Month'] = df.index.month
        df['Day'] = df.index.day
        
        # Remove leap year
        mask = (df['Day'] == 29) & (df['Month'] == 2)
        df = df[~mask].copy(deep=True)
        
        dates = pd.date_range(dt.date(day = 1, month = 1, year = 2023), dt.date(day = 31, month = 12, year = 2023))
        years = df['Year'].drop_duplicates().values
        
        df_years = pd.DataFrame(index = dates, columns= years[:-1])
        
        for year in years[:-1]:
            df_years[year] = df[df['Year']==year].production.values
        df_years['norm']=df[df['Year']==year].norm.values
        df_years['Month'] = df_years.index.month
        df_years['Day'] = df_years.index.day
        
        this_year = df[df['Year']==date_max.year].production
        this_year.index = dates[:len(this_year)]
        
        save_dir = r'P:\QFA\TonyWeather\Hydro Report\figures'
        save_name = r'\reservoir_wtr_' + country
        
        plt.figure()
        plt.plot(df_years[years[:-1]], c='grey', lw = 0.5)
        plt.plot(df_years.norm, c = 'k', lw = 2, label = 'norm')
        plt.plot(this_year, c='r', lw = 2, label = date_max.year)
        plt.legend()
        plt.grid()
        plt.title(country + ' water levels')
        plt.xlabel('date of the year')
        plt.ylabel('Accumulated GWh')
        plt.savefig(save_dir+save_name)
        
        #calculate delta from norm today and last week
        anom= round(df.anomaly.iloc[-1])
        amon_perc = round((df.iloc[-1].production/df.iloc[-1].norm)*100)
        
        anom_w = round(df.anomaly.iloc[-7])
        amon_w_perc = round((df.iloc[-7].production/df.iloc[-7].norm)*100)
        
        #calculate quantile of the distribution
        day = date_max.day
        month = date_max.month
        
        tday = df_years[(df_years['Day'] == day) & (df_years['Month'] == month)].index
        idx = np.where(dates == tday[0])[0][0]
        
        this_week_hist = df_years.iloc[idx-7:idx][years[:-1]].mean(axis = 0) 
        this_week = df.iloc[-8:].production.mean()
        
        quant_one = round(stats.percentileofscore(this_week_hist.values,this_week),1)
        
        
        # print(country)
        # print('current anomaly = {}GWh, at {}% of seasonal normal'.format(anom, amon_perc))
        # print('standing at {}th percentile of the distribution'.format(quant_one))
        # print('last week anomaly = {}GWh, at {}% of seasonal normal'.format(anom_w, amon_w_perc))
        # print('variation of {}% compared to previous week'.format(amon_perc - amon_w_perc))
        # print('*** \n')
        
        data_dict = {'climatology' : df_years, 'current_year' : this_year, 'anomaly': anom, 'anomaly_percent': amon_perc, 'anomaly_quantile': quant_one,
                     'anomaly_w-1': anom_w, 'anomaly_percent_w-1': amon_w_perc}
    
        data[country] = data_dict
        
    return data



if __name__ == '__main__':
    
    countries = ['France','Switzerland','Italy', 'Austria']

    #download data  from volue    
    data = quantify_res_water_levels(countries)
    
    fig=plt.figure(figsize=(14,10))
    columns = 2
    rows = 2
    
    for i, country in enumerate(countries):
        i = i+1
        #retrieve data from dict
        country_data = data[country]
        anom = country_data['anomaly']
        amon_perc = country_data['anomaly_percent']
        quant_one = country_data['anomaly_quantile']
        anom_w = country_data['anomaly_w-1']
        amon_w_perc = country_data['anomaly_percent_w-1']
        
        df_years = country_data['climatology']
        years = df_years.columns[:-3]
        this_year = country_data['current_year']
        
        print(country)
        print('current anomaly = {}GWh, at {}% of seasonal normal'.format(anom, amon_perc))
        print('standing at {}th percentile of the distribution'.format(quant_one))
        print('last week anomaly = {}GWh, at {}% of seasonal normal'.format(anom_w, amon_w_perc))
        print('variation of {}% compared to previous week'.format(amon_perc - amon_w_perc))
        print('*** \n')
        
        fig.add_subplot(rows, columns, i)
        plt.plot(df_years[years], c='grey', lw = 0.5)
        plt.plot(df_years.norm, c = 'k', lw = 2, label = 'norm')
        plt.plot(this_year, c='r', lw = 2, label = this_year.index.year.drop_duplicates()[-1])
        plt.legend()
        plt.grid()
        plt.title(country)
    
    plt.suptitle('Reservoir Water Level Status')
    plt.tight_layout()