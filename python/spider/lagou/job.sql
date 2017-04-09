/*
Navicat MySQL Data Transfer
Source Server         : lagou
Source Server Version : 50613
Source Host           : localhost:3306
Source Database       : lagou
Target Server Type    : MYSQL
Target Server Version : 50613
File Encoding         : 65001
Date: 2016-04-19 22:03:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for job
-- ----------------------------
DROP TABLE IF EXISTS `simplejob`;
CREATE TABLE `simplejob` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(32) DEFAULT NULL,
  `education` varchar(16) NOT NULL COMMENT '０－本科　１－硕士　２－博士　３－大专　４－不限　５－其它',
  `company_full_name` varchar(64) DEFAULT NULL,
  `finance_stage` varchar(32) DEFAULT NULL,
  `work_year_low` int(11) NOT NULL DEFAULT '-1' COMMENT '－１－表示不限',
  `work_year_high` int(11) NOT NULL DEFAULT '-1',
  `salary_low` int(11) NOT NULL DEFAULT '-1' COMMENT '工作年限',
  `salary_high` int(11) NOT NULL DEFAULT '-1',
  `staffs_low` int(11) NOT NULL DEFAULT '-1',
  `staffs_high` int(11) NOT NULL DEFAULT '-1' COMMENT '员工数',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1732298 DEFAULT CHARSET=utf8;
