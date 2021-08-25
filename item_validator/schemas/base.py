from item_validator.schemas.extraction_methods \
    import header_schema, regex_schema, iso_schema, xml_schema

base_schema = {
    'datasets': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    },
    'categories': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'label': {
                    'type': 'string'
                },
                'regex': {
                    'type': 'string'
                }
            }
        }
    },
    'defaults': {
        'type': 'dict',
        'schema': {
            'collection_id': {
                'type': 'string'
            },
            'properties': {
                'type': 'dict',
                'schema': {
                    'datacentre': {
                        'type': 'string'
                    }
                }
            },
            'license': {
                'type': 'string'
            }
        }
    },
    'facets': {
        'type': 'dict',
        'dependencies': 'defaults',
        'schema': {
            'allowed_facets': {
                'type': 'list',
                'schema': {
                    'type': 'string'
                }
            },
            'extraction_methods': {
                'type': 'list',
                'schema': {
                    'anyof': [
                        header_schema,
                        regex_schema,
                        iso_schema,
                        xml_schema,
                    ]
                }
            },
            'aggregation_facets': {
                'type': 'list',
                'schema': {
                    'type': 'string'
                }
            }
        }
    }
}
