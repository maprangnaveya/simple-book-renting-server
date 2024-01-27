def get_all_field_names(model_class):
    return [field.name for field in model_class._meta.get_fields()]
