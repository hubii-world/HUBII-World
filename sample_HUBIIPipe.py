from transformers import pipeline
import pandas as pd

input_file_path = "./Example_data/TestData_2.csv"
output_file_path = "./output.csv"

print("load pipe")
rr2hrv = pipeline(model = "hubii-world/rpeaks-to-hrv-pipeline", trust_remote_code=True)


print("calculate data")
## Calculate HRV for the full file
result = rr2hrv(inputs=input_file_path, sampling_rate=130)
result.to_csv(output_file_path)
print(result.head())

## Calculate HRV with rolling windows
result = rr2hrv(inputs=input_file_path, window_method='rolling',window_size="5m", sampling_rate=130)
result.to_csv(output_file_path)
print(result.head())