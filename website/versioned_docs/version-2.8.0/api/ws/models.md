# nonebot.adapters.feishu.ws.models

WebSocket 相关 API 响应模型。

## _enum_ `FrameType` {#FrameType}

- **说明:** 帧类型。

- **参数**

  auto

  - `CONTROL: 0`

  - `DATA: 1`

## _class_ `MessageType(<auto>)` {#MessageType}

- **说明:** 消息类型字符串。

- **参数**

  auto

## _class_ `FrameSegment(<auto>)` {#FrameSegment}

- **说明:** 分片消息片段，用于重组。

- **参数**

  auto

## _class_ `WsEndpointClientConfig(<auto>)` {#WsEndpointClientConfig}

- **说明:** WebSocket 端点返回的 ClientConfig，字段与 API 驼峰命名一致。

- **参数**

  auto

## _class_ `WsEndpointData(<auto>)` {#WsEndpointData}

- **说明:** WebSocket 端点 API 的 data 字段。

- **参数**

  auto

## _class_ `WsEndpointApiResponse(<auto>)` {#WsEndpointApiResponse}

- **说明:** 获取 WebSocket 端点 API 的完整响应。

- **参数**

  auto

## _class_ `WsEndpointResponse(<auto>)` {#WsEndpointResponse}

- **说明**

  解析后的 WebSocket 端点结果，供客户端使用。

  device_id 与 service_id 从 data.URL 的查询参数中解析得到。

- **参数**

  auto
