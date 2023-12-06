import itertools
import pandas as pd
import os


def find_dependencies(dataset, min_support=0.5, max_lhs_size=2):
    num_records = float(len(dataset))
    dependencies = set()
    attribute_set = set(dataset[0])

    for lhs_size in range(1, max_lhs_size + 1):
        for lhs in itertools.combinations(attribute_set, lhs_size):
            lhs_count = {}
            for record in dataset:
                record_lhs = tuple(record[attr] for attr in lhs)
                if record_lhs in lhs_count:
                    lhs_count[record_lhs] += 1.0
                else:
                    lhs_count[record_lhs] = 1.0

            for record_lhs in lhs_count:
                support = lhs_count[record_lhs] / num_records
                if support >= min_support:
                    rhs_set = attribute_set - set(lhs)
                    for rhs_size in range(1, len(rhs_set) + 1):
                        for rhs in itertools.combinations(rhs_set, rhs_size):
                            rhs_count = {}
                            for record in dataset:
                                record_rhs = tuple(record[attr] for attr in rhs)
                                if record_lhs == tuple(record[attr] for attr in lhs) and record_rhs in rhs_count:
                                    rhs_count[record_rhs] += 1.0
                                elif record_lhs == tuple(record[attr] for attr in lhs):
                                    rhs_count[record_rhs] = 1.0

                            for record_rhs in rhs_count:
                                support_rhs = rhs_count[record_rhs] / num_records
                                confidence = support_rhs / support
                                if confidence >= min_support:
                                    dependencies.add((lhs, rhs))
    return dependencies


folder_input = "dataset"
folder_output = "result_subset_gen"
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)
json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.csv')]
for json_file_name in json_file_names:
    print(os.path.join(folder_input, json_file_name))
    df = pd.read_csv(os.path.join(folder_input, json_file_name), header=None, skiprows=1, on_bad_lines='skip')
    ls = df.values.tolist()
    colNumber = len(df.columns)
    parsed = [list(range(0, colNumber))]
    for l in ls:
        parsed.append(l)
    dep = find_dependencies(parsed, min_support=0.2, max_lhs_size=colNumber - 1)
    toFlush = ""
    for x in dep:
        lhs = ", ".join(map(str, x[0]))
        rhs = str(x[1][0])
        toFlush += (lhs + " -> " + rhs + "\n")

    with open(os.path.join(folder_output, json_file_name.replace("csv", "txt")), "w") as json_file_out:
        json_file_out.write(toFlush)
