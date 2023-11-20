import numpy as np


def Q_mean(Q,  # type: Union[numpy.ndarray, List[Union[float, int]]]
           ):
    # type: (...) -> float
    """
    Examples:
        >>> from test_values import Q_qilian
        >>> Q_mean(Q_qilian)
        17.066013698630137
    """
    return np.mean(Q)


def Q_percentile(Q,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                 percentile=95  # type: int
         ):
    # type: (...) -> float
    """
    Examples:
        >>> from test_values import Q_qilian
        >>> Q_percentile(Q_qilian, 95)
        42.80999999999999
    """
    return np.percentile(Q, percentile)

def low_q_freq(Q,  # type: Union[numpy.ndarray, List[Union[float, int]]]
               ):
    # type: (...) -> float
    """Calculate the frequency of low Q < 0.2 avg Q.
    Examples:
        >>> from test_values import Q_qilian
        >>> low_q_freq(Q_qilian)
        0.06164383561643835
    """
    return np.sum(Q < 0.2 * np.mean(Q)) / len(Q)

def high_q_freq(Q,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                ):
    # type: (...) -> float
    """Calculate the frequency of high Q > 9 median Q.
        Examples:
        >>> from test_values import Q_qilian
        >>> high_q_freq(Q_qilian)
        0.0013698630136986301
    """
    return np.sum(Q > 9 * np.median(Q)) / len(Q)

def runoff_ratio(Q,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                 P  # type: Union[numpy.ndarray, List[Union[float, int]]]
                 ):
    # type: (...) -> float
    return np.sum(Q) / np.sum(P)

def Q_mean_seasonal(Q,  # type: Dict[datetime, float]
                    months_of_year,  # type: List[int]
                    default_season = None  # type: Optional[str]
                    ):
    # type: (...) -> float
    """
    Calculate the mean of seasonal Q.
    Args:
        Q: dict of Q, {datetime: Q, ...}
        months_of_year: list of months, e.g., [4, 5, 6, 7, 8, 9,]
        default_season: default season,
            'wet' for [4, 5, 6, 7, 8, 9, 10]
            'dry' for [1, 2, 3, 11, 12]
            'spring' for [3, 4, 5]
            'summer' for [6, 7, 8]
            'autumn' for [9, 10, 11]
            'winter' for [12, 1, 2]

            Examples:
            >>> from test_values import Q_dict_qilian
            >>> Q_mean_seasonal(Q_dict_qilian, [ 4, 5, 6, 7, 8, 9,])
            25.809661290322584
            >>> Q_mean_seasonal(Q_dict_qilian, None, 'dry')
            6.40677242703533
    """
    if default_season is not None:
        if default_season == 'wet':
            months_of_year = [4, 5, 6, 7, 8, 9, 10]
        elif default_season == 'dry':
            months_of_year = [1, 2, 3, 11, 12]
        elif default_season == 'spring':
            months_of_year = [3, 4, 5]
        elif default_season == 'summer':
            months_of_year = [6, 7, 8]
        elif default_season == 'autumn':
            months_of_year = [9, 10, 11]
        elif default_season == 'winter':
            months_of_year = [12, 1, 2]
        else:
            raise ValueError('Invalid default_season: %s' % default_season)
    Q_seasonal = list()
    for month in months_of_year:
        Q_seasonal.append(np.mean([Q[date] for date in Q if date.month == month]))
    return np.mean(Q_seasonal)
