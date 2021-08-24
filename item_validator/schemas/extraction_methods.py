"""Schema module."""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import item_validator.schemas.pre_processors as pre_processors
import item_validator.schemas.pst_processors as pst_processors

filename_reducer_schema = pre_processors.filename_reducer_schema

isodate_schema = pst_processors.isodate_schema
string_join_schema = pst_processors.string_join_schema

header_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'type': 'dict',
            'schema': {
                'attributes': {
                    'type': 'list',
                    'schema': {
                        'type': 'string'
                    }
                }
            }
        }
    }
}

regex_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'type': 'dict',
            'schema': {
                'regex': {
                    'type': 'string'
                }
            }
        },
        'pre_processors': {
            'type': 'list',
            'schema': {
                'anyof': [
                    filename_reducer_schema,
                ]
            }
        },
        'post_processors': {
            'type': 'list',
            'schema': {
                'anyof': [
                    isodate_schema,
                    string_join_schema,
                ]
            }
        },
    }
}

iso_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'type': 'dict',
            'schema': {
                'url_template': {
                    'type': 'string'
                },
                'extraction_keys': {
                    'type': 'dict',
                    'schema': {
                        'name': {
                            'type': 'string'
                        },
                        'key': {
                            'type': 'string'
                        }
                    }
                }
            }
        },
        'pre_processors': {
            'type': 'list',
            'schema': {
                'anyof': [
                    filename_reducer_schema,
                ]
            }
        },
        'post_processors': {
            'type': 'list',
            'schema': {
                'anyof': [
                    isodate_schema,
                    string_join_schema,
                ]
            }
        },
    }
}

xml_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'type': 'dict',
            'schema': {
                'filter_expr': {
                    'type': 'string'
                },
                'extraction_keys': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string'
                            },
                            'key': {
                                'type': 'string'
                            },
                            'attribute': {
                                'type': 'string'
                            }
                        }
                    }
                },
                'namespaces': {
                    'type': 'dict',
                    'allow_unknown': True,
                },
            }
        }
    }
}
