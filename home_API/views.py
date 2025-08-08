from datetime import datetime

from django.db.models import Q
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics as genrics
from client_API.models import SearchFilter
from client_API.serializers import SearchFilterSerializer, InterestedSearchFilterSerializer, FilterSerializer
from .helper import Interested, SearchFilterObject
from .serializers import ProjectSerializer, UnitSerializer, ProjectSerializer1, UnitSerializer1, AreaSerializer, \
    UnitsSerializer, GovernmentalAreaSerializer, ProjectsSerializer, ImageSerializer, FloorMapSerializer, \
    ProjectDetailsSerializer
from .models import Project, Unit, Area, Units, GovernmentalArea, Image, FloorMap


class ProjectList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        units = Unit.objects.all()
        serializer = UnitSerializer1(units, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['created_on'] = datetime.now()
        data['added_by'] = request.user.id
        data['organization'] = request.user.organization.id

        units = data.pop('units')
        projectSerializer = ProjectSerializer(data=request.data)
        if projectSerializer.is_valid():

            a = projectSerializer.save()
            print(a.id, a.area)
            for unit in units:
                unit['project_id'] = a.id
                unit['organization'] = request.user.organization.id
                unitSerializer = UnitSerializer(data=unit)
                if unitSerializer.is_valid():
                    u = unitSerializer.save()
                    print(u)
                else:
                    print(unitSerializer.errors)
                    return Response(data=unitSerializer.errors, status=400)
                    # print(unitSerializer.errors)
            # projectSerializer.
            return Response(data={}, status=status.HTTP_201_CREATED)
        print(projectSerializer.errors)
        return Response(data=projectSerializer.errors, status=400)


class AreaAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            area = self.get_object(pk)
            serializer = AreaSerializer(area)
            return Response(serializer.data)
        else:
            areas = Area.objects.all().order_by('formatted_version')
            serializer = AreaSerializer(areas, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AreaSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(serializer.data, status=status.HTTP_208_ALREADY_REPORTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        area = self.get_object(pk)
        serializer = AreaSerializer(area, data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except IntegrityError:
            return Response(serializer.data, status=status.HTTP_208_ALREADY_REPORTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        area = self.get_object(pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Area.objects.get(pk=pk)
        except Area.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class OptionsView(APIView):
    def get(self, request):
        units = Units.objects.all()
        governmentalArea = GovernmentalArea.objects.all()
        unitsSerializer = UnitsSerializer(units, many=True)
        governmentalAreaSerializer = GovernmentalAreaSerializer(governmentalArea, many=True)
        responses = {
            "units": unitsSerializer.data,
            "governmentalArea": governmentalAreaSerializer.data,
        }
        return Response(data=responses, status=status.HTTP_200_OK)


class ProjectsView(APIView):
    def get(self, request):
        project = Project.objects.all()
        projectsSerializer = ProjectsSerializer(project, many=True)
        return Response(projectsSerializer.data)

class ProjectsListView(genrics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            return Project.objects.filter(
            Q(
                Q(projectName__icontains=search_query) |
                Q(area__icontains=search_query) |
                Q(developerName__icontains=search_query)
            ) & Q(organization=self.request.user.organization)
            ).order_by('-created_on')
        return Project.objects.filter(organization=self.request.user.organization
        ).order_by('-created_on')

class ProjectView(APIView):
    def get(self, request, pk):
        # TODO transform it to serializer
        project = Project.objects.get(id=pk)
        projectSerializer = ProjectSerializer(project)
        data = projectSerializer.data
        unit = Unit.objects.filter(project_id=pk)
        unitSerializer = UnitSerializer(unit, many=True)
        data.update({'units': unitSerializer.data})
        return Response(data)
        # return Response(projectSerializer.data.update({'nameme': 'akshay'}))

    def put(self, request, pk):
        data = request.data
        try:
            project_id = pk
            project = Project.objects.get(pk=project_id)

        except (KeyError, Project.DoesNotExist):
            return Response(data={'error': 'Invalid project id'}, status=status.HTTP_400_BAD_REQUEST)

        projectSerializer = ProjectSerializer(project, data=data)
        if projectSerializer.is_valid():
            try:
                project_id = pk
                units_to_delete = Unit.objects.filter(project_id=project_id)
                if not units_to_delete.exists():
                    print(f'error: No units found with project_id: {project_id}')
                    # return Response(data={'error': f'No units found with project_id: {project_id}'},
                    #                 status=status.HTTP_404_NOT_FOUND)

                units_to_delete.delete()
                print(f'message:Units deleted successfully')
                # return Response(data={'message': 'Units deleted successfully'}, status=status.HTTP_200_OK)
            except KeyError:
                print(f'error: Invalid request. Project ID not provided.')
                # return Response(data={'error': 'Invalid request. Project ID not provided.'},
                #                 status=status.HTTP_400_BAD_REQUEST)

            projectSerializer.save()

            # Process units if included in the request
            if 'units' in data:
                units = data.pop('units')
                for unit in units:
                    unit['project_id'] = project_id
                    unit_id = unit.get('id')
                    if unit_id:
                        try:
                            unit_obj = Unit.objects.get(pk=unit_id)
                        except Unit.DoesNotExist:
                            return Response(data={'error': f'Invalid self id: {unit_id}'},
                                            status=status.HTTP_400_BAD_REQUEST)
                        unitSerializer = UnitSerializer(unit_obj, data=unit)
                    else:
                        unitSerializer = UnitSerializer(data=unit)

                    if unitSerializer.is_valid():
                        unitSerializer.save()
                    else:
                        return Response(data=unitSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=projectSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            project.delete()
            return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)


class UnitAPIView(APIView):
    def get(self, request, project_id):
        unit = Unit.objects.filter(project_id=project_id)
        unitSerializer = UnitSerializer(unit, many=True)
        return Response(unitSerializer.data)


class InterestedAPIView(APIView):
    def get(self, request, unit_id):
        unit = Unit.objects.get(pk=unit_id)
        # print(unit.serializable_value('self'))

        interested = Interested(unit.id, unit.unit, unit.CarpetArea, unit.price, unit.project_id.area,
                                unit.project_id.rera)
        interested.match()
        searchFilter = SearchFilter.objects.all()
        searchFilterSerializer = InterestedSearchFilterSerializer(searchFilter, many=True)
        for s in searchFilterSerializer.data:
            # print(searchFilter.len())
            # s = searchFilterSerializer.data[0]
            searchFilterObject = SearchFilterObject(s.get('id'), s.get('Area'), s.get('startBudget'),
                                                    s.get('stopBudget'),
                                                    s.get('startCarpetArea'), s.get('stopCarpetArea'),
                                                    s.get('possession'),
                                                    s.get('units'))
            searchFilterObject.printValue()
            s['rating'] = interested.compare_objects(searchFilterObject)
        sorted_data = sorted(searchFilterSerializer.data, key=lambda x: x['rating'], reverse=True)
        return Response(sorted_data)


class FilterAPIView(APIView):
    def post(self, request):
        print(request.data)
        filterSerializer = FilterSerializer(data=request.data)
        if filterSerializer.is_valid():
            print('valid')
            searchFilterObject = SearchFilterObject(client=filterSerializer.validated_data.get('client'),
                                                    Area=filterSerializer.validated_data.get('Area'),
                                                    startBudget=filterSerializer.validated_data.get('startBudget'),
                                                    stopBudget=filterSerializer.validated_data.get('stopBudget'),
                                                    startCarpetArea=filterSerializer.validated_data.get(
                                                        'startCarpetArea'),
                                                    stopCarpetArea=filterSerializer.validated_data.get(
                                                        'stopCarpetArea'),
                                                    possession=filterSerializer.validated_data.get('possession'),
                                                    units=filterSerializer.validated_data.get('units'),
                                                    )
            unit = Unit.objects.all()
            unitSerializer1 = UnitSerializer1(unit, many=True)
            for unit in unitSerializer1.data:
                interested = Interested(unit.get('id'), unit.get('unit'), unit.get('CarpetArea'), unit.get('price'),
                                        unit.get('area'), unit.get('possession'))
                # print(unit.get('rera'))
                unit['rating'] = searchFilterObject.compare_objects(interested)
            sorted_data = sorted(unitSerializer1.data, key=lambda x: x['rating'], reverse=True)

        return Response(sorted_data)

        # try:
        #     unit = Unit.objects.get(pk=unit_id)
        # except Unit.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        #
        # interested = Interested(unit.id, unit.unit, unit.CarpetArea, unit.price, unit.project_id.area,
        #                         unit.project_id.rera)
        # interested.match()
        #
        # search_filters = SearchFilter.objects.all()
        # search_filter_serializer = InterestedSearchFilterSerializer(search_filters, many=True)
        # sorted_data = []
        #
        # for s in search_filter_serializer.data:
        #     search_filter_object = SearchFilterObject(
        #         s.get('client'), s.get('Area'), s.get('startBudget'), s.get('stopBudget'),
        #         s.get('startCarpetArea'), s.get('stopCarpetArea'), s.get('possession'), s.get('units')
        #     )
        #     search_filter_object.match(interested)  # Call the match method to debug
        #
        #     s['rating'] = interested.compare_objects(search_filter_object)
        #     sorted_data.append(s)
        #
        # sorted_data.sort(key=lambda x: x['rating'], reverse=True)
        # return Response(sorted_data)


class Images(APIView):
    def get(self, request):
        a = Image.objects.all()
        b = ImageSerializer(a, many=True)
        return Response(b.data)

    def post(self, request):
        a = ImageSerializer(data=request.data)
        if a.is_valid():
            a.save()
            return Response(a.data, status=status.HTTP_201_CREATED)
        else:
            return Response(a.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageView(APIView):

    def get(self, request, pk):
        a = Image.objects.get(id=pk)
        b = ImageSerializer(a)
        return Response(b.data)

    def delete(self, request, pk):
        try:
            image = Image.objects.get(id=pk)
            image.delete()
            return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            image = Image.objects.get(id=pk)
        except Image.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the existing image
        image.delete()

        # Create a new instance with the updated data
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FloorMaps(APIView):
    def get(self, request):
        a = FloorMap.objects.all()
        b = FloorMapSerializer(a, many=True)
        return Response(b.data)

    def post(self, request):
        a = FloorMapSerializer(data=request.data)
        if a.is_valid():
            a.save()
            return Response(a.data, status=status.HTTP_201_CREATED)
        else:
            return Response(a.errors, status=status.HTTP_400_BAD_REQUEST)


class FloorMapView(APIView):

    def get(self, request, pk):
        a = FloorMap.objects.get(id=pk)
        b = FloorMapSerializer(a)
        return Response(b.data)

    def delete(self, request, pk):
        try:
            image = FloorMap.objects.get(id=pk)
            image.delete()
            return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FloorMap.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            image = FloorMap.objects.get(id=pk)
        except FloorMap.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the existing image
        image.delete()

        # Create a new instance with the updated data
        serializer = FloorMapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetails(AreaAPIView):
    def get(self, request, id):
        project = Project.objects.get(id=id)
        projectSerializer = ProjectDetailsSerializer(project)
        return Response(projectSerializer.data)


class ProjectImages(AreaAPIView):
    def get(self, request, id):
        images = Image.objects.filter(project_id=id)
        imagesSerializer = ImageSerializer(images, many=True)
        return Response(imagesSerializer.data)


class UnitImages(AreaAPIView):
    def get(self, request, id):
        images = FloorMap.objects.filter(unit=id)
        imagesSerializer = FloorMapSerializer(images, many=True)
        return Response(imagesSerializer.data)
