#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import openpyxl
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import re
import DbUtil


def init():
    # 窗口
    window = tk.Tk()
    window.title('图书管理系统')
    window.geometry('450x300')
    # 画布放置图片
    canvas = tk.Canvas(window, height=300, width=500)
    imagefile = tk.PhotoImage(file='background.png')
    image = canvas.create_image(0, 0, anchor='nw', image=imagefile)
    canvas.pack(side='top')
    # 标签 用户名密码
    tk.Label(window, text='用户名').place(x=120, y=115)
    tk.Label(window, text='密  码').place(x=120, y=155)
    # 用户名输入框
    var_usr_name = tk.StringVar()
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=180, y=115)
    # 密码输入框
    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=180, y=155)

    # 登录 注册按钮
    bt_login = tk.Button(window, text='登录', command=lambda: usr_log_in(window, var_usr_name, var_usr_pwd))
    bt_login.place(x=140, y=230)
    bt_logup = tk.Button(window, text='注册', command=lambda: usr_sign_up(window))
    bt_logup.place(x=210, y=230)
    bt_logquit = tk.Button(window, text='退出', command=lambda: usr_quit(window))
    bt_logquit.place(x=280, y=230)
    window.mainloop()


def manager_main(window, usr_name, is_manager):
    usr_quit(window)
    manager = tk.Tk()
    manager.title("书籍管理")
    # 创建菜单对象，锁定到窗口（固定菜单）
    menubar = tk.Menu(manager)
    # 为固定菜单添加【类别  书信息  购买图书  关于我们   帮助】五个主菜单
    menuType = tk.Menu(menubar, tearoff=0)  # tearoff=0：菜单不能从窗口移走
    menuBook = tk.Menu(menubar, tearoff=0)
    menuShopping = tk.Menu(menubar, tearoff=0)
    menuAbout = tk.Menu(menubar, tearoff=0)
    menuHelp = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="类别", menu=menuType)  # 含有下拉子菜单
    menubar.add_cascade(label="书信息", menu=menuBook)
    menubar.add_cascade(label="购买图书", menu=menuShopping)
    menubar.add_cascade(label="关于我们", menu=menuAbout)
    menubar.add_cascade(label="帮助", menu=menuHelp)
    frame_root = tk.Frame(manager, width=500, height=300)
    frame_root.pack()
    frame_type = tk.Frame(frame_root, width=500, height=300)
    frame_book = tk.Frame(frame_root, width=500, height=300)
    frame_shopping = tk.Frame(frame_root, width=500, height=300)
    # 【关于我们】页面
    frame_about = tk.Frame(frame_root, width=500, height=300)
    tk.Label(frame_about, text="作者：jiangydev(王江雨)\n学号：202150827", width=40, height=10).pack()

    # 为【类别】添加下拉式子菜单
    menuType.add_command(label="查看类别",
                         command=lambda: on_type_r_selected(frame_root, frame_type, frame_book, frame_shopping,
                                                            frame_about))
    menuType.add_command(label="增加类别", command=lambda: on_type_c_selected(manager, frame_type))
    menuType.add_command(label="删除类别", command=lambda: on_type_d_selected(manager, frame_type))
    menuType.add_command(label="修改类别", command=lambda: on_type_u_selected(manager, frame_type))

    # 为【书信息】添加下拉式子菜单
    menuBook.add_command(label="查看书信息",
                         command=lambda: on_book_r_selected(frame_root, frame_type, frame_book, frame_shopping,
                                                            frame_about))
    menuBook.add_command(label="增加书信息", command=lambda: on_book_c_selected(manager, frame_book))
    menuBook.add_command(label="删除书信息", command=lambda: on_book_d_selected(manager, frame_book))
    menuBook.add_command(label="修改书信息", command=lambda: on_book_u_selected(manager, frame_book))
    menuBook.add_command(label="导出书信息", command=lambda: on_book_e_selected(manager))

    # 为【购买图书】添加下拉式子菜单
    menuShopping.add_command(label="查看购物车",
                             command=lambda: on_shopping_r_selected(usr_name, frame_root, frame_type, frame_book,
                                                                    frame_shopping,
                                                                    frame_about))
    menuShopping.add_command(label="查看图书列表",
                             command=lambda: on_shopping_c_selected(usr_name, frame_root, frame_type, frame_book,
                                                                    frame_shopping,
                                                                    frame_about))
    menuShopping.add_command(label="导出购物信息", command=lambda: on_shopping_e_selected(manager))

    # 为【关于我们】添加下拉式子菜单
    menuAbout.add_command(label="作者信息",
                          command=lambda: on_about_selected(frame_root, frame_type, frame_book, frame_shopping,
                                                            frame_about))

    # 为【帮助】添加下拉式子菜单
    menuHelp.add_command(label="暂无帮助文档")

    # 如果不是管理员隐藏【类别 书信息】
    if not is_manager:
        menubar.delete(0, 2)
    # 如果是管理员隐藏【购买图书】
    else:
        menubar.delete(3)

    manager.config(menu=menubar)

    # 消息循环
    manager.mainloop()
    pass


