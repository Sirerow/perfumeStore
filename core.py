from flask import session, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from DataBase import DBase
from UserLogin import UserLogin
import base64

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@core_bp.route('/index.html', methods=["GET", "POST"])
def index():
    # Получаем все товары
    products = DBase().getAllProducts()
    products = [list(product) for product in products]
    products.reverse()
    lenProducts = len(products)

    # Преобразуем картинки в base64
    for product in products:
        if product[4]:
            product[4] = base64.b64encode(product[4]).decode('utf-8')

    # Получаем товары из корзины для текущего пользователя (предполагается, что user_id уже есть)
    try:
        user=UserLogin.get_user(current_user)
        if user != None:
            cart_items = DBase().getCartItems(user[0])
        else:
            cart_items = None

        # Создаем список товаров в корзине и подсчитываем общую стоимость
        cart = []
        total_price = 0
        if cart_items != None:
            for item in cart_items:
                product = DBase().getProductById(item[2])
                product_data = {
                    'product_id': product[0],
                    'name': product[1],
                    'price': product[3],
                    'image': base64.b64encode(product[4]).decode('utf-8')  # Преобразуем изображение в base64
                }
                cart.append(product_data)
                total_price += product_data['price']
    except:
        return render_template("index.html", products=products, lenProducts=lenProducts)
    if user!=None:
        return render_template("index.html", products=products, lenProducts=lenProducts, cart=cart, total_price=total_price, admin=user[4])
    else:
        return render_template("index.html", products=products, lenProducts=lenProducts)


@core_bp.route('/product/delete/<int:product_id>', methods=["POST"])
def delete_product(product_id):
    try:
        user = UserLogin.get_user(current_user)
        if user and user[4] == 2:
            DBase().deleteProduct(product_id)
            return redirect('/index.html')
        else:
            return redirect('/index.html')
    except Exception as e:
        print(f"Error deleting product: {e}")
        return redirect('/index.html')

@core_bp.route('/product/edit/<int:product_id>', methods=["POST"])
def edit_product(product_id):
    user = UserLogin.get_user(current_user)
    if user and user[4] == 2:
        product_name = request.form.get('product_name')
        product_about = request.form.get('product_about')
        product_price = request.form.get('product_price')
        print(product_name)
        print(product_about)
        print(product_price)

        if product_name and product_about and product_price:
            try:
                DBase().updateProduct(product_id, product_name, product_about, float(product_price))
            except:print("trigger")

    return redirect('/index.html')



@core_bp.route('/cart/add/<int:product_id>', methods=["GET", "POST"])
def add_to_cart(product_id):
    user=UserLogin.get_user(current_user)
    if user==None:
        return redirect(url_for('auth.login'))
    DBase().addCartItem(user[0], product_id)
    return redirect(url_for('core.index'))

@core_bp.route('/product-details.html', methods=["GET", "POST"])
def product_details():
    products = DBase().getAllProducts()
    products = [list(product) for product in products]
    lenProducts = len(products)

    # Преобразуем картинки в base64
    for product in products:
        if product[4]:
            product[4] = base64.b64encode(product[4]).decode('utf-8')

    # Получаем товары из корзины для текущего пользователя (предполагается, что user_id уже есть)
    try:
        user = UserLogin.get_user(current_user)
        if user != None:
            cart_items = DBase().getCartItems(user[0])
        else:
            cart_items = None

        # Создаем список товаров в корзине и подсчитываем общую стоимость
        cart = []
        total_price = 0
        if cart_items != None:
            for item in cart_items:
                product = DBase().getProductById(item[2])
                product_data = {
                    'product_id': product[0],
                    'name': product[1],
                    'price': product[3],
                    'image': base64.b64encode(product[4]).decode('utf-8')  # Преобразуем изображение в base64
                }
                cart.append(product_data)
                total_price += product_data['price']
        else:
            pass
    except:
        return redirect("auth/login.html")

    # Обработка POST-запроса для добавления отзыва
    if request.method == "POST":
        review_text = request.form.get('review_text')
        product_id = request.form.get('product_id')

        print(request.form)
        print(product_id)

        if review_text and product_id:
            if user:
                DBase().addReview(user[0], product_id, review_text)

    # Получаем данные о товаре по ID
    product_id = request.args.get('id', type=int)
    if not product_id:
        return redirect('/')  # Если ID не передан, перенаправляем на главную

    # Получаем данные о товаре
    product = DBase().getProductById(product_id)
    if not product:
        return render_template("404.html"), 404  # Если товар не найден

    # Получаем все отзывы для данного товара
    reviews = DBase().getReviewsForProduct(product_id)
    print(reviews)
    reviews = [list(review) for review in reviews]
    for review in reviews:
        review[1]=DBase().getUserID(review[1])[1]
    print(reviews)
    # Преобразуем изображение в base64 для отображения
    product_data = {
        'id': product[0],
        'name': product[1],
        'about': product[2],
        'price': product[3],
        'image': base64.b64encode(product[4]).decode('utf-8') if product[4] else None
    }

    return render_template("product-details.html", product=product_data, cart=cart, total_price=total_price, reviews=reviews, admin=user[4])


