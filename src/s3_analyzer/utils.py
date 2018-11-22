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
        if fltr['operation'] == 'eq':
            return entry[fltr['property']] == fltr['value']
        elif fltr['operation'] == 'gt':
            return entry[fltr['property']] > fltr['value']
        elif fltr['operation'] == 'lt':
            return entry[fltr['property']] < fltr['value']
        elif fltr['operation'] == 'regex':
            pattern = re.compile(fltr['value'])
            return pattern.match(entry[fltr['property']])

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
