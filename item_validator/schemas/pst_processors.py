
isodate_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string'
        },
        'inputs': {
            'type': 'dict',
            'schema': {
                'date_keys': {
                    'type': 'list',
                    'schema': {
                        'type': 'string'
                    }
                }
            }
        }
    }
}

string_join_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string'
        },
        'inputs': {
            'type': 'dict',
            'schema': {
                'key_list': {
                    'type': 'list',
                    'schema': {
                        'type': 'string'
                    }
                },
                'delimiter': {
                    'type': 'string'
                },
                'output_key': {
                    'type': 'string'
                }
            }
        }
    }
}
