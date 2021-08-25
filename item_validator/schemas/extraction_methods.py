"""Schema module."""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

from item_validator.schemas.pre_processors import *
from item_validator.schemas.pst_processors import *

header_schema = {
    'type': 'dict',
    'schema': {
        'name': {
            'required': True,
            'type': 'string',
            'regex': 'header_extract'
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'dependencies': 'name',
            'required': True,
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
            'required': True,
            'type': 'string',
            'regex': 'regex',
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'dependencies': 'name',
            'type': 'dict',
            'schema': {
                'regex': {
                    'type': 'string',
                }
            }
        },
        'pre_processors': {
            'dependencies': ['name', 'inputs'],
            'type': 'list',
            'schema': {
                'anyof': [
                    filename_reducer_schema,
                    ceda_observation_schema,
                ]
            }
        },
        'post_processors': {
            'dependencies': ['name', 'inputs'],
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
            'required': True,
            'type': 'string',
            'regex': 'iso19115'
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'dependencies': 'name',
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
            'dependencies': ['name', 'inputs'],
            'type': 'list',
            'schema': {
                'anyof': [
                    filename_reducer_schema,
                    ceda_observation_schema,
                ]
            }
        },
        'post_processors': {
            'dependencies': ['name', 'inputs'],
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
            'required': True,
            'type': 'string',
            'regex': 'xml_extract',
        },
        'description': {
            'type': 'string'
        },
        'inputs': {
            'dependencies': 'name',
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
