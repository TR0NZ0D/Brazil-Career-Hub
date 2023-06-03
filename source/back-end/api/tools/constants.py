"""
api/tools/constants.py

Created by: Gabriel Menezes de Antonio
"""
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

CURRENT_VERSION = '0.0.2'
ENVIRONMENT = __environments.get(1, {})

SUPPORTED_LANGUAGES = (
    ('en-us', 'English'),
    ('pt-br', 'Português (Brasil)')
)

REGISTRATION_STATUS = (
    ('1', 'Null'),
    ('2', 'Active'),
    ('3', 'Suspended'),
    ('4', 'Inapt'),
    ('5', 'Active Not Regular'),
    ('8', 'Extinct')
)

LEGAL_NATURE = (
    ('EI', 'Empresário Individual (EI)'),
    ('EIRELI', 'Empresa Individual de Responsabilidade Limitada (EIRELI)'),
    ('SI', 'Sociedade Simples'),
    ('LTDA', 'Sociedade Empresária Limitada (LTDA)'),
    ('SA', 'Sociedade Anônima (SA)'),
    ('SLU', 'Sociedade Limitada Unipessoal (SLU)')
)

GENDERS = (
    ('NI', 'Not Informed'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('NB', 'Non Binary')
)

DEFAULT_COVER_COLOR = "#1488ac"  # TODO: Change default color after defining color pallete
DEFAULT_PRIMARY_COLOR = "#0b1524"  # TODO: Change default color after defining color pallete
DEFAULT_SECONDARY_COLOR = "#c7c7c5"  # TODO: Change default color after defining color pallete


def __get_str_table(const: tuple[tuple[str, str], ...]) -> str:
    string = "| Key | Description |"
    string += "\n| --- | ----------- |"
    for key, description in const:
        string += f'\n| {key} | {description} |'

    return string


supported_languages__str__: str = __get_str_table(SUPPORTED_LANGUAGES)
genders__str__: str = __get_str_table(GENDERS)
registration_status__str__: str = __get_str_table(REGISTRATION_STATUS)
legal_nature__str__: str = __get_str_table(LEGAL_NATURE)

supported_languages_keys: list[str] = [language[0] for language in SUPPORTED_LANGUAGES]
genders_keys: list[str] = [gender[0] for gender in GENDERS]
registration_status_keys: list[str] = [status[0] for status in REGISTRATION_STATUS]
legal_nature_keys: list[str] = [nature[0] for nature in LEGAL_NATURE]
