'use strict';
const alfy = require('alfy');

// HTTP状态码数据映射
const httpCodes = {
	// 1xx 信息响应
	100: { name: 'Continue', nameCN: '继续', description: 'The server has received the request headers and the client should proceed to send the request body.' },
	101: { name: 'Switching Protocols', nameCN: '切换协议', description: 'The requester has asked the server to switch protocols and the server has agreed to do so.' },
	102: { name: 'Processing', nameCN: '处理中', description: 'The server has received and is processing the request, but no response is available yet.' },
	
	// 2xx 成功响应
	200: { name: 'OK', nameCN: '成功', description: 'The request has succeeded.' },
	201: { name: 'Created', nameCN: '已创建', description: 'The request has been fulfilled and resulted in a new resource being created.' },
	202: { name: 'Accepted', nameCN: '已接受', description: 'The request has been accepted for processing, but the processing has not been completed.' },
	203: { name: 'Non-Authoritative Information', nameCN: '非权威信息', description: 'The server successfully processed the request, but is returning information that may be from another source.' },
	204: { name: 'No Content', nameCN: '无内容', description: 'The server successfully processed the request and is not returning any content.' },
	205: { name: 'Reset Content', nameCN: '重置内容', description: 'The server successfully processed the request, but is not returning any content.' },
	206: { name: 'Partial Content', nameCN: '部分内容', description: 'The server is delivering only part of the resource due to a range header sent by the client.' },
	
	// 3xx 重定向
	300: { name: 'Multiple Choices', nameCN: '多种选择', description: 'Indicates multiple options for the resource that the client may follow.' },
	301: { name: 'Moved Permanently', nameCN: '永久移动', description: 'This and all future requests should be directed to the given URI.' },
	302: { name: 'Found', nameCN: '临时移动', description: 'The resource was found but at a different URI.' },
	303: { name: 'See Other', nameCN: '查看其他位置', description: 'The response to the request can be found under another URI using a GET method.' },
	304: { name: 'Not Modified', nameCN: '未修改', description: 'Indicates that the resource has not been modified since the version specified by the request headers.' },
	307: { name: 'Temporary Redirect', nameCN: '临时重定向', description: 'The request should be repeated with another URI; however, future requests should still use the original URI.' },
	308: { name: 'Permanent Redirect', nameCN: '永久重定向', description: 'The request and all future requests should be repeated using another URI.' },
	
	// 4xx 客户端错误
	400: { name: 'Bad Request', nameCN: '错误请求', description: 'The server cannot or will not process the request due to an apparent client error.' },
	401: { name: 'Unauthorized', nameCN: '未授权', description: 'Similar to 403 Forbidden, but specifically for use when authentication is required and has failed or has not yet been provided.' },
	402: { name: 'Payment Required', nameCN: '需要付款', description: 'Reserved for future use. The original intention was that this code might be used as part of some form of digital cash or micropayment scheme.' },
	403: { name: 'Forbidden', nameCN: '禁止访问', description: 'The request was valid, but the server is refusing action.' },
	404: { name: 'Not Found', nameCN: '未找到', description: 'The requested resource could not be found but may be available in the future.' },
	405: { name: 'Method Not Allowed', nameCN: '方法不被允许', description: 'A request method is not supported for the requested resource.' },
	406: { name: 'Not Acceptable', nameCN: '不可接受', description: 'The requested resource is capable of generating only content not acceptable according to the Accept headers sent in the request.' },
	407: { name: 'Proxy Authentication Required', nameCN: '需要代理授权', description: 'The client must first authenticate itself with the proxy.' },
	408: { name: 'Request Timeout', nameCN: '请求超时', description: 'The server timed out waiting for the request.' },
	409: { name: 'Conflict', nameCN: '冲突', description: 'Indicates that the request could not be processed because of conflict in the request.' },
	410: { name: 'Gone', nameCN: '已删除', description: 'Indicates that the resource requested is no longer available and will not be available again.' },
	411: { name: 'Length Required', nameCN: '需要有效长度', description: 'The request did not specify the length of its content, which is required by the requested resource.' },
	412: { name: 'Precondition Failed', nameCN: '先决条件失败', description: 'The server does not meet one of the preconditions that the requester put on the request.' },
	413: { name: 'Payload Too Large', nameCN: '请求实体过大', description: 'The request is larger than the server is willing or able to process.' },
	414: { name: 'URI Too Long', nameCN: 'URI过长', description: 'The URI provided was too long for the server to process.' },
	415: { name: 'Unsupported Media Type', nameCN: '不支持的媒体类型', description: 'The request entity has a media type which the server or resource does not support.' },
	416: { name: 'Range Not Satisfiable', nameCN: '请求范围不符合要求', description: 'The client has asked for a portion of the file, but the server cannot supply that portion.' },
	417: { name: 'Expectation Failed', nameCN: '未满足期望值', description: 'The server cannot meet the requirements of the Expect request-header field.' },
	418: { name: "I'm a teapot", nameCN: '我是茶壶', description: 'This code was defined in 1998 as one of the traditional IETF April Fools\' jokes.' },
	421: { name: 'Misdirected Request', nameCN: '请求错误定向', description: 'The request was directed at a server that is not able to produce a response.' },
	422: { name: 'Unprocessable Entity', nameCN: '无法处理的实体', description: 'The request was well-formed but was unable to be followed due to semantic errors.' },
	423: { name: 'Locked', nameCN: '已锁定', description: 'The resource that is being accessed is locked.' },
	424: { name: 'Failed Dependency', nameCN: '失败的依赖', description: 'The request failed due to failure of a previous request.' },
	425: { name: 'Too Early', nameCN: '过早', description: 'Indicates that the server is unwilling to risk processing a request that might be replayed.' },
	426: { name: 'Upgrade Required', nameCN: '需要升级', description: 'The client should switch to a different protocol such as TLS/1.0.' },
	428: { name: 'Precondition Required', nameCN: '需要先决条件', description: 'The origin server requires the request to be conditional.' },
	429: { name: 'Too Many Requests', nameCN: '请求过多', description: 'The user has sent too many requests in a given amount of time.' },
	431: { name: 'Request Header Fields Too Large', nameCN: '请求头字段太大', description: 'The server is unwilling to process the request because either an individual header field, or all the header fields collectively, are too large.' },
	451: { name: 'Unavailable For Legal Reasons', nameCN: '因法律原因不可用', description: 'A server operator has received a legal demand to deny access to a resource or to a set of resources.' },
	
	// 5xx 服务器错误
	500: { name: 'Internal Server Error', nameCN: '内部服务器错误', description: 'A generic error message, given when an unexpected condition was encountered and no more specific message is suitable.' },
	501: { name: 'Not Implemented', nameCN: '未实现', description: 'The server either does not recognize the request method, or it lacks the ability to fulfill the request.' },
	502: { name: 'Bad Gateway', nameCN: '错误网关', description: 'The server was acting as a gateway or proxy and received an invalid response from the upstream server.' },
	503: { name: 'Service Unavailable', nameCN: '服务不可用', description: 'The server is currently unavailable (because it is overloaded or down for maintenance).' },
	504: { name: 'Gateway Timeout', nameCN: '网关超时', description: 'The server was acting as a gateway or proxy and did not receive a timely response from the upstream server.' },
	505: { name: 'HTTP Version Not Supported', nameCN: 'HTTP版本不受支持', description: 'The server does not support the HTTP protocol version used in the request.' },
	506: { name: 'Variant Also Negotiates', nameCN: '变体协商', description: 'Transparent content negotiation for the request results in a circular reference.' },
	507: { name: 'Insufficient Storage', nameCN: '存储空间不足', description: 'The server is unable to store the representation needed to complete the request.' },
	508: { name: 'Loop Detected', nameCN: '检测到循环', description: 'The server detected an infinite loop while processing the request.' },
	510: { name: 'Not Extended', nameCN: '未扩展', description: 'Further extensions to the request are required for the server to fulfill it.' },
	511: { name: 'Network Authentication Required', nameCN: '需要网络认证', description: 'The client needs to authenticate to gain network access.' }
};

