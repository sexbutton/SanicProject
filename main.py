from sanic import Sanic, response, json
from sanic.response import text
import random
import string
import os




def generate_name_video(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

upload_folder = 'video/'

app = Sanic("MyHelloWorldApp")


@app.route('/')
async def index(request):
    # Открываем файл с HTML-страницей и считываем его содержимое
    with open('html/test.html', 'r', encoding="UTF-8") as file:
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
    random_name_video = generate_name_video(10) + ".mp4"
    file_path = os.path.join(upload_folder, random_name_video)

    with open(file_path, 'wb') as file:
        file.write(uploaded_file.body)

    return response.text('Файл успешно загружен')

@app.route('/video/prank')
async def serve_video(request):
    # Определите логику для поиска и отправки видео-файла
    # в соответствии с переданным video_filename
    video_path = f'video/prank.mp4'
    return await response.file_stream(video_path)

@app.route('/reg')
async def reg(request):
    with open('html/reg.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()

    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

@app.route('/login')
async def login(request):
    with open('html/login.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()

    # Отправляем HTML-страницу как ответ
    return response.html(html_content)


@app.route("/rickroll")
async def rickroll(request):
    with open('html/rickroll.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()
    
    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)