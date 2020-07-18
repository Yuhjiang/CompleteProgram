# Mysql数据库知识点

## 基本操作

### 数据库操作
- 创建数据库 `CREATE DATABASE database_name;`
- 删除数据库 `DROP DATABASE database_name;`

### 创建表

```txt
CREATE TABLE <表名>
(
字段名1，数据类型 [列级别约束条件] [默认值],
字段名2，数据类型 [列级别约束条件] [默认值],
...
[表级别约束条件]
)
```

Example:

```sql
CREATE TABLE tb_emp1
(
  id INT(11) PRIMARY KEY,
  name VARCHAR(25),
  deptId INT(11),
  salary FLOAT
);
```

#### 主键约束

- 是表中一列或多列的组合，主键约束(Primary Key Constraint)要求主键列的数据唯一，并且不允许为空。可以和其他表做关联，也可以加快数据库查询的速度。

- 单字段主键由一个字段组成，语法规则`字段名 数据类型 PRIMARY KEY [默认值]`。也可以在定义所有列之后指定主键`[CONSTRAINT <约束名>] PRIMARY KEY([字段名])`

  ```sql
  CREATE TABLE tb_emp1
  (
    id INT(11) PRIMARY KEY,
  	...
  );
  
  CREATE TABLE tb_emp1
  (
    id INT(11),
    ...
    PRIMARY KEY(id)
  );
  ```

- 多字段联合主键，`PRIMARY KEY [字段1] [字段2]...`

  ```sql
  CREATE TABLE tb_emp2
  (
    name VARCHAR(25),
    deptId INT(11),
    PRIMARY KEY(name, deptId)
  )
  ```

#### 外键约束

- 外键用来在两个表的数据之间建立链接。外键对应的是参照完整性，可以为空值，如果不是空值则每一个必须等于另一个表中的主键。

  - 主表(父表): 对于两个具有关联关系的表，相关联字段中主键所在的那个表

  - 从表(子表): 对于两个具有关联关系的表，相关联字段中外键所在的那个表

- 创建外键的语法`[CONSTRAINT <约束名>] FOREIGN KEY 字段1 [, 字段2...] REFERENCE <主表名> 主键列1 [, 主键列2, ...]`

  ```sql
  CREATE TABLE tb_emp5
  (
    id INT(11) PRIMARY KEY,
    salary FLOAT,
    CONSTRAINT fk_empt_dept1 FOREIGN KEY(deptId) REFERENCE tb_dept1(id)
  );
  ```

#### 非空约束

- 指定字段的值不能为空。`字段名 数据类型 NOT NULL`

  ```sql
  CREATE TABLE tb_emp8
  (
    name VARCHAR(25) NOT NULL,
    salary FLOAT
  )
  ```

#### 唯一约束

- 要求该列唯一，允许为空，但只能出现一个空值。`字段名 数据类型 UNIQUE`

  ```sql
  CREATE TABLE tb_emp9
  (
    id INT(11) PRIMARY KEY,
    location VARCHAR(50) UNIQUE
  );
  
  CREATE TABLE tb_emp9
  (
    id INT(11) PRIMARY KEY,
    name VARCHAR(22),
    CONSTRAINT STH UNIQUE(name)
  );
  ```

- 一个表中可以有多个字段声明为UNIQUE，但只能有一个PRIMARY声明

#### 使用默认约束

- 追定某列的默认值。`字段名 数据类型 DEFAULT 默认值`

  ```sql
  CREATE TABLE tb_emp7
  (
    id INT(11) PRIMARY KEY,
    deptId INT(11) DEFAULT 1111
  );
  ```

#### 设置表的属性自增

- `字段名 数据类型 AUTO_INCREMENT`

  ```sql
  CREATE TABLE tb_emp7
  (
    id INT(11) PRIMARY KEY AUTO_INCREMENT,
    deptId INT(11) DEFAULT 1111
  );
  ```

### 查看数据表的结构

- 查看表的基本结构：DESCRIBE 表名;  DESC 表名;

  ```sql
  mysql> desc worker;
  +-------+-------------+------+-----+---------+----------------+
  | Field | Type        | Null | Key | Default | Extra          |
  +-------+-------------+------+-----+---------+----------------+
  | ID    | int(11)     | NO   | PRI | NULL    | auto_increment |
  | name  | varchar(30) | YES  |     | NULL    |                |
  +-------+-------------+------+-----+---------+----------------+
  ```

