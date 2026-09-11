from django.shortcuts import render
def index(request):
    context = {
        'welcome': 'Добро пожаловать в систему!',
        'menu': [
            {'url_name': 'home', 'title': 'Главная'},
            {'url_name': 'about', 'title': 'О системе'},
            {'url_name': 'contacts', 'title': 'Контакты'},
        ],
    }
    return render(request, 'journal/index.html', context)
def about(request):
 return render(request, 'journal/about.html')

def contacts(request):
    return render(request, 'journal/contacts.html')