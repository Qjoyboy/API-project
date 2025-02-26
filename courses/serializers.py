from rest_framework import serializers

from courses.models import Course, Lesson, Payment, Subscribe
from courses.services import create_payment
from courses.validators import UrlValidator


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)

class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[UrlValidator()])
    class Meta:
        model = Lesson
        fields = "__all__"


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    url = serializers.URLField(validators=[UrlValidator()])
    lessons = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    sub = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    """Для отображения количества уроков в курсе"""
    @staticmethod
    def get_lessons_count(instance):
        return instance.lessons.count()

    @staticmethod
    def get_lessons(course):
        if not course:
            return []
        lessons = course.lessons.all()
        return LessonSerializer(lessons, many=True).data

    def get_sub(self, obj):
        user = self.context["request"].user
        return Subscribe.objects.filter(course=obj, user=user).exists()

    @staticmethod
    def get_amount(obj):
        return obj.amount


