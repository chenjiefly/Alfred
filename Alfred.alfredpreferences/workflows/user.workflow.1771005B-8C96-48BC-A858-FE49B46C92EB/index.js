'use strict';
const alfy = require('alfy');

const input = alfy.input;
const url = 'https://restapi.amap.com/v3/config/district?extensions=all&showbiz=false&subdistrict=0&key=8257bcf6e54f72284347adb671aeeca2&s=rsv3&output=json';
const levelMap = {  // 行政等级映射表
	country: {
		label: '国',
		val: 0
	},
	province: {
		label: '省',
		val: 1
	},
	city: {
		label: '地市',
		val: 2
	},
	district: {
		label: '区县',
		val: 3
	}
};

// 地理编码查询
// https://restapi.amap.com/v3/config/district?extensions=all&showbiz=false&subdistrict=0&key=8257bcf6e54f72284347adb671aeeca2&s=rsv3&output=json&keywords=%E5%AE%81%E6%B3%A2
alfy.fetch(`${url}&keywords=${encodeURIComponent(input)}`, {
	transform: (res = {}) => {
		const {
			info,  // 请求状态，OK表示请求成功
			districts = []  // 返回结果数组
		} = res;

		// 不需要绘制行政边界，把polyline字段过滤掉，这个字段数据量太大，会alfy处理时会出错
		return info === 'OK' ? districts.map((d = {}) => {
			const { name, adcode, citycode, center, level } = d;
		
			return { name, adcode, citycode, center, level };
		}) : [];
	}
}).then((districts) => {
	const results = districts.sort((a, b) => (  // 按层级归类排序一下
		levelMap[a.level].val - levelMap[b.level].val
	)).map((d = {}) => {
		let { name, adcode, citycode, center, level } = d;

		d.level = level = levelMap[level].label;
		citycode = citycode.length > 0 ? citycode.toString() : '无';
		center = center.length > 0 ? `[${center.toString()}]` : '无';

		return {
			title: `${name}，级别：${level}，区号：${citycode}`,
			subtitle: `地理编码：${adcode}，中心坐标：${center}`,
			arg: JSON.stringify(d, null, 2)
		};
	});
	
	alfy.output(results);
}).catch(err => {
	alfy.error(`错误信息: ${JSON.stringify(err)}`)
});


