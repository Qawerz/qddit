from django.http import HttpResponse


def index(request):
    return HttpResponse("""
    <h2>Првет случайный пользоватеь интернаета  </h2>
        Ты находишься на тестовом сервере Django<br>
            <a href="/contacts">Мои контакты</a>
    """)


def status(request):
    return HttpResponse('<h2>OK</h2>')


def contacts(request):
    return HttpResponse("""
        <a href="http://vk.com/qawerz">VK</a>
    """)