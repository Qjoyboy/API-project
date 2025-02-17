from rest_framework import serializers

from courses.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True,source='lesson')

    class Meta:
        model = Course
        fields = "__all__"

