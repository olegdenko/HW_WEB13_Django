import os
from pipes import quote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from django.core.paginator import Paginator

from quotes.forms import AuthorForm, QuoteForm
from .models import Quote, Author, Tag

# Create your views here.


def main(request, page=1):
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)

    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'top_tags': top_tags})


def get_all_tags():
    return Tag.objects.all()


def author_detail(request, author_id):
    top_tags = Tag.objects.annotate(
        num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    author = Author.objects.get(id=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author, 'top_tags': top_tags})


def tag_quotes(request, tag):
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    quotes_with_tag = Quote.objects.filter(tags__name=tag)
    return render(request, 'quotes/tag_quotes.html', context={'quotes': quotes_with_tag, 'tag': tag, 'top_tags': top_tags})


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect(to="quotes:root")
    return render(
        request,
        "quotes/add_author.html",
        context={"title": "Web 10 hw!", "form": form}
    )


@login_required
def add_quote(request):
    form = QuoteForm(instance=Quote())
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            selected_tags = request.POST.getlist('tags')
            quote.tags.set(selected_tags)
            return redirect(to="quotes:root")

    return render(
        request,
        "quotes/add_quote.html",
        context={"title": "Web 10 hw!", "form": form, "tags": get_all_tags()}
    )

@login_required
def logined_quotes(request, page=1):
    quotes = Quote.objects.filter(user=request.user).all()
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)
    return render(request, 'quotes/index.html', context={"title": "Web 10 hw!", 'quotes': quotes_on_page})


@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)

    if quote.user == request.user:
        if request.method == "POST":
            quote.delete()
            return redirect('quotes:quote_list')

        return render(request, 'quotes/index.html', {'quote': quote})
    else:

        return redirect('quotes:quote_list')


@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if quote.user == request.user:
        if request.method == "POST":
            # form = QuoteForm(request.POST, instance=quote)
            form = QuoteForm(request.POST or None, instance=quote)
            # if form.is_valid():
            if request.method == "POST" and form.is_valid():
                form.save()
                return redirect(to="quotes:root")
        else:
            form = QuoteForm(instance=quote)

        return render(request, 'quotes/edit_quote.html', {'form': form, 'quote': quote})
    else:
        return redirect('quotes:quote_list')


def login(request):
    return render(request, "user/signin.html", context={"title": "Web 10 hw!"})


def register(request):
    return render(
        request, "user/signup.html", context={"title": "Web 10 hw!"}
    )
# def main(request, page=1):
#     db = get_postgresql(DATABASES)
#     quotes = db.quotes.find()
#     per_page = 10
#     paginator = Paginator(list(quotes), per_page)
#     quotes_on_page = paginator.page(page)
#     return render(request, 'quotes/index.html', context={})
#     return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})
