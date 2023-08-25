from sanic import Sanic, response, json, redirect, html, file
import random
import string
import os
from database import *
from sanic import Sanic
from sanic.response import text, html
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sanic.request import Request



def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

upload_folder = 'video/'

app = Sanic("MyHelloWorldApp")

# Настройка Jinja2 для Sanic
env = Environment(
    loader=FileSystemLoader('templates'),  # Папка с шаблонами
    autoescape=select_autoescape(['html', 'xml'])
)

@app.route('/video/<filename:str>')
async def serve_video(request, filename):
    return await response.file_stream('video/'+filename)

@app.route('/images/<filename:str>')
async def serve_image(request, filename):
    return await response.file_stream('Images/'+filename)
     

@app.route('/')
async def index(request):
    # Открываем файл с HTML-страницей и считываем его содержимое
    with open('templates/index.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()

    # Отправляем HTML-страницу как ответ
    return response.html(html_content)


@app.route('/addvideo')
async def addvideo(request):
    # Открываем файл с HTML-страницей и считываем его содержимое
    with open('templates/addvideo.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()

    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

@app.route('/account')
async def account_info(request: Request):
    # Здесь вы можете получить информацию об аккаунте и передать ее в шаблон Jinja2
    template = env.get_template('MyAccount.html')
    cookies = str(request.cookies.get('Auth'))
    account_data = Database.GetUserData(Database.get_user_id(cookies))
    return response.html(template.render(account=account_data))

@app.route('/upload', methods=['POST'])
async def upload_video(request):
    uploaded_file = request.files.get('video')
    if not uploaded_file:
        return response.text('Файл не загружен')

    # Сохраните файл на сервере
    random_name_video = generate_random_string(10) + ".mp4"
    file_path = os.path.join(upload_folder, random_name_video)

    with open(file_path, 'wb') as file:
        file.write(uploaded_file.body)

    return response.text('Файл успешно загружен')

def validationpassword(password:str, passwordrepeat:str):
    len_password = False
    if len(password) < 8:
        len_password = False
    else:
        len_password = True

    digits_in_password = True
    # Проверка наличия цифр в пароле
    if not any(char.isdigit() for char in password):
        digits_in_password = False

    char_in_password = True
    # Проверка наличия букв в пароле
    if not any(char.isalpha() for char in password):
        char_in_password = False

    punctuation_in_password = True
    # Проверка наличия символов пунктуации в пароле
    if not any(char in string.punctuation for char in password):
        punctuation_in_password = False

    checkpassword = True
    if password != passwordrepeat:
        checkpassword = False
    
    return len_password and digits_in_password and char_in_password and punctuation_in_password and checkpassword

@app.route('/reg', methods=['POST'])
async def reg(request):
    cookiestring = generate_random_string(10)
    while(Database.CookieExists(cookiestring)):
        cookiestring = generate_random_string(10)
    Database.reg_user(cookiestring, request.form.get('username'), request.form.get('password'), request.form.get('nickname'))
    response = redirect('/')
    response.cookies['Auth'] = cookiestring
    
    return response

@app.route('/register')
async def register(request):
    cookies = str(request.cookies.get('Auth'))
    if cookies != 'None':
        response = redirect('/')
        return response
    with open('templates/register.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()
        response = html(html_content)
        return response
    
@app.route('/log', methods=['POST'])
async def log(request):
        cookiestring = generate_random_string(10)
        while(Database.CookieExists(cookiestring)):
             cookiestring = generate_random_string(10)
        Login = request.form.get('username')
        if Database.LoginUser(Login,request.form.get('password')) != None:
             Database.create_session(cookiestring, Login)
        response = redirect('/')
        response.cookies['Auth'] = cookiestring
        return response
@app.route('/login')
async def login(request):
    cookies = str(request.cookies.get('Auth'))
    if cookies != 'None':
            response = redirect('/')
            return response
    with open('templates/login.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()
        response = html(html_content)
    # Отправляем HTML-страницу как ответ
    return response
@app.route("/check")
async def check(request):
    return response.text(request.cookies.get('Auth'))
@app.route("/reset")
async def reset(request):
    response = text("Reset")
    response.cookies['Auth'] = None
    return response

@app.route("/rickroll")
async def rickroll(request):
    with open('templates/rickroll.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()
    
    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000)