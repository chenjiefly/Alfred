'use strict';
const alfy = require('alfy');

function formatTimestamp(timestamp) {
    const date = new Date(parseInt(timestamp));
    if (isNaN(date.getTime())) {
        return null;
    }
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function parseTimeString(timeString) {
    // 匹配 YYYY-MM-DD HH:mm:SS 格式
    const regex = /^(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})$/;
    const match = timeString.match(regex);
    
    if (!match) {
        return null;
    }
    
    const [, year, month, day, hours, minutes, seconds] = match;
    const date = new Date(year, month - 1, day, hours, minutes, seconds);
    
    if (isNaN(date.getTime())) {
        return null;
    }
    
    return date.getTime();
}

function isTimestamp(input) {
    // 检查是否为纯数字且长度合理（10位秒级或13位毫秒级时间戳）
    const num = parseInt(input);
    return !isNaN(num) && /^\d+$/.test(input.trim()) && (input.length === 10 || input.length === 13);
}

function isTimeString(input) {
    // 检查是否匹配 YYYY-MM-DD HH:mm:SS 格式
    const regex = /^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$/;
    return regex.test(input.trim());
}

const input = alfy.input || '';
const trimmedInput = input.trim();
let results = [];

if (input === ' ') {
    // 当输入为空格时，显示当前时间戳和格式化时间
    const now = Date.now();
    const nowString = formatTimestamp(now);
    const nowSeconds = Math.floor(now / 1000);
    
    results.push({
        title: now.toString(),
        subtitle: '当前时间戳 (毫秒级)',
        arg: now.toString(),
    });
    
    results.push({
        title: nowString,
        subtitle: '当前时间 (YYYY-MM-DD HH:mm:SS)',
        arg: nowString,
    });
} else if (!trimmedInput) {
    results.push({
        title: '时间转换工具',
        subtitle: '请输入时间戳或 YYYY-MM-DD HH:mm:SS 格式的时间字符串，或输入空格查看当前时间',
        arg: '',
    });
} else if (isTimestamp(trimmedInput)) {
    // 输入是时间戳，转换为时间字符串
    let timestamp = parseInt(trimmedInput);
    
    // 如果是10位时间戳（秒级），转换为13位（毫秒级）
    if (trimmedInput.length === 10) {
        timestamp = timestamp * 1000;
    }
    
    const timeString = formatTimestamp(timestamp);
    
    if (timeString) {
        results.push({
            title: timeString,
            subtitle: `时间戳 ${trimmedInput} 转换为时间字符串`,
            arg: timeString,
        });
        
        // 同时提供当前时间戳作为参考
        const now = Date.now();
        const nowString = formatTimestamp(now);
        results.push({
            title: nowString,
            subtitle: `当前时间 (时间戳: ${now})`,
            arg: nowString,
        });
    } else {
        results.push({
            title: '无效的时间戳',
            subtitle: '请输入有效的时间戳',
            arg: '',
        });
    }
} else if (isTimeString(trimmedInput)) {
    // 输入是时间字符串，转换为时间戳
    const timestamp = parseTimeString(trimmedInput);
    
    if (timestamp !== null) {
        const timestampSeconds = Math.floor(timestamp / 1000);
        
        results.push({
            title: timestamp.toString(),
            subtitle: `时间字符串转换为时间戳 (毫秒级)`,
            arg: timestamp.toString(),
        });
        
        results.push({
            title: timestampSeconds.toString(),
            subtitle: `时间字符串转换为时间戳 (秒级)`,
            arg: timestampSeconds.toString(),
        });
    } else {
        results.push({
            title: '无效的时间格式',
            subtitle: '请使用 YYYY-MM-DD HH:mm:SS 格式',
            arg: '',
        });
    }
} else {
    // 输入格式不匹配，提供帮助信息
    results.push({
        title: '格式不正确',
        subtitle: '请输入时间戳或 YYYY-MM-DD HH:mm:SS 格式的时间字符串',
        arg: '',
    });
    
    // 提供当前时间作为示例
    const now = Date.now();
    const nowString = formatTimestamp(now);
    results.push({
        title: `示例: ${nowString}`,
        subtitle: `当前时间 (时间戳: ${now})`,
        arg: nowString,
    });
}

alfy.output(results);
