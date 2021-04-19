import pickle

import os
folder = os.path.dirname(os.path.abspath(__file__))
file_ = os.path.join(folder,'database/zoekopdrachten.txt')

my_reader_obj = open(file_, mode="rb")
read_list = pickle.load(my_reader_obj)
print(read_list)