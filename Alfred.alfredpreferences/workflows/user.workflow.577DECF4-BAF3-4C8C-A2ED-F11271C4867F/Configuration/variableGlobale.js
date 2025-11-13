/**
 * 该文件名- variableGlobale
 * 编码作者- 许道龙
 * 创建日期- 2016/12/13 13:22
 * 作者邮箱- xudaolong@vip.qq.com
 * 作者博客- http://xudaolong.github.io/
 * 修改时间-
 * 修改备注-
 * 编码内容-
 */

'use strict';

const CryptoJS = require('crypto-js');
const alfy = require('alfy');

function truncate(q) {
    const len = q.length;
    if(len <= 20) return q;

    return q.substring(0, 10) + len + q.substring(len - 10, len);
}

module.exports = {
    youDaoApi: 'https://openapi.youdao.com/api',
    getParams: function () {
        const query = alfy.input;
        const appKey = '773a7c9fba06170a';
        const appSecret = 'zmA9G2pciKaqMehI3CbucCdSYXro9Sl8';
        const salt = (new Date).getTime();
        const curtime = Math.round(new Date().getTime() / 1000);
        const str = appKey + truncate(query) + salt + curtime + appSecret;
        const sign = CryptoJS.SHA256(str).toString(CryptoJS.enc.Hex);

        return {
            q: query,
            appKey: appKey,
            salt: salt,
            from: 'zh-CHS',
            to: 'en',
            sign: sign,
            signType: 'v3',
            curtime: curtime,
        };
        return {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            json: {
                q: query,
                appKey: appKey,
                salt: salt,
                from: 'zh-CHS',
                to: 'EN',
                sign: sign,
                signType: 'v3',
                curtime: curtime,
            }
        }
    },
    filter: {
        prep: [
            'and', 'or', 'the', 'a', 'at', 'of'
        ],
        prefix: [],
        suffix: [
            'ing', 'ed', 'ly'
        ],
        verb: [
            'was'
        ]
    }
};