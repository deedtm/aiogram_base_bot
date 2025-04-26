import json
import importlib as il
import re
from dataclasses import make_dataclass, dataclass
from typing import Optional
from time import sleep
from os import path as p
from os import makedirs


files_imports: dict[str, list] = {}


def mkdir_with_init(dir_path: str, exist_ok: bool = True) -> None:
    makedirs(dir_path, exist_ok=exist_ok)
    init_file = p.join(dir_path, "__init__.py")
    if not p.exists(init_file):
        with open(init_file, "w", encoding="utf-8") as f:
            pass  # создаёт пустой файл


def init_class_template(filepath: str):
    with open(filepath) as f:
        data = json.load(f)

    kwargs = {p.basename(filepath).split(".")[0]: data}
    datacls_path = p.join(p.dirname(filepath), "enums")
    cls, filename = to_dataclass(datacls_path, **kwargs)
    export_dataclass(cls, datacls_path, filename)
    return cls


def to_dataclass(datacls_path: Optional[str] = __file__, **cls):
    global files_imports

    var_name = next(name for name in cls.keys())
    class_name = "".join(word.capitalize() for word in var_name.lower().split("_"))

    fields = []
    attributes = list(cls.values())[0]
    for name, value in attributes.items():
        if isinstance(value, dict):
            cls_name = "".join(word.capitalize() for word in name.split("_"))
            datacls, imports = to_dataclass(**{name: value})
            mod_dir = "mod_" + var_name
            path = p.join(datacls_path, mod_dir)
            export_dataclass(datacls, path, imports)
            sleep(1)
            mod = il.import_module(f".enums.{mod_dir}.{name}", package="templates")
            value = getattr(mod, cls_name)()
            if not var_name in files_imports:
                files_imports.update({var_name: []})
            imports = files_imports[var_name]
            imports.append(f"from .{mod_dir}.{name} import {cls_name}")
        fields.append((name, type(value), value))

    return make_dataclass(class_name, fields), var_name


def export_dataclass(cls, base_path: str, general_filename: str):
    anns = getattr(cls, "__annotations__", {})
    lines = [
        f"\t{name}: {typ.__name__} = {repr(getattr(cls, name))}"
        for name, typ in anns.items()
    ]
    imports = files_imports.get(general_filename, [])
    body = "\n".join(lines) if lines else "    pass"
    src = (
        "from dataclasses import dataclass\n"
        + "\n".join(imports)
        + f"\n\n@dataclass\nclass {cls.__name__}:\n"
        f"{body}\n"
    )

    filename = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower() + ".py"
    filepath = p.join(base_path, filename)
    mkdir_with_init(p.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(src)
