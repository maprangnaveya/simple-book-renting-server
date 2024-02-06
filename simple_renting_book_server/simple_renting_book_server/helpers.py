from django.utils.html import mark_safe


def get_all_field_names(model_class):
    return [field.name for field in model_class._meta.get_fields()]


def image_tag_thumbnail(image, max_width=500):
    if image:
        return mark_safe(
            '<img src="{}" width="{}" height="{}" style="max-width:{}px; height:auto;" referrerpolicy="strict-origin"/>'.format(
                image.url,
                image.width,
                image.height,
                max_width,
            )
        )
    return ""
