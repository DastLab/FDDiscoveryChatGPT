#!/bin/bash
rm -r stats
python tool/extract_statistics.py result_formatter result_anova stats
python tool/extract_statistics.py result_formatter result_apriori stats
python tool/extract_statistics.py result_formatter result_corr_reg stats
python tool/extract_statistics.py result_formatter result_linear_reg stats
python tool/extract_statistics.py result_formatter result_subset_gen stats
python tool/extract_statistics.py result_formatter result_pairw stats
python tool/extract_statistics.py result_formatter result_tane stats