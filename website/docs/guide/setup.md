---
sidebar_position: 2
description: 配置连接

options:
  menu:
    weight: 20
    category: guide
---

# 配置连接

## 创建应用与启用应用“机器人”能力

::: tip
此部分可参考[飞书开放平台-快速开发机器人-创建应用](https://open.feishu.cn/document/home/develop-a-bot-in-5-minutes/create-an-app)部分的文档。

:::

## 开启应用权限

应用拥有所需权限后，才能调用飞书接口获取相关信息。如果需要用到所有飞书平台的 API，请开启所有应用权限。

在仅群聊功能的情况下，需要为应用开启用户、消息、通讯录和群聊权限组所有权限。

## 配置飞书事件订阅

::: tip

在添加事件订阅时请注意，带有**（历史版本）**字样的事件的格式为**不受支持的旧版事件格式**，请使用对应的**新版事件（不带历史版本字样）作为替代**。

:::

目前，飞书适配器支持以下事件：
| 事件名称 | 事件描述|
| ---- | ---- |
|接收消息|机器人接收到用户发送的消息。|
|消息已读|用户阅读机器人发送的单聊消息。|
|群解散|群组被解散。|
|群配置更改|群组配置被修改后触发此事件，包含：群主转移、群基本信息修改、群权限修改。|
|机器人进群|机器人被添加至群聊。|
|机器人被移出群|机器人被移出群聊。|
|用户进群|新用户进群。|
|撤销拉用户进群|撤销拉用户进群。|
|用户被移出群|用户主动退群或被移出群聊。|

## 编写一个适用于飞书适配器的插件并加载

插件代码范例：

```python
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.feishu import Bot as FeishuBot, MessageEvent

helper = on_command("say")


@helper.handle()
async def feishu_helper(bot: FeishuBot, event: MessageEvent, state: T_State):
    message = event.get_message()
    await helper.finish(message, at_sender=True)
```

以上代码注册了一个对飞书平台适用的`say`指令，并会提取`/say`之后的内容发送到事件所对应的群或私聊。

大功告成！现在可以试试向机器人发送类似`/say Hello, Feishu!`的消息进行测试了。