# Treeview、列名、排列方式
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    print(tv.get_children(''))
    l.sort(reverse=reverse)  # 排序方式
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):  # 根据排序后索引移动
        tv.move(k, '', index)
        # print(k)
    # 重写标题，使之成为再点倒序的标题
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def build_type(frame_type):
    for widget in frame_type.winfo_children():
        widget.destroy()
    columns = ("类别编号", "类别名")
    treeview = ttk.Treeview(frame_type, columns=columns, show='headings')
    treeview.column("类别编号", width=100, anchor='center')  # 表示列,不显示
    treeview.column("类别名", width=250, anchor='center')
    treeview.heading('类别编号', text='类别编号')
    treeview.heading('类别名', text='类别名')
    treeview.grid()

    query = ("SELECT tid, tname FROM `booktype`")
    cnx = DbUtil.open_db()
    cursor = cnx.cursor()
    cursor.execute(query)
    i = 1
    for (tid, tname) in cursor:
        treeview.insert('', i, values=(tid, tname))
        i = i + 1

    DbUtil.close_db(cursor, cnx)

    for col in columns:  # 给所有标题加（循环上边的“手工”）
        treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))


# 查看类别
def on_type_r_selected(frame_root, frame_type, frame_book, frame_shopping, frame_about):
    build_type(frame_type)
    frame_type.pack()
    frame_book.forget()
    frame_shopping.forget()
    frame_about.forget()


# 新增类别
def on_type_c_selected(manager, frame_type):
    def inserttodb():
        # 获取输入框内的内容
        tid = t_id.get().strip()
        tname = t_name.get().strip()
        if tid == '' or tname == '':
            tk.messagebox.showerror(message='类别编号或名称为空')
        else:
            query = ("INSERT INTO `booktype`(tid, tname) VALUES ('%s', '%s')" % (tid, tname))
            try:
                cnx = DbUtil.open_db()
                cursor = cnx.cursor()
                cursor.execute(query)
                cnx.commit()
                DbUtil.close_db(cursor, cnx)
                tk.messagebox.showinfo('成功', '新增类别成功')
                type_c.destroy()
                build_type(frame_type)
            except:
                tk.messagebox.showerror('错误', '新增类别失败')

    type_c = tk.Toplevel(manager)
    type_c.title('新增类别')
    type_c.geometry('350x150')
    # 类别编号变量及标签、输入框
    t_id = tk.StringVar()
    tk.Label(type_c, text='请输入类别编号：').place(x=10, y=10)
    tk.Entry(type_c, textvariable=t_id).place(x=150, y=10)
    # 类别名变量及标签、输入框
    t_name = tk.StringVar()
    tk.Label(type_c, text='请输入类别名：').place(x=10, y=50)
    tk.Entry(type_c, textvariable=t_name).place(x=150, y=50)
    # 确认注册按钮及位置
    bt_confirm_c = tk.Button(type_c, text='新增', command=inserttodb)
    bt_confirm_c.place(x=150, y=90)


# 删除类别信息
def on_type_d_selected(manager, frame_type):
    def delete_type_by_id():
        # 获取输入框内的内容
        tid = t_id.get().strip()
        if tid == '':
            tk.messagebox.showerror(message='类别编号为空')
        else:
            query = ("SELECT COUNT(*) FROM `booktype` WHERE tid='%s'" % (tid))
            cnx = DbUtil.open_db()
            cursor = cnx.cursor()
            cursor.execute(query)
            if cursor.fetchone()[0] == 1:
                query = ("DELETE FROM `booktype` WHERE tid='%s'" % (tid))
                try:
                    cursor.execute(query)
                    cnx.commit()
                    DbUtil.close_db(cursor, cnx)
                    tk.messagebox.showinfo('成功', '删除类别成功')
                    type_d.destroy()
                    build_type(frame_type)
                except:
                    tk.messagebox.showerror('错误', '删除类别失败')
            else:
                tk.messagebox.showerror('错误', '删除类别失败, 该类别编号不存在')

    type_d = tk.Toplevel(manager)
    type_d.title('删除类别信息')
    type_d.geometry('350x150')
    # 类别编号变量及标签、输入框
    t_id = tk.StringVar()
    tk.Label(type_d, text='请输入类别编号：').place(x=10, y=50)
    tk.Entry(type_d, textvariable=t_id).place(x=150, y=50)
    # 确认删除按钮及位置
    bt_confirm_d = tk.Button(type_d, text='确认删除', command=delete_type_by_id)
    bt_confirm_d.place(x=150, y=90)


