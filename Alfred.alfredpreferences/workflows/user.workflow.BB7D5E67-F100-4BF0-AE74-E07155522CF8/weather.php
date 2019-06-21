<?php

require_once('workflows.php');

class Weather{

	private $url = "http://api.map.baidu.com/telematics/v3/weather?output=json&ak=Gy7SGUigZ4HxGYDaq9azWy09&location=";

	public function getWeather($query){
		$workflows = new Workflows();
		$api = $this->url.$query;
		$res = $workflows->request($api);
		$res = json_decode( $res );
		if ($res->error === 0) {
			$pm25 = $res->results[0]->pm25;
			$first = 1;
			$forecast = $res->results[0]->weather_data;
			foreach($forecast as $key=>$value) {
				$date = mb_substr($value->date,0,2,'utf-8');
				$title = $date."      ".$value->weather;
				$subtitle = $value->wind."，温度：".$value->temperature;
				if ($first==1) {
					$realtimeweater = mb_substr($value->date,2,mb_strlen($value->date),'utf-8');
					$title = $title."      ".$realtimeweater;
					if ($pm25!="") {
						$subtitle = $subtitle."，PM2.5：".$pm25;						
					}
					$first=0;	
				}

				$workflows->result( $key,
									$query,
									$title,
									$subtitle,
									$this->getWeatherIcon($value->weather));
			}
		}else{
			$workflows->result(	'',
		  						'',
					  			'没查到呀', 
					  			'没找到你所查询城市的天气',
					  			$this->getWeatherIcon('unknown'));
		}

		echo $workflows->toxml();
	}

	function getWeatherIcon($weather) {
		if ($weather == 'icon') {
			return 'cloudy2.png';
		} elseif ($weather == 'unknown') {
			return 'unknown.png';
		}
		$map = array('晴' => 'sunny.png', 
					 '晴见多云' => 'cloudy1.png',
					 '晴转多云' => 'cloudy3.png',
					 '多云转晴' => 'cloudy4.png',
					 '阴转晴' => 'cloudy4.png',
					 '多云' => 'cloudy5.png',
					 '阴' => 'overcast.png',
					 '雨' => 'light_rain.png',
					 '阵雨' => 'shower1.png',
					 '小雨' => 'shower1.png',
					 '中雨' => 'shower2.png',
					 '大雨' => 'shower3.png',
					 '暴雨' => 'shower3.png',
					 '雷阵雨' => 'tstorm1.png',
					 '雷阵雨转中雨' => 'tstorm2.png',
					 '雷阵雨转大雨' => 'tstorm3.png',
					 '雷阵雨转暴雨' => 'tstorm3.png',
					 '雨夹雪' => 'sleet.png',
					 '冰雹' => 'hail.png',
					 '阵雪' => 'snow1.png',
					 '小雪' => 'snow1.png',
					 '中雪' => 'snow2.png',
					 '大雪' => 'snow3.png',
					 '暴雪' => 'snow4.png',
					 '大暴雪' => 'snow5.png',
					 '雾' => 'mist.png',
					 '大雾' => 'fog.png',
					 '霾' => 'haze.png',
					 '雾霾' => 'haze.png',
					 );
		foreach ($map as $key => $value) {
			if ($weather == $key) {
				return $value;
			}
		}

		foreach (array_reverse($map) as $key => $value) {
			if (strstr($weather, $key)) {
				return $value;
			}
		}

		return 'unknown.png';
	}

}