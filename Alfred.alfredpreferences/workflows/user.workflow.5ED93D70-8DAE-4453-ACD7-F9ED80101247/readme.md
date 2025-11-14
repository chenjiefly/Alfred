# alfred-http-codes [![Build Status](https://travis-ci.org/chenjiefly/alfred-http-codes.svg?branch=master)](https://travis-ci.org/chenjiefly/alfred-http-codes)

> HTTP状态码查询 Alfred Workflow

## 功能特性

- 🔍 快速查询HTTP状态码
- 🌐 支持中英文状态码名称和详细描述
- 📖 直接跳转到MDN官方文档
- 🎯 支持精确匹配和模糊搜索
- ✨ 友好的错误提示和使用指导

## 安装

```
$ npm install --global alfred-http-codes
```

*需要 [Node.js](https://nodejs.org) 4+ 和 Alfred [Powerpack](https://www.alfredapp.com/powerpack/).*

## 使用方法

在Alfred中输入 `http`，然后输入HTTP状态码进行查询。

### 示例

- `http 200` - 查询200状态码
- `http 404` - 查询404状态码  
- `http 50` - 模糊搜索所有包含"50"的状态码

### 支持的状态码

#### 1xx 信息响应
- 100 Continue (继续)
- 101 Switching Protocols (切换协议)
- 102 Processing (处理中)

#### 2xx 成功响应
- 200 OK (成功)
- 201 Created (已创建)
- 202 Accepted (已接受)
- 204 No Content (无内容)
- 206 Partial Content (部分内容)
- 等等...

#### 3xx 重定向
- 301 Moved Permanently (永久移动)
- 302 Found (临时移动)
- 304 Not Modified (未修改)
- 307 Temporary Redirect (临时重定向)
- 等等...

#### 4xx 客户端错误
- 400 Bad Request (错误请求)
- 401 Unauthorized (未授权)
- 403 Forbidden (禁止访问)
- 404 Not Found (未找到)
- 418 I'm a teapot (我是茶壶)
- 429 Too Many Requests (请求过多)
- 等等...

#### 5xx 服务器错误
- 500 Internal Server Error (内部服务器错误)
- 502 Bad Gateway (错误网关)
- 503 Service Unavailable (服务不可用)
- 504 Gateway Timeout (网关超时)
- 等等...

## 输出格式

选择状态码后会自动跳转到对应的MDN文档页面：
`https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/{状态码}`

## 许可证

MIT © [子泷](https://github.com/chenjiefly/Alfred)
