from tkinter import *
from tkinter import ttk
import sqlite3

class Product:
  """docstring for product"""
  db_name = 'database.db'
  def __init__(self, wind):
    self.wind = wind
    self.wind.title('Praful Technologies')

    frame = LabelFrame(self.wind,text = 'Add New Record')
    frame.grid (row = 0, column = 1)

    Label (frame, text = 'Name:').grid(row = 1, column = 1)
    self.name = Entry (frame)
    self.name.grid(row = 1, column = 2)

    Label(frame, text = 'Price:').grid (row = 2, column = 1)
    self.price = Entry(frame)
    self.price.grid(row = 2, column = 2)

    ttk.Button (frame, text = 'Add Record', command = self.adding).grid(row = 3, column = 2)
    self.message = Label(text = '', fg = 'red')
    self.message.grid (row = 3,column = 0)

    self.tree = ttk.Treeview (height = 10, column = 2)
    self.tree.grid(row = 4, column = 0, columnspan = 2)
    self.tree.heading('#0',text = 'Name' , anchor = W)
    self.tree.heading(2 , text = 'Price', anchor = W)

    ttk.Button(text = 'Delete Record' , command = self.deleting).grid(row = 5 , column = 0)
    ttk.Button(text = 'Edit Record' , command = self.editing).grid(row = 5 , column = 1)
    self.viewing_records()

  def run_query(self, query, parameters = ()):
    with sqlite3.connect (self.db_name) as conn:
      cursor = conn.cursor()
      query_result = cursor.execute (query, parameters)
      conn.commit()
    return query_result
  def viewing_records (self):
    records = self.tree.get_children()
    for element in records:
      self.tree.delete(element)
    query = 'SELECT * FROM product ORDER BY name DESC '
    db_rows = self.run_query(query)
    for row in db_rows:
      self.tree.insert('',0,text = row[1], values = row[2])


  def validation(self):
    return len(self.name.get()) !=0 and len(self.price.get()) !=0

  def adding (self):
    if self.validation():
        query = 'INSERT INTO product VALUES (NULL, ?, ?)'
        parameters = (self.name.get(), self.price.get())
        self.run_query(query, parameters)
        self.message['text'] = 'Record [] added'.format (self.name.get())
        self.name.delete(0, END)
        self.price.delete(0,END)
    else:
        self.message['text'] = 'name field or  price field is empty'
    self.viewing_records()
    

  def deleting (self):
    self.message['text'] = ""
    try:
        self.tree.item(self.tree.selection())['text']
    except IndexError as e:
        self.message['text'] = 'Please, select record!'
        return

    self.message['text'] = ""
    name = self.tree.item(self.tree.selection())['text']
    query = 'DELETE FROM product WHERE name = ?'
    self.run_query(query,(name, ))
    self.message['text'] = 'Record() deleted.'.format(name)
    self.viewing_records ()


  def editing(self):
    self.message['text'] = ""
    try: self.tree.item(self.tree.selection())['values'][0]
    except IndexError as e:
        self.message['text'] = 'Please, select record!'
        return

    name = self.tree.item(self.tree.selection())['text']
    old_price = self.tree.item (self.tree.selection())['values'][0]

    self.edit_wind = Toplevel()
    self.edit_wind.title('Editing')

    Label(self.edit_wind, text = 'Old name:').grid(row=0, column = 1)
    Entry (self.edit_wind, textvariable = StringVar(self.edit_wind, value = name),state = 'readonly').grid(row = 0, column = 2)
    Label(self.edit_wind, text ='New name:').grid(row=1,column=1)
    new_name = Entry(self.edit_wind)
    new_name.grid(row=1,column = 2)

    Label(self.edit_wind, text = 'Old price:').grid(row=2, column = 1)
    Entry (self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price),state = 'readonly').grid(row = 2, column = 2)
    Label(self.edit_wind, text ='New price:').grid(row=3,column=1)
    new_price = Entry(self.edit_wind)
    new_price.grid(row=3,column = 2)

    Button(self.edit_wind, text = 'Save changes', command = lambda:self.edit_records(new_name.get(), name, new_price.get(),old_price)).grid(row =4, column = 2, sticky= W)

    self.edit_wind.mainloop()


  def edit_records(self, new_name, name, new_price, old_price):
    query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
    parameters = (new_name , new_price, name, old_price)
    self.run_query (query, parameters)
    self.edit_wind.destroy()
    self.message['text'] = 'Record() changed,'.format(name)
    self.viewing_records()



if __name__ == '__main__':
  wind = Tk()
  application = Product(wind)
  wind.mainloop()