# 修改类别
def on_type_u_selected(manager, frame_type):
    def inserttodb():
        # 获取输入框内的内容
        tid = t_id.get().strip()
        tidn = t_id_n.get().strip()
        tnamen = t_name_n.get().strip()
        if tid == '' or tidn == '' or tnamen == '':
            tk.messagebox.showerror(message='类别编号或名称为空')
        else:
            query = ("SELECT COUNT(*) FROM `booktype` WHERE tid='%s'" % (tid))
            cnx = DbUtil.open_db()
            cursor = cnx.cursor()
            cursor.execute(query)
            if cursor.fetchone()[0] == 1:
                query = ("UPDATE `booktype` SET tid='%s', tname='%s' WHERE tid='%s'" % (tidn, tnamen, tid))
                try:
                    cursor.execute(query)
                    cnx.commit()
                    DbUtil.close_db(cursor, cnx)
                    tk.messagebox.showinfo('成功', '修改类别成功')
                    type_u.destroy()
                    build_type(frame_type)
                except:
                    tk.messagebox.showerror('错误', '修改类别失败')
            else:
                tk.messagebox.showerror('错误', '修改类别失败, 该类别编号不存在')

    type_u = tk.Toplevel(manager)
    type_u.title('修改类别')
    type_u.geometry('380x200')
    # 类别编号变量及标签、输入框
    t_id = tk.StringVar()
    tk.Label(type_u, text='请输入需要修改的类别编号：').place(x=10, y=10)
    tk.Entry(type_u, textvariable=t_id).place(x=180, y=10)
    # 类别编号变量及标签、输入框
    t_id_n = tk.StringVar()
    tk.Label(type_u, text='请输入新的类别编号：').place(x=10, y=50)
    tk.Entry(type_u, textvariable=t_id_n).place(x=180, y=50)
    # 类别名变量及标签、输入框
    t_name_n = tk.StringVar()
    tk.Label(type_u, text='请输入新的类别名：').place(x=10, y=90)
    tk.Entry(type_u, textvariable=t_name_n).place(x=180, y=90)
    # 确认注册按钮及位置
    bt_confirm_c = tk.Button(type_u, text='修改', command=inserttodb)
    bt_confirm_c.place(x=180, y=130)


