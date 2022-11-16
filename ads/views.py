import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from ads.models import Category, Ad
from avito import settings
from users.models import User


def root(request):
    return JsonResponse({
        "status": "ok"
    })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "category": ad.category.name,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)
        author = get_object_or_404(User, username=ads_data['author'])
        category = get_object_or_404(Category, name=ads_data['category'])

        ad = Ad.objects.create(
            name=ads_data['name'],
            author=author,
            price=ads_data['price'],
            description=ads_data['description'],
            is_published=ads_data['is_published'],
            image=ads_data['image'],
            category=category,
        )
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "category": ad.category.name,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None
        })


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list.all = self.object_list.order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        items_list = []
        for ad in page_object:
            items_list.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.first_name,
                "price": ad.price,
                "description": ad.description,
                "category": ad.category.name,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None
            })
        response = {
            "items": items_list,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category", "is_published", "image"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ads_data = json.loads(request.body)
        # author = get_object_or_404(User, pk=ads_data['author'])
        # category = get_object_or_404(Category, pk=ads_data['category'])
        if 'name' in ads_data:
            self.object.name = ads_data["name"]

        if 'price' in ads_data:
            self.object.price = ads_data["price"]
        if 'description' in ads_data:
            self.object.description = ads_data["description"]

        if 'is_published' in ads_data:
            self.object.is_published = ads_data["is_published"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "category": self.object.category.name,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        categories = self.object_list.all()

        response = []
        for cat in categories:
            response.append({
                "id": cat.id,
                "name": cat.name,
            })

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        Cat = self.get_object()

        return JsonResponse({
            "id": Cat.id,
            "name": Cat.name,
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        ad = Category.objects.create(
            name=cat_data['name'],
        )
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)
        if 'name' in cat_data:
            self.object.name = cat_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImage(UpdateView):
    model = Ad
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get('images')
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "category": self.object.category.name,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
        })
