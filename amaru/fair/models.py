from django.db import models
from person.models import Person, Group


class Crop(models.Model):
    """Modelo para los rubros agrícolas

    El código Ecocrop se corresponde con la base de datos Ecocrop de la FAO
    http://ecocrop.fao.org/ que guarda información detallada relevante de los
    rubros agrícolas.
    """
    name = models.CharField(max_length=50)
    ecocrop_code = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Unity(models.Model):
    """Modelo de las Unidades de Medida

    Equivalencia en Kg. de cada unidad de medida para cada rubro.
    """

    crop = models.ForeignKey('Crop')
    name = models.CharField(max_length=50)
    kg_per_unity = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['crop', 'name']


FAIR_TYPE = (
    ('C', 'Feria Comunera'),
    ('O', 'Otra'),
)

FAIR_STATUS = (          # Estado de organización de la feria
    ('I', 'Inicio'),     # Recién creada
    ('S', 'Solicitud'),  # Recibiendo solicitudes
    ('C', 'Compra'),     # Solicitudes finalizadas, se inicia la compra
    ('A', 'Asignación'), # Compra finalizada, se realiza la asignación
    ('V', 'Venta'),      # Asignación realizada, se procede a la venta
    ('F', 'Finalizada'), # Feria realizada
)


class Fair(models.Model):
    """Modelo de las Ferias (Comuneras)

    Se refiere a todos los eventos que organizan los nodos comuneros, incluidos
    los bodegones de la planta.
    """

    fair_type = models.CharField(max_length=1, choices=FAIR_TYPE, default='C')
    status = models.CharField(max_length=1, choices=FAIR_TYPE, default='I')
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=250, blank=True)
    begin = models.DateTimeField()
    end = models.DateTimeField(blank=True)

    def __str__(self):
        return 'Feria: %s %s' % (self.name, self.begin)

    class Meta:
        ordering = ['begin', 'name']


class FairRecord(models.Model):
    """Modelo base para registro"""

    fair = models.ForeignKey('Fair')
    crop = models.ForeignKey('Crop')
    unity = models.ForeignKey('Unity')
    date = models.DateField()
    quantity = models.FloatField()

    class Meta:
        abstract = True


class Request(FairRecord):
    """Modelo de las Solicitudes

    Para cada Feria, especifica la cantidad de cada rubro por cada nodo
    comunero. Incluye los órdenes de compra de la planta.
    """

    group = models.ForeignKey('Group')

    def __str__(self):
        return 'Solicitud: %s %s %s' % (self.group, self.date, self.crop)

    class Meta:
        ordering = ['group']


class Purchase(FairRecord):
    """Modelo de Compras

    Registro de las compras, cantidad de cada rubro por productor para una feria
    dada.
    """

    person = models.ForeignKey('Person')
    rate = models.FloatField()  # precio unitario
    subtotal = models.FloatField()

    def __str__(self):
        return 'Compra: %s %s %s' % (self.person, self.date, self.crop)

    class Meta:
        ordering = ['person']


class Allocation(FairRecord):
    """Modelo de Asignación

    Unidades asignadas de cada rubro por cada grupo (Nodo Comunero) para una Feria dada.
    Es una venta desde el punto de vista de la Planta.
    """

    group = models.ForeignKey('Group')
    leak = models.FloatField(blank=True)     # fuga
    decline = models.FloatField(blank=True)  # merma
    loss = models.FloatField(blank=True)     # pérdida
    donation = models.FloatField(blank=True) # donación

    def __str__(self):
        return 'Asignación: %s %s %s' % (self.node_comunero, self.date, self.crop)

    class Meta:
        ordering = ['group']


class Sale(FairRecord):
    """Modelo de Venta

    Cantidades vendidas de cada rubro en cada Nodo Comunero para una Feria dada.
    """

    group = models.ForeignKey('Group')
    leftover = models.FloatField()
    rate = models.FloatField()
    subtotal = models.FloatField()
    leak = models.FloatField(blank=True)     # fuga
    decline = models.FloatField(blank=True)  # merma
    loss = models.FloatField(blank=True)     # pérdida
    donation = models.FloatField(blank=True) # donación

    def __str__(self):
        return 'Venta: %s %s %s' % (self.group, self.date, self.crop)

    class Meta:
        ordering = ['group']

