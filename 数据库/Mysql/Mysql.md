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

## 数据库概念

### 数据库引擎

#### 1. InnoDB存储引擎
- 支持事务安全表（ACID），支持行锁定和外键。Mysql5.5之后是默认引擎
- 提供了提交、回滚和崩溃恢复能力的事务安全特性
- 为处理巨大数据量的最大性能设计
- 在主内存中缓存数据和索引而维持自己的缓冲池。表和索引放在同一个逻辑表空间中，表空间可以包含多个文件。
- 锁是行级的，粒度小，写操作不会锁定全表，在并发高的时候，效率高。适合update和insert多的表
- 支持外键完整性约束
- 不保存行数，执行 `SELECT COUNT(*) FROM table;`时需要全表扫描。

#### 2. MyISAM存储引擎
- 不支持事务
- 用一个变量保存了整个表的行数，查询快
- 锁是表级的，所以频繁更新数据效率低，适合大量查询的表
- 每个表的最大索引数是64（可以通过编译改变），最大的键长度是1000B（也可以通过编译改变）
- BLOB和TEXT列可以被索引，NULL允许在索引的列中
- 可以把数据文件和索引文件放在不同的目录下
- 每个字符列可以有不同的字符集
- 创建数据库时，产生3个文件，frm存储表定义，MYD是数据文件，MYI是索引文件

#### 3. MEMORY存储引擎

- 将表中数据存储到内存中，为查询和引用其他表数据提供快速访问
- MEMORY每个表最多支持32个索引，每个索引16列，以及500B最大键长度
- 存储引擎执行HASH和BTREE索引
- 可以在一个MEMORY表中有非唯一键
- 使用一个固定的记录长度格式
- 不支持BLOB和TEXT
- 支持AUTO_INCREMENT列和对可包含NULL值的列索引
- 所有客户端共享，内容被存在内存中
- 不再需要MEMORY表时，执行`DELETE FROM  or TRUNCATE TABLE or DROP TABLE`

### 聚集索引和非聚集索引
- InnoDB是聚集索引，MyISAM是非聚集索引。
- 聚集索引的文件存放在主键索引的叶子节点上，所以InnoDB必须要有主键。主键索引效率高，辅助索引需要查两次，第一次查主键索引，再通过主键查询到数据
- 非聚集索引的数据文件是分离的，索引保存的数据文件的指针，主键索引和辅助索引是分离的。

### Mysql的MVCC原理

