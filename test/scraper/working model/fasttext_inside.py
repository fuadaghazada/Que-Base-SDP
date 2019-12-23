
import fasttext as ft

model = ft.train_supervised('model.train', epoch = 5000)

print(model.labels)
def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

print_results(*model.test('model.test'))
#model.save_model("last_model_final.bin")