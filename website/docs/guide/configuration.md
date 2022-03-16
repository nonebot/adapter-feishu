---
sidebar_position: 3
description: 配置访问令牌、签名

options:
  menu:
    weight: 30
    category: guide
---

# 在 NoneBot 配置中添加相应配置

在 `.env` 文件中添加以下配置

```
APP_ID=<yourAppId>
APP_SECRET=<yourAppSecret>
VERIFICATION_TOKEN=<yourVerificationToken>
```

复制所创建应用**“凭证和基础信息”**中的 **App ID** 、 **App Secret** 和 **“事件订阅”** 中的 **Verification Token** ，替换上面相应的配置的值。

此外，对于飞书平台的事件订阅加密机制，飞书适配器也提供 `ENCRYPT_KEY` 配置项。

```
ENCRYPT_KEY=<yourEncryptKey>
```

当此项不为空时，飞书适配器会认为用户启用了加密机制，并对事件上报中的密文进行解密。

对于[Lark(飞书平台海外版)](https://www.larksuite.com) 的用户，飞书适配器也提供**实验性**支持，仅需要在配置文件中添加 `IS_LARK=true` 即可。

```
IS_LARK=true
```
