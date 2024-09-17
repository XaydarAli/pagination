from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        pages = requests.get("http://127.0.0.1:8000/users/?size=4").json()["pages"]

        if int(page) <= int(pages):

            if page is None:
                data = requests.get(f"http://127.0.0.1:8000/users/?size=4").json()["items"]
                return render(request, "home.html",
                              context={"users": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.1:8000/users/?page={page}&size=4").json()["items"]
            return render(request, "home.html",
                          context={"users": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "home.html", context={"message": "Not found"})


class PostView(View):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        pages = requests.get(f"http://127.0.0.1:8000/posts/?size=3").json()["pages"]

        if int(page) <= int(pages):

            if page is None:
                data = requests.get(f"http://127.0.0.1:8000/posts/?size=4").json()["items"]
                return render(request, "post.html",
                              context={"posts": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.1:8000/posts/?page={page}&size=4").json()["items"]
            return render(request, "post.html",
                          context={"posts": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "post.html", context={"message": "Not found"})


class CommentView(View):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        pages = requests.get(f"http://127.0.0.1:8000/comments/?size=3").json()["pages"]

        if int(page) <= int(pages):

            if page is None:
                data = requests.get(f"http://127.0.0.1:8000/comments/?size=4").json()["items"]
                return render(request, "comment.html",
                              context={"comments": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.1:8000/comments/?page={page}&size=4").json()["items"]
            return render(request, "comment.html",
                          context={"comments": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "comment.html", context={"message": "Not found"})
