import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

dataset_id = {
    "chess": {"id": "1", "aa": 3},
    "abalone": {"id": "2", "aa": 1},
    "nursery": {"id": "3", "aa": 9},
    "electricity_normalizer": {"id": "4", "aa": 5},
    "customer_shopping_data": {"id": "5", "aa": 4},
    "fraudfull": {"id": "6", "aa": 7},
    "poker-hand": {"id": "7", "aa": 10},
    "firewall": {"id": "8", "aa": 6},
    "adult": {"id": "9", "aa": 2},
    "letter": {"id": "10", "aa": 8},
    "sgemm_product_rounded": {"id": "11", "aa": 11},

}


def order_by_id(v):
    toRet = []
    for e in dataset_id.values():
        toRet.append(v[e["aa"] - 1])
    return toRet


def generate_plot_res(fig, axs, alg, tp, gen, spec, hyfd, gptfd, errate):
    itemsleft = {
        "Common FDs": tp,
        "Specializations": spec
    }
    itemsright = {
        "Errors": errate,
        "Generalizations": gen
    }
    font = 14
    op = 1
    gridOp = 0.5
    colorLine = "g"
    markerLine = "o"
    x = np.arange(len(files))
    x_label = np.arange(len(files)) + 1
    x_label = list(map(lambda x: "D" + str(x), x_label))
    width = 0.4  # the width of the bars
    multiplier = -1

    axs[0].plot(hyfd, marker=markerLine, color=colorLine, alpha=op, label='HyFD', linestyle='dashed')
    axs[0].tick_params(axis='both', labelsize=font + 3)

    maxleft = max(hyfd)
    bar_color = ["r", "y"]
    iter = 0
    for attribute, measurement in itemsleft.items():
        offset = (width / 2) * multiplier
        rects = axs[0].bar(x + offset, measurement, width, label=attribute, color=bar_color[iter], edgecolor="black")
        if max(measurement) > maxleft:
            maxleft = max(measurement)
        axs[0].bar_label(rects, size=font, labels=[item if item > 0 else "" for item in measurement])
        multiplier *= (-1)
        iter += 1

    axs[0].set_xticks(x, x_label)
    axs[0].margins(x=0.01)

    axs[1].tick_params(axis='both', labelsize=font + 3)
    multiplier = -1
    iter = 0
    maxright = max(gptfd)
    axs[1].plot(gptfd, marker=markerLine, color="y", alpha=op, label="ChatGPT Algorithm", linestyle='dashed')
    for attribute, measurement in itemsright.items():
        offset = (width / 2) * multiplier

        rects = axs[1].bar(x + offset, measurement, width, label=attribute, edgecolor="black")
        if max(measurement) > maxright:
            maxright = max(measurement)
        axs[1].bar_label(rects, size=font, labels=[item if item > 0 else "" for item in measurement])
        multiplier *= (-1)
        iter += 1
    axs[1].set_xticks(x, x_label)
    axs[1].margins(x=0.01)

    axs[0].grid(alpha=gridOp)
    axs[1].grid(alpha=gridOp)


    axs[1].yaxis.labelpad = 20

    if alg == "tane":
        alg = "Tane"
        axs[0].set_yscale('symlog')
        # axs[0].set_ylabel("symlog")
        axs[0].set_ylim(0, 200)

    if alg == "pairw":
        alg = "Pair-wise"
        axs[0].set_yscale('symlog')
        # axs[0].set_ylabel("symlog")
        axs[0].set_ylim(0, 200)

        axs[1].set_yscale('symlog')
        # axs[1].set_ylabel("symlog")
        axs[1].set_ylim(0, 50)

    if alg == "subset_gen":
        alg = "Subset gen."
        axs[0].set_yscale('symlog')
        # axs[0].set_ylabel("symlog")
        axs[0].set_ylim(0, 400)

        axs[1].set_yscale('symlog')
        # axs[1].set_ylabel("symlog")
        axs[1].set_ylim(0, 5000)

    if alg == "linear_reg":
        alg = "Linear reg."
        #axs[1].yaxis.labelpad = 24

        axs[0].set_yscale('symlog')
        # axs[0].set_ylabel("symlog")
        axs[0].set_ylim(0, 200)

        axs[1].set_ylim(0, 10)

    if alg == "corr_reg":
        alg = "Corr. & Regr."
        axs[0].set_yscale('symlog')
        # axs[0].set_ylabel("symlog")
        axs[0].set_ylim(0, 200)

        axs[1].set_yscale('symlog')
        # axs[1].set_ylabel("symlog")
        axs[1].set_ylim(0, 100)

    if alg == "anova":
        alg = "Anova"

        # axs[0].legend(framealpha=1, ncol=3, shadow=True)
        # axs[1].legend(framealpha=1, ncol=3, shadow=True)

        axs[0].set_yscale('symlog')
        # axs[0].set_ylabel("symlog")
        axs[0].set_ylim(0, 200)

        axs[1].set_yscale('symlog')
        # axs[1].set_ylabel("symlog")
        axs[1].set_ylim(0, 600)

    if alg == "apriori":
        alg = "Apriori"

        axs[0].set_yscale('symlog')
        axs[1].set_yscale('symlog')
        # axs[0].set_ylabel("symlog")
        axs[0].set_ylim(0, 900)
        axs[1].set_ylim(0, 700000)

    axs[1].yaxis.set_label_position("right")
    axs[1].yaxis.tick_right()
    axs[1].set_ylabel(alg, rotation=-90, fontsize=18)


parser = argparse.ArgumentParser(description='Genera plot dal file result.csv')
parser.add_argument('file', help="File result.csv")
parser.add_argument('--outfolder', dest="outfolder", help="Esporta csv (default false)")

args = parser.parse_args()

output_folder = args.outfolder
if output_folder:
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
file_path = args.file

df = pd.read_csv(file_path)
'''df.precision = df.precision.round(4)
df.recall = df.recall.round(4)
df.f1score = df.f1score.round(4)
'''
algs = df.alg.unique()
files = df.file.unique()
algscut = list(map(lambda x: x[0:7], df.alg.unique()))
filescut = list(map(lambda x: x[0:5], df.file.unique()))

tp = df.groupby(["alg"])["TP"].apply(list)

gen = df.groupby(["alg"])["generalizzazioni(unique)"].apply(list)
spec = df.groupby(["alg"])["specializzazioni(unique)"].apply(list)
hyfd = df.groupby(["alg"])["hyfd_fd"].apply(list)
gptfd = df.groupby(["alg"])["gpt_fd(unique)"].apply(list)
errate = df.groupby(["alg"])['errate(no coumuni/spec/gen)'].apply(list)

fig, axs = plt.subplots(figsize=(15, 17), layout='constrained',
                        nrows=7, ncols=2, sharex=True)


r = 0

for a in algs:
    generate_plot_res(fig, axs[r], a, order_by_id(tp[a]), order_by_id(gen[a]), order_by_id(spec[a]),
                      order_by_id(hyfd[a]),
                      order_by_id(gptfd[a]), order_by_id(errate[a]))
    r += 1

fig.tight_layout()
fig.subplots_adjust(hspace=0.1)
if output_folder:
    plt.savefig(os.path.join(output_folder, "res.pdf"), format="pdf")
else:
    plt.show()
plt.clf()
