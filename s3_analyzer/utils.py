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

def map_region_name_to_code(region_name):
    regions = {
        'US East (N. Virginia)': 'us-east-1',
        'US East (Ohio)': 'us-east-2',
        'US West (N. California)': 'us-west-1',
        'US West (Oregon)': 'us-west-2',
        'Canada (Central)': 'ca-central-1',
        'EU (Frankfurt)': 'eu-central-1',
        'EU (Ireland)': 'eu-west-1',
        'EU (London)': 'eu-west-2',
        'EU (Paris)': 'eu-west-3',
        'Asia Pacific (Tokyo)': 'ap-northeast-1',
        'Asia Pacific (Seoul)': 'ap-northeast-2',
        'Asia Pacific (Osaka-Local)': 'ap-northeast-3',
        'Asia Pacific (Singapore)': 'ap-southeast-1',
        'Asia Pacific (Sydney)': 'ap-southeast-1',
        'Asia Pacific (Mumbai)': 'ap-south-1',
        'South America (Sao Paulo)': 'sa-east-1',
        'AWS GovCloud (US-East)': 'us-gov-east-1',
        'AWS GovCloud (US)': '	us-gov-west-1'
    }

    return regions[region_name]

def map_storage_class_name_to_code(class_name):
    classes = {
        'One Zone - Infrequent Access': 'ONEZONE_IA',
        'Standard - Infrequent Access': 'STANDARD_IA',
        'Amazon Glacier': 'GLACIER',
        'Standard': 'STANDARD',
        'Reduced Redundancy': 'RRS'
    }

    return classes[class_name]