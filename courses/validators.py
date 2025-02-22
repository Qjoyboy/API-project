from rest_framework.serializers import ValidationError

class UrlValidator:
    def __init__(self, field="https://youtube.com"):
        self.field = field

    def __call__(self, value):
        if not value.startswith(self.field) and not value.startswith(""):
            raise ValidationError(
                f"URL must start with {self.field}, but got {value}",
                params={"value":value}
            )



