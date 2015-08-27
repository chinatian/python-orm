# 使用python千行代码搞定数据库分布分表
## 要解决的问题
- 应用程序随着业务量增加主要的性能瓶颈在数据库存取上
- 大多数数据库没有完善的分库分表的机制，单表超过1000万速度会明显下降
- 本文章是通过python语言实现一个可在生产环境下使用的一套分库分表系统
## 技术储备
- 要求python2.6+，但不是3
- 安装mysql数据库
- 在win下或者linux下下载各种资源包使python能够连接mysql
- 能够使用python独立完成程序的编写

## 代码编写
### 基本原理说明
如何解决怎么分配主键id的问题，其实这个问题有两个一是主键如何分配，二是主键id如何不重复
在每个数据内放置一个单独记录该数据中有哪些表并且每个表当前最大id是多少。
该表数据结构如下
<pre><code>
CREATE TABLE `seq` (
  `id` bigint(20) NOT NULL,
  `tb` varchar(32) NOT NULL,
  UNIQUE KEY `tb_UNIQUE` (`tb`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='生成id序列号';
</code></pre>
- seq存放数据如下：
id  tb
1	user_0
17	user_1
417	user_10
177	user_11
193	user_12
209	user_13
225	user_14
241	user_15
289	user_2
49	user_3
65	user_4
337	user_5
97	user_6
113	user_7
129	user_8
145	user_9
1	user_index_0
17	user_index_1
161	user_index_10
177	user_index_11
193	user_index_12
209	user_index_13
225	user_index_14
241	user_index_15
33	user_index_2
49	user_index_3
65	user_index_4
337	user_index_5
97	user_index_6
113	user_index_7
129	user_index_8
145	user_index_9


 
每个数据库中都会存在这样一个表，主键的id分配由各自的数据库负责，减少由中心服务器分配带来的压力单点的问题。
 
3.2 分库分表的规模设定
设定分为16个数据库，每个表在每个数据库中有16个分表。
比如user表：
CREATE TABLE `user_0` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(200) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=36583 DEFAULT CHARSET=utf8;
建立16个数据库，每个数据库中user表的数量为16个，这样user表会有16×16个分表
数据库截图如下：
 
每个数据库中user表的截图如下：
 
3.3 代码编写
3.3.1 目录结构
 
db - 数据库访问工具类
moddels - 数据模型
sql - 数据库创建及数据表创建
3.3.2 数据库访问工具类
直接使用Facebook的开源代码，截图如下：
 
 
3.3.3 数据库创建及数据表创建
数据库以及表的创建需要编写程序实现，主要代码存在sql中
  
第一步：init_db.py 负责创建16个数据库：
 
第二步：seq.py在每个表中创建seq表
 
第三步：创建具体数据表
 
3.3.4 核心models层说明
 

base.py 作为全部models的基类，其他类需继承 代码截屏如下：
 
 
3.4 代码使用
插入：
 
查询：
 


