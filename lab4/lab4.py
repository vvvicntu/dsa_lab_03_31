from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Секретный ключ нужен для работы сессий (авторизации)
app.secret_key = 'secret_key'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Имитация базы данных
users_db = {}

# Модель пользователя
class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id              # уникальный ID
        self.email = email        # email (логин)
        self.password = password  # пароль
        self.name = name          # имя пользователя


# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

# Главная страница 
@app.route('/')
def index():
    # Если пользователь авторизован, показываем приветствие, иначе перенаправляем на страницу входа
    if current_user.is_authenticated:
        return render_template('index.html', name=current_user.name)

    return redirect(url_for('login'))


# GET /login (страница входа)
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# POST /login (обработка входа)
@app.route('/login', methods=['POST'])
def login_post():
    # Получаем данные из формы
    email = request.form.get('email')
    password = request.form.get('password')

    # Ищем пользователя по email
    user = None
    for u in users_db.values():
        if u.email == email:
            user = u
            break

    # Если пользователь не найден
    if not user:
        flash('Пользователь не найден')
        return redirect(url_for('login'))

    # Проверка пароля
    if user.password != password:
        flash('Неверный пароль')
        return redirect(url_for('login'))

    # Авторизация пользователя (создание сессии)
    login_user(user)

    return redirect(url_for('index'))



# GET /signup (страница регистрации)
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


# POST /signup (регистрация)
@app.route('/signup', methods=['POST'])
def signup_post():
    # Получаем данные из формы
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Проверяем, есть ли уже пользователь
    for u in users_db.values():
        if u.email == email:
            flash('Пользователь уже существует')
            return redirect(url_for('signup'))

    # Создаём нового пользователя
    user_id = str(len(users_db) + 1)
    new_user = User(user_id, email, password, name)

    # Сохраняем в "базу данных"
    users_db[user_id] = new_user

    # После регистрации отправляем на страницу входа
    return redirect(url_for('login'))


# ================================
# /logout (выход)
# ================================

@app.route('/logout')
@login_required
def logout():
    """
    Выход пользователя:
    - завершает сессию
    - перенаправляет на страницу входа
    """

    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)