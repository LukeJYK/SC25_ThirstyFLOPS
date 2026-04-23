import argparse
import sys
from embodied import calculate_embodied_water
from operational import calculate_operational_water

def parse_args():
    parser = argparse.ArgumentParser(description="ThirstyFLOPS: Data Center Water Footprint Calculator")


    # Embodied CPU
    parser.add_argument("--cpu_number", type=int, required=True)
    parser.add_argument("--cpu_location", type=str, required=True)
    parser.add_argument("--cpu_node", type=int, required=True)
    parser.add_argument("--cpu_yield_rate", type=float, required=True)
    parser.add_argument("--cpu_die_area_mm2", type=float, required=True)
    parser.add_argument("--cpu_memory_gb", type=float, required=True)
    parser.add_argument("--cpu_ic_water_liters", type=float, required=True)
    
    # Embodied GPU
    parser.add_argument("--gpu_number", type=int, required=True)
    parser.add_argument("--gpu_location", type=str, required=True)
    parser.add_argument("--gpu_node", type=int, required=True)
    parser.add_argument("--gpu_yield_rate", type=float, required=True)
    parser.add_argument("--gpu_die_area_mm2", type=float, required=True)
    parser.add_argument("--gpu_memory_gb", type=float, required=True)
    parser.add_argument("--gpu_ic_water_liters", type=float, required=True)
 
    #embodied memory
    parser.add_argument("--dram_size_gb", type=float, required=True)
    
    #embodied SSD
    parser.add_argument("--ssd_size_gb", type=float, required=True)
    
    #embodied HDD
    parser.add_argument("--hdd_size_gb", type=float, required=True)
    
    
    #operational parameters
    
    parser.add_argument("--wue", type=float, default=None)
    parser.add_argument("--wetbulb", type=float, default=None)
    parser.add_argument("--energy", type=float, required=True)
    parser.add_argument("--pue", type=float, required=True)
    parser.add_argument("--energy_mix", type=dict,default=None)
    parser.add_argument("--ewf", type=float, required=True)
    parser.add_argument("--wsi_direct", type=float, required=True)
    parser.add_argument("--wsi_indirect", type=float, required=True)
    
    args = parser.parse_args()

    # Enforce mutual exclusivity
    if args.wue is None and args.wetbulb is None:
        print("Error: You must provide either --wue or --wetbulb.")
        sys.exit(1)
    if args.wue is not None and args.wetbulb is not None:
        print("Error: Please provide only one of --wue or --wetbulb, not both.")
        sys.exit(1)
    
    if args.ewf is None and args.energy_mix is None:
        print("Error: You must provide either --ewf or --energy_mix.")
        sys.exit(1)
    if args.ewf is not None and args.energy_mix is not None:
        print("Error: Please provide only one of --ewf or --energy_mix, not both.")
        sys.exit(1)
    return args

def main():
    
    
    args = parse_args()


    # Calculate embodied water footprint
    embodied_config = {
        "cpu_number": args.cpu_number,
        "cpu_location": args.cpu_location,
        "cpu_node": args.cpu_node,
        "cpu_yield_rate": args.cpu_yield_rate,
        "cpu_die_area_mm2": args.cpu_die_area_mm2,
        "cpu_memory_gb": args.cpu_memory_gb,
        "cpu_ic_water_liters": args.cpu_ic_water_liters,
        
        "gpu_number": args.gpu_number,
        "gpu_location": args.gpu_location,
        "gpu_node": args.gpu_node,
        "gpu_yield_rate": args.gpu_yield_rate,
        "gpu_die_area_mm2": args.gpu_die_area_mm2,
        "gpu_memory_gb": args.gpu_memory_gb,
        "gpu_ic_water_liters": args.gpu_ic_water_liters,

        "dram_size_gb": args.dram_size_gb,
        
        "ssd_size_gb": args.ssd_size_gb,
        
        "hdd_size_gb": args.hdd_size_gb,
    }
    
    embodied_cpu, embodied_gpu, embodied_dram, embodied_ssd, embodied_hdd = calculate_embodied_water(embodied_config)
    
    
    #operational water footprint
    operational_config = {
        "wue": args.wue,
        "wetbulb": args.wetbulb,
        "energy": args.energy,
        "pue": args.pue,
        "energy_mix": args.energy_mix,
        "ewf": args.ewf,
        "wsi_direct": args.wsi_direct,
        "wsi_indirect": args.wsi_indirect
    }
    
    offsite_water, onsite_water, _,_ = calculate_operational_water(operational_config)
    embodied_water = embodied_cpu + embodied_gpu + embodied_dram + embodied_ssd + embodied_hdd
    operational_water = offsite_water + onsite_water
    return embodied_water, operational_water
    
    
if __name__ == "__main__":
    embodied, operational = main()
    print(f"Embodied Water Footprint: {embodied:.2f} liters")
    print(f"Operational Water Footprint: {operational:.2f} liters")
