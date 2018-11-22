import argparse
from global_analyzer import GlobalAnalyzer
from bucket_analyzer import BucketAnalyzer


def main_bucket(args):
    analyzer = BucketAnalyzer(bucket_name=args.bucket_name,
                              filters=args.filter,
                              grouping=args.group_by,
                              size_unit=args.size_unit,
                              prefix=args.prefix)
    analyzer.build_info()
    print(analyzer.get_string_info())


def main_global(args):
    analyzer = GlobalAnalyzer(filters=args.filter, grouping=args.group_by, size_unit=args.size_unit)
    analyzer.build_info()
    print(analyzer.get_string_info())


if __name__ == '__main__':

    def transform_filters(filters):
        result = []
        for f in filters:
            if f[1] not in ['eq', 'regex', 'gt', 'lt']:
                raise Exception('operation "{}" used to filter property "{}" is not defined'.format(f[1], f[0]))
            result.append(dict(property=f[0], operation=f[1], value=f[2]))

        return result

    parser = argparse.ArgumentParser(description='S3 bucket analyzer')
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'sub-command'

    # bucket parser
    parser_bucket = subparsers.add_parser('bucket', help='Get detailed information of a specific bucket')
    parser_bucket.add_argument('bucket_name', help='The name of the bucket to analyze')
    parser_bucket.add_argument('-gb', '--group-by', default=None, choices=['storage_class', 'encryption_type'],
                               help='Options to group files by. Leave empty to show everything in one list')
    parser_bucket.add_argument('-f', '--filter', action='append', nargs=3, metavar=('property', 'comparator', 'value'),
                               help='filter the results. You can add multiple filters. The comparator can be one of: '
                                    + 'eq (equals), regex (matches regex), gt (greater than), lt (less than)')
    parser_bucket.add_argument('-su', '--size-unit', default='B', choices=['B', 'KB', 'MB', 'GB', 'TB'],
                               help='the size unit')
    parser_bucket.add_argument('-p', '--prefix', default=None,
                               help='only gets the objects that start with this prefix. '
                                    + 'This is different from filters in that filters fetch all the data but then '
                                    + 'filter it, while prefix only fetches the data that starts with that prefix')

    parser_bucket.set_defaults(func=main_bucket)

    # global parser
    parser_global = subparsers.add_parser('global', help='Get summarized information of all your buckets')
    parser_global.add_argument('-gb', '--group-by', default=None, choices=['location'],
                               help='Options to group buckets by. Leave empty to show everything in one list')
    parser_global.add_argument('-f', '--filter', action='append', nargs=3, metavar=('property', 'comparator', 'value'),
                               help='filter the results. You can add multiple filters. The comparator can be one of: '
                                    + 'eq (equals), regex (matches regex), gt (greater than), lt (less than)')
    parser_global.add_argument('-su', '--size-unit', default='B', choices=['B', 'KB', 'MB', 'GB', 'TB'],
                               help='the size unit')

    parser_global.set_defaults(func=main_global)

    ########################
    args = parser.parse_args()
    if args.filter is not None:
        try:
            args.filter = transform_filters(args.filter)
        except Exception as e:
            parser.error(e)

    args.func(args)

