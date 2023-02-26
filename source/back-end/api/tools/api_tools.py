from .constants import CURRENT_VERSION as __version, ENVIRONMENT as __env
from django.conf import settings
from PIL import Image

version = f'v{__version}'
num_version = __version
environment = __env.get('long_desc', 'Unknown')


def generate_version() -> str:
    return f'v{__version} [{__env.get("short_desc", "?")}]'


def resize_image(img, new_width):
    img_path = settings.MEDIA_ROOT.joinpath(img.name)
    img = Image.open(img_path)
    width, height = img.size
    new_height = round((new_width * height) / width)

    if width <= new_width:
        img.close()
        return

    new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    new_img.save(
        img_path,
        optimize=True,
        quality=60
    )
    new_img.close()


def description_generator(title: str, description: str | None = None, responses: dict[str, dict[str, str]] | None = None) -> str:
    """
    Response struct:
        {
            "200": {
                "description": "ok",
                "reason": "all ok"
            }
        }
    """
    desc = f"""# {title}"""
    desc += "\n---"
    if description:
        desc += f"\n {description}"
        desc += "\n---"

    if responses:
        desc += "\n## The below table defines the HTTP Status codes that this API may return"
        desc += "\n| Status Code | Description | Reason |"
        desc += "\n| ----------- | ----------- | ------ |"
        for response_code in responses.keys():
            response = responses[response_code]
            code_col = f"| {response_code} "
            desc_col = f"| {response.get('description', 'None')} "
            reas_col = f"| {response.get('reason', 'None')} |"
            resp_str = f"\n{code_col}{desc_col}{reas_col}"
            desc += resp_str

    return desc
