from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import models


# Функция для главной страницы
def home_page(request):
    # Курсы, Категории, Скидки
    category = models.Category.objects.all()
    courses = models.Course.objects.all()
    sales = models.Sale.objects.all()

    context = {'category': category, 'courses': courses, 'sales': sales}

    return render(request, 'homepage.html', context)


# Функция для вывода продуктов из категории
def get_category(request, pk):
    current_category = models.Category.objects.get(category_name=pk)
    courses_from_category = models.Course.objects.filter(course_category=current_category)

    return render(request, 'category.html', {'courses': courses_from_category, 'category': current_category})


# Функция для вывода определенного продукта
def get_course(request, pk):
    current_product = models.Course.objects.get(course_name=pk)

    return render(request, 'product.html', {'course': current_product})


# Функция для добавления курса в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        # Получаем курс
        current_course = models.Course.objects.get(course_name=pk)

        # Добавляем в корзину
        models.Cart(user_id=request.user.id, user_product=current_course).save()

        # Перенаправляем обратно на страницу с курсом
        return redirect(f'/course/{pk}')


# Функция для получения корзины
def get_user_cart(request):
    current_user_cart = models.Cart.objects.filter(user_id=request.user.id)

    return render(request, 'cart.html', {'user_cart': current_user_cart})


# Функция подтверждения заказа
def order_confirmation(request):
    user_cart = models.Cart.objects.filter(user_id=request.user.id)

    for i in user_cart:
        models.Cabinet(user_id=request.user.id, user_courses=i.user_product).save()

    # Очистка корзины
    user_cart.delete()

    # Перенаправляем
    return redirect('/')


# Функция для работы с кабинетом пользователя
def get_user_cabinet(request):
    user_cabinet = models.Cabinet.objects.filter(user_id=request.user.id)

    return render(request, 'cabinet.html', {'user_cabinet': user_cabinet})


# Функция для работы с оплаченными курсами
def get_paid_course(request, pk):
    current_course_program = models.Course.objects.get(course_name=pk)
    paid_course_program = models.Programs.objects.filter(course_name=current_course_program)
    checker = models.Cabinet.objects.filter(user_courses=current_course_program).exists()

    if checker:
        return render(request, 'learning_zone.html', {'course_program': paid_course_program})

    return redirect('/')
