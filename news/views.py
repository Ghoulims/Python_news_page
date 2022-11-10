from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

class HomeNews (ListView):
    model = News
    template_name = 'news/home_news_list.html' 
    context_object_name = 'news'
    paginate_by = 2
    #extra_context = {'title':'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'] ,is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'
 

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'




#_______________________________________________________________________________#

#def index(request):
#    news = News.objects.order_by('-created_at')
#    context = {
#        'news': news, 
#        'title': 'Список новостей',
#    }
#    return render(request, 'news/index.html', context=context)


#def get_category(request, category_id):
#    news = News.objects.filter(category_id=category_id)
#    category = Category.objects.get(pk=category_id)
#    return render(request, 'news/category.html', {'news': news, 'category':category})


#def view_news(request, news_id):
    #news_item = News.objects.get(pk=news_id)
#    news_item = get_object_or_404(News, pk=news_id)
#    return render(request, 'news/view_news.html', {'news_item': news_item})


#def add_news(request):
#    if request.method == 'POST':
#        form = NewsForm(request.POST)
#        if form.is_valid():
#            #print(form.cleaned_data)
#            #news = News.objects.create(**form.cleaned_data)
#            news = form.save()
#            return redirect(news)
#    else:
#        form = NewsForm()
#    return render(request, 'news/add_news.html', {'form':form})