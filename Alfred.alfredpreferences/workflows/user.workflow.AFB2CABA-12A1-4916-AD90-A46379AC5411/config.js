module.exports = {
  // 图片配置
  image: {
    width: 200,
    height: 200,
    backgroundColor: 'transparent'
  },
  
  // 文字配置
  text: {
    fontSize: 128,
    fontFamily: 'PingFang SC',
    fontWeight: 'bold',
    // 浅色彩色渐变配置
    gradient: {
      start: { x: 0, y: 0 },
      end: { x: 200, y: 0 },
      colors: [
        // { position: 0, color: '#007AFF' }, // 支付宝
        // { position: 1, color: '#5E5CE6' }
        { position: 0, color: '#FF8C00' }, // 淘宝
        { position: 1, color: '#FF6A00' }
      ]
    }
  },
  
  // 背景配置
  background: {
    color: '#FFFFFF',
    borderRadius: 20,
    padding: 20,
    opacity: 0.9
  },
  
  // 输出配置
  output: {
    directory: '/Users/chenjie/Downloads',
    format: 'png',
    quality: 1.0
  }
};
