import cPickle as pickle

airports_data_dict = {}
airports_search_arr = []

with open('airport-codes.dat', 'r') as f:
    for line in f:
        line = line.strip('\r\n')
        data = line.split('|')

        name = data[0]
        name_lower = name.lower()

        code = data[1]
        code_lower = code.lower()

        fullname = code + ' - ' + name

        airports_data_dict[name_lower] = fullname
        airports_data_dict[code_lower] = fullname

        airports_search_arr.append(name_lower)
        airports_search_arr.append(code_lower)

pickle.dump(airports_data_dict, open('airports_data_dict.p', 'wb'))
pickle.dump(airports_search_arr, open('airports_search_arr.p', 'wb'))