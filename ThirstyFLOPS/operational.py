
import numpy as np
import json

def get_wue(tw_c):
    s = 3
    wetBulbTemp = (tw_c*9/5)+32 # Convert Celsius to Fahrenheit
    directWue = s/(s-1)*(6e-5* wetBulbTemp**3 - 0.01 * wetBulbTemp**2 + 0.61 * wetBulbTemp - 10.4)
    return np.clip(directWue, 0.05, None)   

def get_ewf(energy_mix):
    with open('./source_ewf.json', 'r') as file:
        energy_ewf = json.load(file)
    ewf = (energy_mix['biomass'] * energy_ewf['biomass'] + \
              energy_mix['geothermal'] * energy_ewf['geothermal'] + \
                energy_mix['hydro'] * energy_ewf['hydro'] + \
                energy_mix['solar'] * energy_ewf['solar'] + \
                energy_mix['wind'] * energy_ewf['wind'] + \
                energy_mix['nuclear'] * energy_ewf['nuclear'] + \
                energy_mix['coal'] * energy_ewf['coal'] + \
                energy_mix['gas'] * energy_ewf['gas'] + \
                energy_mix['oil'] * energy_ewf['oil'])/sum(energy_mix.values())
    return ewf
     

def calculate_operational_water(config):
    """
    Calculate the operational water footprint for a given configuration.
    """
    if config['wue'] is not None:
        wue = config['wue']
    else:
        wue = get_wue(config['wetbulb'])
    
    if config['ewf'] is not None:  
        ewf = config['ewf']
    else:
        ewf =  get_ewf(config['energy_mix'])
    
    onsite_water = config['energy'] * wue * config['wsi_direct'] 
    offsite_water = config['energy'] * ewf * config['wsi_indirect'] * config['pue']
    water_intensity = wue + ewf * config['pue']
    water_intensity_wsi = wue*config['wsi_direct'] + ewf * config['pue'] * config['wsi_indirect']
    return offsite_water, onsite_water, water_intensity, water_intensity_wsi