- 查看表的详细结构: SHOW CREATE TABLE <表名\G>

  ```sql
  mysql> show create table worker \G
  *************************** 1. row ***************************
         Table: worker
  Create Table: CREATE TABLE `worker` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`ID`)
  ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  ```

### 修改数据表

- 修改表名`ALTER TABLE <表名> RENAME [TO] <新表名>;`

  ```sql
  ALTER TABLE tb_dept3 RENAME tb_dept4;
  ```

- 修改字段的数据类型`ALTER TABLE <表名> MODIFY <字段名> <数据类型>;`

  ```sql
  ALTER TABLE tm_dept1 MODIFY name VARCHAR(30);
  ```

- 修改字段名 `ALTER TABLE <表名> CHANGE <旧字段名> <新字段名> <新数据类型>;`

  ```sql
  ALTER TABLE tmp_dept1 CHANGE location loc VARCHAR(50);
  ALTER TABLE tmp_dept1 CHANGE loc location VARCHAR(60);
  ```

- 添加字段名 `ALTER TABLE <表名> ADD <新字段名> <数据类型> [约束条件] [FIRST | AFTER 已存在的字段名];`

  ```sql
  - 添加无完整性约束条件
  ALTER TABLE tb_dept1 ADD managerId INT(10);
  
  - 添加有完整性约束条件的字段
  ALTER TABLE tb_dept1 ADD column1 VARCHAR(12) NOT NULL;
  
  - 在表的第一列添加一个字段
  ALTER TABLE tb_dept1 ADD column2 INT(11) FIRST;
  
  - 在表的指定列后添加一个字段
  ALTER TABLE tb_dept1 ADD column3 INT(11) AFTER name;
  ```

- 删除字段 `ALTER TABLE <表名> DROP <字段名>`

  ```sql
  ALTER TABLE tb_dept1 DROP column2;
  ```

- 修改字段的排列位置 `ALTER TABLE <表名> MODIFY <字段1> <数据类型> FIRST|AFTER <字段2>;`

  ```sql
  ALTER TABLE tb_dept1 MODIFY column1 VARCHAR(12) FIRST;
  ALTERT TABLE tb_dept1 MODIFY column1 VARCHAR(12) AFTER location;
  ```

- 更改表的存储引擎 `ALTER TABLE <表名> ENGINE=<更改后的存储引擎名>;`

  ```sql
  ALTER TABLE tb_deptment3 ENGINE=MyISAM;
  ```

- 删除表的外键约束 `ALTER TABLE <表名> DROP FOREIGN KEY <外键约束名>;`

## 数据类型

### 整数类型

| 类型名称  | 存储需求 | 有符号                 | 无符号       |
| --------- | -------- | ---------------------- | ------------ |
| TINYINT   | 1byte    | -128~127               | 0~255        |
| SMALLINT  | 2byte    | -32768~32767           | 0~65535      |
| MEDIUMINT | 3byte    | -8388608~8388607       | 0~16777215   |
| INT       | 4byte    | -2147483648~2147483647 | 0~4294967295 |
| BIGINT    | 8byte    |                        | ...          |

- INT(11)，其中11指的是显示宽度，和类型的数据位数无关。如果数据少于指定的宽度会用空格填充，如果超过显示宽度还是正常显示不会被强制显示成宽度。

### 浮点数和定点数类型

- 浮点数有两种：单精度浮点类型FLOAT和双精度浮点类型DOUBLE。定点类型只有一种DECIMAL。浮点数和定点数都可以用(M, N)表示，M称为精度，表示总共的位数，N称为标度，表示小数的位数。

  | 类型名称           | 存储需求 |
  | ------------------ | -------- |
  | FLOAT              | 4bytes   |
  | DOUBLE             | 8bytes   |
  | DECIMAL(M, D), DEC | M+2bytes |

- DECIMAL可能的最大取值范围与DOUBLE一致，但有效的取值范围由M和D决定。DOUBLE的数据超过定义的标度时，会产生警告

- 对精度要求高的情况下使用DECIMAL

### 文本字符串

