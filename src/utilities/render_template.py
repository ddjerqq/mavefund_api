from __future__ import annotations

import os

from starlette.templating import _TemplateResponse

from src import PATH

from fastapi.templating import Jinja2Templates

TEMPLATES = Jinja2Templates(
    directory=os.path.join(PATH, "templates")
)


def render_template(
        name: str,
        context: dict,
        status_code: int = 200,
        headers: dict[str, str] = None,
        media_type: str | None = None
) -> "_TemplateResponse":
    """render a template from the "templates" folder.
    pass vars in the context kwarg, or pass as dict
    """
    return TEMPLATES.TemplateResponse(name, context, status_code, headers, media_type)
