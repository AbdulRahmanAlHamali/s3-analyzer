import boto3
try:
    from . import utils
except Exception:
    import utils
import math
from ast import literal_eval


class GlobalAnalyzer:

    def __init__(self, filters, grouping, size_unit):
        self.filters = filters
        self.grouping = grouping
        self.size_unit = size_unit
        self.info_list = []
        self.grouped_info = None

    def build_info(self):

        pricing_info = self._prepare_pricing_info()

        s3 = boto3.resource('s3')

        for bucket in s3.buckets.all():
            bucket_info = dict()

            bucket_info['name'] = bucket.name

            bucket_info['creation_date'] = bucket.creation_date.strftime("%Y-%m-%d %H:%M:%S")

            bucket_info['number_of_files'] = int(sum(1 for _ in bucket.objects.all()))

            bucket_info['total_size'] = float(sum(o.size for o in bucket.objects.all()))
            bucket_info['total_size'] = utils.convert_size(bucket_info['total_size'], self.size_unit)

            bucket_info['last_modified'] = max(bucket.objects.all(), key=lambda o: o.last_modified, default=None)
            if bucket_info['last_modified'] is None:
                bucket_info['last_modified'] = bucket_info['creation_date']
            else:
                bucket_info['last_modified'] = bucket_info['last_modified'].last_modified.strftime("%Y-%m-%d %H:%M:%S")

            bucket_info['location'] = s3.meta.client.get_bucket_location(Bucket=bucket.name)['LocationConstraint']

            bucket_info['cost'] = self._get_bucket_cost(bucket, pricing_info, bucket_info['location'])

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

    def _get_bucket_cost(self, bucket, pricing_info, bucket_location):

        total_by_storage_class = dict()

        for object in bucket.objects.all():
            storage_class = object.storage_class
            if storage_class not in total_by_storage_class:
                total_by_storage_class[storage_class] = 0
            total_by_storage_class[storage_class] += object.size

        cost = 0

        for storage_class, size in total_by_storage_class.items():
            class_pricing_info = pricing_info[storage_class][bucket_location]

            for price_range in class_pricing_info:
                if size >= price_range['begin_range'] and size < price_range['end_range']:
                    cost += price_range['price'] * size / (1024 * 1024 * 1024)
                    break

        return cost

    def _prepare_pricing_info(self):
        # for some reason only the us-east-1 pricing endpoint is working
        pricing = boto3.client('pricing', 'us-east-1')

        volumeTypesResponse = pricing.get_attribute_values(
            ServiceCode='AmazonS3',
            AttributeName='volumeType'
        )

        volumeTypes = list(map(lambda x: x['Value'], volumeTypesResponse['AttributeValues']))
        volumeTypes = list(filter(lambda x: x != 'Tags', volumeTypes))

        result = dict()
        for volumeType in volumeTypes:
            price = pricing.get_products(
                ServiceCode='AmazonS3',
                Filters=[
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'volumeType',
                        'Value': volumeType
                    }
                ]
            )

            storage_class = utils.map_storage_class_name_to_code(volumeType)

            result[storage_class] = dict()
            for entry in price['PriceList']:
                # because we receive it as a string
                entry = literal_eval(entry)

                location = entry['product']['attributes']['location']
                location_code = utils.map_region_name_to_code(location)

                options = next(iter(entry['terms']['OnDemand'].values()))['priceDimensions']

                resulting_options = []
                for _, option in options.items():
                    resulting_options.append({
                        'begin_range': int(option['beginRange']),
                        'end_range': math.inf if option['endRange'] == 'Inf' else int(option['endRange']),
                        'price': float(option['pricePerUnit']['USD'])
                    })

                result[storage_class][location_code] = resulting_options

        return result
