from numpy import mean


def mean_index(param):
    minus = 100000
    m_index = 0
    for i in range(len(param)):
        if abs(param[i] - mean(param)) < minus:
            m_index = i
    return m_index
