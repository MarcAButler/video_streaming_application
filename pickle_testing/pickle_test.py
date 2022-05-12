import pickle

example_dict = {1:"6",
                2: "2",
                3: "f"
}

# pickle_out = open("dict.pickle", "wb")
test_data = pickle.dumps(example_dict)
print(test_data)

# Load
loaded_data = pickle.loads(test_data)
print(loaded_data)



# pickle_out.close()


# pickle_in = open("dict.pickle", "rb")
# example_dict = pickle.load(pickle_in)

# print(example_dict)
# print(example_dict[2])