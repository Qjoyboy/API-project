from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, Lesson, Payment, Subscribe
from courses.paginators import CoursePaginator
from courses.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscribeSerializer
from courses.services import create_payment, retrieve_payment
from courses.tasks import send_email_of_update
from users.models import User


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('bought_course','payment_method')
    ordering_filter =('pay_date',)

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        currency = request.data.get("currency","rub")
        user = User.objects.get(id=request.data.get("email"))
        course_bought = Course.objects.get(id=request.data.get("course_bought"))

        if not all([amount, currency, user, course_bought]):
            return Response({"error":"Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        client_secret, payment_id = create_payment(int(amount), currency)

        if isinstance(client_secret, str):
            payment = Payment.objects.create(
                email=user,
                course_bought=course_bought,
                amount=amount,
                payment_method="card",
                session_id=client_secret,

                is_paid=False
            )
            return Response({"client_secret":client_secret, "ID":payment_id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"Ошибка при создании платежа"}, status=status.HTTP_400_BAD_REQUEST)

class PaymentRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    lookup_field = 'payment_intent_id'

    def get_object(self):
        payment_intent_id = self.request.GET.get("payment_intent_id")
        payment = retrieve_payment(payment_intent_id)
        # if not payment:
        #     raise NotFound("Payment not found or invalid ID")
        return payment

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
        send_email_of_update.delay()
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
            return Response({"error":f"Поле sub должно быть труе или фалсе. У вас - {sub_value}"}, status=400)

        if sub_value:
            Subscribe.objects.get_or_create(course=course, user=user)
        else:
            Subscribe.objects.filter(course=course, user=user).delete()
        return Response({"sub":sub_value}, status=200)





