<?php

require ('workflows.php');

//Weather::Go('beijing');
date_default_timezone_set('UTC');

class Weather{
    static protected $searchUrl = 'http://apis.baidu.com/heweather/weather/free?';
    /**
     * 百度appkey
     * @var string
     */
    static protected $appkey = '8d784dda33bb262c31cf152c5d6457ae';
    /** ip get url */
    static protected $getipUrl = 'https://pjialin.com/test/ip.php';
    /** workflow ins */
    static protected $w;
    /** save curl error */
    static protected $curlError;

	static public function Go($query)
	{
        self::DoSearch($query);
	}

	/**
	 *  进行搜索
	 */
    static protected function DoSearch($query)
    {
        self::$w = new Workflows();
        $searchRes = self::getSearchContent($query);  
        $searchRes = self::execContent($searchRes);

        self::showAlfred($searchRes,$query);
//        print_r(self::$w->results());
        echo self::$w->toxml();
    }

    /**
     * 获取搜索内容
     */
    static protected function getSearchContent($query)
    {
        /** 获取方式
         * 如果查询为空 通过 ip获取城市
         * 否者通过查询城市名获取
         */
        if($query == ''){
            $argu = ['cityip'=> file_get_contents(self::$getipUrl)];
        }else 
            $argu = ['city'=>$query];
        $url = self::$searchUrl . http_build_query($argu);
        return self::curl($url,false,[
            CURLOPT_HTTPHEADER  =>  [
                'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                'apikey: '. self::$appkey
            ]
        ]);
    }
    /**
     * 显示到Alfred
     */ 
    static protected function showAlfred($info,$query){
        $argu = [
                'query' => $query,
            ];
        self::getargu($argu);
        if($info !== false){
            if($info->status == 'ok')
            {
                /** 实况天气 */
                $nowStr = $info->basic->city . '，实时：' . $info->now->tmp . '℃，' . $info->now->cond->txt . (isset($info->aqi->qlty) ? '，空气质量 ' . $info->aqi->qlty : '') . '，' . $info->now->wind->dir . $info->now->wind->sc;
                    self::$w->result(self::getuid(),self::getargu(['copy'=>$nowStr]),$nowStr,'',self::geticon($info->now->cond->code));
                /** 未来七天 */
                foreach($info->daily_forecast as $v){
                    $tmpStr = $v->cond->txt_d == $v->cond->txt_n ? $v->cond->txt_d : $v->cond->txt_d .'转'. $v->cond->txt_n;
                    $tmpStr .= '，'. ($v->tmp->min == $v->tmp->max ? $v->tmp->min : $v->tmp->min . '-' . $v->tmp->max) . '℃';
                    $tmpStr .= '，' . $v->wind->dir . $v->wind->sc;
                    $dayInfo = self::getDateInfo(strtotime($v->date));
                    $tmpStrMin = ($dayInfo['day'] ? $dayInfo['day'] .'，': '') . $dayInfo['week'] .'，' . $v->date;
                    self::$w->result(self::getuid(),self::getargu(['copy'=>$tmpStr]),$tmpStr,$tmpStrMin,self::geticon($v->cond->code_d));
                }
            }else{
                
                self::$w->result(self::getuid(),self::getargu(['copy'=>$info->status]),'咦，获取失败了',$info->status == 'unknown city' ? '未找到该城市' : $info->status,self::geticon());
            }
        }
        else 
        {
            $error = self::$curlError;
            self::$w->result(self::getuid(),self::getargu(['copy'=>$query]),'什么也没找到呀，检查下网络试试',$error,self::geticon());
        }

    }

    /**
     * 处理搜索结果
     */
    static protected function execContent($content)
    {
        $execRes = json_decode($content);
        return $execRes ? $execRes->{"HeWeather data service 3.0"}[0] : false;
    }

    /**
     * @param string $url 地址
     * @param bool|false $data post数据
     * @param array $s_option curl参数
     * @return mixed
     */
    static protected function curl($url, $data = false,$s_option = []){
        $ch = curl_init();
        $option = [
            CURLOPT_URL => $url,
            CURLOPT_HEADER => 0,
            CURLOPT_FOLLOWLOCATION => TRUE,
            CURLOPT_TIMEOUT => 10,
            CURLOPT_RETURNTRANSFER => TRUE,
            CURLOPT_SSL_VERIFYPEER => 0,
        ];
        if ( $data ) {
            $option[CURLOPT_POST] = 1;
            $option[CURLOPT_POSTFIELDS] = http_build_query($data);
        }
        foreach($s_option as $k => $v){
            $option[$k] = $v;
        };
        curl_setopt_array($ch, $option);
        $response = curl_exec($ch);
        if (curl_errno($ch) > 0) {
            self::$curlError = curl_error($ch);
            //exit("CURL ERROR:$url " . curl_error($ch));
        }
        curl_close($ch);
        return $response;
    }

    /**
     * 获取节点uid
     */
    static protected function getUid()
    {
        return time() . mt_rand(1000,9999);
    }
    /**
     * 获取图标
     */
    static protected function getIcon($name = ''){
        if($name+0 > 0)
            return 'weatherico/' .$name .'.png';
        return 'weather.ico';
    }

    /**
     * 返回值Argu
     */
    static protected function getArgu($info = [],$clean = false)
    {
        static $data = [];
        if($clean === true) 
            $data = [];
        $data = array_merge($data,$info);
        return json_encode($data,JSON_UNESCAPED_UNICODE);
    } 

    /**
     * 获取日期信息
     */
    static protected function getDateInfo($time = null){
        if(is_null($time)) $time = time();
        /** 获得星期 */ 
        $weeks = [
            1 => '一',
            2 => '二',
            3 => '三',
            4 => '四',
            5 => '五',
            6 => '六',
            7 => '天',
        ];

        $week = date('N',$time); 
        return [
            'week' => '星期' . $weeks[$week],
            'day' => self::getDayShow($time - strtotime(date('Y-m-d')))
        ];
    }

    /**
     * 获得时间显示方式
     */
    static protected function getDayShow($s){
        if($s < 86400) 
            $str = '今天';
        else if($s < 86400 * 2)
            $str = '明天';
        else if($s < 86400 * 3)
            $str = '后天';
        else 
            $str = '';
        return $str;
    }

}
