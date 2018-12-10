/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50715
 Source Host           : localhost:3306
 Source Schema         : pythontest

 Target Server Type    : MySQL
 Target Server Version : 50715
 File Encoding         : 65001

 Date: 29/11/2018 11:37:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bookinfo
-- ----------------------------
DROP TABLE IF EXISTS `bookinfo`;
CREATE TABLE `bookinfo`  (
  `bid` int(10) NOT NULL COMMENT '书ID',
  `bname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '书名',
  `bprice` decimal(10, 2) NULL DEFAULT NULL COMMENT '书价',
  `tid` int(4) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `bcount` int(255) UNSIGNED NULL DEFAULT NULL COMMENT '书数量',
  PRIMARY KEY (`bid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bookinfo
-- ----------------------------
INSERT INTO `bookinfo` VALUES (2, 'def', 12.00, 0001, 1);
INSERT INTO `bookinfo` VALUES (4, 'Docker容器技术', 80.00, 0004, 28);

-- ----------------------------
-- Table structure for booktype
-- ----------------------------
DROP TABLE IF EXISTS `booktype`;
CREATE TABLE `booktype`  (
  `tid` int(4) UNSIGNED ZEROFILL NOT NULL COMMENT '类别编号',
  `tname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '类别名',
  PRIMARY KEY (`tid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of booktype
-- ----------------------------
INSERT INTO `booktype` VALUES (0001, 'None');
INSERT INTO `booktype` VALUES (0002, 'Java');
INSERT INTO `booktype` VALUES (0003, 'PYTHON');
INSERT INTO `booktype` VALUES (0004, 'Docker');
INSERT INTO `booktype` VALUES (0006, 'PHP');
INSERT INTO `booktype` VALUES (0007, 'Ruby');
INSERT INTO `booktype` VALUES (0008, '123');

-- ----------------------------
-- Table structure for shoplist
-- ----------------------------
DROP TABLE IF EXISTS `shoplist`;
CREATE TABLE `shoplist`  (
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `bid` int(10) UNSIGNED NOT NULL,
  `scount` int(255) UNSIGNED NOT NULL,
  PRIMARY KEY (`username`, `bid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shoplist
-- ----------------------------
INSERT INTO `shoplist` VALUES ('123', 2, 2);
INSERT INTO `shoplist` VALUES ('123', 4, 2);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `is_manager` tinyint(1) NOT NULL DEFAULT 0 COMMENT '1 是管理员，0是普通用户',
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('123', '123', 0);
INSERT INTO `user` VALUES ('m', '123', 1);
INSERT INTO `user` VALUES ('man', '123', 1);
INSERT INTO `user` VALUES ('manager', '123', 1);
INSERT INTO `user` VALUES ('root', 'root', 1);

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo`  (
  `userno` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户编号',
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `gender` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '性别',
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `telephone` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '电话',
  PRIMARY KEY (`userno`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES (1, '123', '123', '0', NULL, NULL, NULL);
INSERT INTO `userinfo` VALUES (4, 'root', 'root', 'jiangydev', '男', 'jiangydev@gmail.com', '15195893199');
INSERT INTO `userinfo` VALUES (7, 'm', '123', 'm', '男', 'jiangydev@gmail.com', '15195893199');
INSERT INTO `userinfo` VALUES (8, 'manager', '123', 'manager', '男', 'jiangydev@qq.com', '15195893199');
INSERT INTO `userinfo` VALUES (9, 'man', '123', 'jiang', '男', 'sdfsa@qq.com', '15195893199');

SET FOREIGN_KEY_CHECKS = 1;
