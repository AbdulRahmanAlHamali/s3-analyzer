import boto3
try:
    from . import utils
except Exception:
    import utils

class BucketAnalyzer:

    def __init__(self, bucket_name, filters, grouping, size_unit, prefix):
        self.bucket_name = bucket_name
        self.filters = filters
        self.grouping = grouping
        self.size_unit = size_unit
        self.info_list = []
        self.grouped_info = None
        self.prefix = '' if prefix is None else prefix

    def build_info(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)

        for object in bucket.objects.filter(Prefix=self.prefix):
            object_info = dict()

            object_info['key'] = object.key

            object_info['size'] = utils.convert_size(float(object.size), self.size_unit)

            object_info['last_modified'] = object.last_modified.strftime("%Y-%m-%d %H:%M:%S")

            object_info['storage_class'] = object.storage_class

            self.info_list.append(object_info)

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

