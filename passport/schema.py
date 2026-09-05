"""Small strict schema vocabulary; all supported keywords are enforced."""
import json
import re
from pathlib import Path

class Invalid(ValueError):
    pass

def validate(value, schema, path="$"):
    kinds = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}
    kind = schema["type"]
    if type(value) is not kinds[kind]:
        raise Invalid(f"{path}: expected {kind}")
    if "enum" in schema and value not in schema["enum"]:
        raise Invalid(f"{path}: unsupported value")
    if kind == "object":
        props = schema["properties"]
        if schema.get("additionalProperties") is False and set(value) - set(props):
            raise Invalid(f"{path}: unknown fields {sorted(set(value)-set(props))}")
        if set(schema.get("required", [])) - set(value):
            raise Invalid(f"{path}: required fields missing")
        for key, item in value.items():
            if key in props:
                validate(item, props[key], path+"."+key)
    if kind == "array":
        if len(value) > schema.get("maxItems", 1000):
            raise Invalid(f"{path}: too many items")
        for i, item in enumerate(value):
            validate(item, schema["items"], f"{path}[{i}]")
    if kind == "string":
        if not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", 10000):
            raise Invalid(f"{path}: invalid length")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            raise Invalid(f"{path}: invalid format")
    if kind == "integer" and not schema.get("minimum", 0) <= value <= schema.get("maximum", 1000000000000):
        raise Invalid(f"{path}: outside limits")
    return value

def load_schema(name):
    return json.loads((Path(__file__).parent/"schemas"/(name+".json")).read_text())

def check(name, value):
    return validate(value, load_schema(name))

def parse(text):
    if len(text.encode()) > 1000000:
        raise Invalid("JSON exceeds 1 MB")
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise Invalid("duplicate JSON key")
            result[k] = v
        return result
    try:
        return json.loads(text, object_pairs_hook=pairs)
    except (ValueError, RecursionError) as exc:
        raise Invalid("Invalid JSON") from exc
