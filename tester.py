import pickle as pk

b_a = pk.load(open('./accuracy/best_accuracy.pkl', 'rb'))

print(str(b_a))