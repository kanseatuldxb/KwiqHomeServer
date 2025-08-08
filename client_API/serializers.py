from rest_framework import serializers

from organization.models import Employee
from .models import Client, SearchFilter, FollowUp, Feedback

class ClientEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name','email']

class ClientSerializer(serializers.ModelSerializer):
    assignees_to = ClientEmployeeSerializer(many=True)
    assignees_to_self = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id',
            'fname',
            'lname',
            'phoneNO',
            'massageNO',
            'email',
            'added_by',
            'organization',
            'created_on',
            'assignees_to',
            'assignees_to_self',
            'status'
        ]

    def get_assignees_to_self(self, obj):
        # Return the value of 'assignees_to_self' from the annotated queryset
        return getattr(obj, 'assignees_to_self', 0)

    # def get_assigned_to(self, obj):
    #     # return obj.assigned_to.username if obj.assigned_to else None
    #     if obj.assigned_to:
    #         return {
    #             'id': obj.assigned_to.id,
    #             'username': obj.assigned_to.username
    #         }

class SearchFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchFilter
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchFilter
        fields = [
            'Area',
            'startBudget',
            'stopBudget',
            'startCarpetArea',
            'stopCarpetArea',
            'possession',
            'units',
        ]


class InterestedSearchFilterSerializer(serializers.ModelSerializer):
    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()

    class Meta:
        model = SearchFilter
        fields = ['client', 'Area', 'startBudget', 'stopBudget', 'startCarpetArea', 'stopCarpetArea', 'possession',
                  'requirements', 'units', 'fname', 'lname']

    def get_fname(self, obj):
        return obj.client.fname

    def get_lname(self, obj):
        return obj.client.lname


class FollowUpSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField()
    class Meta:
        model = FollowUp
        fields = [
            'id',
            'client',
            'message',
            'actions',
            'date_sent',
            'done',
            'added_by',
        ]

    def get_added_by(self, obj):
        return obj.added_by.name if obj.added_by else ''


class FollowUpDateSerializer(serializers.ModelSerializer):
    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()

    class Meta:
        model = FollowUp
        fields = [
            'client',
            'message',
            'actions',
            'date_sent',
            'done',
            'fname',
            'lname'
        ]

    def get_fname(self, obj):
        return obj.client.fname

    def get_lname(self, obj):
        return obj.client.lname


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
