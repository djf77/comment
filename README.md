# 留言板任务接口

## BaseURL

http://8.129.238.142:5000/

## 全局错误：

401：请先登录

（未登录无法进入个人页面修改信息，上传留言，修改留言，删除留言）

## 注册接口

```
POST /add
```

请求参数

```
{
	"username": "用户名",
	"password": "密码",
	"sex": "性别",
	"age": "阿拉伯数字",
	"address": "居住地"
}
```

**响应参数**

```
{
	"status": 200
	"msg": "注册成功"
}
```

**失败时：**

`HTTP/1.1 400 Bad Request`

```
1. username参数已存在
2. 缺少参数 username
3. 缺少参数 password
4. 缺少参数 sex
5. 缺少参数 age
6. 缺少参数 address
```

## 登录接口

```
POST /login
```

**请求参数**

```
{
	"username": "用户名",
	"password": "密码"
}
```

**响应参数**

```
{
	"status": 200
	"msg": "登录成功"
}
```

**失败时：**

`HTTP/1.1 400 Bad Request`

```
用户名或密码错误
```

## 个人信息页面

```
GET/me
```

**响应参数**

```
[
        "用户名",
	"性别",
	"阿拉伯数字",
	"居住地"
]
```

## 修改用户名

```
PUT/username
```

请求参数

```
{
	"username": "用户名"
}
```

响应参数

**成功时：**

```
{
	"status": 200
	"msg": "修改用户名成功"
}
```

**失败时：**

`HTTP/1.1 400 Bad Request`

```
1. 缺少参数 username
2. username参数已存在
```

## 修改密码

```
PUT/password
```

请求参数

```
{
	"password": "密码"
}
```

响应参数

**成功时：**

```
{
	"status": 200
	"msg": "修改密码成功"
}
```

**失败时：**

`HTTP/1.1 400 Bad Request`

```
缺少参数 password
```

## 修改个人信息

```
PUT/information
```

请求参数

```
{
	"sex": "性别",
	"age": "阿拉伯数字",
	"address": "居住地"
}
```

响应参数

**成功时：**

```
{
	"status": 200
	"msg": "修改个人信息成功"
}
```

**失败时：**

`HTTP/1.1 400 Bad Request`

```
1. 缺少参数 sex
2. 缺少参数 age
3. 缺少参数 address
```

 

## 留言部分：

## 查看留言

```
GET/
```

**响应参数**（想这样）

```
[
    [
        "id1",
        "上传者1",
        "留言1",
        "上传时间",
        "上次修改时间"
    ],
    [
        "id2",
        "上传者2",
        "留言2",
        "上传时间",
        "上次修改时间"
    ],
    [
        "id3",
        "上传者3",
        "留言3",
        "上传时间",
        "上次修改时间"
    ]
]
```

## 上传留言

```
POST /add_comment
```

**未登录时：401**

请求参数

```
{
	"comment": "留言"
}
```

**响应参数**

```
{
	"status": 200
	"msg": "上传成功"
}
```

**失败时：**

`HTTP/1.1 400 Bad Request`

```
1. 缺少参数 comment
```

## 修改留言
```
PUT /update_comment
```

**未登录时：401**

请求参数

```
{
        "id": "数字",
	"comment": "留言"
}
```

**响应参数**

```
{
	"status": 200
	"msg": "修改成功"
}
```
**失败时：**

`HTTP/1.1 400 Bad Request`

```
1. 缺少参数 id
2. 缺少参数 comment
```
## 删除留言

```
DELETE /delete_comment
```

**未登录时：401**

**响应参数**

```
{
	"status": 200
	"msg": "删除成功"
}
```
**失败时：**

`HTTP/1.1 400 Bad Request`

```
缺少参数 id
```