def build_shopping(frame_shopping, username, option):
    def on_treeview_click(event):
        cnx = DbUtil.open_db()
        cursor = cnx.cursor()
        for item in treeview.selection():
            item_text = treeview.item(item, "values")
            bid = item_text[0]
            query = ("SELECT bcount FROM `bookinfo` WHERE `bookinfo`.bid = '%s'" % (bid))
            cursor.execute(query)
            book_balance = cursor.fetchone()[0]
            query = ("SELECT scount FROM `shoplist` WHERE bid = '%s' AND username = '%s'" % (bid, username))
            cursor.execute(query)
            result = cursor.fetchone()
            shop_balance = 0 if result is None else result[0]
            if item_text[5] == '双击从购物车删除':
                if shop_balance > 1:
                    query_update_shop = (
                        "UPDATE `shoplist` SET scount = '%s' WHERE username = '%s' AND bid = '%s'" % (
                            shop_balance - 1, username, bid))
                    query_update = ("UPDATE `bookinfo` SET bcount = '%s' WHERE bid = '%s'" % (book_balance + 1, bid))
                    try:
                        cursor.execute(query_update_shop)
                        cursor.execute(query_update)
                        cnx.commit()
                        tk.messagebox.showinfo(message='从购物车删除成功！')
                    except:
                        cnx.rollback()
                        tk.messagebox.showerror(message='从购物车删除失败！')
                elif shop_balance == 1:
                    query_delete = (
                        "DELETE FROM `shoplist` WHERE username = '%s' AND bid = '%s'" % (username, bid))
                    query_update = ("UPDATE `bookinfo` SET bcount = '%s' WHERE bid = '%s'" % (book_balance + 1, bid))
                    try:
                        cursor.execute(query_delete)
                        cursor.execute(query_update)
                        cnx.commit()
                        tk.messagebox.showinfo(message='从购物车删除成功！')
                    except:
                        cnx.rollback()
                        tk.messagebox.showerror(message='从购物车删除失败！')
                else:
                    tk.messagebox.showerror(message='无法从购物车删除，数量异常！')
            elif item_text[5] == '双击加入购物车':
                if shop_balance > 0:
                    query_update_shop = (
                        "UPDATE `shoplist` SET scount = '%s' WHERE username = '%s' AND bid = '%s'" % (
                            shop_balance + 1, username, bid))
                    query_update = ("UPDATE `bookinfo` SET bcount = '%s' WHERE bid = '%s'" % (book_balance - 1, bid))
                    try:
                        cursor.execute(query_update_shop)
                        cursor.execute(query_update)
                        cnx.commit()
                        tk.messagebox.showinfo(message='加入购物车成功！')
                    except:
                        tk.messagebox.showerror(message='加入购物车失败！')
                elif shop_balance == 0:
                    query_insert = (
                        "INSERT INTO `shoplist`(username, bid, scount) VALUES ('%s', '%s', '%s')" % (username, bid, 1))
                    query_update = ("UPDATE `bookinfo` SET bcount = '%s' WHERE bid = '%s'" % (book_balance - 1, bid))
                    try:
                        cursor.execute(query_insert)
                        cursor.execute(query_update)
                        cnx.commit()
                        tk.messagebox.showinfo(message='加入购物车成功！')
                    except:
                        tk.messagebox.showerror(message='加入购物车失败！')
                else:
                    tk.messagebox.showerror(message='无库存，无法加入购物车！')
            elif item_text[5] == '去付款':
                tk.messagebox.showerror(message='支付功能开发中......')
            else:
                tk.messagebox.showerror(message='非法操作！')
        DbUtil.close_db(cursor, cnx)
        build_shopping(frame_shopping, username, option)

    # 如果是查看购物车，显示删除、+1、-1，到0就是删除
    if option == 'shop':
        query = (
            "SELECT i.bid bid, i.bname bname, i.bprice bprice, b.tname tname, i.bcount bcount, l.scount scount FROM `booktype` b, `bookinfo` i, `shoplist` l WHERE b.tid = i.tid AND i.bid = l.bid AND l.username = '%s'" % (
                username))
        null_remind = '温馨提示：购物车暂无物品'
        book_opt = '双击从购物车删除'
        table_4 = '已购数量'
    # 如果是购物列表，显示添加到购物车，若以已经在购物车，不在购物列表显示
    elif option == 'book':
        query = (
            "SELECT i.bid bid, i.bname bname, i.bprice bprice, b.tname tname, i.bcount bcount FROM `booktype` b, `bookinfo` i WHERE b.tid = i.tid AND i.bid not in (SELECT DISTINCT bid FROM shoplist l WHERE l.username != '%s')" % (
                username))
        null_remind = '温馨提示：系统中暂无可购物品'
        book_opt = '双击加入购物车'
        table_4 = '库存'
    else:
        tk.messagebox.showerror(message='非法选择！')
        return False

    for widget in frame_shopping.winfo_children():
        widget.destroy()
    columns = ("书编号", "书名", "书价", "类别", table_4, "操作")
    treeview = ttk.Treeview(frame_shopping, columns=columns, show='headings')
    treeview.column("书编号", width=100, anchor='center')  # 表示列,不显示
    treeview.column("书名", width=150, anchor='center')
    treeview.column("书价", width=90, anchor='center')
    treeview.column("类别", width=100, anchor='center')
    treeview.column(table_4, width=90, anchor='center')
    treeview.column("操作", width=200, anchor='center')
    treeview.heading('书编号', text='书编号')
    treeview.heading('书名', text='书名')
    treeview.heading('书价', text='书价')
    treeview.heading('类别', text='类别')
    treeview.heading(table_4, text=table_4)
    treeview.heading('操作', text='操作')

    cnx = DbUtil.open_db()
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    # 如果查询到数据则显示，无数据则显示“购物车无商品”
    if cursor.rowcount == 0:
        for widget in frame_shopping.winfo_children():
            widget.destroy()
        tk.Label(frame_shopping, text=null_remind, width=80, height=5).pack()
    else:
        i = 0
        for k in result:
            treeview.insert('', i, values=(k[0], k[1], k[2], k[3], k[4] if option == 'book' else k[5], book_opt))
            i = i + 1
        if option == 'shop':
            query = (
                "SELECT SUM(bprice*scount) total FROM `bookinfo` i, `shoplist` l WHERE i.bid = l.bid AND l.username = '%s'" % (
                    username))
            cursor.execute(query)
            result = cursor.fetchone()
            treeview.insert('', i, values=('金额合计：', 'RMB ￥', 0 if result is None else result[0], '', '', '去付款'))
        treeview.grid()
        for col in columns:  # 给所有标题加（循环上边的“手工”）
            treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
        treeview.bind("<Double-1>", on_treeview_click)
    DbUtil.close_db(cursor, cnx)


