import pandas as pd
from itertools import combinations
import os


def tane(df):
    fds = set()
    for col in df.columns:
        lhs = frozenset([col])
        rhs = frozenset(df.columns.difference(lhs))
        fds.add((lhs, rhs))

    while True:
        new_fds = set()
        for fd in fds:
            lhs, rhs = fd
            for i in range(1, len(lhs) + 1):
                for combination in combinations(lhs, i):
                    x = frozenset(combination)
                    y = lhs.difference(x).union(rhs)
                    if df[x.union(y)].drop_duplicates().shape[0] == df[x.union(y)].shape[0]:
                        new_fds.add((x, y))

        if not new_fds.issubset(fds):
            fds = fds.union(new_fds)
        else:
            break

    for fd in fds.copy():
        lhs, rhs = fd
        fds.remove(fd)
        for attr in lhs:
            if (frozenset([attr]), rhs) not in fds:
                fds.add((frozenset([attr]), rhs))

    return fds


folder_input = "dataset"
folder_output = "result_tane"
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)
json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.csv')]
for json_file_name in json_file_names:
    print(os.path.join(folder_input, json_file_name))
    try:
        df = pd.read_csv(os.path.join(folder_input, json_file_name), header=None, skiprows=1, on_bad_lines='skip')
        result = tane(df)
        toFlush = ""
        for x in result:
            toFlush += (", ".join(map(str, list(x[1]))) + " -> " + ",".join(map(str, list(x[0]))) + "\n")

        with open(os.path.join(folder_output, json_file_name.replace("csv", "txt")), "w") as json_file_out:
            json_file_out.write(toFlush)
    except:
        print("Errore")
