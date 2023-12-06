import pandas as pd
from itertools import combinations
from sklearn import preprocessing
import os


def parse_object_to_int(df):
    le = preprocessing.LabelEncoder()
    for i in df.columns:
        type_col = df[i].dtype
        if type_col == 'object':
            df[i] = le.fit_transform(df[i].values)


def find_dependencies(dataset, min_support=0.1, min_confidence=0.8):
    # df = pd.DataFrame(dataset)
    df = dataset

    all_attributes = set(df.columns)

    attribute_support = {}
    for attribute in all_attributes:
        attribute_support[frozenset([attribute])] = df[attribute].sum() / len(df)

    frequent_itemsets = [frozenset([attribute]) for attribute in all_attributes
                         if attribute_support[frozenset([attribute])] >= min_support]

    k = 2
    while len(frequent_itemsets) > 0:
        candidate_itemsets = set(combinations(all_attributes, k))

        candidate_support = {}
        for itemset in candidate_itemsets:
            itemset_support = df[list(itemset)].all(axis=1).sum() / len(df)
            candidate_support[frozenset(itemset)] = itemset_support

        frequent_itemsets_k = [itemset for itemset in candidate_itemsets
                               if candidate_support[frozenset(itemset)] >= min_support]

        for itemset in frequent_itemsets_k:
            for i in range(1, len(itemset)):
                itemset = set(itemset)
                lhs = set(combinations(itemset, i))
                for left in lhs:
                    right = frozenset(itemset - set(left))
                    if frozenset(left) in attribute_support:
                        confidence = candidate_support[frozenset(itemset)] / attribute_support[frozenset(left)]
                        if confidence >= min_confidence:
                            yield [left, right]

        frequent_itemsets = frequent_itemsets_k
        k += 1


folder_input = "dataset"
folder_output = "result_apriori"
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)
json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.csv')]
for json_file_name in json_file_names:
    print(os.path.join(folder_input, json_file_name))
    df = pd.read_csv(os.path.join(folder_input, json_file_name), header=None, skiprows=1, on_bad_lines='skip')
    parse_object_to_int(df)
    generator = find_dependencies(df, min_confidence=1)
    toFlush = ""
    for x in generator:
        lhs = list(x[1])
        rhs = list(x[0])
        toFlush += (", ".join(map(str, lhs)) + " -> " + str(rhs[0]) + "\n")

    with open(os.path.join(folder_output, json_file_name.replace("csv", "txt")), "w") as json_file_out:
        json_file_out.write(toFlush)
