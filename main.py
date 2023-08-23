from sanic import Sanic, response
from sanic.response import text
from sanic import json

app = Sanic("MyHelloWorldApp")

@app.route('/')
async def index(request):
    # Открываем файл с HTML-страницей и считываем его содержимое
    with open('html/test.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()

    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

@app.route('/video/prank')
async def serve_video(request):
    # Определите логику для поиска и отправки видео-файла
    # в соответствии с переданным video_filename
    video_path = f'video/prank.mp4'
    return await response.file(video_path)

@app.route("/rickroll")
async def rickroll(request):
    with open('html/rickroll.html', 'r', encoding="UTF-8") as file:
        html_content = file.read()
    
    # Отправляем HTML-страницу как ответ
    return response.html(html_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)