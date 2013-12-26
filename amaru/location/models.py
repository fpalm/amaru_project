from django.contrib.gis.db import models


class PersonLocation(models.Model):
    """Localización de personas

    Puntos de localización de personas (naturales y jurídicas).
    """

    person = models.OneToOneField('Person', primary_key=True)
    location = models.PointField()
    objects = models.GeoManager()

    def __str__(self):
        return 'Persona: {}'.format(self.person)

    class Meta:
        ordering = ['person']


class GroupLocation(models.Model):
    """Localización de grupos

    Puntos de localización de grupos.
    """

    group = models.OneToOneField('Group', primary_key=True)
    location = models.PointField()
    objects = models.GeoManager()

    def __str__(self):
        return 'Grupo: {}'.format(self.grupo)

    class Meta:
        ordering = ['group']


class LandLots(models.Model):
    """Parcelas"""

    owner = models.OneToOneField('Person', unique=True)
    land_lots = models.MultiPolygonField()
    objects = models.GeoManager()

    def __str__(self):
        return 'Parcelas: {}'.format(self.owner)

    class Meta:
        ordering = ['owner']


class FairLocation(models.Model):
    """Localización de las ferias

    Pensado para ser aplicado en la logística de las ferias.
    """

    fair = models.ForeignKey('Fair')
    group = models.ForeignKey('Group')
    location = models.PointField()
    objects = models.GeoManager()

    def __str__(self):
        return 'Feria: {} Grupo: {}'.format(self.fair.name, self.group.name)

    class Meta:
        unique_together = ('fair', 'group')
        ordering = ['owner']
