import pandas as pd
import matplotlib.pyplot as plt

def plot_data(path, sep=',', header=None, ptype=None):
    print('Plotting')
    data = pd.read_csv(path, sep=sep, header=header)
    if ptype is None:
        data.plot(subplots=True, title=path)
    elif 'decision' in ptype:
        data = data.ix[data[2]==1]
        data.plot(subplots=True, title=path)

    plt.show()
