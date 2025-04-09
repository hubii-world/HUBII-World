import pandas as pd
import neurokit2 as nk


# Variables
input_file_path = "C://Biosignal_Analysis//data//HubiiRec_HR_Testdata_Large.csv" # Path to the datafile
output_file_path = "C://Biosignal_Analysis//data//HRV_Features.csv"
window_length = 50  # Number of rows per window
step_size = 10  # Step size for sliding
sampling_rate = 130 # Sampling rate o fhte hr sensor

# Load data
#df = pd.read_csv(file_path, sep=';')
df = pd.read_csv(input_file_path, sep=',')

# Convert SystemTime to datetime
df["SystemTime"] = pd.to_datetime(df["SystemTime"], errors="coerce")

# Convert SystemTime to numeric timestamp (in seconds)
df["Timestamp"] = df["SystemTime"].astype("int64") // 1e9

# Convert "rr (ms)" to float (handling comma separators)
#df["rr (ms)"] = pd.to_numeric(df["rr (ms)"].str.replace(",", "."), errors="coerce")

# Function to generate sliding windows
def generate_sliding_windows(data, window_length, step_size):
    windows = []
    for start in range(0, len(data) - window_length + 1, step_size):
        end = start + window_length
        windows.append(data.iloc[start:end])
    return windows



# Generate sliding windows
windows = generate_sliding_windows(df, window_length, step_size)

# Process each window and compute HRV features
hrv_results = []
timestamps_start = []
timestamps_end = []

for window in windows:
    rr_intervals = window["interbeat_interval"].dropna().values  # Remove NaN values

    if len(rr_intervals) > 1:  # Ensure at least two RR intervals for HRV calculation
        try:
            r_peaks = nk.intervals_to_peaks(rr_intervals, sampling_rate=sampling_rate)
            hrv_features = nk.hrv_time(r_peaks, sampling_rate=sampling_rate)  # Sampling rate = 1000Hz (RR is in ms)
            hrv_results.append(hrv_features)
            timestamps_start.append(window["SystemTime"].min())  # Store min timestamp of window
            timestamps_end.append(window["SystemTime"].max())  # Store max timestamp of window
        except Exception as e:
            print(f"Error processing HRV for window starting at {window['SystemTime'].min()}: {e}")

# Combine results into a single dataframe
if hrv_results:
    hrv_df = pd.concat(hrv_results, ignore_index=True)
    hrv_df["timestamp_start"] = timestamps_start
    hrv_df["timestamp_end"] = timestamps_end

    # Save the results to a CSV file
    hrv_df.to_csv(output_file_path, sep=',', index=False)

    print(f"HRV features saved to {output_file_path}")
else:
    print("No valid HRV data was computed.")

# Print dataframe info for debugging
print(df.info())

