create database if not exists `emaildata`;


create table if not exists `info`(
`id` int unsigned not null auto_increment primary key comment '主键',
`validation` char(32) not null default '' comment '用于验证该客服已经存在',
`username` char(10) not null default '' comment '姓名',
`age` char(20) not null default '' comment '年龄',
`sex` char(2) not null default '' comment '性别',
`phone` char(13) not null default '' comment '手机',
`email` char(255) not null default '' comment '邮箱',
`address` char(255) not null default '' comment '地址',
`source` char(50) not null default '' comment '来源',
`froms` char(100) not null default '' comment '来自邮箱',
`texts` text comment '其他资料',
`deliverytime` char(30) comment '投递时间',
`position` char(100) not null default '' comment '应聘职位',
`addtime` datetime,
UNIQUE KEY `validation` (`validation`)
)engine=innoDB default charset=utf8;

create table if not exists `statistical`(
`id` int unsigned not null auto_increment primary key comment '主键',
`info_id` int not null default 0 comment 'info表id',
`addtime` datetime,
UNIQUE KEY `info_id` (`info_id`)
)engine=innoDB default charset=utf8;


#配置表
create table if not exists `config`(
`id` int unsigned not null auto_increment primary key comment '主键',
`emailname` char(20) not null default '' comment '邮箱用户名',
`emailpwd` char(30) not null default '' comment '邮箱密码',
`emailpwd2` char(30) not null default '' comment '邮箱独立密码',
`followuserid` char(20) not null default '' comment '领取人 followUserId',
`addtime` datetime,
UNIQUE KEY `emailname` (`emailname`)
)engine=innoDB default charset=utf8;

