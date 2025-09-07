#!/usr/bin/env bash

set -e

# cd to the root of the project
cd "$(dirname "$0")/.."

nb-autodoc nonebot.adapters.feishu
cp -r ./build/nonebot/* ./website/docs/api/
yarn prettier
