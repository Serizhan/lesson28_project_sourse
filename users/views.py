import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from avito import settings
from users.models import User, Location
from users.serializers import UserCreateSerializer, LocationSerializer


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list.all = self.object_list.order_by('username')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        items_list = []
        for user in page_object:
            items_list.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.location.all())),
                "total_ads": user.ads.filter(is_published=True).count()
            })
        response = {
            "items": items_list,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.location.all())),
            "total_ads": user.ads.filter(is_published=True).count()
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["username"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)
        if 'first_name' in user_data:
            self.object.first_name = user_data["first_name"]
        if 'last_name' in user_data:
            self.object.last_name = user_data["last_name"]
        if 'age' in user_data:
            self.object.age = user_data["age"]
        if 'role' in user_data:
            self.object.role = user_data["role"]
        if 'locations' in user_data:
            for loc_name in user_data["locations"]:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.location.all())),
        })


# @method_decorator(csrf_exempt, name="dispatch")
# class UserCreateView(CreateView):
#     model = User
#     fields = ["username"]
#
#     def post(self, request, *args, **kwargs):
#         user_data = json.loads(request.body)
#         user = User.objects.create(
#             username=user_data['username'],
#             first_name=user_data['first_name'],
#             last_name=user_data['last_name'],
#             role=user_data['role'],
#             age=user_data['age'],
#         )
#
#         if 'locations' in user_data:
#             for loc_name in user_data["locations"]:
#                 loc, _ = Location.objects.get_or_create(name=loc_name)
#                 user.location.add(loc)
#
#         return JsonResponse({
#             "id": user.id,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "username": user.username,
#             "role": user.role,
#             "age": user.age,
#             "locations": list(map(str, user.location.all())),
#         })


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
