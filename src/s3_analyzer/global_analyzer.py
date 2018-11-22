import boto3
import utils


class GlobalAnalyzer:

    def __init__(self, filters, grouping, size_unit):
        self.filters = filters
        self.grouping = grouping
        self.size_unit = size_unit
        self.info_list = []
        self.grouped_info = None

    def build_info(self):
        s3 = boto3.resource('s3')

        for bucket in s3.buckets.all():
            bucket_info = dict()

            bucket_info['name'] = bucket.name

            bucket_info['creation_date'] = bucket.creation_date.strftime("%Y-%m-%d %H:%M:%S")

            bucket_info['number_of_files'] = int(sum(1 for _ in bucket.objects.all()))

            bucket_info['total_size'] = int(sum(o.size for o in bucket.objects.all()))
            bucket_info['total_size'] = utils.convert_size(bucket_info['total_size'], self.size_unit)

            bucket_info['last_modified'] = max(bucket.objects.all(), key=lambda o: o.last_modified, default=None)
            if bucket_info['last_modified'] is None:
                bucket_info['last_modified'] = bucket_info['creation_date']
            else:
                bucket_info['last_modified'] = bucket_info['last_modified'].last_modified.strftime("%Y-%m-%d %H:%M:%S")

            bucket_info['location'] = s3.meta.client.get_bucket_location(Bucket=bucket.name)['LocationConstraint']

            self.info_list.append(bucket_info)

        if self.filters is not None:
            self.info_list = utils.run_filters(self.info_list, self.filters)

        if self.grouping is not None:
            self.grouped_info = utils.get_grouped_info(self.info_list, self.grouping)

    def get_string_info(self):

        if self.grouped_info is not None:
            str = ''
            for group, buckets in self.grouped_info.items():
                str += '* ' + group + '\n'
                str += utils.get_table_info(buckets) + '\n'

            return str
        else:
            return utils.get_table_info(self.info_list)