@core_bp.route('/remove-from-cart', methods=["POST"])
def remove_from_cart():
    product_id = request.form.get('product_id')  # Получаем ID товара для удаления
    if not product_id:
        return redirect('/')  # Если ID не передан, перенаправляем на главную

    # Получаем пользователя
    user = UserLogin.get_user(current_user)
    if not user:
        return redirect('/login')  # Если пользователь не найден, редиректим на страницу логина

    # Удаляем товар из корзины
    DBase().deleteFromCart(user[0], product_id)

    # После удаления товара обновляем корзину
    cart_items = DBase().getCartItems(user[0])
    cart = []
    total_price = 0
    for item in cart_items:
        product = DBase().getProductById(item[2])
        if product:
            product_data = {
                'product_id': product[0],
                'name': product[1],
                'price': product[3],
                'image': base64.b64encode(product[4]).decode('utf-8') if product[4] else None  # Преобразуем изображение в base64
            }
            cart.append(product_data)
            total_price += product_data['price']

    # Возвращаем обновленную корзину на главную страницу (или на другую страницу, если нужно)
    return redirect("/index.html")

@core_bp.route('/my-account.html', methods=["GET", "POST"])
def account():
    if request.method=="GET":
        try:
            user=UserLogin.get_user(current_user)
            admin=user[4]
            print(user)
            print(admin)
            if admin==1:
                # Получаем все товары
                products = DBase().getAllProducts()
                products = [list(product) for product in products]
                products.reverse()
                lenProducts = len(products)

                # Преобразуем картинки в base64
                for product in products:
                    if product[4]:
                        product[4] = base64.b64encode(product[4]).decode('utf-8')

                # Получаем товары из корзины для текущего пользователя (предполагается, что user_id уже есть)
                try:
                    user = UserLogin.get_user(current_user)
                    if user != None:
                        cart_items = DBase().getCartItems(user[0])
                    else:
                        cart_items = None

                    # Создаем список товаров в корзине и подсчитываем общую стоимость
                    cart = []
                    total_price = 0
                    if cart_items != None:
                        for item in cart_items:
                            product = DBase().getProductById(item[2])
                            product_data = {
                                'product_id': product[0],
                                'name': product[1],
                                'price': product[3],
                                'image': base64.b64encode(product[4]).decode('utf-8')
                                # Преобразуем изображение в base64
                            }
                            cart.append(product_data)
                            total_price += product_data['price']
                except: redirect("auth/login.html")
                print(1)
                return render_template("my-account.html",user=user,products=products, lenProducts=lenProducts, cart=cart, total_price=total_price, admin=user[4])
            elif admin==2:
                print(2)
                return render_template("admin.html")
            else:
                print(3)
                return redirect("auth/login.html")
        except:
            return redirect("auth/login.html")
    else:
        try:
            # Получаем данные из формы
            product_name = request.form.get('product_name')
            product_price = request.form.get('product_price')
            product_about = request.form.get('product_about')
            product_image = request.files.get('product_image')
            # Если все поля заполнены
            if product_name and product_price and product_about and product_image:
                image_data = product_image.read()
                DBase().addProduct(product_name, product_about, product_price, image_data)
                return redirect("/index.html")
            else:
                return redirect("/my-account.html")
        except Exception as e:
            print(f"Error: {e}")
            return redirect("index.html")


@core_bp.route('/delete-review/<int:review_id>', methods=["POST"])
@login_required
def delete_review(review_id):
    user = UserLogin.get_user(current_user)
    if user and user[4] == 2:
        DBase().deleteReview(review_id)
        return redirect(request.referrer)
    return redirect("/")
