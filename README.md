# Elasticsearch Vectra Exporter

Python utility library to send Vectra detections to Elasticsearch

## File structure

```
.
├── README.md                   | This file
├── __init__.py                 | The main Python class file
├── ecs_mapping.csv             | CSV file that contains the mapping data
├── mapping.py                  | Utility file for handling mapping functions
├── searching.py                | Utility file for searching/traversing detections
├── reference                   | 
│   ├── all_ecs_fields.csv      | All of the possible ECS fields to map to
│   ├── all_vectra_fields.md    | All of the Vectra key/value combinations
│   └── index_template.json     | Index template data to import into Elastic
└── tests                       |
    ├── __init__.py             | (empty file)
    └── remapping_test.py       | Pytest unit test file
```

## Adding the index template to Elastic

The index template JSON file is located in the `reference` folder. You can take that JSON and use the following PUT request in Kibana `Management > Dev Tools` to send it to your Elastic instance (or use something like curl/Postman):

```
PUT _index_template/vectra-ecs
{
  "template": {
    "mappings": {
      "_routing": {
        "required": false
      },
...
```

## Setting up the connection

First make an ElasticVectraExporter object. There are two ways to do this depending on whether or not you're using Elastic Cloud or self-hosted Elastic.

Self-hosted:

```python
client = elastic_vectra_lib.ElasticVectra(host="https://elastic_url:9200", username="user_here", password="password_here")
```

Elastic Cloud:

```python
client = elastic_vectra_lib.ElasticVectra(cloud_id="XXXXX", username="user_here", password="password_here")
```

For development environments, you may also use `verify_certs=False` as a parameter when SSL verification is not set up yet.

Once this is setup you can test the connection with Elastic by running the following:

```python
print(client.get_info())
```

You should see output similar to the following:

```json
{
    "name": "elastic_name",
    "cluster_name": "elastic_cluster",
    "cluster_uuid": "_XXXXXXXXXXX",
    "version": {
        "number": "X.X.X",
        "build_type": "XXXXX",
        "build_hash": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "build_date": "1969-01-01T15:15:15.901688194Z",
        "build_snapshot": false,
        "lucene_version": "X.X.X",
        "minimum_wire_compatibility_version": "X.XX.X",
        "minimum_index_compatibility_version": "X.X.X"
    },
    "tagline": "You Know, for Search"
}
```

If you see this, you are ready to send detections.

## Sending detections

WIP
