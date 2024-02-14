---
description: Changelog
toc_max_heading_level: 2
---

# 更新日志

## v2.4.0

### 🚀 新功能

- Feat: 添加 pydantic v2 兼容支持 [@he0119](https://github.com/he0119) ([#94](https://github.com/nonebot/adapter-feishu/pull/94))

### 💫 杂项

- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#93](https://github.com/nonebot/adapter-feishu/pull/93))

## v2.3.2

### 🐛 Bug 修复

- Fix: 序列化消息时检查消息长度 [@StarHeartHunt](https://github.com/StarHeartHunt) ([#89](https://github.com/nonebot/adapter-feishu/pull/89))

### 💫 杂项

- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#86](https://github.com/nonebot/adapter-feishu/pull/86))
- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#84](https://github.com/nonebot/adapter-feishu/pull/84))
- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#82](https://github.com/nonebot/adapter-feishu/pull/82))

## v2.1.1

### 💫 杂项

- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#79](https://github.com/nonebot/adapter-feishu/pull/79))

## v2.0.2

### 🚀 新功能

- Feat: 更新平台消息段参数 [@StarHeartHunt](https://github.com/StarHeartHunt) ([#75](https://github.com/nonebot/adapter-feishu/pull/75))

### 💫 杂项

- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#73](https://github.com/nonebot/adapter-feishu/pull/73))

## v2.0.1

### 🐛 Bug 修复

- Fix: 删除过时的 `bot.type` 定义及更新 `bot.__init__` 签名 [@StarHeartHunt](https://github.com/StarHeartHunt) ([#67](https://github.com/nonebot/adapter-feishu/pull/67))

### 💫 杂项

- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#65](https://github.com/nonebot/adapter-feishu/pull/65))

## v2.0.0

### 💫 杂项

- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#52](https://github.com/nonebot/adapter-feishu/pull/52))

## v2.0.0-beta.8

### 💫 杂项

- :arrow_up: auto update by pre-commit hooks [@pre-commit-ci](https://github.com/pre-commit-ci) ([#36](https://github.com/nonebot/adapter-feishu/pull/36))

## v2.0.0-beta.7

### 🐛 Bug 修复

- Bug: feishu `at_sender` param in group chat fail to work

## v2.0.0b3

- 修复适配器启动时 Authorization 头构造问题

## v2.0.0b2

- 添加多 Bot 实例支持，对应修改了配置格式
- 修复过期 Token 的缓存问题
