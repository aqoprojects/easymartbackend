from django.core.exceptions import ValidationError

def validate_Icon_size(image):
  max_size_mb = 1
  if image.size > max_size_mb * 1024 * 1024:
    raise ValidationError(f"Image size should not exceed {max_size_mb}MB.")