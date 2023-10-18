from rest_framework import serializers
from measurement.models import Measurement, Sensor


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['sensor_id', 'temperature', 'created_at']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'title', 'description', 'measurements']


class SensorChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['description']
