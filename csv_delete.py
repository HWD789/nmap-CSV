import pandas as pd
import csv
import os
import sys
import time
import re
import json

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

if not os.path.isdir('./data'):
    os.mkdir('./data')


def CSVDelete(*args):
    csv_file = args[0]
    detele_line = args[1]
    data = pd.read_csv(csv_file)
    # 删除行数下标,不算header
    data_new = data.drop(detele_line)
    data_new.to_csv(csv_file, index=0)
if __name__ == "__main__":
    CSVDelete('./data/test.csv',[25])