#### 基本原理
[Mysql MVCC原理](https://juejin.im/post/5c68a4056fb9a049e063e0ab)
- MVCC是多版本并发控制，简单地说每个连接到数据库的用户看到的数据只是一个快照，在写操作或
事务提交之前对于其他用户是不可见
- 在更新一条数据库记录时，不会直接覆盖旧数据，而是将旧数据标记为过时版本，并在其他地方增加
新版本数据，新旧数据会同时存在。这种方式允许其他用户读取正在被别人修改的数据的旧数据。
- 需要系统周期性整理过时的旧数据。Mysql的MVCC提供了时点一致性视图，并发控制下的读事务一般
使用时间戳或事务ID去标记当前读的数据库的版本，读取这个版本的数据。
- 这种情况下读写是分离的，读取旧版本数据，写入新版本数据
- 一句话总结：MVCC就是同一份数据临时保存多版本的方式，进而实现并发控制

#### 实现细节
1. Mysql建表的时候，每个表有三个隐藏的行，其中两个是`DB_TRX_ID数据行的版本号`&`回滚指针DB_ROLL_PTR`
2. 插入数据的时候，事务的ID会记录到DB_TRX_ID
3. 删除数据的时候，事务的ID会记录到DB_ROLL_PT，数据当时并没有被实际删除
4. 修改数据的时候，会事先复制一条被修改的数据，并在DB_ROLL_PT记录事务ID，然后在新的数据里
记录DB_TRX_ID
5. 查询的时候：1、查询数据行版本号早于当前事务版本的数据行记录；2、查询删除版本号为NULL或大于
当前事务版本号的数据，确保查询的数据行记录在事务开启前没有被删除。

## 数据库概念

### 事务的4个特性
1. 原子性：事务是在逻辑上不可分割的操作单元，其所有语句要么全都执行要么全都不执行
2. 一致性：逻辑上的保证操作，将数据库从某个一致性状态转换到另一个一致性状态（比如两个共有5000元，互相赚钱都要保证这两个人总和还是5000元）
3. 隔离性：在并发的情况下，避免同时对数据库的多个操作对数据一致性产生影响，需要隔离并发运行的多个事务间的互相影响
4. 持久性：一旦事务提交成功，对数据的修改是持久性的。即时发生了系统故障，已提交的事务所做的数据的修改也不会丢失。

### 事务的不进行隔离会产生的问题
1. 脏读：A事务读取了被B事务正在修改但没有提交的数据。B事务在多次修改某个数据，但一直未提交修改。这是另一个A事务来读取被B修改的数据，会造成两个事务的数据不一致
2. 不可重复读：同一个事务中，同一个查询在Time1时刻读取某一行，在time2时刻重新读取这一行数据，发现一行的数据已经被另一个事务修改或删除了。 <i>不可重复读是由于事务并发修改同一条记录导致的</i>
3. 幻读：同一个事务中，同一查询多次执行的时候，由于其他插入操作的事务提交，会导致每次返回不同的结果集。<i>幻读是由于并发事务增加记录导致的</i>

### 事务的四种隔离级别
1. Read Uncommited未提交读：所有事务都可以看到其他未提交事务的执行结果。
2. Read Committed提交读：大多数数据库默认的隔离级别。一个事务从开始直到提交，其他事务都不可读取到期间修改的结果。
3. Repeated Read可重复读：确保同一个事务在多次读取同样的数据时候，得到同样的结果（InnoDB通过MVCC实现）
4. Serializable可串行化：最高的隔离级别，强制事务的排序，强制事务串行执行，使之不能相互冲突。原理是在每个读的数据行上加上共享锁。

### 视图的概念
- 视图是从数据库基本表中选取数据组成的逻辑窗口。它是一个虚拟表，内容由查询定义。行和列数据来自由定义视图的查询引用的表，并在引用视图的时候动态生成。
- 对视图的修改实际上会对基表修改，基表的修改也会反映在视图上。
- 视图的作用
    1. 隐藏了原表的数据的复杂性，提供了一定的逻辑独立性
    2. 可以控制用户可以访问的内容
    3. 能够简化结构，执行复杂查询操作
    4. 使用户能够以多种角度、更灵活地观察和共享同一数据
    
### SQL注入
- 用户恶意构造sql语句传给服务器，服务在使用用户的输入去数据库查询的时候触发用户精心构造的sql语句。
- 为防止sql注入攻击，需要注意：
    1. 不要信任用户的输入，通过正则匹配或限制长度的方式对用户的输入进行校验， 对单引号进行转换
    2. 永远不要使用动态拼装SQL语句，可以使用参数化的SQL或存储过程进行数据查询
    3. 不使用管理员权限的数据库连接，建议为每个应用赋予单独的权限
    4. 对机密的信息不直接存储，而是加密或hash处理
    5. 应用的异常提示应给出尽量少的信息，最好使用自定义的错误信息对原始的错误信息进行包装
    6. 借助软件和网站平台对SQL注入进行检测
    
### 乐观锁和悲观锁
#### 1. 悲观锁
- 每次去读取数据的时候，都认为别的事务会修改数据。所以，每次在读数据的时候，都会上锁，以防止其他事务读取或修改这些数据。悲观锁会导致其他修改同个数据的事务阻塞。
- 适合更新频繁的表

#### 2. 乐观锁
- 每次去读数据的时候都认为别的事务不会修改，但在更新的时候，会判断在此期间别人有没有去更新这个数据。
- 适合更新不频繁，查询比较多的场合。
- 使用版本控制的乐观锁增加Number or Timestamp or Date列，知道最后修改的时间，每次修改的前后比对值是否相同，相同说明期间没有被别人修改过，修改数据后更新字段。
- 使用校验和检查数据前后有无更新，但是资源开销大



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

