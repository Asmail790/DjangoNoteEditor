from django.db.models import Model


def get_field(name:str,model:Model):

    return model._meta.get_field(name)
