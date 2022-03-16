---
sidebar_position: 1
description: 安装

options:
  menu:
    weight: 10
    category: guide
---

# 安装飞书适配器

```bash
pip install nonebot-adapter-feishu
```

## 注册飞书适配器

在 `bot.py` 中添加：

```python title=bot.py {2,7}
import nonebot
from nonebot.adapters.feishu import Adapter as FeishuAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(FeishuAdapter)
```
