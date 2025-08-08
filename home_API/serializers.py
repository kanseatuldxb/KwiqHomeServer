from rest_framework import serializers
from .models import Project, Unit, Area, Units, GovernmentalArea, Image, FloorMap


class ProjectSerializer(serializers.ModelSerializer):
    # units = UnitSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['area', 'projectName', 'projectType', 'developerName', 'landParcel', 'landmark', 'areaIn',
                  'waterSupply', 'floors', 'flatsPerFloors', 'totalUnit', 'availableUnit', 'amenities', 'parking',
                  'longitude', 'latitude', 'transport', 'readyToMove', 'power', 'goods', 'rera',
                  'possession', 'contactPerson', 'contactNumber', 'marketValue', 'lifts', 'brokerage', 'incentive',
                  'image', 'url', 'created_on', 'added_by', 'organization']

    def get_image(self, obj):
        images = Image.objects.filter(project_id=obj.id)

        if images.exists():
            first_image_serializer = ImageSerializer(images.first())
            return first_image_serializer.data.get('image')
        return None


class ProjectDetailsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'area', 'projectName', 'projectType', 'developerName', 'landmark', 'areaIn', 'amenities',
                  'parking',
                  'transport', 'readyToMove', 'power', 'goods', 'rera', 'possession', 'image', 'units', 'url']

    def get_image(self, obj):
        images = Image.objects.filter(project_id=obj.id)

        if images.exists():
            first_image_serializer = ImageSerializer(images.first())
            return first_image_serializer.data.get('image')
        return None

    def get_units(self, obj):
        units = Unit.objects.filter(project_id=obj.id)
        serializedUnit = UnitSerializer(units, many=True)
        return serializedUnit.data


class UnitSerializer(serializers.ModelSerializer):
    floor_map = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = [
            'id',
            'project_id',
            'unit',
            'CarpetArea',
            'price',
            'floor_map',
            'organization'
        ]

    def get_floor_map(self, obj):
        data = FloorMap.objects.filter(unit=obj.id)
        serialize = FloorMapSerializer(data, many=True)
        return serialize.data


class ProjectSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['projectName', 'area', 'rera']


class UnitSerializer1(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    possession = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    project_units = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['project_id', 'project_name', 'area', 'possession', 'unit', 'CarpetArea', 'price', 'longitude',
                  'latitude',
                  'amenities', 'project_units', 'image']

    def get_project_units(self, obj):
        unit = Unit.objects.filter(project_id=obj.project_id)
        unit = UnitSerializer(unit, many=True)
        return unit.data

    def get_project_name(self, obj):
        return obj.project_id.projectName

    def get_area(self, obj):
        return obj.project_id.area

    def get_possession(self, obj):
        return obj.project_id.possession

    def get_longitude(self, obj):
        return obj.project_id.longitude

    def get_latitude(self, obj):
        return obj.project_id.latitude

    def get_amenities(self, obj):
        return obj.project_id.amenities

    def get_image(self, obj):
        images = Image.objects.filter(project_id=obj.project_id)

        if images.exists():
            first_image_serializer = ImageSerializer(images.first())
            return first_image_serializer.data.get('image')
        return None


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'


class GovernmentalAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentalArea
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'area', 'projectName', 'developerName', 'image']

    def get_image(self, obj):
        images = Image.objects.filter(project_id=obj.id)

        if images.exists():
            first_image_serializer = ImageSerializer(images.first())
            return first_image_serializer.data.get('image')
        return None


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Image
        fields = '__all__'


class FloorMapSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = FloorMap
        fields = '__all__'
