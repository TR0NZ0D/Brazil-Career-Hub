__environments = {
    0: {
        'long_desc': 'Unknown',
        'short_desc': '?'
    },
    1: {
        'long_desc': 'Development',
        'short_desc': 'Dev'
    },
    2: {
        'long_desc': 'Production',
        'short_desc': 'Prod'
    }
}

CURRENT_VERSION = '0.0.1'
ENVIRONMENT = __environments.get(1, {})
