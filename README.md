# S3 Analyzer

This package is an analyzer for Amazon S3 consumption developed in Python3

## Installation

## Usage

The analyzer has two modes:

### Global mode:

This mode allows you to see information about all your S3 buckets. You can access the global mode like this:

```
python s3_analyzer global
```

The global analyzer supports the following options:

| Short Name | Long Name  | Description | Possible Values  | Default Value  | 
|------------|------------|---|---|---|
| -gb        | --group-by | Options to group buckets by. Leave empty to show everything in one list  | location  | None  |
| -f         | --filter   | Filters the results. You can as many filters as you need. Each filter needs to look like:<br>`-f property comparator value`<br>For example:<br>`-f name regex buckets*`<br>The property can be one of:<br>* name<br>* creation_date<br>* number_of_files<br>* total_size<br>* last_modified<br>* location<br>The comparator can be one of:<br>* eq (equals)<br>* regex (matches regex)<br>* gt (greater than)<br>* lt (less than) |   |   |
| -su        | --size-unit| The unit to use for sizes | B, KB, MB, GB, TB  | B |

### Bucket mode:

This mode allows you to see information about a specific S3 bucket. You can access the bucket mode like this:

```
python s3_analyzer bucket bucket_name
```

Where `bucket_name` is the name of your bucket

The bucket analyzer supports the following options:

| Short Name | Long Name  | Description | Possible Values  | Default Value  | 
|------------|------------|---|---|---|
| -gb        | --group-by | Options to group files by. Leave empty to show everything in one list  | storage_class  | None  |
| -f         | --filter   | Filters the results. You can as many filters as you need. Each filter needs to look like:<br>`-f property comparator value`<br>For example:<br>`-f key regex some_file*`<br>The property can be one of:<br>* key<br>* size<br>* last_modified<br>* storage_class<br>The comparator can be one of:<br>* eq (equals)<br>* regex (matches regex)<br>* gt (greater than)<br>* lt (less than) |   |   |
| -su        | --size-unit| The unit to use for sizes | B, KB, MB, GB, TB  | B |
| -p         | --prefix   | only gets the objects that start with this prefix. This is different from filters in that filters fetch all the data but then filter it, while prefix only fetches the data that starts with that prefix | | None |
