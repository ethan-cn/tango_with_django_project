from django.shortcuts import render, redirect
from django.urls import reverse
from rango.forms import CategoryForm, PageForm
from rango.models import Page
from rango.models import Category

from django.http import HttpResponse


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)


def index(request):
    # return HttpResponse("Rango says hey there partner!<a href='/rango/about/'>About</a>")
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
    #                 'categories': category_list,
    #                 'pages': page_list}

    context_dict = {'categories': category_list, 'pages': page_list}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # return HttpResponse(‘Rango says here is the about page.<a href=“/rango/”>Index</a>’)
    #   prints out whether the method is a GET or a POST
    print(request.method)
    #   prints out the username, if no one is logged in it prints 'AnonymousUser'
    print(request.user)
    return render(request, 'rango/about.html', {})



def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
        # Now that the category is saved, we could confirm this.
        # For now, just redirect the user back to the index view.
            return index(request)
        else:
            # The supplied form contained errors just print them to the terminal.

            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


# def get_category_list(current_category=None):
#     return {'categories': Category.objects.all(),
#             'current_category': current_category}
