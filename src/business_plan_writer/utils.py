from typing import get_args
from docxtpl import DocxTemplate
from pathlib import Path
from pydantic import BaseModel

def build_tree(model: type[BaseModel], indent: int = 0) -> str:
    lines = []
    for name, field in model.model_fields.items():
        type_ = field.annotation
        desc = field.description or ""
        prefix = "  " * indent + f"- {name} ({type_.__name__ if hasattr(type_, '__name__') else type_})"
        if desc:
            prefix += f": {desc}"
        lines.append(prefix)

        # Nested BaseModel
        if hasattr(type_, "model_fields"):
            lines.append(build_tree(type_, indent + 1))

        # List of BaseModel
        elif str(type_).startswith("list") and hasattr(get_args(type_)[0], "model_fields"):
            inner = get_args(type_)[0]
            lines.append(build_tree(inner, indent + 1))
    return "\n".join(lines)

def render_docx_template(template_path: str, context: dict, output_path: str | Path = Path("사업계획서.docx")) -> Path:
    template_path = Path(template_path)
    doc = DocxTemplate(template_path)

    doc.render(context)

    output_path = Path(output_path)
    doc.save(output_path)
    return output_path