| 类型名称   | 说明                                        | 存储需求                                                 |
| ---------- | ------------------------------------------- | -------------------------------------------------------- |
| CHAR(M)    | 固定长度字符串                              | Mbytes,1≤M≤255                                           |
| VARCHAR(M) | 变长字符串                                  | L+1bytes，L≤M&1≤M≤255                                    |
| TINYTEXT   | 非常小的字符串                              | L+1bytes, L<2^8                                          |
| TEXT       | 小的字符串                                  | L+2bytes, L<2^16                                         |
| MEDIUMTEXT | 中等大小的字符串                            | L+3bytes, L<2^24                                         |
| LONGTEXT   | 大的字符串                                  | L+4bytes, L<2^32                                         |
| ENUM       | 枚举类型，只能有一个枚举字符串值            | 1or2byte2,取决于枚举值的数目                             |
| SET        | 一个集合，字符串对象可以有零个或多个SET成员 | 1、2、3、4or8bytes，取决于集合成员的数量（最多64个成员） |

- VARCHAR和TEXT是变长类型，存储需求取决于列值的实际长度和记录字符串的长度。
- CHAR(M)为固定长度字符串，定义时指定字符串列长，保存时右侧填充空格到指定长度。检索到CHAR时，尾部的空格会被删除
- VARCHAR(M)是长度可变字符串，M表示最大的列长度，VARCHAR最大实际长度由最长的行的大小和使用的字符集确定。例如定义了VARCHAR(50)，存储了10个字符时，实际存储的字符串为10个字符+1结束字符
- TEXT保存非二进制字符串，适合文章内容，评论等
- ENUM，其值为创建表时指定的枚举值 `字段名 ENUM('x', 'y', 'z')`ENUM列总有一个默认值，如果将ENUM列声明为NULL，NULL值则为该列第一个有效值，并且默认值为NULL，如果ENUM列被声明为NOT NULL，默认值为允许的值列表第一个元素。

### 二进制字符串类型

| 类型名称      | 存储要求        |
| ------------- | --------------- |
| BIT(M)        | 大约(M+7)/8字节 |
| BINARY(M)     | M字节           |
| VARBINARY(M)  | M+1字节         |
| TINYBLOB(M)   | L+1字节，L<2^8  |
| BLOB(M)       | L+2, L<2^16     |
| MEDIUMBLOB(M) | L+3, L<2^24     |
| LONGBLOB(M)   | L+4, L<2^32     |

### 如何选择数据类型

- 整数和浮点数
  - 使用浮点数时，存入的数值会根据定义的小数位进行四舍五入，DOUBLE精度比FLOAT高
- 浮点数和定点数
  - 当长度一定的情况下，DOUBLE和FLOAT能比DECIMAL表示更大的数据范围，但由于浮点数四舍五入会有误差，精确度要求高的场景下选择DECIMAL
  - DECIMAL在MySQL中是字符串存储的
- CHAR和VARCHAR选择
  - char是固定长度字符，VARCHAR是可变长度字符
  - char会自动删除插入数据的尾部空格，varchar会保留尾部空格
  - char处理速度比varchar快，但是浪费存储空间
  - 对于MyISAM引擎，推荐使用char代替varchar，提高检索速度
  - InnoDB引擎下，使用可变长度的数据类型，因为InnoDB数据表的存储格式不分固定长度和可变长度。
- BLOB和TEXT
  - BLOB是二进制字符串，主要存储图片、音频信息
  - TEXT只能存储纯文本文件
- timestamp和datetime
  - 尽量使用timestamp存储，空间效率高于datetime

## 数据库查询

### 字符串模糊匹配

- `%`匹配任意长度的字符，包括零字符
- `_`一次只能匹配任意一个字符

### having和where的区别

- where用在分组之前筛选记录，where排除的记录不再包括在分组中

- having是在数据分组之后进行过滤来选择分组

  ```sql
  SELECT s_id, GROUP_CONCAT(f_name) AS names
  FROM fruits
  GROUP BY s_id HAVING COUNT(f_name) > 1;
  ```

### 连接查询

#### 内连接查询

内连接列出两张表中与连接条件相匹配的数据行，组成新纪录。双方都满足条件的记录才会出现在结果关系中。

```sql
SELECT suppliers.s_id, s_name, f_name, f_price
FROM fruits, supplies
WHERE fruits.s_id = suppliers.s_id;

SELECT suppliers.s_id, s_name, f_name, f_price
FROM fruits INNER JOIN supplies
ON fruits.s_id = suppliers.s_id;
```

自连接（连接的表都是自己）

```sql
SELECT f1.f_id, f1.f_name
FROM fruits AS f1, fruits AS f2
WHERE f1.s_id == f2.s_id AND f2.f_id = 'a1';
```

#### 外连接查询