# 购物车信息
def on_shopping_r_selected(usr_name, frame_root, frame_type, frame_book, frame_shopping, frame_about):
    build_shopping(frame_shopping, usr_name, 'shop')
    frame_type.forget()
    frame_book.forget()
    frame_shopping.pack()
    frame_about.forget()


# 购买图书
def on_shopping_c_selected(usr_name, frame_root, frame_type, frame_book, frame_shopping, frame_about):
    build_shopping(frame_shopping, usr_name, 'book')
    frame_type.forget()
    frame_book.forget()
    frame_shopping.pack()
    frame_about.forget()


# 导出购物车信息
def on_shopping_e_selected(manager):
    pass


def build_book(frame_book):
    for widget in frame_book.winfo_children():
        widget.destroy()
    columns = ("书编号", "书名", "书价", "类别", "库存")
    treeview = ttk.Treeview(frame_book, columns=columns, show='headings')
    treeview.column("书编号", width=100, anchor='center')  # 表示列,不显示
    treeview.column("书名", width=100, anchor='center')
    treeview.column("书价", width=100, anchor='center')
    treeview.column("类别", width=100, anchor='center')
    treeview.column("库存", width=100, anchor='center')
    treeview.heading('书编号', text='书编号')
    treeview.heading('书名', text='书名')
    treeview.heading('书价', text='书价')
    treeview.heading('类别', text='类别')
    treeview.heading('库存', text='库存')
    treeview.grid()

    query = (
        "SELECT bid, bname, bprice, tname, bcount FROM `booktype`, `bookinfo` WHERE `booktype`.tid=`bookinfo`.tid")
    cnx = DbUtil.open_db()
    cursor = cnx.cursor()
    cursor.execute(query)
    i = 1
    for (bid, bname, bprice, tname, bcount) in cursor:
        treeview.insert('', i, values=(bid, bname, bprice, tname, bcount))
        i = i + 1
    DbUtil.close_db(cursor, cnx)

    for col in columns:  # 给所有标题加（循环上边的“手工”）
        treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))


# 查看书信息
def on_book_r_selected(frame_root, frame_type, frame_book, frame_shopping, frame_about):
    build_book(frame_book)
    frame_type.forget()
    frame_book.pack()
    frame_shopping.forget()
    frame_about.forget()


