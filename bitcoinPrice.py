# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
base_path = os.path.join(os.getcwd(), 'data')  # relative to current working directory
print("Searching in:", base_path)
for dirname, _, filenames in os.walk(base_path):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df=pd.read_csv(base_path + '/btcusd_1-min_data.csv')