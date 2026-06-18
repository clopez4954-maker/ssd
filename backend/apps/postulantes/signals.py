from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Postulante

@receiver(post_save, sender=User)
def crear_postulante(sender, instance, created, **kwargs):
    if created:
        # Check if it's a superuser or staff to prevent creating Postulante unnecessarily, 
        # but let's allow it or filter out based on role if necessary. 
        # Actually, creating it for any user is safe.
        Postulante.objects.get_or_create(
            user=instance,
            defaults={
                'cedula': instance.username,
                'telefono': '',
                'ficha_completada': False,
                'nombre_completo': instance.get_full_name() or instance.username,
            }
        )
