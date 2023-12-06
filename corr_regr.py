import pandas as pd
from scipy.stats import linregress
import os


def corr_regr(file):
    df = pd.read_csv(file, header=None, skiprows=1, on_bad_lines='skip')

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype("category").cat.codes

    corr_matrix = df.corr()
    corr = ""
    for col1 in df.columns:
        for col2 in df.columns:
            if col1 != col2 and df[col1].nunique() > 1:
                slope, intercept, r_value, p_value, std_err = linregress(df[col1], df[col2])
                if r_value > 0.8:
                    corr += (f"{col1} -> {col2}" + "\n")
    return corr


folder_input = "dataset"
folder_output = "result_corr_reg"
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)
json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.csv')]
for json_file_name in json_file_names:
    print(os.path.join(folder_input, json_file_name))
    try:
        toFlush=corr_regr(os.path.join(folder_input, json_file_name))
        with open(os.path.join(folder_output, json_file_name.replace("csv", "txt")), "w") as json_file_out:
            json_file_out.write(toFlush)
    except:
        print("Errore")