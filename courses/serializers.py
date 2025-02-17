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

    lessons = LessonSerializer(many=True,source='lesson', required=False)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    """Для отображения количества уроков в курсе"""
    @staticmethod
    def get_lessons_count(instance):
        return instance.lesson.count()


    """Переопределяем метод create для того чтобы можно было создавать курсы без уроков"""
    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons', [])
        course = Course.objects.create(**validated_data)

        for lessons_data in lessons_data:
            Lesson.objects.create(course=course, **lessons_data)

        return course