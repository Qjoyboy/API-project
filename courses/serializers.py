from rest_framework import serializers

from courses.models import Course, Lesson, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    # lessons = LessonSerializer(many=True,source='lesson.all', required=False)
    lessons = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()

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