const input = alfy.input.trim();

// 如果没有输入，显示使用说明
if (!input) {
	alfy.output([
		{
			title: 'HTTP状态码查询',
			subtitle: '请输入HTTP状态码，例如：200, 404, 500',
			icon: {
				path: 'icon.png'
			}
		}
	]);
	return;
}

// 检查输入是否为数字
const code = parseInt(input, 10);
if (isNaN(code)) {
	alfy.output([
		{
			title: '输入错误',
			subtitle: '请输入有效的HTTP状态码数字',
			icon: {
				path: 'icon.png'
			}
		}
	]);
	return;
}

// 查找匹配的状态码
const results = [];

// 精确匹配
if (httpCodes[code]) {
	const statusCode = httpCodes[code];
	results.push({
		title: `${code} ${statusCode.name} (${statusCode.nameCN})`,
		subtitle: statusCode.description,
		arg: `https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/${code}`,
		icon: {
			path: 'icon.png'
		}
	});
} else {
	// 如果没有精确匹配，查找相似的状态码
	const similarCodes = Object.keys(httpCodes)
		.map(key => parseInt(key, 10))
		.filter(statusCode => statusCode.toString().includes(input))
		.slice(0, 10); // 限制结果数量

	if (similarCodes.length > 0) {
		similarCodes.forEach(statusCode => {
			const codeInfo = httpCodes[statusCode];
			results.push({
				title: `${statusCode} ${codeInfo.name} (${codeInfo.nameCN})`,
				subtitle: codeInfo.description,
				arg: `https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/${statusCode}`,
				icon: {
					path: 'icon.png'
				}
			});
		});
	} else {
		// 没有找到任何匹配的状态码
		results.push({
			title: `未找到状态码 ${code}`,
			subtitle: '请检查输入的状态码是否正确',
			arg: 'https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status',
			icon: {
				path: 'icon.png'
			}
		});
	}
}

alfy.output(results);
