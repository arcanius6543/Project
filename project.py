import tkinter as tk
from tkinter import ttk
import sqlite3

# класс главного окна
class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
        self.db=db
        self.view_records()
    
      # инициализация виджетов главного окна
    def init_main(self):
         toolbar=tk.Frame(bg='#d7d7d7',bd=2) # создаем панель виджетов
         toolbar.pack(side=tk.TOP,fill=tk.X)
      

           #кнопка добавления
         self.img_add=tk.PhotoImage(file='./img/add.png') # добавляем иконку
         btn_add=tk.Button(toolbar,text='Добавить',bg='#d7d7d7',
         bd=0,image=self.img_add,
         command=self.open_child)
   
         btn_add.pack(side=tk.LEFT)

          # кнопка изменения
         self.img_upd = tk.PhotoImage(file='./img/update.png')
         btn_upd = tk.Button(toolbar, text='Изменить', bg='#d7d7d7',
                            bd=0, image=self.img_upd,
                            command=self.open_update_child)
         btn_upd.pack(side=tk.LEFT)

          # кнопка удаления
         self.img_del = tk.PhotoImage(file='./img/delete.png')
         btn_del = tk.Button(toolbar, text='Удалить', bg='#d7d7d7',
                            bd=0, image=self.img_del,
                            command=self.delete_records)
         btn_del.pack(side=tk.LEFT)
        



        # кнопка поиска
         self.img_search = tk.PhotoImage(file='./img/search.png')
         btn_search = tk.Button(toolbar,text='Найти', bg='#d7d7d7',
                            bd=0, image=self.img_search,
                            command=self.open_search)
         btn_search.pack(side=tk.LEFT)



         # кнопка обновления
         self.img_refresh = tk.PhotoImage(file='./img/refresh.png')
         btn_refresh= tk.Button(toolbar,text='Найти', bg='#d7d7d7',
                            bd=0, image=self.img_refresh,
                            command=self.view_records)
         btn_refresh.pack(side=tk.LEFT)

         #таблица
         self.tree=ttk.Treeview(self,columns=('id','name','phone','email'),
        height=17,show='headings')
         self.tree.column('id',width=45,anchor=tk.CENTER)
         self.tree.column('name',width=300,anchor=tk.CENTER) 
         self.tree.column('phone',width=150,anchor=tk.CENTER)
         self.tree.column('email',width=150,anchor=tk.CENTER)

         self.tree.heading('id',text='id')
         self.tree.heading('name',text='ФИО')
         self.tree.heading('phone',text='Телефон')
         self.tree.heading('email',text='E-mail')

         self.tree.pack(side=tk.LEFT)



         #добавляем scroll bar
         scroll=tk.Scrollbar(self,command=self.tree.yview)
         scroll.pack(side=tk.LEFT,fill=tk.Y)
         self.tree.configure(yscrollcommand=scroll.set)
  # метод добавления данных  
    def records(self,name,phone,email):
        self.db.insert_data(name,phone,email)
        self.view_records()
    
    # метод изменения данных
    def update_record(self,name,phone,email):
        id=self.tree.set(self.tree.selection()[0],'#1')
        self.db.cur.execute('''
    UPDATE users 
    SET name=?, phone=?, email=?
    WHERE id=?
            ''', (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    #метод удаления 
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute('DELETE FROM users WHERE id = ?',
                                (self.tree.set(row, '#1'), ))
        self.db.conn.commit()
        self.view_records()
 
 #отображение данных в  treeview
    def view_records(self):
        self.db.cur.execute('SELECT * FROM users') # выбираем все из таблицы
        [ self.tree.delete(i) for i in self.tree.get_children()]  # удаляем из дерева элемент
        [self.tree.insert('','end',values=i) for i  in self.db.cur.fetchall()] #заполняем дерево


    # метод поиска данных
    def search_records(self, name):
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ?', 
                            ('%' + name + '%', ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # метод вызывающий дочернее окно
    def open_child(self):
        Child()

 # метод вызывающий дочернее окно для редактирования данных
    def open_update_child(self):
        Update()
    # метод вызывающий дочернее окно для поиска данных
    def open_search(self):
        Search()

# класс дочернего окна
class Child(tk.Toplevel):
     def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view=app

    # инициализация виджетов дочернего  окна
     def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200')
        self.resizable(False,False)

        # перехватываем все события
        self.grab_set()

        # перехватываем фокус
        self.focus_set()

        Label_name=tk.Label(self,text='ФИО:')
        Label_name.place(x=50,y=50)
        Label_phone=tk.Label(self,text="Телефон")
        Label_phone.place(x=50,y=80)
        Label_email=tk.Label(self,text="E-mail")
        Label_email.place(x=50,y=110)
        
        
        self.entry_name=tk.Entry(self)
        self.entry_name.place(x=200,y=50)
        self.entry_phone=tk.Entry(self)
        self.entry_phone.place(x=200,y=80)
        self.entry_email=tk.Entry(self)
        self.entry_email.place(x=200,y=110)
     

        # кнопка закрыть
        btn_cancel=tk.Button(self,text='Закрыть',command=self.destroy)
        btn_cancel.place(x=200,y=150)
       
        # кнопка добавить
        self.btn_add=tk.Button(self,text='Добавить')
        self.btn_add.bind('<Button-1>',lambda ev:self.view.records(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                            self.entry_email.get()))
        self.btn_add.place(x=265,y=150)




# класс дочернего окна для изменения данных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db=db
        self.default_data()


    def init_update(self):
        self.title('Изменение контакта')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>', 
                          lambda ev: self.view.update_record(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                            self.entry_email.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')                                                    
        self.btn_upd.place(x=265, y=150)


    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * from users WHERE id = ?', (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

# класс окна для поиска
class Search(tk.Toplevel):
      def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view=app
     
     
      def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False,False)

        # перехватываем все события
        self.grab_set()

        # перехватываем фокус
        self.focus_set()

        Label_name=tk.Label(self,text='ФИО:')
        Label_name.place(x=30,y=30)
       
        self.entry_name=tk.Entry(self)
        self.entry_name.place(x=130,y=30)
        
        # кнопка закрыть
        btn_cancel=tk.Button(self,text='Закрыть',command=self.destroy)
        btn_cancel.place(x=150,y=70)
       
        # кнопка поиска
        self.btn_add=tk.Button(self,text='Поиск')
        self.btn_add.bind('<Button-1>', lambda ev:self.view.search_records(self.entry_name.get()))
                                                           
        self.btn_add.place(x=225,y=70)

# класс БД
class Db():
    def  __init__(self):
        self.conn=sqlite3.connect('Contacts.db')
        self.cur=self.conn.cursor()
        self.cur.execute('''  CREATE TABLE IF NOT EXISTS users(
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     phone TEXT,
                     email TEXT) ''' ) # создание базы данных
        self.conn.commit()
    
    # добавление данных в дб
    def insert_data(self,name,phone,email):
        self.cur.execute('''
        INSERT INTO users(name,phone,email) 
        VALUES(?,?,?)''',(name,phone,email))  
        self.conn.commit()

        

# при запуске программы
if  __name__=='__main__':
    root=tk.Tk()  # cоздаем обьект класса  Tk
    db=Db()
    app=Main(root) # создаем экземпляр класса Main
    app.pack()
    root.title('Телефонная книга') # название
    root.geometry('665x450') # задаем размеры окна
    root.resizable(False,False) # запрет на изменение высоты и ширины
    root.mainloop() #запуск цикла событий

