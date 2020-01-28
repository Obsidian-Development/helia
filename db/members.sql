/*
Navicat SQLite Data Transfer

Source Server         : test123
Source Server Version : 31300
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 31300
File Encoding         : 65001

Date: 2017-04-17 20:45:45
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for members
-- ----------------------------
DROP TABLE IF EXISTS "main"."members";
CREATE TABLE "members" (
"userid"  INTEGER NOT NULL,
"coins"  INTEGER NOT NULL DEFAULT 0,
"user_mention"  TEXT,
PRIMARY KEY ("userid" ASC)
);
PRAGMA foreign_keys = ON;
