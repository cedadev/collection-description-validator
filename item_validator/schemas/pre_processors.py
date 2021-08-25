
filename_reducer_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string',
            'regex': 'filename_reducer'
        }
    }
}

ceda_observation_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string',
            'regex': 'ceda_observation'
        },
        'inputs': {
            'type': 'dict',
            'schema': {
                'url_template': {
                    'type': 'string'
                }
            }
        }
    }
}
