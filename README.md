# ChatGPTvsHyFD
 

1. **runhydfd.sh**: Use HyFD (https://github.com/codocedo/hyfd) in order to find the valid FDs of the datasets in "dataset" folder. 
The results of each dataset are written in ./json/'dataset_name'.json. The file results/hyfd_results.txt contains the execution report.
2. **tool/hyfd_result_formatter.py**: Used to generate formatted FDs from HyFD results. The outputs are written in "result_formatter" folder
3. **anova.py, apriori.py, corr_reg.py, linear_reg.py, pair_wise.py, subset_generation.py, tane.py**: Run the ChatGPT generated algorithms on the datasets in "dataset" 
folder and save formatted results in "result_%alg name%".
4. **tool/match_dependencies_folder.py**: Used to compare the discovery result of two algorithms over all datasets.
5. **generate_results.sh**: Run the tool/match_dependencies_folder.py to compare all result of ChatGPT algorithms with HyFD.
6. **tool/extract_statistics.py**: Used to extract information about discovery result of a ChatGPT algorithm compared to HyFD. 
7. **generate_stats.sh**: Run the tool/extract_statistics.py for all extracted result of ChatGPT algorithms compared with HyFD.
8. **tool/plot.py**: Plot the required information for all ChatGPT discovery algorithms. 


## Data Usage Agreement/ How to cite

By using this study, you agree to cite the following article: 
```
@inproceedings{caruccio2023fdchatgpt,
  title={Discovering Functional Dependencies: Can We Use ChatGPT to Generate Algorithms?},
  author={Loredana Caruccio, Stefano Cirillo, Tullio Pizzuti, and Giuseppe Polese},
  booktitle={Italian Conference on Big Data and Data Science (ITADATA)},
  year={2023}
}
```
