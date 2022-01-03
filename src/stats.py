import numpy as np
import scipy.stats as stats

################################
# STATS FUNCTIONS
################################


def mode(x):
    """The most common value."""
    return stats.mode(x)[0]


def x_range(x):
    """Difference between maximum and minimum."""
    return max(x) - min(x)


def sample_std(x):
    """Sample standard deviation."""
    return np.std(x, ddof=1)


def standard_error(x):
    """Sample standard error."""
    return sample_std(x) / np.sqrt(len(x))


def CI95(x):
    """Confidence interval at 95%"""

    z_score = 1.96  # Z_score = 1.96 for 95%
    sample_size = len(x)
    std = np.std(x, ddof=1)

    confidence_interval = z_score * (std / np.sqrt(sample_size))

    return confidence_interval


# QUANTILES
def Q1(x):
    """First quartile."""
    return x.quantile(0.25)


def Q2(x):
    """Second quartile."""
    return x.quantile(0.5)


def Q3(x):
    """Third quartile."""
    return x.quantile(0.75)


def IQR(x):
    """Inter quartile range."""
    return Q3(x) - Q1(x)


def lowerLimit(x):
    """Lower limit."""
    return Q1(x) - 1.5 * IQR(x)


def upperLimit(x):
    """Upper limit."""
    return Q3(x) + 1.5 * IQR(x)


def outliers(x):
    """Values below lower limit or above upper limit."""
    return sum([sum(x < lowerLimit(x)), sum(x > upperLimit(x))])


def prcnt_outliers(x):
    """How many outliers in comparison to total samples."""
    return (outliers(x) / len(x)) * 100


# SKEW AND KURTOSIS
def skew(x):
    """A measure of dataset symmetry."""
    return stats.skew(x, bias=False)


def kurtosis(x):
    """A measure of outliers."""
    return stats.kurtosis(x, bias=False)


def print_outliers(s_df, station_quantiles, column):
    # Get session ids associated with
    outliers_dict = {}

    s_of_interest = list(station_quantiles[column].loc[station_quantiles[column].outliers > 0].index)
    soi_df = s_df.loc[s_df["Station"].isin(s_of_interest)]

    for station, grp in soi_df.groupby("Station"):
        lower = station_quantiles[column]["lowerLimit"][station]
        upper = station_quantiles[column]["upperLimit"][station]
        outliers_dict[station] = grp.loc[(grp[column] <= lower) | (grp[column] >= upper)][["Session Id", column]].values

    # Print Session id's of interest
    outlier_ids = []

    print("=== OUTLIERS ===")

    for station, sessions in outliers_dict.items():
        print(f"{station}:")
        for session in sessions:

            outlier_ids.append(session[0])
            print(f"\t{session[0]} - {column} = {round(session[1], 2)}")

        print()

    print(f"Unique outliers: {sorted(set(outlier_ids))}")

    return outlier_ids
