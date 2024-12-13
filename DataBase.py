import sqlite3
from PIL import Image
import io

class DBase():
    def __init__(self):
        self.con = sqlite3.connect('Dbase.db')
        self.cur = self.con.cursor()

    def createTableUsers(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Users (id_user INTEGER PRIMARY KEY autoincrement, login TEXT, email TEXT, password TEXT, access_status INTEGER)")
        self.con.commit()

    def getAllUsers(self):
        users = self.cur.execute("SELECT * FROM Users").fetchall()
        return users

    def addUser(self,login,email,password,status=1):
        trigger=True
        users=DBase().getAllUsers()
        for i in users:
            if login==i[1]:
                trigger=False
                return 0
        if trigger:
            self.cur.execute("INSERT INTO Users (login,email,password,access_status) VALUES (?,?,?,?)",(login,email,password,status))
            self.con.commit()
            return 1

    def getUserID(self, id_user):
        user = self.cur.execute("SELECT * FROM Users WHERE id_user = ?", (id_user,)).fetchone()
        return user

    def getUserByLogin(self,login):
        user = self.cur.execute("SELECT * FROM Users WHERE login = ?", (login,)).fetchone()
        return user

    def getUserByEmail(self,login):
        user = self.cur.execute("SELECT * FROM Users WHERE email = ?", (login,)).fetchone()
        return user

    def getUser(self, login,password):
        user=self.cur.execute("SELECT * FROM Users WHERE login=? and password=?", (login,password)).fetchone()
        return user


    #Группа к которой будут относиться продукты
    def createTableTypes(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Types (id_type INTEGER PRIMARY KEY autoincrement, name TEXT)")
        self.con.commit()

    def getAllTypes(self):
        types = self.cur.execute("SELECT * FROM Types").fetchall()
        return types

    def addType(self,name):
        trigger = True
        types = DBase().getAllTypes()
        for i in types:
            if name == i[1]:
                trigger = False
                return 0
        if trigger:
            self.cur.execute("INSERT INTO Types (name) VALUES (?)", (name,))
            self.con.commit()
            return 1

    def getTypeIdByName(self,name):
        type = self.cur.execute("SELECT id_type FROM Types WHERE name=?", (name,)).fetchone()
        if type==None:
            return False
        return type[0]

    def createTableCart(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Cart (id INTEGER PRIMARY KEY AUTOINCREMENT,id_user INTEGER,id_product INTEGER)""")
        self.con.commit()

    def addCartItem(self, user_id, product_id):
        self.cur.execute("INSERT INTO Cart (id_user, id_product) VALUES (?, ?)",(user_id,product_id))
        self.con.commit()

    def getCartItem(self, user_id, product_id):
        cart = self.cur.execute("SELECT * FROM Cart WHERE id_user = ? AND id_product = ?",(user_id,product_id)).fetchone()
        return cart

    def getCartItems(self, user_id):
        cart = self.cur.execute("SELECT * FROM Cart WHERE id_user = ?", (user_id,)).fetchall()
        return cart

    def deleteFromCart(self,id_user,id_tracking):
        self.cur.execute("DELETE FROM Cart WHERE id_user=? and id_product=?", (id_user,id_tracking))
        self.con.commit()

    def createTableProducts(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Products (id_product INTEGER PRIMARY KEY autoincrement, name TEXT, about TEXT, price FLOAT, picture BLOB)")
        self.con.commit()

    def addProduct(self, name, about, price, picture):
        self.cur.execute("INSERT INTO Products (name, about, price, picture) VALUES (?, ?, ?, ?)",(name, about, price, sqlite3.Binary(picture)))
        self.con.commit()


    def changeProduct(self,id_product, new_price):
        self.cur.execute("UPDATE Products SET price=? WHERE id_product=?", (new_price,id_product))
        self.con.commit()

    def getAllProducts(self):
        products = self.cur.execute("SELECT * FROM Products").fetchall()
        return products

    def getProductById(self, id):
        products = self.cur.execute("SELECT * FROM Products WHERE id_product=?",(id,)).fetchone()
        return products

    def deleteProduct(self, product_id):
        self.cur.execute("DELETE FROM Products WHERE id_product = ?", (product_id,))
        self.cur.execute("DELETE FROM Cart WHERE id_product=?", (product_id,))
        self.con.commit()

    def updateProduct(self, product_id, name, about, price):
        self.cur.execute("UPDATE Products SET name = ?, about = ?, price = ? WHERE id_product = ?", (name, about, price, product_id))
        self.con.commit()

    def createTableReviews(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Reviews (id_review INTEGER PRIMARY KEY autoincrement, id_user INTEGER, id_product INTEGER, text TEXT)")
        self.con.commit()

    def addReview(self, id_user,id_product, text):
        self.cur.execute("INSERT INTO Reviews (id_user, id_product, text) VALUES (?, ?, ?)",(id_user,id_product, text))
        self.con.commit()

    def deleteReview(self,id_review):
        self.cur.execute("DELETE FROM Reviews WHERE id_review=?",(id_review,))
        self.con.commit()

    def getAllReviews(self):
        reviews = self.cur.execute("SELECT * FROM Reviews").fetchall()
        return reviews

    def getReviewsForProduct(self, id_product):
        reviews = self.cur.execute("SELECT * FROM Reviews WHERE id_product=?", (id_product,)).fetchall()
        return reviews



'''
    def createTableCarts(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Cart (id_tracking INTEGER PRIMARY KEY autoincrement, id_user TEXT, product TEXT)")
        self.con.commit()

    def addProductToCart(self,id_user,product):
        self.cur.execute("INSERT INTO Cart (id_user, product) VALUES (?,?)", (id_user,product))
        self.con.commit()


    def deleteUsersCart(self, id_user):
        self.cur.execute("DELETE FROM Cart WHERE id_user=?", (id_user,))
        self.con.commit()'''

if __name__ == "__main__":
    DBase().createTableProducts()
    DBase().createTableUsers()
    DBase().createTableCart()
    DBase().createTableReviews()
    DBase().addUser("admin", "admin@gmail.com", "admin", 2)
    DBase().addUser("user", "user@gmail.com", "user")
    image_path = 'assets/img/test/tester.png'
    image = Image.open(image_path)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    DBase().addProduct("f", "f", 66, image_bytes)