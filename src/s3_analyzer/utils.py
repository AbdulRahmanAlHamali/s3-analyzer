import re
from tabulate import tabulate


def get_grouped_info(info_list, grouping):
    result = dict()
    for info in info_list:
        if info[grouping] not in result:
            result[info[grouping]] = []
        result[info[grouping]].append(info)

    return result


def run_filters(info_list, filters):
    def filter_runner(entry, fltr):

        entry_value = entry[fltr['property']]
        if type(entry_value) == int:
            filter_value = int(fltr['value'])
        elif type(entry_value) == float:
            filter_value = float(fltr['value'])
        else:
            filter_value = fltr['value']

        if fltr['operation'] == 'eq':
            return entry_value == filter_value
        elif fltr['operation'] == 'gt':
            return entry_value > filter_value
        elif fltr['operation'] == 'lt':
            return entry_value < filter_value
        elif fltr['operation'] == 'regex':
            pattern = re.compile(filter_value)
            return pattern.match(entry_value)

    result = info_list
    for f in filters:
        result = list(filter(lambda entry: filter_runner(entry, f), result))

    return result


def convert_size(value, target):
    if target == 'B':
        return value
    elif target == 'KB':
        return value / 1024
    elif target == 'MB':
        return value / 1024 / 1024
    elif target == 'GB':
        return value / 1024 / 1024 / 1024
    elif target == 'TB':
        return value / 1024 / 1024 / 1024 / 1024


def get_table_info(info):
    return tabulate(info, headers='keys', tablefmt="fancy_grid", numalign='left', stralign='left')