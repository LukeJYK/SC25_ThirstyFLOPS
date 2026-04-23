import json
import math
import sys
from pathlib import Path


def CPU_embodied(location, node, yield_rate, die_area, CPU_memory, IC_CPU):
    with open(f'{Path(__file__).parents[1]}/manufacture/UPW.json', 'r') as f1:
        UPW = json.load(f1)
    with open(f'{Path(__file__).parents[1]}/manufacture/EPA.json', 'r') as f2:
        EPA = json.load(f2)
    PUE = 1.2
    upw = UPW[str(node)]
    epa = EPA[str(node)]
    ewf = 0
    WUE = 0
    if location == 'GlobalFoundries':
        ewf = 2.3
        WUE = 4.52
    elif location == 'TSMC':
        ewf = 1.4
        WUE = 7
    else:
        sys.exit('Error: location not found')
    
    PCW = epa*WUE
    WPA = epa*ewf*PUE
    packaging = IC_CPU * 0.6
    memory = CPU_memory * 0.8
    return die_area/100 * (upw + PCW + WPA)/yield_rate + packaging + memory

def GPU_embodied(location, node, yield_rate, die_area, GPU_memory, IC_GPU):
    with open(f'{Path(__file__).parents[1]}/manufacture/UPW.json', 'r') as f1:
        UPW = json.load(f1)
    with open(f'{Path(__file__).parents[1]}/manufacture/EPA.json', 'r') as f2:
        EPA = json.load(f2)
    PUE = 1.2
    upw = UPW[str(node)]
    epa = EPA[str(node)]
    if location == 'GlobalFoundries ':
        ewf = 2.5
        WUE = 4.52
    elif location == 'TSMC':
        ewf = 1.4
        WUE = 7
    
    PCW = epa*WUE
    WPA = epa*ewf*PUE
    packaging = IC_GPU * 0.6
    memory = GPU_memory * 0.8
    return die_area/100 * (upw + PCW + WPA)/yield_rate + packaging + memory

def memory_embodied(DRAM_size):
    """
    Estimate the embodied water footprint for memory.
    Parameters:
    -----------
    memory_size : float
        Total memory size required (in GB) for the HPC system (DRAM+GPU).
    Returns:
    --------
    float
        Total embodied water consumption (in liters) of memory,
        based on the number of 24GB LPDDR4X  drives required.
    Notes:
    ------
    - This function assumes the use of SK hynix 24GB LPDDR4X  drives.(SK hynix Sustainability Report 2021)
    - The water per capacity (WPC) value includes packaging-related water.
    """
    
    WPC = 0.8 #L/GB
    DRAM_water_single = (24 * WPC) # 24GB
    dram_num  = math.ceil(DRAM_size/24) # 24GB
    return dram_num * DRAM_water_single

def SSD_embodied(SSD_memory):
    """
    Estimate the embodied water footprint for SSD.
    Parameters:
    -----------
    SSD_memory : float
        Total HDD storage required (in GB) for the HPC system.
    Returns:
    --------
    float
        Total embodied water consumption (in liters) for the HDD subsystem,
        based on the number of 7680g drives required.
    Notes:
    ------
    - This function assumes the use of Seagate Nytro 3331-7680g drives.
    - The water per capacity (WPC) value includes packaging-related water.
    """
    SSD_size = 7680 #in GB
    WPC = 0.0224
    SSD_water_single = (SSD_size * WPC)
    SSD_number = math.ceil(SSD_memory/SSD_size)
    return SSD_number*SSD_water_single

def HDD_embodied(HDD_memory):    
    """
    Estimate the embodied water footprint for HDD. 
    Parameters:
    -----------
    HDD_memory : float
        Total HDD storage required (in GB) for the HPC system.
    Returns:
    --------
    float
        Total embodied water consumption (in liters) for the HDD subsystem,
        based on the number of 22TB drives. You can change to any hardware.
    Notes:
    ------
    - This function assumes the use of Seagate EXOS X22 (22TB) drives.
    - The water per capacity (WPC) value includes packaging-related water.
    """
    HDD_szie = 22*1024 #in GB
    WPC = 0.03318 
    HDD_water_single = (HDD_szie * WPC)
    HDD_number = math.ceil(HDD_memory/HDD_szie) 
    return HDD_number*HDD_water_single


def HPC_embodied(
    CPU_number, GPU_numer, DRAM_size, SSD_size, HDD_size, CPU_water, GPU_water):
    return CPU_number * CPU_water + GPU_numer * GPU_water + memory_embodied(DRAM_size) + SSD_embodied(SSD_size) + HDD_embodied(HDD_size)
    
def calculate_embodied_water(config):
    """
    Calculate the embodied water footprint for a given configuration.
    """
    CPU_water_per_CPU = CPU_embodied(
        location=config["cpu_location"],
        node=config["cpu_node"],
        yield_rate=config["cpu_yield_rate"],
        die_area=config["cpu_die_area_mm2"],
        CPU_memory=config["cpu_memory_gb"],
        IC_CPU=config["cpu_ic_water_liters"]
    )
    GPU_water_per_GPU = GPU_embodied(
        location=config["gpu_location"],
        node=config["gpu_node"],
        yield_rate=config["gpu_yield_rate"],
        die_area=config["gpu_die_area_mm2"],
        GPU_memory=config["gpu_memory_gb"],
        IC_GPU=config["gpu_ic_water_liters"]
    )
    
    memory_water = memory_embodied(config["dram_size_gb"])
    ssd_water = SSD_embodied(config["ssd_size_gb"])
    hdd_water = HDD_embodied(config["hdd_size_gb"])
    
    return CPU_water_per_CPU * config["cpu_number"], GPU_water_per_GPU * config["gpu_number"], memory_water, ssd_water, hdd_water
    
    