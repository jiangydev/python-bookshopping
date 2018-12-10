## Python 实训项目

#### 项目名称

GUI小程序 - 网上书店

#### 数据表结构

- user:用户名(主键)，密码，是否管理员
- userInfo:用户编号(自增),用户名,密码,真实姓名，性别，邮箱，电话
- booktype：类别编号(tid)，类别名
- bookinfo:bid,bname,bprice,tid,bcount

#### 实现功能

- 首页

  - 登陆: 用户名，密码

  - 注册: 用户名, 密码, 真实姓名，性别，邮箱，电话，是否注册为管理员

    >对密码一致性，邮箱、电话格式进行校验

- 主界面

  - 菜单栏:类别  书信息  购买图书  关于我们   帮助
  - 类别: 查看、新增、修改、删除类别
  - 书信息: 查看、新增、修改、删除图书信息，导出图书信息
  - 购买图书：购物车加入、删除图书，列出购买的详细信息与总金额

  > 管理员界面没有购买图书功能；
  >
  > 用户界面没有管理图书类别、图书信息功能；

