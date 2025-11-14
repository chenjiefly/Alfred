'use strict';
const alfy = require('alfy');
const { generateTextIcon } = require('./imageGenerator');

async function main() {
	const inputText = alfy.input;
	
	if (!inputText || inputText.trim() === '') {
		alfy.output([
			{
				title: '请输入要生成图标的文字',
				subtitle: '输入文字后按回车生成图标',
				valid: false
			}
		]);
		return;
	}

	try {
		// 生成图标
		const imagePath = await generateTextIcon(inputText);
		
		alfy.output([
			{
				title: `已生成文字图标: ${inputText}`,
				subtitle: `图片已保存到: ${imagePath}`,
				arg: imagePath,
				text: {
					copy: imagePath,
					largetype: `图标已生成: ${inputText}\n保存路径: ${imagePath}`
				}
			}
		]);
	} catch (error) {
		alfy.output([
			{
				title: '生成图标失败',
				subtitle: error.message,
				valid: false
			}
		]);
	}
}

main().catch(error => {
	alfy.output([
		{
			title: '程序执行错误',
			subtitle: error.message,
			valid: false
		}
	]);
});
