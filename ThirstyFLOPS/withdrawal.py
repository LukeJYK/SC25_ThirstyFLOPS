


location_factor = {
    "Wetland": {
        "Description": "Natural purification benefits",
        "Factor": 0.5
    },
    "Lake / River": {
        "Description": "Neutral impact",
        "Factor": 1.0
    },
    "Wastewater Treatment Plant": {
        "Description": "Requires further treatment",
        "Factor": 1.5
    },
    "Ocean": {
        "Description": "Dilution and wide dispersion",
        "Factor": 0.7
    }
}

pollutant_factor = {
    "BOD": {
        "Description": "Biochemical Oxygen Demand",
        "HazardFactor": 1.0
    },
    "COD": {
        "Description": "Chemical Oxygen Demand",
        "HazardFactor": 1.5
    },
    "Heavy Metals": {
        "Description": "Sum of Pb, Cd, Hg, etc.",
        "HazardFactor": 5.0
    },
    "TSS": {
        "Description": "Total Suspended Solids",
        "HazardFactor": 0.8
    }
}

scarcity_factor = {
    "Potable water": {
        "Description": "High scarcity due to competition with drinking water use",
        "Factor": 0.90
    },
    "Non-potable — Recycled water": {
        "Description": "Reused water, moderate scarcity impact",
        "Factor": 0.40
    },
    "Non-potable — Rainwater harvesting": {
        "Description": "Collected naturally, very low scarcity impact",
        "Factor": 0.10
    },
    "Non-potable — Industrial reuse": {
        "Description": "Reclaimed from industrial processes, low to moderate scarcity impact",
        "Factor": 0.25
    },
    "Non-potable — Surface raw water (low quality)": {
        "Description": "Untreated surface water with limited use, low scarcity impact",
        "Factor": 0.15
    }
}



def calculate_withdrawal(water_discharge, pollutant_factor, location_factor, water_footprint, potable_factor, non_potable_factor,potable_percentage,non_potable_percentage,rho):
    adjusted_water_discharge = water_discharge * pollutant_factor * location_factor
    
    water_reuse = adjusted_water_discharge * rho
    water_withdrawal =water_footprint+adjusted_water_discharge
    
    potable_water_withdrawal = water_withdrawal * potable_percentage
    non_potable_water_withdrawal = water_withdrawal *non_potable_percentage
    
    adjusted_potable_water_withdrawal = potable_water_withdrawal * potable_factor
    adjusted_non_potable_water_withdrawal = non_potable_water_withdrawal * non_potable_factor
    
    return water_reuse, adjusted_water_discharge, adjusted_non_potable_water_withdrawal, adjusted_potable_water_withdrawal, water_withdrawal