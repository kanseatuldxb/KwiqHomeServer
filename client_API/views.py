from os import remove
from re import search

from django.db.models import Q, Case, When, Count, Value, IntegerField
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from organization.models import Employee
from organization.serializers import EmployeeSerializer
from .models import Client, SearchFilter, FollowUp, Feedback
from .serializers import ClientSerializer, SearchFilterSerializer, FollowUpSerializer, FeedbackSerializer, \
    FollowUpDateSerializer
# from django.shortcuts import get_object_or_404
from datetime import datetime


# View for Client model
class ClientAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = ClientSerializer(data=request.data)
    #     if serializer.is_valid():
    #         client = serializer.save()
    #         print(client.id)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        data = request.data
        data['added_by'] = request.user.id
        data['organization'] = request.user.organization.id
        client_serializer = ClientSerializer(data=data)
        if client_serializer.is_valid():
            client = client_serializer.save()

            # Create SearchFilter instance associated with the newly created client
            search_filter_data = request.data.get('search_filter', {})
            search_filter_data['client'] = client.id
            # search_filter_data['added_by'] = request.user.id

            search_filter_serializer = SearchFilterSerializer(data=search_filter_data)

            if search_filter_serializer.is_valid():
                search_filter_serializer.save()
                response_data = {
                    'client': client_serializer.data,
                    'search_filter': search_filter_serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                # Delete the newly created client if the SearchFilter creation fails
                client.delete()
                return Response(search_filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for SearchFilter model
class SearchFiltersAPIView(APIView):
    def get(self, request):
        filters = SearchFilter.objects.all()
        serializer = SearchFilterSerializer(filters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SearchFilterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchFilterAPIView(APIView):
    def get(self, request, id):
        filters = SearchFilter.objects.get(id=id)
        serializer = SearchFilterSerializer(filters)
        return Response(serializer.data)

    def post(self, request):
        serializer = SearchFilterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            filter_instance = SearchFilter.objects.get(id=id)
        except SearchFilter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SearchFilterSerializer(filter_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk):
    #     # Retrieve the object to update
    #     try:
    #         instance = SearchFilter.objects.get(pk=pk)
    #     except SearchFilterSerializer.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     # Update the object with the new data
    #     serializer = SearchFilterSerializer(instance, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for FollowUp model
class FollowUpsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        client_id = request.query_params.get('client_id', None)
        target_date = request.query_params.get('target_date', None)
        done_param = request.GET.get('done', False)
        if target_date:
            followups = FollowUp.objects.filter(date_sent__date=target_date, done=done_param).order_by('date_sent')
            serializer = FollowUpDateSerializer(followups, many=True)
            return Response(serializer.data)

            pass
        if not client_id:
            return Response("client_id parameter is missing.", status=status.HTTP_400_BAD_REQUEST)

        client = get_object_or_404(Client, id=client_id)
        followups = FollowUp.objects.filter(client=client, done=False).order_by('date_sent')
        serializer = FollowUpSerializer(followups, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['added_by'] = request.user.id
        serializer = FollowUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for Feedback model
class FeedbacksAPIView(APIView):
    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Get the related follow-up
            follow_up_id = serializer.validated_data['follow_up']
            print(follow_up_id.id)
            follow_up = get_object_or_404(FollowUp, id=follow_up_id.id)

            # Set the follow-up as done
            follow_up.done = True
            follow_up.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUpAPIView(APIView):
    def get(self, request, id):
        followUp = FollowUp.objects.get(id=id)
        serializer = FollowUpSerializer(followUp)
        return Response(serializer.data)


class FollowUpDate(APIView):
    def get(self, request):
        date_param = request.GET.get('date', None)
        if date_param:
            try:
                # Parse the datetime string to a Python datetime object
                date_param = datetime.strptime(date_param, '%Y-%m-%dT%H:%M:%S.%f')
                # Filter FollowUps based on the provided date
                followups = FollowUp.objects.filter(date_sent__date=date_param.date())
            except ValueError:
                return Response({'error': 'Invalid date format. Use "YYYY-MM-DDTHH:MM:SS.000".'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            followups = FollowUp.objects.all()

        serializer = FollowUpSerializer(followups, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = FollowUpSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailsAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, client_id):
        print(request.headers)
        try:
            # Get the client instance based on the provided client_id
            client = Client.objects.get(id=client_id)

            # Serialize the client data
            client_serializer = ClientSerializer(client)

            # Filter followups based on done parameter (optional query parameter)
            done_param = request.GET.get('done', None)
            followups = FollowUp.objects.filter(client=client, done=False).order_by('date_sent')
            if done_param:
                followups = followups.filter(done=done_param.lower() == 'true')

            # Filter feedbacks based on response parameter (optional query parameter)
            response_param = request.GET.get('response', None)
            feedbacks = Feedback.objects.filter(follow_up__client=client)
            if response_param:
                feedbacks = feedbacks.filter(response=response_param)

            # Serialize filtered followups and feedbacks
            followup_serializer = FollowUpSerializer(followups, many=True)
            feedback_serializer = FeedbackSerializer(feedbacks, many=True)

            searchFilters = SearchFilter.objects.get(client=client)
            searchFiltersSerializer = SearchFilterSerializer(searchFilters)
            # return Response(serializer.data)

            # Combine the serialized data into a single response
            response_data = client_serializer.data
            response_data['followups'] = followup_serializer.data
            response_data['feedback'] = feedback_serializer.data
            response_data['searchFilter'] = searchFiltersSerializer.data

            return Response(response_data)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, client_id):
        client = Client.objects.get(id=client_id)
        if client:
            client.delete()
            return Response({"message": "Client deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

class ClientListView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # organization = self.request.user.organization
        # return Client.objects.filter(organization=organization)
        search_query = self.request.query_params.get('search_query', None)
        query = Client.objects.filter(organization=self.request.user.organization)
        # order by is assignees_to

        # print headers
        if search_query:
            # return Client.objects.filter(Q(fname__icontains=search_query) | Q(lname__icontains=search_query)).order_by('-created_on')
            query = query.filter(Q(fname__icontains=search_query) | Q(lname__icontains=search_query))

        query = query.annotate(
            assignees_to_self = Case(
                When(assignees_to=self.request.user, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-assignees_to_self', '-created_on')
        return query

class ClientEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee_ids = request.data.get('employee_ids', [])
        client_id = request.data.get('client_id')
        if not client_id:
            return Response({'error': 'client_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        client = get_object_or_404(Client, id=client_id, organization=request.user.organization)
        employees = Employee.objects.filter(id__in=employee_ids, organization=request.user.organization)
        # get new employees
        new_employees = employees.exclude(id__in=client.assignees_to.values_list('id', flat=True))
        print(new_employees)
        removed_employees = client.assignees_to.exclude(id__in=employee_ids)
        print(removed_employees)
        client.assignees_to.set(employees)
        return Response({'message': 'Employee assigned to client successfully'}, status=status.HTTP_200_OK)

    def get(self, request):
        organization = request.user.organization
        search = request.query_params.get('search', None)
        client_id = request.query_params.get('client_id', None)

        # Get client and its assigned employees
        client = get_object_or_404(Client, id=client_id, organization=organization)
        user_type_order = Case(
            When(user_type='CEO', then=1),
            When(user_type='Manager', then=2),
            When(user_type='LocalityManager', then=3),
            When(user_type='VisitorCaller', then=4),
            When(user_type='Caller', then=5),
            When(user_type='Visitor', then=6),
            default=7
        )
        client_employee = client.assignees_to.all().order_by(user_type_order)

        # Get all employees in the organization
        employees = Employee.objects.filter(organization=organization).order_by(user_type_order)

        # Apply search filter if provided
        if search:
            employees = employees.filter(name__icontains=search)

        # Exclude assigned employees from the remaining employees
        remaining_employees = employees.exclude(id__in=client_employee.values_list('id', flat=True))

        # Combine the client employees first, followed by the remaining employees
        combined_employees = list(client_employee) + list(remaining_employees)

        # Serialize and return the data
        serializer = EmployeeSerializer(
            combined_employees,
            many=True,
            context={
                'client': client,
                'current_user_type': request.user.user_type  # Keep this for context if needed
            }
        )
        return Response(serializer.data)
