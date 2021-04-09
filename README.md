# class-manager
本项目为Flask实现的课堂管理系统

主要开发工具为Flask + Ajax + Mysql

##主要功能
1.提供三种用户——教师、学生、管理员的登录、修改密码功能

2.提供学生用户的注册功能

3.提供教师创建课堂、查看课堂学生、随机点名、记录学生平时成绩的功能

4.提供学生搜索课堂、加入课堂、查看自己的课堂列表的功能

5.提供管理员增删改查用户信息的功能

##项目运行
修改config.py中的数据库配置

安装依赖

```bash
pip install -r requirements.txt
```

初始化和创建migration文件

```bash
python app.py db init
python app.py db migrate
```

建表

```bash
python app.py db upgrade
```

启动服务器

```bash
python app.py runserver
```