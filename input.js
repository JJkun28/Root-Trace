let _input = {
	"start": "U500",
	// 封面：clan 填姓氏（可复姓，如欧阳）；留空则用始祖姓名开头识别。motto 为祖训，单独自填。
	"cover": {
		"clan": "",
		"motto": "慎终追远　民德归厚"
	},
	"members": {
		"I500": {
			"name": "锅底虾煤饼",
			"title": "族长",
			"birth_date": "12.03.1955",
			"lunar_birthday": "正月十一",
			"zodiac": "羊",
			"death_date": "",
			"image_path": "images/pattern-kettle-shrimp.jpg",
			"biography": "传说能在三分钟内把铁锅炖出彩虹味，族谱第一页就写着他。"
		},
		"I501": {
			"name": "歪脖鸭梨婶",
			"title": "配偶",
			"birth_date": "08.07.1958",
			"lunar_birthday": "五月廿二",
			"zodiac": "狗",
			"death_date": "",
			"image_path": "images/pattern-crooked-pear.jpg",
			"biography": "专门收集向左歪的水果，家里晾衣绳永远比地面高两寸。"
		},
		"I502": {
			"name": "拧巴茄子七",
			"title": "长子",
			"birth_date": "16.08.1987",
			"lunar_birthday": "七月廿三",
			"zodiac": "兔",
			"death_date": "",
			"image_path": "images/pattern-twisted-eggplant.jpg",
			"biography": "名字里的「七」没有第七个含义，单纯因为茄子拧了七圈。"
		},
		"I503": {
			"name": "呼噜碗豆姑",
			"title": "配偶",
			"birth_date": "11.10.1985",
			"lunar_birthday": "八月廿八",
			"zodiac": "牛",
			"death_date": "",
			"image_path": "images/pattern-snoring-bean.jpg",
			"biography": "睡觉时碗豆会自己排队，醒来发现全在枕头底下。"
		},
		"I504": {
			"name": "噗噜香蕉娃",
			"title": "长子",
			"birth_date": "13.05.2010",
			"lunar_birthday": "四月初一",
			"zodiac": "虎",
			"death_date": "",
			"image_path": "images/pattern-plop-banana.jpg",
			"biography": "走路带香蕉皮音效，但从未滑倒过，科学界至今不解。"
		},
		"I505": {
			"name": "咕噜南瓜妞",
			"title": "次女",
			"birth_date": "12.12.2013",
			"lunar_birthday": "十一月初十",
			"zodiac": "蛇",
			"death_date": "",
			"image_path": "images/pattern-gurgle-pumpkin.jpg",
			"biography": "南瓜灯不用蜡烛，她一笑就会自己亮，亮度随心情波动。"
		}
	},
	"links": [
		["I500", "U500"],
		["I501", "U500"],
		["U500", "I502"],
		["I502", "U501"],
		["I503", "U501"],
		["U501", "I504"],
		["U501", "I505"]
	]
};
