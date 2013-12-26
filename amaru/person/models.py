from django.db import models


LEGAL_PERSON = (
    ('N', 'Natural'),
    ('J', 'Jurídica'),
)


class Person(models.Model):
    """Modelo base para personas"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=50, blank=True)
    legal_type = models.CharField(max_length=1, choices=LEGAL_PERSON, default='N')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name', 'first_name']


GROUP_TYPE = (
    ('C', 'Nodo Comunero'),
    ('O', 'Otro'),
)


class Group(models.Model):
    """Modelo base para los Grupos

    Representa cada uno de los nodos de la Red Comunera que organizan las
    ferias. La planta que realiza bodegones se considera un nodo.
    """

    name = models.CharField(max_length=50)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=20)
    group_type = models.CharField(max_length=1, choices=GROUP_TYPE, default='C')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

ROLE_TYPE = (
    ('C', 'Contacto'),
    ('O', 'Otro'),
)


class Member(models.Model):
    """Membresía de las personas a Grupos"""

    person = models.ForeignKey('Person')
    group = models.ForeignKey('Group')
    role = models.CharField(max_length=1, choices=ROLE_TYPE, default='O')

    def __str__(self):
        return '{} - {}'.format(self.person, self.group)

    class Meta:
        unique_together = ('person', 'group')
        ordering = ['person', 'group']
