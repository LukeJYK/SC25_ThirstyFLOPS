import os
import pandas as pd
script_dir = os.path.dirname(os.path.abspath(__file__))


def process_polaris():
    #process polaris data
    csv_path = os.path.join(script_dir, '..', 'HPC_logs', 'ANL-ALCF-DJC-POLARIS_20230101_20231231.csv')
    df = pd.read_csv(csv_path)
    df['START_TIMESTAMP'] = pd.to_datetime(df['START_TIMESTAMP'], errors='coerce')
    df['END_TIMESTAMP'] = pd.to_datetime(df['END_TIMESTAMP'], errors='coerce')
    df['NODES_USED'] = pd.to_numeric(df['NODES_USED'], errors='coerce')
    total_nodes = 560
    start_date = pd.Timestamp('2023-01-01 00:00:00')
    end_date = pd.Timestamp('2023-12-31 23:59:59')
    df = df[(df['END_TIMESTAMP'] >= start_date) & (df['START_TIMESTAMP'] <= end_date)]
    start_events = df.groupby('START_TIMESTAMP')['NODES_USED'].sum()
    end_events = df.groupby('END_TIMESTAMP')['NODES_USED'].sum()
    events = pd.concat([start_events, -end_events]).groupby(level=0).sum().sort_index()
    usage = events.cumsum() 
    timeline = pd.date_range(start='2023-01-01 00:00:00', end='2023-12-31 23:59:59', freq='10T')
    usage_timeline = usage.reindex(timeline, method='ffill').fillna(0)
    utilization = usage_timeline / total_nodes
    daily_utilization = utilization.groupby(utilization.index.date).mean()
    daily_utilization.index = pd.to_datetime(daily_utilization.index)
    save_path = os.path.join(script_dir, '..', 'HPC_util_power', 'polaris_util.txt')
    with open(save_path, "w") as f:
        for value in daily_utilization:
            f.write(f"{value:.4f}\n")

def process_frontier():
    energy_path = os.path.join(script_dir, '..', 'HPC_logs', 'frontier_energy.txt')
    time_path = os.path.join(script_dir, '..', 'HPC_logs', 'frontier_time.txt')
    with open(energy_path, "r") as f:
        energy_lines = f.readlines()
    energy_values = [float(line.strip()) for line in energy_lines]
    with open(time_path, "r") as f:
        time_lines = f.readlines()
    time_values = [line.strip() for line in time_lines]
    df = pd.DataFrame({"timestamp": time_values, "energy": energy_values})

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%m/%d/%y %H:%M")
    df["date"] = df["timestamp"].dt.date
    daily_avg = df.groupby("date")["energy"].mean()
    save_path = os.path.join(script_dir, '..', 'HPC_util_power', 'frontier_energy.txt')
    with open(save_path, "w") as f:
        for day, avg in daily_avg.items():
            f.write(f"{avg:.4f}\n")
            
def process_fugaku():
    log_path = os.path.join(script_dir, '..', 'HPC_logs', 'sysusage.csv')
    df = pd.read_csv(log_path, parse_dates=['sdt'])
    df['sdt'] = pd.to_datetime(df['sdt'], utc=True)
    df['edt'] = pd.to_datetime(df['edt'], utc=True)
    start_date = pd.Timestamp('2023-01-01', tz='UTC')
    end_date = pd.Timestamp('2023-12-31 23:59:59', tz='UTC')
    df = df[(df['sdt'] >= start_date) & (df['sdt'] <= end_date)]
    df['sdt_day'] = df['sdt'].dt.floor('D')
    econm_by_day = df.groupby('sdt_day')['econm'].sum()
    nnuma_by_day = df.groupby('sdt_day')['nnuma'].mean()

    full_days = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D', tz='UTC')
    econm_by_day = econm_by_day.reindex(full_days, fill_value=0)
    nnuma_by_day = nnuma_by_day.reindex(full_days, fill_value=0)
    save_path = os.path.join(script_dir, '..', 'HPC_util_power', 'fugaku_energy.txt')
    with open(save_path, "w") as f:
        for value in econm_by_day:
            f.write(f"{value:.4f}\n")
    
def process_marconi():
    import shutil
    log_path = os.path.join(script_dir, '..', 'HPC_logs', 'marconi_util.txt')
    destination_path = os.path.join(script_dir, '..', 'HPC_util_power', 'marconi_util.txt')
    shutil.copyfile(log_path, destination_path)
process_polaris()
process_frontier()
process_fugaku()
process_marconi()
print("Data processing completed successfully.")