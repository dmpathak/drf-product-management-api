from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        if not file.name.endswith(".json"):
            raise serializers.ValidationError("Only JSON files are allowed.")
        return file
