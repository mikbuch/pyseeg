import pandas as pd
import matplotlib.pyplot as plt

def plot_data(path, sep=','):
    data = pd.read_csv(path, sep=sep)
    data.plot(subplots=True)
    plt.show()
