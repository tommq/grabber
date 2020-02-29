from datetime import datetime as dt


def dt_from_str(string_input):
    return dt.strptime(string_input, '%Y-%m-%d %H:%M:%S.%f')
