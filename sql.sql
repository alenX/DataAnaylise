DROP TABLE IF EXISTS `dt_douban_new_books`;
CREATE TABLE `dt_douban_new_books` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TITLE` varchar(128) DEFAULT NULL,
  `AUTHOR` varchar(128) DEFAULT NULL,
  `DESC` varchar(128) DEFAULT NULL,
  `HREF` varchar(512) DEFAULT NULL,
  `SRC` text,
  `CONTENT` blob,
  `SCORE` double DEFAULT NULL,
  `BATCHDATE` varchar(0) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dt_douban_new_books
-- ----------------------------