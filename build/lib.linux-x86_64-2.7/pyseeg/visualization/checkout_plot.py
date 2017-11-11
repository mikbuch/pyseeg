import pandas as pd
import matplotlib.pyplot as plt

def plot_data(path, sep=',', header=None):
    data = pd.read_csv(path, sep=sep, header=header)
    data.plot(subplots=True, title=path)
    plt.show()
