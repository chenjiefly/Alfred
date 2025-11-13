/**
 * 该文件名- variableStyle
 * 编码作者- 许道龙
 * 创建日期- 2016/12/13 13:37
 * 作者邮箱- xudaolong@vip.qq.com
 * 作者博客- http://xudaolong.github.io/
 * 修改时间-
 * 修改备注-
 * 编码内容-
 */

'use strict';

const alfy = require('alfy');
const qs = require('qs');
const filter = require('./variableFilter.js');

module.exports = {
    core: function (api, params, style) {
        if (!process.env.appKey || !process.env.appSecret) {
            alfy.output([{
                title: '错误：appKey或appSecret未配置。',
                subtitle: '请至 workflow 右上角的 [X] 点开后的配置框中填写。',
                arg: 'error',
                icon: {
                    path: alfy.icon.error
                }
            }]);
            return;
        }
        
        alfy.fetch(`${api}?${qs.stringify(params)}`).then(result => {
            if (result.errorCode == 0) {
                //结果
                let result_value = [];
                // 过滤中文
                let reg = /^[a-zA-Z ]/;
                // 标准翻译结果 : translation
                let result_translation = result.translation;
                for (let i = 0, len = result_translation.length; i < len; i++) {
                    if (reg.test(result_translation[i])) {
                        result_value.push({
                            title: style(result_translation[i]),
                            subtitle: `标准翻译 => ${result_translation[i]}`,
                            arg: style(result_translation[i]),
                        });
                    }
                }

                alfy.output(result_value);
            } else {
                alfy.output([{
                    title: '抱歉',
                    subtitle: `无相关记录`,
                    arg: 'error',
                }]);
            }
        });
    },
    bigHump: function (s) {
        let strArr = filter.run(s);
        strArr[0] = strArr[0].charAt(0).toUpperCase() + strArr[0].substring(1);
        // 单词首字母大写
        for (let i = 1; i < strArr.length; i++) {
            strArr[i] = strArr[i].charAt(0).toUpperCase() + strArr[i].substring(1);
        }
        return strArr.join('');
    },
    hump: function (s) {
        let strArr = filter.run(s);
        // 单词首字母大写
        for (let i = 1; i < strArr.length; i++) {
            strArr[i] = strArr[i].charAt(0).toUpperCase() + strArr[i].substring(1);
        }
        return strArr.join('');
    },
    namedConst: function (s) {
        let strArr = filter.run(s);
        for (let i = 0; i < strArr.length; i++) {
            strArr[i] = strArr[i].toUpperCase();
        }
        return strArr.join('_');
    },
    underline: function (s) {
        let strArr = filter.run(s);
        for (let i = 0; i < strArr.length; i++) {
            strArr[i] = strArr[i].toLowerCase();
        }
        return strArr.join('_');
    }
};