from transformers import pipeline

rr2hrv = pipeline(model = "hubii-world/rpeaks-to-hrv-pipeline", trust_remote_code=True)

file_path = "./Example_data/RRIntervalExample.csv"

## Calculate HRV for the full file
result = rr2hrv(inputs=file_path, sampling_rate=1024)
result.head()


## Calculate HRV with rolling windows
result = rr2hrv(inputs=file_path, window_method='rolling',window_size="5m", sampling_rate=130)
result.head()