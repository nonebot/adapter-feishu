---
sidebar_position: 2
description: 配置连接

options:
  menu:
    - category: guide
      weight: 30
---

# 配置连接

## 创建应用与启用应用“机器人”能力

:::tip 提示
此部分可参考[飞书开放平台-快速开发机器人-创建应用](https://open.feishu.cn/document/home/develop-a-bot-in-5-minutes/create-an-app)部分的文档。

:::

## 在 NoneBot 配置文件中添加相应配置

复制所创建应用**“凭证和基础信息”**中的 **App ID** 、 **App Secret** 和 **“事件订阅”** 中的 **Verification Token** ，替换以下配置模板中的值。

如果在飞书开发者后台的事件订阅中配置了事件上报的 Encrypt Key，也需要传入 FEISHU_BOTS 中。

当 `encrypt_key` 存在且不为空时，飞书适配器会认为用户启用了加密机制，并对事件上报中的密文进行解密。

如果不需要启用加密功能，请将配置项中的 `encrypt_key` 键值对删去，或将 `encrypt_key` 置为 `null`。

对于[Lark(飞书平台海外版)](https://www.larksuite.com) 的用户，飞书适配器也提供**实验性**支持，仅需要在配置文件中将 `is_lark` 改为 `true`。

```bash
FEISHU_BOTS='
[
  {
    "app_id": "<your app_id>",
    "app_secret": "<your app_secret>",
    "verification_token": "<your app_verification_token>",
    "encrypt_key": "<your encrypt_key>",
    "is_lark": false
  }
]
'
```

飞书适配器支持同时传入多份配置，仅需要按相同格式传入 `FEISHU_BOTS` 即可。

```bash
FEISHU_BOTS='
[
  {
    "app_id": "<your app_id>",
    "app_secret": "<your app_secret>",
    "verification_token": "<your app_verification_token>",
    "encrypt_key": "<your encrypt_key>",
    "is_lark": false
  },
  {
    "app_id": "<your app_id2>",
    "app_secret": "<your app_secret2>",
    "verification_token": "<your app_verification_token2>",
    "encrypt_key": "<your encrypt_key>",
    "is_lark": false
  }
]
```

## 开启应用权限

应用拥有所需权限后，才能调用飞书接口获取相关信息。如果需要用到所有飞书平台的 API，请开启所有应用权限。

在仅群聊功能的情况下，需要为应用开启用户、消息、通讯录和群聊权限组所有权限，并且启用机器人角色以便获取机器人昵称。

## 配置飞书事件订阅

### 配置上报地址

飞书适配器会自动注册以下地址作为事件订阅上报入口点。

由于飞书开放平台的事件订阅并不会上报 App ID，在填写事件订阅请求网址时，请按照如下格式填写，对应的以 `$` 开头的变量请使用 `.env.*` 文件中所定义的值进行替换，`$app_id` 替换为飞书开放平台提供的 App ID。

```bash
http://$HOST:$PORT/feishu/$app_id
```

### 配置事件订阅列表

:::tip 提示

在添加事件订阅时请注意，带有**（历史版本）**字样的事件的格式为**不受支持的旧版事件格式**，请使用对应的**新版事件（不带历史版本字样）作为替代**。

:::

## 编写一个适用于飞书适配器的插件并加载

插件代码范例：

```python
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.feishu import Bot as FeishuBot, MessageEvent

helper = on_command("say")


@helper.handle()
async def feishu_helper(
    bot: FeishuBot,
    event: MessageEvent,
    state: T_State,
    command_arg: Message = CommandArg(),
):
    await helper.finish(command_arg, at_sender=True)
```

以上代码注册了一个对飞书平台适用的 `say` 指令，并会提取 `/say` 之后的内容发送到事件所对应的群或私聊。

大功告成！现在可以试试向机器人发送类似 `/say Hello, Feishu!` 的消息进行测试了。
