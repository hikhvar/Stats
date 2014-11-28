# -*- coding: UTF-8 -*-
import numpy as np
import itertools
#import scipy.stats as stats
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt



def get_plot_modes():
    return sorted(REGISTERED_PLOTS.keys())

def draw_plot(mode, axis, dataframe, start=None, end=None, xkcd = False):
    axis.cla()
    if start is None:
        start = 0
    if end is None:
        end = float("inf")
    if len(dataframe) < 1:
        return
    df = dataframe[(dataframe.date >= start) & (dataframe.date <=end)]
    function, kwargs = REGISTERED_PLOTS[mode]
    if xkcd == True:
        with plt.xkcd():
            function(axis, df, **kwargs)
    else:
        function(axis, df, **kwargs)


def normpdf(x, mu, sigma):
    u = (x-mu)/(1.0 * np.abs(sigma))
    y = (1.0/(np.sqrt(2.0*np.pi)*np.abs(sigma)))*np.exp(-u*u/2.0)
    return y

def _plot_average(axis, df, plot_std = False):
    dates, date_mapping = _get_datemapping(df)
    for schuetze in df.schuetze.unique():
        df_sub = df[df.schuetze == schuetze]
        agg = df_sub.groupby("human_readable")["result"].agg(func=np.mean)
        std_agg = df_sub.groupby("human_readable")["result"].agg(func=np.std)
        x = []
        y = []
        std = []
        for date, mean in agg.iteritems():
            x.append(date_mapping[date])
            y.append(mean)
        line = axis.plot(x,y, label=schuetze, marker="o")[0]
        if plot_std:
            for _, i in std_agg.iteritems():
                std.append(i)
            y = np.array(y)
            std = np.array(std)
            lower, upper = y - std, y + std
            axis.fill_between(x, lower, upper, alpha=0.2, color=line.get_color())
    axis.set_xticks(list(xrange(len(dates))))
    axis.set_xticklabels(dates)
    axis.margins(0.1)
    _make_legend(axis)

def _plot_distribution(axis, df):
    for schuetze in df.schuetze.unique():
        df_sub = df[df.schuetze == schuetze]
        mean, std = np.mean(df_sub.result), np.std(df_sub.result)
        x = np.arange(0, 54.5, 0.05)
        y = normpdf(x, mean, std)
        lower = round(mean - 1.96 * std, 1)
        upper = round(mean + 1.96 * std, 1)
        label = schuetze + ": " + str(lower) + " - "  + str(upper)
        axis.plot(x,y, label=label)
    axis.set_xlim(40,55)
    _make_legend(axis)

def _plot_histogram(axis, df):
    for schuetze in df.schuetze.unique():
        df_sub = df[df.schuetze == schuetze]
        hist,_ = np.histogram(df_sub.result, bins=545, density=True, range=(0,54.5))
        x = np.arange(0, 54.5, 0.1)
        axis.plot(x, hist, label=schuetze)
    axis.set_xlim(40,55)
    _make_legend(axis)

def _plot_team_distribution(axis, df, sort_function=None):
    def _get_starting(fullname):
        name = fullname.split(" ")
        name = map(lambda x: x[0], name)
        return "".join(name)
    schuetzen = df.schuetze.unique()
    schuetzen_params = {}
    for sch in schuetzen:
        df_sub = df[df.schuetze == sch]
        schuetzen_params[sch] = np.mean(df_sub.result), np.std(df_sub.result)
    best = []
    for team in itertools.combinations(schuetzen, 4):
        team_mean, team_std = 0, 0
        for i in xrange(4):
            sch = team[i]
            mean, std = schuetzen_params[sch]
            team_mean += mean
            team_std += std
        best.append((team_mean, team_std, team))
        best = sort_function(best)[0:5]
    for mean, std, team in best:
        x = np.arange(180, 218, 0.05)
        y = normpdf(x, mean, std)
        teamname = "+".join(map(lambda x: _get_starting(x), team))
        lower = round(mean - 1.96 * std, 1)
        upper = round(mean + 1.96 * std, 1)
        teamname = teamname + ": " + str(lower) + " - "  + str(upper)
        line = axis.plot(x,y, label=teamname)[0]
    axis.set_xlim(180, 218,)
    _make_legend(axis)

def _plot_activity(axis, df):
    """
        plot the activity over time.
    """
    dates, date_mapping = _get_datemapping(df)
    agg = df.groupby("human_readable")["result"].agg(func=len)
    agg_schuetzen = df.groupby("human_readable")["schuetze"].agg(func=_unique)
    x = []
    y = []
    for date, saetze in agg.iteritems():
        x.append(date_mapping[date])
        y.append(saetze)
    n = []
    for _, schuetzen in agg_schuetzen.iteritems():
        n.append(float(schuetzen))
    normed_y = np.array(y) / np.array(n)
    axis.plot(x,normed_y,label="Erfasste Saetze pro Schuetze", marker="o")
    #axis.plot(x, y, label="Saetze gesamt", marker="o")
    axis.plot(x, n, label="Schuetzen", marker="o")
    axis.set_xticks(list(xrange(len(dates))))
    axis.set_xticklabels(dates)
    axis.margins(0.1)
    _make_legend(axis)

def _unique(series):
    return series.nunique()

def _get_datemapping(df):
    """
        return the mapping of human_readable dates to 
        integer numbers for plotting. Mapping is a dict.
        Furthermore return a sorted list of the dates.
    """
    dates = sorted(df.human_readable.unique())
    date_mapping = {}
    for index, d in enumerate(dates):
        date_mapping[d] = index
    return dates, date_mapping

def _sort_mean_first(best):
    """
        sort the teams by mean value first, then std. 
    """
    return sorted(best, reverse=True)


def _sort_std_first(best):
    """
        sort the teams by std value first, then mean. 
    """
    sort = sorted(best, reverse=True)
    return sorted(sort, key=lambda satz: satz[1])

def _make_legend(axis):
    if len(axis.get_lines()) > 0:
        axis.legend(loc=2)


# Name of plot : (function, kwargs)
REGISTERED_PLOTS = {
    "Verlauf des Durchschnitts"     : (_plot_average, {}),
    "Verlauf der Abweichung"        : (_plot_average, {"plot_std":True}),
    "Theo. Verteilung"              : (_plot_distribution, {}),
    "Verteilung"                    : (_plot_histogram, {}),
    "Team Verteilung mean"          : (_plot_team_distribution, {"sort_function":_sort_mean_first}),
    "Team Verteilung std."          : (_plot_team_distribution, {"sort_function":_sort_std_first}),
    "Beteiligung"                   : (_plot_activity, {})
}