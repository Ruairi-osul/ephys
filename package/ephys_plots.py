import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches


def spike_heatmap(st_df, ax, vmin=-3, vmax=3, scaler=None, norm_period=3600,
                  line=3600, line_lab='Citalopram Administration', title=None):
    if scaler is None:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()

    scaler.fit(st_df.iloc[:norm_period, :])
    dfp = pd.DataFrame(scaler.transform(st_df), columns=st_df.columns)
    dfp.index = np.round(st_df.index / 60)
    dfp = dfp.transpose()
    sns.heatmap(dfp, ax=ax, cmap='coolwarm', vmin=vmin, vmax=vmax,
                cbar_kws={'label': 'Normalised firing rate'})
    plt.xticks(rotation=90)

    if hasattr(line, '__iter__'):
        for l in line:
            plt.axvline(x=line)
    elif line:
        plt.axvline(x=line, color='k', linewidth=5, label=line_lab)
    ax.set_xlabel('Time [minutes]')
    ax.set_ylabel('Neuron id')
    if title:
        ax.set_title(title)
    ax.legend()
    return ax


def heatmap_by_cluster(data_categories,
                       data_ts,
                       cluster_lab='hc_cluster',
                       scaler=None,
                       norm_period=3600, vmin=-3, vmax=3,
                       cmap='coolwarm', spacing=True,
                       size=(25, 10), label=True):

    data_categories = data_categories.sort_values(cluster_lab)

    row_color_series = data_categories[['colors']]
    row_color_series.index = data_categories.neuron_id.values
    mapper = {}
    for cat in data_categories['hc_cluster'].unique():
        mapper[cat] = data_categories[data_categories['hc_cluster'] == cat]['colors'].values[0]

    dfp = _scale_format_data(
        data_ts, data_categories=data_categories,
        scaler=scaler, norm_period=norm_period)

    cm = sns.clustermap(dfp, row_colors=row_color_series,
                        row_cluster=False, col_cluster=False,
                        vmin=vmin, vmax=vmax, cmap=cmap, figsize=size,
                        xticklabels=4)

    if len(data_ts > 60):
        axvlines(60, ax=cm.ax_heatmap, linewidth=5,
                 color='k', label='Citalopram Administration')
    # cm.ax_heatmap.legend()

    if spacing:
        for line in np.arange(0, data_categories.shape[1], 1):
            cm.ax_heatmap.axhline(line, color='w')
    if label:
        cm.ax_heatmap.legend(bbox_to_anchor=(0.5, 1.1), loc=2)
        cm.ax_heatmap = _legend_maker(mapper, ax=cm.ax_heatmap)
    return cm


def _scale_format_data(data_ts, data_categories, scaler=None, norm_period=3600):
    if scaler is None:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()

    scaler.fit(data_ts.iloc[:norm_period, :])
    dfp = pd.DataFrame(scaler.transform(data_ts.values), columns=data_ts.columns)
    dfp.index = np.round(np.linspace(-norm_period, norm_period, data_ts.shape[0]) / 6, 2)
    dfp = dfp.transpose()
    dfp.index = data_categories.neuron_id.values
    return dfp


def _legend_maker(mapper, ax):
    patches = [mpatches.Patch(color=color, label=cat)
               for cat, color in mapper.items()]

    legends = ax.legend(loc='best',
                        bbox_to_anchor=(0.3, 1.1),
                        handles=patches,
                        frameon=True,
                        markerscale=10, prop={'size': 10.5})
    legends.set_title(title='Neuron Categories', prop={'size': 20})
    return ax


def _gen_row_colors(data_categories, n_colors, cluster_lab):
    category_names = data_categories[cluster_lab].unique()
    colors = sns.color_palette(n_colors=n_colors)
    mapper = {cluster: color for cluster, color in zip(category_names, colors)}
    row_color_series = data_categories[cluster_lab].map(mapper)
    row_color_series.index = data_categories.neuron_id.values
    return row_color_series, data_categories, mapper


def axvlines(xs, ax=None, **plot_kwargs):
    """
    Draw vertical lines on plot
    :param xs: A scalar, list, or 1D array of horizontal offsets
    :param ax: The axis (or none to use gca)
    :param plot_kwargs: Keyword arguments to be passed to plot
    :return: The plot object corresponding to the lines.
    """
    if ax is None:
        ax = plt.gca()
    xs = np.array((xs, ) if np.isscalar(xs) else xs, copy=False)
    lims = ax.get_ylim()
    x_points = np.repeat(xs[:, None], repeats=3, axis=1).flatten()
    y_points = np.repeat(np.array(lims + (np.nan, ))
                         [None, :], repeats=len(xs), axis=0).flatten()
    plot = ax.plot(x_points, y_points, scaley=False, **plot_kwargs)
    return plot


def ifr_plot(col, ax):
    col.plot(ax=ax)
    med = np.median(col)
    plt.axhline(med, color='k', linewidth=4,
                linestyle='--', label='median firing rate')

    ax.fill_between(col.index, col, alpha=0.45)
    return ax


def scatter_by_shank(df, ax, recording=None):
    df['shank'] = df.apply(
        lambda x: 'shank 1' if x['channel'] <= 16 else 'shank 2', axis=1)
    g = df.groupby('shank')
    for name, group in g:
        ax.scatter(y=group['mfr'], x=group['cv isi'], label=name)
        ax.legend()
    ax.set_xlabel('CV ISI')
    ax.set_ylabel('Mean Firing Rate')
    if recording:
        ax.set_title(f'Recording {recording}')
    plt.tight_layout()
    df.drop('shank', axis=1, inplace=True)
    return ax
