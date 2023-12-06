import pandas as pd
import os


def find_dependencies(csv_file):
    df = pd.read_csv(csv_file, header=None, skiprows=1, on_bad_lines='skip')

    dependencies = {}

    for col1 in df.columns:
        for col2 in df.columns:
            if col1 == col2:
                continue

            is_functional_dependency = True
            for i, row in df.iterrows():
                subset = df.loc[df[col1] == row[col1]]

                if len(subset[col2].unique()) > 1:
                    is_functional_dependency = False
                    break

            if is_functional_dependency:
                if col1 not in dependencies:
                    dependencies[col1] = set()
                dependencies[col1].add(col2)

    return dependencies


folder_input = "dataset"
folder_output = "result_terzo"
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)
json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.csv')]
for json_file_name in json_file_names:
    print(os.path.join(folder_input, json_file_name))
    try:
        result = find_dependencies(os.path.join(folder_input, json_file_name))
        toFlush = ""
        for key, value in result.items():
            for y in value:
                toFlush += (str(key) + " -> " + str(y) + "\n")


        with open(os.path.join(folder_output, json_file_name.replace("csv", "txt")), "w") as json_file_out:
            json_file_out.write(toFlush)
    except Exception as e:
        print(e)
        print("Errore")