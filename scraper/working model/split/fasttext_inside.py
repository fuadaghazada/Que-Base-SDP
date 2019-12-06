
import fasttext as ft

model = ft.load_model("fully_trained_model.bin")
def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

#print_results(*model.test('model.test'))
'''
model = ft.train_supervised('data_final_merged_shuffled.txt', epoch = 5000)
#exit(0)
print(model.labels)
def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

#print_results(*model.test('xab'))
model.save_model("fully_trained_model.bin")
'''