# 新增书信息
def on_book_c_selected(manager, frame_book):
    def inserttodb():
        # 获取输入框内的内容
        bid = b_id.get().strip()
        bname = b_name.get().strip()
        bprice = b_price.get().strip()
        tid = t_id.get().strip()
        bcount = b_count.get().strip()
        if bid == '' or bname == '' or bprice == '' or tid == '' or bcount == '':
            tk.messagebox.showerror(message='输入框不能为空')
        else:
            query = ("INSERT INTO `bookinfo`(bid, bname, bprice, tid, bcount) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                bid, bname, bprice, tid, bcount))
            try:
                cnx = DbUtil.open_db()
                cursor = cnx.cursor()
                cursor.execute(query)
                cnx.commit()
                DbUtil.close_db(cursor, cnx)
                tk.messagebox.showinfo('成功', '新增图书信息成功')
                book_c.destroy()
                build_book(frame_book)
            except:
                tk.messagebox.showerror('错误', '新增图书信息失败')

    book_c = tk.Toplevel(manager)
    book_c.title('新增书信息')
    book_c.geometry('350x280')
    # 书编号变量及标签、输入框
    b_id = tk.StringVar()
    tk.Label(book_c, text='请输入书编号：').place(x=10, y=10)
    tk.Entry(book_c, textvariable=b_id).place(x=150, y=10)
    # 书名变量及标签、输入框
    b_name = tk.StringVar()
    tk.Label(book_c, text='请输入书名：').place(x=10, y=50)
    tk.Entry(book_c, textvariable=b_name).place(x=150, y=50)
    # 书价变量及标签、输入框
    b_price = tk.StringVar()
    tk.Label(book_c, text='请输入书价：').place(x=10, y=90)
    tk.Entry(book_c, textvariable=b_price).place(x=150, y=90)
    # 类别编号变量及标签、输入框
    t_id = tk.StringVar()
    tk.Label(book_c, text='请输入书类别编号：').place(x=10, y=130)
    tk.Entry(book_c, textvariable=t_id).place(x=150, y=130)
    # 类别名变量及标签、输入框
    b_count = tk.StringVar()
    tk.Label(book_c, text='请输入书数量：').place(x=10, y=170)
    tk.Entry(book_c, textvariable=b_count).place(x=150, y=170)
    # 确认注册按钮及位置
    bt_confirm_c = tk.Button(book_c, text='新增', command=inserttodb)
    bt_confirm_c.place(x=150, y=210)


# 删除类图书信息
def on_book_d_selected(manager, frame_book):
    def delete_book_by_id():
        # 获取输入框内的内容
        bid = b_id.get().strip()
        if bid == '':
            tk.messagebox.showerror(message='图书编号为空')
        else:
            query = ("SELECT COUNT(*) FROM `bookinfo` WHERE bid='%s'" % (bid))
            cnx = DbUtil.open_db()
            cursor = cnx.cursor()
            cursor.execute(query)
            if cursor.fetchone()[0] == 1:
                query = ("DELETE FROM `bookinfo` WHERE bid='%s'" % (bid))
                try:
                    cursor.execute(query)
                    cnx.commit()
                    DbUtil.close_db(cursor, cnx)
                    tk.messagebox.showinfo('成功', '删除图书成功')
                    book_d.destroy()
                    build_book(frame_book)
                except:
                    tk.messagebox.showerror('错误', '删除图书失败')
            else:
                tk.messagebox.showerror('错误', '删除图书失败, 该图书编号不存在')

    book_d = tk.Toplevel(manager)
    book_d.title('删除图书信息')
    book_d.geometry('350x150')
    # 类别编号变量及标签、输入框
    b_id = tk.StringVar()
    tk.Label(book_d, text='请输入图书编号：').place(x=10, y=50)
    tk.Entry(book_d, textvariable=b_id).place(x=150, y=50)
    # 确认删除按钮及位置
    bt_confirm_d = tk.Button(book_d, text='确认删除', command=delete_book_by_id)
    bt_confirm_d.place(x=150, y=90)


# 修改图书
def on_book_u_selected(manager, frame_book):
    def inserttodb():
        # 获取输入框内的内容
        bido = b_id_o.get().strip()
        bid = b_id.get().strip()
        bname = b_name.get().strip()
        bprice = b_price.get().strip()
        tid = t_id.get().strip()
        bcount = b_count.get().strip()
        if bido == '' or bid == '' or bname == '' or bprice == '' or tid == '' or bcount == '':
            tk.messagebox.showerror(message='输入框不能为空')
        else:
            query = ("SELECT COUNT(*) FROM `bookinfo` WHERE bid='%s'" % (bido))
            cnx = DbUtil.open_db()
            cursor = cnx.cursor()
            cursor.execute(query)
            if cursor.fetchone()[0] == 1:
                query = (
                    "UPDATE `bookinfo` SET bid='%s', bname='%s', bprice='%s', tid='%s', bcount='%s' WHERE tid='%s'" % (
                        bid, bname, bprice, tid, bcount, bido))
                try:
                    cursor.execute(query)
                    cnx.commit()
                    DbUtil.close_db(cursor, cnx)
                    tk.messagebox.showinfo('成功', '修改图书信息成功')
                    book_u.destroy()
                    build_book(frame_book)
                except:
                    tk.messagebox.showerror('错误', '修改图书信息失败')
            else:
                tk.messagebox.showerror('错误', '修改图书信息失败, 该图书编号不存在')

    book_u = tk.Toplevel(manager)
    book_u.title('修改图书信息')
    book_u.geometry('380x320')
    # 类别编号变量及标签、输入框
    b_id_o = tk.StringVar()
    tk.Label(book_u, text='请输入需要修改的图书编号：').place(x=10, y=10)
    tk.Entry(book_u, textvariable=b_id_o).place(x=180, y=10)
    # 书编号变量及标签、输入框
    b_id = tk.StringVar()
    tk.Label(book_u, text='请输入新的书编号：').place(x=10, y=50)
    tk.Entry(book_u, textvariable=b_id).place(x=180, y=50)
    # 书名变量及标签、输入框
    b_name = tk.StringVar()
    tk.Label(book_u, text='请输入新的书名：').place(x=10, y=90)
    tk.Entry(book_u, textvariable=b_name).place(x=180, y=90)
    # 书价变量及标签、输入框
    b_price = tk.StringVar()
    tk.Label(book_u, text='请输入新的书价：').place(x=10, y=130)
    tk.Entry(book_u, textvariable=b_price).place(x=180, y=130)
    # 类别编号变量及标签、输入框
    t_id = tk.StringVar()
    tk.Label(book_u, text='请输入新的书类别编号：').place(x=10, y=170)
    tk.Entry(book_u, textvariable=t_id).place(x=180, y=170)
    # 类别名变量及标签、输入框
    b_count = tk.StringVar()
    tk.Label(book_u, text='请输入新的书数量：').place(x=10, y=210)
    tk.Entry(book_u, textvariable=b_count).place(x=180, y=210)
    # 确认注册按钮及位置
    bt_confirm_c = tk.Button(book_u, text='修改', command=inserttodb)
    bt_confirm_c.place(x=150, y=250)


# 导出书信息
def on_book_e_selected(manager):
    def export():
        file_name = f_name.get().strip()
        if file_name == '':
            tk.messagebox.showerror(message='文件名不能为空')
        else:
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet['A1'] = '图书编号'
            sheet['B1'] = '图书名称'
            sheet['C1'] = '图书价格'
            sheet['D1'] = '图书类别'
            sheet['E1'] = '图书库存'
            query = (
                "SELECT bid, bname, bprice, tname, bcount FROM `booktype`, `bookinfo` WHERE `booktype`.tid=`bookinfo`.tid")
            cnx = DbUtil.open_db()
            cursor = cnx.cursor()
            cursor.execute(query)
            i = 2
            for (bid, bname, bprice, tname, bcount) in cursor:
                sheet['A%s' % i] = bid
                sheet['B%s' % i] = bname
                sheet['C%s' % i] = bprice
                sheet['D%s' % i] = tname
                sheet['E%s' % i] = bcount
                i = i + 1
            DbUtil.close_db(cursor, cnx)
            time_file = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
            file_name = file_name + '-' + time_file + '.xlsx'
            wb.save(file_name)
            tk.messagebox.showinfo('成功', '导出图书信息成功')
            book_e.destroy()

    book_e = tk.Toplevel(manager)
    book_e.title('导出图书信息')
    book_e.geometry('350x150')
    # 类别编号变量及标签、输入框
    f_name = tk.StringVar()
    tk.Label(book_e, text='请输入文件名(不需要后缀)：').place(x=10, y=50)
    tk.Entry(book_e, textvariable=f_name).place(x=180, y=50)
    # 确认导出按钮及位置
    bt_confirm_d = tk.Button(book_e, text='确认导出', command=export)
    bt_confirm_d.place(x=180, y=90)


# 关于我们
def on_about_selected(frame_root, frame_type, frame_book, frame_shopping, frame_about):
    frame_type.forget()
    frame_book.forget()
    frame_shopping.forget()
    frame_about.pack()


# 登录函数
def usr_log_in(window, var_usr_name, var_usr_pwd):
    # 输入框获取用户名密码
    usr_name = var_usr_name.get().strip()
    usr_pwd = var_usr_pwd.get().strip()
    # 用户名密码不能为空
    if usr_name == '' or usr_pwd == '':
        tk.messagebox.showerror(message='用户名或密码不能为空！')
    else:
        # 从数据库中获取用户信息
        query = ("SELECT COUNT(*) FROM `user` WHERE username = '%s'" % usr_name)
        cnx = DbUtil.open_db()
        cursor = cnx.cursor()
        cursor.execute(query)
        if cursor.fetchone()[0] == 1:
            # 判断用户名和密码是否匹配
            query = ("SELECT username, password, is_manager FROM `user` WHERE username = '%s' AND password = '%s'" % (
                usr_name, usr_pwd))
            cursor.execute(query)
            result = cursor.fetchone()
            DbUtil.close_db(cursor, cnx)
            if result is not None:
                # tk.messagebox.showinfo(title='welcome', message='欢迎您：' + usr_name)
                # 进入主界面
                is_manger = False if (result[2] == 0) else True
                manager_main(window, usr_name, is_manger)
            else:
                tk.messagebox.showerror(message='密码错误')
        # 不在数据库中弹出是否注册的框
        else:
            is_signup = tk.messagebox.askyesno('欢迎', '您还没有注册，是否现在注册')
            if is_signup:
                usr_sign_up()


# 注册函数
def usr_sign_up(window):
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        nun = new_username.get().strip()
        np = new_pwd.get().strip()
        npf = new_pwd_confirm.get().strip()
        nn = new_name.get().strip()
        ng = new_gender.get().strip()
        ne = new_email.get().strip()
        nt = new_telephone.get().strip()
        nm = new_manager.get().strip()

        if np == '' or nun == '' or npf == '' or nn == '' or ng == '' or ne == '' or nt == '' or nm == '':
            tk.messagebox.showerror('错误', '输入框不能为空！')
        elif np != npf:
            tk.messagebox.showerror('错误', '密码前后不一致')
        elif re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', ne) is None:
            tk.messagebox.showerror('错误', '邮箱格式不正确')
        elif re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', nt) is None:
            tk.messagebox.showerror('错误', '手机号格式不正确')
        else:
            query = ("SELECT COUNT(*) FROM `user` WHERE username = '%s'" % (nun))
            cnx = DbUtil.open_db()
            cursor = cnx.cursor()
            cursor.execute(query)
            if cursor.fetchone()[0] != 0:
                tk.messagebox.showerror('错误', '用户名已存在')
            else:
                query = ("INSERT INTO `user`(username, password, is_manager) VALUES ('%s', '%s', '%s')" % (nun, np, nm))
                query1 = (
                    "INSERT INTO `userinfo`(username, password, `name`, gender, email, telephone) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                        nun, np, nn, ng, ne, nt))
                try:
                    cursor.execute(query)
                    cursor.execute(query1)
                    cnx.commit()
                    DbUtil.close_db(cursor, cnx)
                    tk.messagebox.showinfo('欢迎', '注册成功')
                    # 注册成功关闭注册框
                    window_sign_up.destroy()
                except:
                    print()
                    tk.messagebox.showinfo('错误', '注册失败')
                    cnx.rollback()

    # 新建注册界面
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x400')
    window_sign_up.title('注册')
    # 用户名变量及标签、输入框
    new_username = tk.StringVar()
    tk.Label(window_sign_up, text='请输入用户名：').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=new_username).place(x=150, y=10)
    # 密码变量及标签、输入框
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='请输入密码：').place(x=10, y=50)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='请再次输入密码：').place(x=10, y=90)
    tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)
    # 真实姓名变量及标签、输入框
    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='请输入真实姓名：').place(x=10, y=130)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=130)
    # 性别变量及标签、输入框
    new_gender = tk.StringVar()
    new_gender.set('男')
    tk.Label(window_sign_up, text='请输入性别：').place(x=10, y=170)
    tk.Radiobutton(window_sign_up, text='男', variable=new_gender, value='男').place(x=150, y=170)
    tk.Radiobutton(window_sign_up, text='女', variable=new_gender, value='女').place(x=220, y=170)
    # 邮箱变量及标签、输入框
    new_email = tk.StringVar()
    tk.Label(window_sign_up, text='请输入邮箱：').place(x=10, y=210)
    tk.Entry(window_sign_up, textvariable=new_email).place(x=150, y=210)
    # 电话变量及标签、输入框
    new_telephone = tk.StringVar()
    tk.Label(window_sign_up, text='请输入电话：').place(x=10, y=250)
    tk.Entry(window_sign_up, textvariable=new_telephone).place(x=150, y=250)
    # 是否为管理员变量及标签、输入框
    new_manager = tk.StringVar()
    new_manager.set(0)
    tk.Label(window_sign_up, text='是否注册为管理员：').place(x=10, y=290)
    tk.Radiobutton(window_sign_up, text='否', variable=new_manager, value=0).place(x=150, y=290)
    tk.Radiobutton(window_sign_up, text='是', variable=new_manager, value=1).place(x=220, y=290)
    # 确认注册按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='确认注册', command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=340)


# 退出的函数
def usr_quit(window):
    window.destroy()


if __name__ == "__main__":
    init()
