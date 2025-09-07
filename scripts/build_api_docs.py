from pathlib import Path

from nb_autodoc import ModuleManager
from nb_autodoc.builders.markdown import MarkdownBuilder
from nb_autodoc.config import Config

import nonebot.adapters

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)

config = Config(output_dir=str((Path(__file__).parent.parent / "build").resolve()))
module = ModuleManager("nonebot.adapters.feishu", config=config)
builder = MarkdownBuilder(module)
builder.write()

for modname, path in builder.paths.items():
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("<factory>", ""), encoding="utf-8")
