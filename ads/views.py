from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from ads.models import Category, Ad, Selection
from ads.permissions import IsOwnerSelection, IsOwnerAdOrStaff
from ads.serializers import AdListSerializer, SelectionListSerializer, SelectionDetailSerializer, \
    SelectionSerializer, CategorySerializer, AdSerializer, AdDetailSerializer


def root(request):
    return JsonResponse({
        "status": "ok"
    })


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')

    default_serializer = AdSerializer
    serializer_class = {
        'list': AdListSerializer,
        'retrieve': AdDetailSerializer
    }

    default_permission = [AllowAny()]
    permissions = {
        'create': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsOwnerAdOrStaff()],
        'partial_update': [IsAuthenticated(), IsOwnerAdOrStaff()],
        'destroy': [IsAuthenticated(), IsOwnerAdOrStaff()]
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()

    default_serializer = SelectionSerializer
    serializer_class = {
        'list': SelectionListSerializer,
        'retrieve': SelectionDetailSerializer
    }

    default_permission = [AllowAny()]
    permissions = {
        'create': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsOwnerSelection()],
        'partial_update': [IsAuthenticated(), IsOwnerSelection()],
        'destroy': [IsAuthenticated(), IsOwnerSelection()]
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer)
