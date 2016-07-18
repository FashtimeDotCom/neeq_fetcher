# NEEQ数据抓取程序文档
## 简介
本项目主要用于从[**全国中小企业股份转让系统**](http://www.neeq.com.cn/)的官方网站上抓取一些公开的交易方面的数据

抓取程序由Python3代码编写支持，读取指定接口的数据以后解析为JSON格式，将数据通过MySQL官方开发的Connector/Python support存入MySQL的数据库，格式为InnoDB

数据库配置（该配置可以在fetch_config.py文件中随时进行更改）

	'user': 'stock',
	'password': 'password',
	'host': '192.168.202.161',
	'database': 'stockdb'


目前项目功能包括

- 指定日期的交易提示信息
- 指定日期的日报统计信息
- 做市商信息（包括推荐，做市的详细信息）

	| 任务类型  | 目标网址   | 目标数据库表格    |   预计时间     |
	| ---------|:-------------: | ------------:|-----------:|
	| 交易提示   |http://www.neeq.com.cn/disclosure/tradingtips.html           |       RECORD（记录）  | 每日数据约1－2秒，支持读取历史数据
	| 日报统计   |http://www.neeq.com.cn/static/statisticdata.html        |   STAT（统计） | 每日数据约1－2秒，支持读取历史数据|
	| 做市商信息 | http://www.neeq.com.cn/nq/listedMakerInfo.html        |   MAKER（做市商）, MAKE（做市商做市）, RECOMMEND（做市商推荐）               | 3-5分钟，不支持历史数据


## 使用接口
通过查看网页源代码所获取的接口（暂时不明确是否为公开接口）

	TARGET = {
	    'recommend': '/makerInfoController/qryRecnumList.do',
	    'maker': '/makerInfoController/listMakerInfo.do',
	    'make': '/makerInfoController/qryMakenumList.do',
	    'tradingtips': '/tradingtipsController/tradingtips.do',
	    'stat': '/marketStatController/dailyReport.do'
	}

参数说明：

	tradingtips接口：
		'publishDate' 指发布日期，要求格式为YYYY-MM-DD
		'xxfcbj' 指类型，0对应基础层，1对应创新层
	stat接口：
		'HQJSRQ' 指发布日期，要求格式为YYYY-MM-DD
	maker接口：
		'page' 指页码
		备注：发送请求时若不传入page参数则会默认返回第一页的数据，在返回数据的字典（JSON）中包括一条总页数的参数，可以拿来用
	make接口：
		'page' 指页码，备注同上
		'stkaccout' 指券商账户代码，数据来源于maker接口返回的参数
	recommend接口：
		'page' 指页码，备注同上
		'makerName' 指券商账户代码，数据来源于maker接口返回的参数
		备注：在maker接口返回的数据中包括makerName这个参数但值为券商名称，实际在recommend接口中的这个makerName仍然接受的为券商账户代码


## 配置（CentOS）
###系统要求：

- MySQL
- Python3.4 及以上
- mysql-connector for python (Connector/Python)

**准备工作之安装Python：**

- 准备编译环境

        yum groupinstall 'Development Tools'
        yum install zlib-devel bzip2-devel openssl-devel ncurese-devel

- 下载Python代码包（3.5.1版本为例）

	    wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz

- 编译

	    tar Jxvf Python-3.5.1.tar.xz
	    cd Python-3.5.1
	    ./configure --prefix=/usr/local/python3
	    make && make install

	- 注意：

	    Python3.5.1 安装编译安装时会默认安装 pip 如果出现：
	    Ignoring ensurepip failure: pip 1.5.6 requires SSL/TLS
	    未安装编译环境，重新安装该编译环境并重新编译 Python3.5.1
	    yum install zlib-devel bzip2-devel openssl-devel ncurese-devel

- 可能需要的备份Python

		mv /usr/bin/python usr/bin/python2.7
		ln -s /usr/local/python3/bin/python3.5 /usr/bin/python
		ln -s /usr/local/python3/bin/pip3 /usr/bin/pip

	检查版本：

		python --version
		预期结果 Python 3.5.1

		pip --version
		预期结果 pip 8.1.2 from /path/to/your/python3.5/site-packages (python 3.5)

- 其他参考：

	- [http://www.jianshu.com/p/8bd6e0695d7f](http://www.jianshu.com/p/8bd6e0695d7f)

**准备工作之安装Connector/Python**

	https://dev.mysql.com/doc/connector-python/en/connector-python-installation-source.html

## 简易使用说明

- 文字版说明引导程序

		cd ~/Desktop/neeq_fetcher/src
		python setup.py
		备注：一定要切换到目录后再输入python setup.py
		使用类似 python ~/Desktop/neeq_fetcher/src/setup.py 是不行的

- 通过脚本直接操作

		首先cd到文件目录，以当前情况为例：
			cd ~/Desktop/neeq_fetcher/src

		重置数据库：

			重置交易提示及日报统计
				python init_db.py

			重置做市商信息（包括推荐／做事信息）
				python init_db_maker.py

		抓取数据：

			交易提示：
				抓取当日交易提示
				例如 python tradingtips.py

				抓取指定日期交易提示 日期格式 YYYY-MM-DD
				例如 python tradingtips.py 2016-03-01 2016-03-15

			日报统计：
				抓取前一日日报统计
				例如 python statdata.py

				抓取指定日期交易提示 日期格式 YYYY-MM-DD
				例如 python tradingtips.py 2016-04-04 2016-06-01

			做市商信息：
				例如 python listedmaker.py
				备注：时间较长，一般3-5分钟

- Shell命令操作

		一共有两个shell脚本，分别为init.sh和fetch.sh
		放置于系统的$HOME目录便于使用
		使用：
			初始化数据库（全部）
			cd ~
			. init.sh

			获取数据
			cd ~
			. fetch.sh $task {$start} {$end}
			备注：
				$task 参数可接受的值为
				tradingtips   指交易提示
				statdata      指日报统计
				listedmaker   指做市商信息
			 	当$task参数为tradingtips或statdata时，$start和$end参数作为可选参数，分别代表起始日期和终止日期。
			 	若不填写则默认抓取当前日期数据


##更改数据库配置

~~目前配置类参数只有数据库的参数转移到了fetch_config.py文件中，之后做简易重构时候会把参数都移到这个文件~~

更改数据库配置只需要到fetch\_config.py文件中找到DB_CONFIG这个字典更改参数即可

例如

	DB_CONFIG = {
	    'user': 'stock',
	    'password': 'password',
	    'host': '192.168.202.161',
	    'database': 'stockdb'
	}

## Crontab 配置
由于以上脚本都需要每日进行执行，所以配置了crontab定时定期自动运行脚本，已经由http://www.atool.org/crontab.php和实际部署测试过

	0 15 * * * /usr/bin/python /root/Desktop/neeq_fetcher/src/tradingtips.py >> /root/Desktop/log.txt

	5 15 * * 2,3,4,5,6 /usr/bin/python /root/Desktop/neeq_fetcher/src/statdata.py >> /root/Desktop/log.txt

	10 15 * * * /usr/bin/python /root/Desktop/neeq_fethcer/src/listedmaker.py >> /root/Desktop/log.txt


##数据库结构说明

**需要注意的是所有表的所有记录都有时间戳，列名为last_updated**

1. **RRCORD**表（交易提示）

	| 列名            | 含义           | 备注                    |
	| -------------  |:-------------: | ----------------------:|
	| ID     			 | ID            |   主键                  |
	| type_name      | 提示类型        |   比如新股挂牌，加入做市等 |
	| type_code      | 类型代码        |   四位数字               |
	| comp_code      | 公司股票代码     |                        |
	| comp_name      | 公司名称        |                        |
	| class          | 分层           |   基础层为0，创新层为1     |
	| postdate       | 日期           |   代表这条交易提示是哪一天的 |



2. **STAT**表（日报统计）

	| 列名            | 含义            | 备注                   |
	| -------------  |:-------------: | ----------------------:|
	| ID     			 | ID             |   主键                 |
	| type_name      | 类型            |   做市转让或协议转让      |
	| guapai         | 挂牌公司家数      |   四位数字              |
	| xinzeng        | 当日新增家数      |                        |
	| z_guben        | 总股本     		  |      单位：亿元         |
	| lt_guben       | 流通股本         |    单位：亿元            |
	| cj_zhishu      | 成交股票支数      |                        |
	| cj_jine        | 成交股票金额      |   单位：万              |
	| cj_shuliang    | 成交股票数量      |   单位：万              |
	| postdate       | 日报日期         |   代表这条日报是哪一天的  |


3. **SYSLOG**表（针对前两个表读取情况的日志记录）

	| 列名            | 含义           | 备注                    |
	| -------------  |:-------------: | ----------------------:|
	| ID     			 | ID            |   主键                  |
	| mission_type   | 任务类型        |   1是读取交易提示 2是读取日报 |
	| status         | 完成状态        | True代表完成 反之未完成   |
	| log_date       | log日期        |  记录的任务的日期，并不是执行日期|



4. **MAKER**表（做市商基本信息）

	| 列名            | 含义           | 备注                    |
	| -------------  |:-------------: | ----------------------:|
	| m_code         | 做市商账户代码    |    主键                |
	| m_name         | 做市商名称       |                        |
	| m_type         | 做市商类型       |                        |
	| recnum         | 推荐数量         |                        |
	| makernum       | 做市数量         |                        |



5. **RECOMMEND**表（做市商推荐信息，详细）

	| 列名            | 含义           | 备注                    |
	| -------------  |:-------------: | ----------------------:|
	| ID     			 | ID            |   主键                  |
	| m_name         | 做市商名称      |                         |
	| m_code         | 做市商账户代码   |                         |
	| s_code         | 股票代码      	|                         |
	| s_name         | 股票名称        |                         |
	| t_type         | 转让类型        |                         |
	| guapai_date    | 挂牌日期        |                         |


6. **MAKE**表（做市商做市信息，详细）

	| 列名            | 含义           | 备注                    |
	| -------------  |:-------------: | ----------------------:|
	| ID     			 | ID            |   主键                  |
	| host           | 主办券商        |                         |
	| host_code      | 券商账户代码     |                         |
	| s_code         | 股票代码      	|                         |
	| s_name         | 股票名称        |                         |
	| t_type         | 转让类型        |                         |
