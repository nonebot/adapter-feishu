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

```python
from nonebot.adapters.feishu import Bot as FeishuBot

driver.register_adapter("feishu", FeishuBot)
```
