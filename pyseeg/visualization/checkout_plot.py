import pandas as pd
import matplotlib.pyplot as plt

def plot_data(path, sep=',', header=None, trigger_only=False):
    data = pd.read_csv(path, sep=sep, header=header)
    if not trigger_only:
        data.plot(subplots=True, title=path)
    else:
        plt.plot(data[5])
        plt.ylim(-0.1,1.1)
    plt.show()