- LEFT JOIN：返回包括左表中所有记录和右表中连接字段相等的记录

  ```sql
  SELECT customers.c_id, orders.o_num 
  FROM customers LEFT JOIN orders 
  ON customers.c_id = orders.c_id;
  
  +-------+-------+
  | c_id  | o_num |
  +-------+-------+
  | 10001 | 30001 |
  | 10003 | 30002 |
  | 10001 | 30005 |
  |  1004 |  NULL |
  | 10002 |  NULL |
  +-------+-------+
  ```

- RIGHT JOIN：返回包括右表中所有记录和左表中连接字段相等的记录

  ```sql
  SELECT customers.c_id, orders.o_num 
  FROM customers RIGHT JOIN orders 
  ON customers.c_id = orders.c_id;
  
  +-------+-------+
  | c_id  | o_num |
  +-------+-------+
  | 10001 | 30001 |
  | 10003 | 30002 |
  |  NULL | 30003 |
  |  NULL | 30004 |
  | 10001 | 30005 |
  +-------+-------+
  ```

- FULL JOIN：全连接，返回所有数据行

  ```sql
  SELECT customers.c_id, orders.o_num 
  FROM customers LEFT JOIN orders 
  ON customers.c_id = orders.c_id 
  UNION 
  SELECT customers.c_id, orders.o_num
  FROM customers RIGHT JOIN orders 
  ON customers.c_id = orders.c_id;
  
  +-------+-------+
  | c_id  | o_num |
  +-------+-------+
  | 10001 | 30001 |
  | 10003 | 30002 |
  | 10001 | 30005 |
  |  1004 |  NULL |
  | 10002 |  NULL |
  |  NULL | 30003 |
  |  NULL | 30004 |
  +-------+-------+
  ```

### UNION和UNION ALL区别

- UNION ALL不会删除重复行，并且执行所需的资源少
- UNION会自动删除重复的行

## 索引

## 索引创建删除方式

```sql
CREATE TABLE table_name [col_name data_type] [UNIQUE|FULLTEXT|SPATIAL] [INDEX|KEY] [index_name] [col_name {length}] [ASC|DESC]

ALTER TABLE table_name ADD [UNIQUE|FULLTEXT|SPATIAL] [INDEX|KEY] [index_name] (col_name[length], ..) [ASC|DESC]

CREATE [UNIQUE|FULLTEXT|SPATIAL] [INDEX|KEY] [index_name] ON table_name (col_name[length], ...) [ASC | DESC]

ALTER TABLE table_name DROP INDEX index_name

DROP INDEX index_name ON table_name;
```

### 索引分类

#### 普通索引和唯一索引

- 普通索引和唯一索引：普通索引是Mysql的基本索引类型，允许在定义索引的列中插入重复值和空值。唯一索引的值必须唯一，但允许有空值。主键索引是特殊的唯一索引，不允许有空值

- 创建表的时候创建索引

  ```sql
  CREATE TABLE book
  (
  	bookid INT NOT NULL,
  	bookname VARCHAR(255) NOT NULL,
  	year_publication YEAR NOT NULL,
  	INDEX(year_publication)
  )
  
  CREATE TABLE book
  (
  	id INT NOT NULL,
  	name CHAR(30) NOT NULL,
  	UNIQUE INDEX UniqIdx(id)
  );
  ```

- 在已存在的表上创建索引

  ```sql
  ALTER TABLE book ADD INDEX BKnameIdx(bookname(30));
  
  ALTER TABLE book ADD UNIQUE INDEX UniqidIdx (bookId);
  ```

#### 单列索引和组合索引

- 单列索引即一个索引只包含单个列，一个表可以有多个单列索引

- 组合索引指在多个字段组合上创建的索引，只有在查询条件中使用了这些字段的左边字段时，索引才会被使用。使用组合索引遵循最左前缀集合

- 创建表的时候创建索引

  ```sql
  CREATE TABLE t2
  (
    id INT NOT NULL,
    name CHAR(50) NULL,
    INDEX SingleIdx(name(20))
  );
  
  CREATE TABLE t3
  (
    id INT NOT NULL,
    name CHAR(30) NOT NULL,
    INDEX MultiIdx(id, name(10))
  );
  ```

- 在已存在的表上创建索引

  ```sql
  ALTER TABLE book ADD INDEX BkcmtIdx(comment(50));
  
  ALTER TABLE book ADD INDEX BkAuANDInfoIdx (authors(30), info(50));
  ```

#### 全文索引

