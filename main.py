from sanic import Sanic, response, json, redirect, html
from sanic_session import Session
import random
import string
import os
from sanic_session import Session, InMemorySessionInterface
from database import Database
from sanic import Sanic
from sanic.response import text, HTTPResponse
from sanic.cookies import Cookie




def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

upload_folder = 'video/'

app = Sanic("MyHelloWorldApp")


@app.route('/')
async def index(request):
    # Открываем файл с HTML-страницей и считываем его содержимое
    with open('html/index.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()

    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

@app.route('/account')
async def account(request):
    # Открываем файл с HTML-страницей и считываем его содержимое
    with open('html/account.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()

    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

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
@app.route('/getUserLogin')
async def UserLoginServe(request):
    cookies = str(request.cookies.get('Auth'))
    response = json({'Username': Database.get_user_id(cookies), 'Password':'Пошел нахуй'})
    return response

@app.route('/video/prank')
async def serve_video(request):
    # Определите логику для поиска и отправки видео-файла
    # в соответствии с переданным video_filename
    video_path = f'video/prank.mp4'
    return await response.file_stream(video_path)

@app.route('/reg', methods=['POST'])
async def reg(request):
        cookiestring = generate_random_string(10)
        Database.reg_user(cookiestring, request.form.get('username'), request.form.get('password'))
        response = redirect('/')
        response.cookies['Auth'] = cookiestring
        
        return response
@app.route('/register')
async def register(request):
    cookies = str(request.cookies.get('Auth'))
    if cookies != 'None':
        response = redirect('/')
        return response
    with open('html/reg.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()
        response = html(html_content)
        return response
    
    
@app.route('/log', methods=['POST'])
async def log(request):
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
    with open('html/login.html', 'r', encoding="UTF-8") as file:
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
    with open('html/rickroll.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()
    
    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000)