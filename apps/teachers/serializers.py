from attr import attr
from django.apps import apps
from django.forms import ValidationError
from rest_framework import serializers
from apps.students.models import Assignment,GRADE_CHOICES


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        if 'content' in attrs and attrs['content']:
            raise ValidationError({'non_field_errors':'Teacher cannot change the content of the assignment'})
        
        if attrs['grade'] not in dict(GRADE_CHOICES):
              raise ValidationError(attrs['grade'] +' is not a valid choice.')
        
        if 'state' in attrs:
            if attrs['state'] == 'DRAFT':
                raise ValidationError({'non_field_errors':'SUBMITTED assignments can only be graded'})
            if attrs['state'] == 'GRADED' :
                raise ValidationError({'non_field_errors':'GRADED assignments cannot be graded again'})

        if self.partial:
            return attrs

        return super().validate(attrs)
