from typing import get_args

def build_tree(model, indent: int = 0) -> str:
    """모델 구조를 트리 형태 문자열로 반환"""
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