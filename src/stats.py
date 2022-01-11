import numpy as np
import pandas as pd
import scipy.stats as stats

################################
# CENTRAL TENDENCY
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


def CV(x):
    """Coefficient of variation."""
    return sample_std(x) / np.mean(x)


################################
# QUANTILES
################################


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


################################
# OUTLIERS
################################


def outliers(x):
    """Values below lower limit or above upper limit."""
    return sum([sum(x < lowerLimit(x)), sum(x > upperLimit(x))])


def prcnt_outliers(x):
    """How many outliers in comparison to total samples."""
    return (outliers(x) / len(x)) * 100


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


################################
# SKEW AND KURTOSIS
################################


def skew(x):
    """A measure of dataset symmetry."""
    return stats.skew(x, bias=False)


def kurtosis(x):
    """A measure of outliers."""
    return stats.kurtosis(x, bias=False)


################################
# ANOVA
################################


def perform_ANOVA(df, param="PM2.5", alpha=0.1, group_name="Sensor"):
    def get_SST(df, param="PM2.5"):
        """Computes sum of squares total for a dataframe.

        Returns: SST (sum of squares total), SST_df (degrees of freedom)
        """

        grand_mean = df[param].mean()

        SST = np.sum((df[param] - grand_mean) ** 2)
        SST_df = len(df) - 1

        return SST, SST_df

    def get_SSW(df, param="PM2.5"):
        """Computes sum of squares within for a dataframe.

        Returns: SSW (sum of squares within), SSW_df (degrees of freedom)
        """

        # distance between data point and their respective mean
        SSW = 0

        for sensor, grp in df.groupby(group_name):
            mean = grp[param].mean()
            SSW += np.sum((grp[param] - mean) ** 2)

        SSW_df = np.sum(df.groupby(group_name)[param].count() - 1)

        return SSW, SSW_df

    def get_SSB(df, param="PM2.5"):
        """Computes sum of squares between for a dataframe.

        Returns: SSB (sum of squares between), SSB_df (degrees of freedom)
        """

        ## SSB - Sum of squares between. Variation between groups.
        SSB = 0
        grand_mean = df[param].mean()

        for sensor, grp in df.groupby(group_name):
            mean = grp[param].mean()
            records = len(grp)

            SSB += records * ((mean - grand_mean) ** 2)

        SSB_df = len(df[group_name].unique()) - 1

        return SSB, SSB_df

    # Compute Sum of Squares
    SST, SST_df = get_SST(df, param)  # Sum of squares total
    SSW, SSW_df = get_SSW(df, param)  # Sum of squares within
    SSB, SSB_df = get_SSB(df, param)  # Sum of squares between

    # F statistic
    F_statistic = (SSB / SSB_df) / (SSW / SSW_df)

    # F critical
    F_critical = stats.f.ppf(1 - alpha, SSB_df, SSW_df)

    # P-value
    p_value = 1 - stats.f.cdf(F_statistic, SSB, SSW)

    # Combine into dataframe
    headers = ["SST", "SSW", "SSB", "Alpha", "F-stat", "F-crit", "P-value", "F-stat > F-crit", "p-value < alpha"]
    row = [SST, SSW, SSB, alpha, F_statistic, F_critical, p_value, F_statistic > F_critical, p_value < alpha]

    row = [f"{v} (Significant Difference)" if v == True else v for v in row]
    row = [f"{v} (Failed to reject Null Hypothesis)" if v == False else v for v in row]

    anova_df = pd.DataFrame(row, headers)

    return anova_df
