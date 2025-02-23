from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, Lesson, Payment, Subscribe
from courses.paginators import CoursePaginator
from courses.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscribeSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('bought_course','payment_method')
    ordering_filter =('pay_date',)

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def get_permissions(self):
        if self.action == 'create' or self.action =='destroy':
            return [IsAuthenticated(), IsOwner()]
        if self.action == 'update' or self.action =='partial_update':
            return [IsAuthenticated(), IsModerator(), IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_role == "moderator":
            return Course.objects.all()
        return Course.objects.filter(owner=user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        item = serializer.save(owner=self.request.user)
        item.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

class SubscribeActiveAPIView(generics.UpdateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    """Напишу честно, я не понял как сделать отдельный класс с валидацией проверки на булево.
    Поэтому внедрил валидацию в саму вьюху, от чего код стал громоздким.
    Минусы: код стал некрасивым
    Плюсы: это вроде как работает, а значит нельзя трогать
    1:1))))"""

    def update(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=kwargs["pk"])
        user = request.user

        sub_value = request.data.get("sub")
        if not isinstance(sub_value, bool):
            return Response({"error":f"Поле sub должно быть true или false. У вас - {sub_value}"}, status=400)

        if sub_value:
            Subscribe.objects.get_or_create(course=course, user=user)
        else:
            Subscribe.objects.filter(course=course, user=user).delete()
        return Response({"sub":sub_value}, status=200)





