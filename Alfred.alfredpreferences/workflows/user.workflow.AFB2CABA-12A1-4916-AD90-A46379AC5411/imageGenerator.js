const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');
const config = require('./config');

/**
 * 生成文字图标
 * @param {string} text - 要生成的文字
 * @returns {Promise<string>} - 生成的图片文件路径
 */
async function generateTextIcon(text) {
  if (!text || text.trim() === '') {
    throw new Error('文字内容不能为空');
  }

  const { image, text: textConfig, background, output } = config;
  
  // 创建画布
  const canvas = createCanvas(image.width, image.height);
  const ctx = canvas.getContext('2d');

  // 设置透明背景
  ctx.clearRect(0, 0, image.width, image.height);

  // 绘制圆角白色背景
  drawRoundedBackground(ctx, background, image);

  // 绘制渐变文字
  drawGradientText(ctx, text.trim(), textConfig, image);

  // 生成文件名和路径
  const timestamp = Date.now();
  const fileName = `text_icon_${timestamp}.${output.format}`;
  const filePath = path.join(output.directory, fileName);

  // 确保输出目录存在
  if (!fs.existsSync(output.directory)) {
    fs.mkdirSync(output.directory, { recursive: true });
  }

  // 保存图片
  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync(filePath, buffer);

  return filePath;
}

/**
 * 绘制圆角背景
 */
function drawRoundedBackground(ctx, backgroundConfig, imageConfig) {
  const { color, borderRadius, padding, opacity } = backgroundConfig;
  const { width, height } = imageConfig;

  ctx.save();
  ctx.globalAlpha = opacity;
  ctx.fillStyle = color;

  // 绘制圆角矩形
  const x = padding;
  const y = padding;
  const w = width - padding * 2;
  const h = height - padding * 2;
  const r = borderRadius;

  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
  ctx.fill();

  ctx.restore();
}

/**
 * 绘制渐变文字
 */
function drawGradientText(ctx, text, textConfig, imageConfig) {
  const { fontSize, fontFamily, fontWeight, gradient } = textConfig;
  const { width, height } = imageConfig;

  // 设置字体
  ctx.font = `${fontWeight} ${fontSize}px ${fontFamily}`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // 创建渐变
  const grad = ctx.createLinearGradient(
    gradient.start.x,
    gradient.start.y,
    gradient.end.x,
    gradient.end.y
  );

  // 添加渐变色
  gradient.colors.forEach(colorStop => {
    grad.addColorStop(colorStop.position, colorStop.color);
  });

  // 设置填充样式为渐变
  ctx.fillStyle = grad;

  // 绘制文字（居中）
  const centerX = width / 2;
  const centerY = height / 2;
  
  // 如果文字太长，自动调整字体大小
  const maxWidth = width - 60; // 留出边距
  let currentFontSize = fontSize;
  
  while (ctx.measureText(text).width > maxWidth && currentFontSize > 12) {
    currentFontSize -= 2;
    ctx.font = `${fontWeight} ${currentFontSize}px ${fontFamily}`;
  }

  ctx.fillText(text, centerX, centerY);
}

module.exports = {
  generateTextIcon
};
