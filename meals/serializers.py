from django.db import transaction
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth.models import User

from backend_test.settings import DEFAULT_COUNTRY
from .models import Employee, Menu, Meal, Order


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class SlackEmployeeSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        validated_data['user'] = User.objects.create_user(**user_data)
        return Employee.objects.create(**validated_data)

    def to_internal_value(self, attrs):
        profile = attrs['user']['profile']
        return {
            'slack_user': attrs['user'].pop('id'),
            # Profile slack must have a country defined, if not set settings.DEFAULT_COUNTRY
            'country': profile.pop('country') if 'country' in profile else DEFAULT_COUNTRY,
            'user': {
                'username': profile.pop('email'),
                'first_name': profile.pop('first_name'),
                'last_name': profile.pop('last_name'),
                'password': User.objects.make_random_password(),
            }
        }


class MealSerializer(ModelSerializer):

    class Meta:
        model = Meal
        fields = "__all__"


class MenuSerializer(ModelSerializer):
    meals = PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all(), write_only=True)
    options = SerializerMethodField(read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'date', "state", "options", "meals", "country", )

    def validate(self, attrs):
        menu = Menu.objects.filter(date=attrs['date'], state=Menu.STATE_OPEN, country=attrs['date'])
        if menu:
            raise ValidationError(f"Already exists a open menu for today in {attrs['country']}")

    @staticmethod
    def get_options(menu):
        return MealSerializer(menu.meals, many=True).data


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
