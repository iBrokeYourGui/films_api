import os

from src import app

if __name__ == '__main__':
    # эта строка нужно для публикации на хероку. Заменять захаржкоженый код на переменные окружения
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0')
