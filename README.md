# Book-Supply-and-Marketing-System

<p>A system that manage the supply and marketing for the book store. Midterm PJ of database course.</p>

<p>基于django框架，采用MTV模式，后端数据库采用PostgreSQL，集成设计的图书供销书店系统</p>


---
## 运行方式

- clone后在pycharm中打开，在Book_Manage_System文件夹下的settings.py中根据本人数据库更改属性
  ```DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Books_Manage',
        'USER':'postgres',
        'PASSWORD': '678101',
        'HOST' : 'localhost',
        'PORT': '5432',
    }
}```
- 在终端中输入以下代码，创建超级管理员，并根据提示词输入对应的用户名与密码

```python manage.py createsuperuser```

- 运行程序，打开网页
  ```python manage.py runserver```
