from rest_framework import serializers

from courses.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True,source='lesson', required=False)

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons', [])
        course = Course.objects.create(**validated_data)

        for lessons_data in lessons_data:
            Lesson.objects.create(course=course, **lessons_data)

        return course