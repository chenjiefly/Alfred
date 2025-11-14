'use strict';
const alfy = require('alfy');

const list = [
	{
		label: '身份证',
		value: '339005198911162151',
	}, {
		label: '手机号',
		value: '15867167788',
	}, {
		label: '域账号',
		value: 'cj85996',
	}, {
		label: '域邮箱-集团',
		value: 'cj85996@alibaba-inc.com',
	}, {
		label: '域邮箱-淘宝',
		value: 'cj85996@taobao.com',
	}, {
		label: '阿里云邮箱',
		value: 'ichenjie@aliyun.com',
	}, {
		label: '网易163邮箱',
		value: 'chenjiefly@163.com',
	}, {
		label: '网易yeah邮箱',
		value: 'ichenjie@yeah.net',
	},
];


const options = list.map(item => {
	const { label, value } = item;
	
	return {
		title: label,
		subtitle: value,
		arg: value,
	}
})

alfy.output(alfy.inputMatches(options, 'title'));
