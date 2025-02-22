from rest_framework import serializers

from courses.models import Course, Lesson, Payment, Subscribe
from courses.validators import UrlValidator


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

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

    lessons = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    sub = serializers.SerializerMethodField()

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

    def get_sub(self,obj):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user, course=obj).exists()
        return False


