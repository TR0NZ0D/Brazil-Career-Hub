from .constants import CURRENT_VERSION as __version, ENVIRONMENT as __env

version = f'v{__version}'
environment = __env.get('long_desc', 'Unknown')


def generate_version() -> str:
    return f'v{__version} [{__env.get("short_desc", "?")}]'
