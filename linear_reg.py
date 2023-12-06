import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import os


def find_dependencies(df, threshold=0.95):
    # df = pd.DataFrame(dataset)
    columns = df.columns
    dependencies = set()

    for col in columns:
        X = df.drop([col], axis=1)
        y = df[col]

        reg = LinearRegression().fit(X, y)
        r2 = reg.score(X, y)

        if r2 >= threshold:
            lhs = tuple(X.columns)
            rhs = (col,)
            dependencies.add((lhs, rhs))

    return dependencies


def parse_object_to_int(df):
    le = preprocessing.LabelEncoder()
    for i in df.columns:
        type_col = df[i].dtype
        if type_col == 'object':
            df[i] = le.fit_transform(df[i].values)


folder_input = "dataset"
folder_output = "result_linear_reg"
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)
json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.csv')]
for json_file_name in json_file_names:
    print(os.path.join(folder_input, json_file_name))
    try:
        df = pd.read_csv(os.path.join(folder_input, json_file_name), header=None, skiprows=1, on_bad_lines='skip')
        parse_object_to_int(df)
        dep = find_dependencies(df, threshold=0.5)
        toFlush = ""
        for x in dep:
            lhs = ", ".join(map(str, x[0]))
            rhs = str(x[1][0])
            toFlush += (lhs + " -> " + rhs + "\n")
        with open(os.path.join(folder_output, json_file_name.replace("csv", "txt")), "w") as json_file_out:
            json_file_out.write(toFlush)
    except:
        print("Errore")
