# NEEQ数据抓取程序简易文档

## 配置（CentOS）
###系统要求：

	- MySQL
	- Python3.4 及以上
	- mysql-connector for python (Connector/Python)

**准备工作之安装Python：**

1. 准备编译环境

        yum groupinstall 'Development Tools'
        yum install zlib-devel bzip2-devel openssl-devel ncurese-devel

2. 下载Python代码包（3.5.1版本为例）

	    wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz

3. 编译

	    tar Jxvf Python-3.5.1.tar.xz
	    cd Python-3.5.1
	    ./configure --prefix=/usr/local/python3
	    make && make install

	注意：

	    Python3.5.1 安装编译安装时会默认安装 pip 如果出现：
	    Ignoring ensurepip failure: pip 1.5.6 requires SSL/TLS
	    未安装编译环境，重新安装该编译环境并重新编译 Python3.5.1
	    yum install zlib-devel bzip2-devel openssl-devel ncurese-devel

4. 可能需要的备份Python

		mv /usr/bin/python usr/bin/python2.7
		ln -s /usr/local/python3/bin/python3.5 /usr/bin/python
		ln -s /usr/local/python3/bin/pip3 /usr/bin/pip

	检查版本：

		python --version
		pip --version

5. 其他参考：

		http://www.jianshu.com/p/8bd6e0695d7f

**准备工作之安装Connector/Python**

	https://dev.mysql.com/doc/connector-python/en/connector-python-installation-source.html

## 简易使用说明

1. 文字版说明引导程序

		cd ~/Desktop/neeq_fetcher/src
		python setup.py
		备注：一定要切换到目录后再输入python setup.py
		使用类似 python ~/Desktop/neeq_fetcher/src/setup.py 是不行的

2. 通过脚本直接操作

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
				python tradingtips.py

				抓取指定日期交易提示 日期格式 YYYY-MM-DD
				python tradingtips.py start end

			日报统计：
				抓取前一日日报统计
				python statdata.py

				抓取指定日期交易提示 日期格式 YYYY-MM-DD
				python tradingtips.py start end

			做市商信息：
				python listedmaker.py
				备注：时间较长，一般3-5分钟

3. Shell命令操作

		一共有两个shell脚本，分别为init.sh和fetch.sh
		使用：
			初始化数据库（全部）
			cd ~
			. init.sh
			
			获取数据
			

##更改数据库配置

目前配置类参数只有数据库的参数转移到了fetch_config.py文件中，之后做简易重构时候会把参数都移到这个文件

更改数据库配置只需要到fetch_config.py文件中找到DB_CONFIG这个字典更改参数即可

例如

	DB_CONFIG = {
	    'user': 'stock',
	    'password': 'stock123',
	    'host': '192.168.202.161',
	    'database': 'stockdb'
	}


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