- 全文索引类型为FULLTEXT，在定义索引的列上支持值的全文查找，允许在这些索引列中插入重复值和空值。全文索引可以在CHAR，TEXT和VARCHAR类型的列上创建。只有M有ISAM支持全文索引

- 创建表的时候创建索引

  ```sql
  CREATE TABLE t4
  (
    id INT NOT NULL,
    name CHAR(30) NOT NULL,
    info VARCHAR(255),
    FULLTEXT INDEX FullTxtIdx(info)
  );
  ```

- 在已存在的表上创建索引

  ```sql
  ALTER TABLE t6 ADD FULLTEXT INDEX infoFullIdx (info);
  ```

  

#### 空间索引

- 对空间数据类型的字段建立索引，创建空间索引的列必须声明为NOT NULL，只能在M y ISAM中使用

- 创建表的时候创建索引

  ```sql
  CREATE TABLE t5
  (
    g GEOMETRY NOT NULL,
    SPATIAL INDEX spatIdx(g)
   ) ENGINE=MyISAM;
  ```

## 性能分析

### EXPLAIN

```sql
+----+-------------+--------+------------+------+---------------+------+---------+------+------+----------+-------+
| id | select_type | table  | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra |
+----+-------------+--------+------------+------+---------------+------+---------+------+------+----------+-------+
|  1 | SIMPLE      | fruits | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    8 |   100.00 | NULL  |
+----+-------------+--------+------------+------+---------------+------+---------+------+------+----------+-------+
```

- id: SELECT标识符

- select_type:

  - SIMPLE: 简单查询，不包含连接查询和子查询
  - PRIMARY：主查询或者是最外层的查询
  - UNION：表示连接查询的第2个或后面的查询语句
  - DEPENDENT UNION：连接查询中的第2个或后面的查询语句，取决于外面的查询
  - UNION RESULT：连接查询的结果
  - SUBQUERY：子查询中第1个query查询
  - DEPENDENT SUBQUERY：子查询中第1个SELECT，取决于外面的查询
  - DERIVED：到处表的SELECT

- table：查询的表

- type: 从最佳类型到最差类型

  - system: 该表是仅有一行的系统表

  - const: 数据表最多一个匹配行

    ```sql
     explain select * from fruits where f_id = 'a1';
    +----+-------------+--------+------------+-------+------------------------+---------+---------+-------+------+----------+-------+
    | id | select_type | table  | partitions | type  | possible_keys          | key     | key_len | ref   | rows | filtered | Extra |
    +----+-------------+--------+------------+-------+------------------------+---------+---------+-------+------+----------+-------+
    |  1 | SIMPLE      | fruits | NULL       | const | PRIMARY,index_id_price | PRIMARY | 40      | const |    1 |   100.00 | NULL  |
    +----+-------------+--------+------------+-------+------------------------+---------+---------+-------+------+----------+-------+
    ```

  - eq_ref: 对于每个来自前面的表的行组合，从该表中读取一行。当一个索引的所有部分都在查询使用并且索引是UNIQUE或PRIMARY KEY时，可用这种类型

  - ref: 对于来自前面z的表的任意行组合，将从该表中读取所有匹配的行。这种类型用于索引既不是UNIQUE也不是PRIMARY KEY的情况，或者查询中用了索引列的左子集

  - ref_or_null: 连接类型同ref，但是可以搜索包含NULL的行

  - index_merge: 使用了索引合并优化方法，key列包含了使用的索引的清单，key_len包含了使用的索引的最长的关键元素

  - unique_subquery: 是一个索引查询函数，可以完全替代子查询

    ```sql
    value IN (SELECT primary key FROM single_table WHERE some_expr)
    ```

  - index_subquery: 类似unique_subquery，可以替换IN子查询，适合下列形式的子查询中非唯一索引

    ```sql
    value IN (SELECT key_column FROM single_table WHERE some_expr)
    ```

  - range: 只检索给定范围的行，使用一个索引选择行。key显示了使用哪个索引，key_len包含所有索引的最长关键元素

  - index: 连接类型和ALL相同，但只扫描索引树

  - ALL: 对于前面表的任意行组合，进行完整的表扫描

- possible_keys: 指出Mysql能用哪个索引
- key: 查询实际使用到的索引
- key_len: Mysql选择索引字段按字节计算的长度
- ref: 表示使用哪个列或常数与索引一起来查询
- rows: Mysql在表中查询时必须检查的行数

