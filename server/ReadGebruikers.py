import pickle

import os
folder = os.path.dirname(os.path.abspath(__file__))
gebruikers_file = os.path.join(folder,'database/Gebruikers.txt')

my_reader_obj = open(gebruikers_file, mode="rb")
read_list = pickle.load(my_reader_obj)
print(read_list)