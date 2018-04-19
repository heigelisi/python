create database if not exists `spider`;

create table if not exists `dz`(
`id` int(11) unsigned not null auto_increment primary key,
`url` char(250) not null default '' comment '网址',
`title` varchar(500) not null default '' comment '网站标题'
)engine=innodb default charset=utf8 comment '抓取到的dz';


create table if not exists `stay`(
`id` int(11) unsigned not null auto_increment primary key,
`url` char(250) not null default '' comment '网址',
`title` varchar(500) not null default '' comment '网站标题'
)engine=innodb default charset=utf8 comment '等待抓取';

create table if not exists `already`(
`id` int(11) unsigned not null auto_increment primary key,
`url` char(250) not null default '' comment '网址',
`title` varchar(500) not null default '' comment '网站标题'
)engine=innodb default charset=utf8 comment '已经抓取';