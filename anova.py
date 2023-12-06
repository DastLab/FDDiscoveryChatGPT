import pandas as pd
from scipy.stats import f_oneway
from sklearn import preprocessing
import os


def find_dependencies(dataset, alpha=0.05):
    df = pd.DataFrame(dataset)
    columns = df.columns
    dependencies = set()

    for col1 in columns:
        for col2 in columns:
            if col1 == col2:
                continue

            groups = []
            for val in df[col2].unique():
                val_group = df[df[col2] == val][col1]
                if len(val_group) < 2:
                    continue
                groups.append(val_group)

            if len(groups) < 2:
                continue

            p_value = f_oneway(*groups).pvalue
            if p_value < alpha:
                lhs = (col2,)
                rhs = (col1,)
                dependencies.add((lhs, rhs))

    return dependencies


def parse_object_to_int(df):
    le = preprocessing.LabelEncoder()
    for i in df.columns:
        type_col = df[i].dtype
        if type_col == 'object':
            df[i] = le.fit_transform(df[i].values)


folder_input = "dataset"
folder_output = "result_anova"
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)
json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.csv')]
for json_file_name in json_file_names:
    print(os.path.join(folder_input, json_file_name))

    df = pd.read_csv(os.path.join(folder_input, json_file_name), header=None, skiprows=1, on_bad_lines='skip')
    parse_object_to_int(df)
    dep = find_dependencies(df)
    toFlush = ""
    for x in dep:
        toFlush += (", ".join(map(str, x[0])) + " -> " + str(x[1][0]) + "\n")

    with open(os.path.join(folder_output, json_file_name.replace("csv", "txt")), "w") as json_file_out:
        json_file_out.write(toFlush)


