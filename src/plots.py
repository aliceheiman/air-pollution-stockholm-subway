################################
# LIBRARIES
################################
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from matplotlib import dates

# Matplotlib settings
plt.style.use("seaborn")

params = {
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "axes.labelsize": 20,
    "legend.fontsize": 20,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18,
    "text.usetex": False,
    "figure.figsize": [10, 5],
    "axes.grid": True,
}

plt.rcParams.update(params)
plt.close("all")

# Apply the default theme
sns.set_theme()

################################
# GENERAL PLOTTING FUNCTIONS
################################


def format_time_axis():
    plt.gcf().autofmt_xdate()
    myFmt = dates.DateFormatter("%H:%M:%S")
    plt.gca().xaxis.set_major_formatter(myFmt)


def plot_sensor_distributions(s_df, title, fig_name=False, bins=False, param="PM2.5", with_textbox=False):
    def add_textbox(graph_text, ax):
        # Build a rectangle in axes coords
        left, width = 0.45, 0.5
        bottom, height = 0.45, 0.5
        right = left + width
        top = bottom + height

        p = plt.Rectangle((left, bottom), width, height, fill=False, linewidth=0)
        p.set_transform(axs[i].transAxes)
        p.set_clip_on(False)
        ax.add_patch(p)

        t = ax.text(
            right,
            top,
            graph_text,
            horizontalalignment="right",
            verticalalignment="top",
            transform=axs[i].transAxes,
            fontsize=18,
        )
        t.set_bbox(dict(facecolor="white", alpha=0.5, edgecolor="white"))

    sensor_count = len(s_df["Sensor"].unique())

    fig, axs = plt.subplots(ncols=sensor_count, dpi=250, sharey=True, figsize=[20, 7])

    i = 0
    for label, grp in s_df.groupby(["Sensor"]):
        mean = grp[param].mean()
        median = grp[param].median()
        std = grp[param].std()
        s_skew = stats.skew(grp[param], bias=False)
        s_kurt = stats.kurtosis(grp[param], bias=False)

        if bins:
            sns.histplot(grp, x=param, ax=axs[i], kde=True, color=sns.color_palette()[i], bins=bins)
        else:
            sns.histplot(grp, x=param, ax=axs[i], kde=True, color=sns.color_palette()[i])

        axs[i].tick_params(axis="x", labelsize=18)
        axs[i].tick_params(axis="y", labelsize=18)

        axs[i].set_xlabel(param, fontsize=20)
        axs[i].set_ylabel("Count", fontsize=20)
        axs[i].set_title(f"Sensor {label}", fontsize=20)

        axs[i].axvline(mean, c="k", linestyle="--", label="mean")
        axs[i].axvline(median, c="c", linestyle="--", label="median")

        graph_text = (
            # fr"$mean={round(mean, 2)}$" + "\n" +
            # fr"$\sigma={round(std, 2)}$" + "\n" +
            fr"$skew={round(s_skew, 2)}$"
            + "\n"
            + fr"$kurt={round(s_kurt, 2)}$"
        )

        axs[i].legend(fontsize=14)

        if with_textbox:
            add_textbox(graph_text, axs[i])

        i += 1

    plt.tight_layout()
    fig.subplots_adjust(top=0.85)
    fig.suptitle(title, fontsize=30)

    if fig_name:
        plt.savefig(fig_name)

    plt.plot()


def plot_QQ_plots(s_df, title, param="PM2.5", fig_name=False):
    fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(10, 7), dpi=200)

    for sensor, ax in zip(s_df["Sensor"].unique(), axs.flatten()):
        stats.probplot(s_df[s_df["Sensor"] == sensor][param], dist="norm", plot=ax)
        ax.set_title(f"Sensor {sensor}", fontsize=14)

    plt.suptitle(title, fontsize=16)
    plt.tight_layout()

    if fig_name:
        plt.savefig(fig_name)

    plt.show()


def plot_sensors_over_time(df, title, param="PM2.5", size=[12, 5], fig_name=False):
    fig, ax = plt.subplots(figsize=size, dpi=200)

    for label, grp in df.groupby("Sensor"):
        ax.plot(grp["Timestamp"], grp[param], label=label, linewidth=2)

    ax.set_title(title)
    ax.set_ylabel(param)
    ax.legend(fontsize=12, loc=4, frameon=True, facecolor="#fff")
    format_time_axis()

    plt.tight_layout()

    if fig_name:
        plt.savefig(fig_name)

    plt.show()
