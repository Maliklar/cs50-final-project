## most important functions are here
from datetime import date, datetime, timedelta
from typing import cast
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from scipy.interpolate import make_interp_spline





def user_records_plot(x, y, charName):
    if(len(x) < 4 and len(y) < 4):
        return f"/main/graphs/no_data_to_show.png"
    xs = np.array(x)
    ys = np.array(y)
    X_Y_Spline = make_interp_spline(xs, ys)
    X_ = np.linspace(xs.min(), xs.max(), 80)
    Y_ = X_Y_Spline(X_)
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,4), dpi=80)
    plt.title(charName)
    plt.plot(X_, Y_)
    plt.grid(True)
    plt.xticks(x, rotation=90)
    plt.xlabel('Try', )
    plt.ylabel('WPM')
    plt.tight_layout()
    plt.savefig(f"main/static/main/graphs/{charName}.png")
    return f"/static/main/graphs/{charName}.png"


def quote_records_plot(x, y, charName):
    if(len(x) < 4 and len(y) < 4):
        return f"/main/graphs/no_data_to_show.png"
    xs = np.array(x)
    ys = np.array(y)
    X_Y_Spline = make_interp_spline(xs, ys)
    X_ = np.linspace(xs.min(), xs.max(), 80)
    Y_ = X_Y_Spline(X_)
    plt.switch_backend('AGG')
    plt.figure(figsize=(8, 4), dpi=80)
    plt.title(charName)
    plt.plot(X_, Y_)
    plt.grid(True)
    plt.xticks(x, rotation=90)
    plt.xlabel('Try', )
    plt.ylabel('WPM')
    plt.tight_layout()
    plt.savefig(f"main/static/main/graphs/{charName}.png")
    return f"/main/graphs/{charName}.png"
