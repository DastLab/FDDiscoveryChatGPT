#!/bin/bash
python tool/match_dependencies_folder.py result_formatter result_anova results
python tool/match_dependencies_folder.py result_formatter result_apriori results
python tool/match_dependencies_folder.py result_formatter result_corr_reg results
python tool/match_dependencies_folder.py result_formatter result_linear_reg results
python tool/match_dependencies_folder.py result_formatter result_subset_gen results
python tool/match_dependencies_folder.py result_formatter result_pairw results
python tool/match_dependencies_folder.py result_formatter result_tane results