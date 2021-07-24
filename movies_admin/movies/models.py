from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.core.validators import MinValueValidator

class Genre(TimeStampedModel):
    name = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True, null=True)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')
        db_table = 'genre'

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    full_name = models.CharField(_('полное имя'), max_length=255)
    birth_date = models.DateField(_('дата рождения'), blank=True, null=True)

    class Meta:
        verbose_name = _('человек')
        verbose_name_plural = _('люди')
        db_table = 'person'

    def __str__(self):
        return self.full_name


class Filmwork(TimeStampedModel):
    title = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True, null=True)
    creation_date = models.DateField(_('дата создания фильма'), blank=True, null=True)
    certificate = models.TextField(_('сертификат'), blank=True, null=True)
    file_path = models.FileField(_('файл'), upload_to='film_works/', blank=True, null=True)
    rating = models.FloatField(_('рейтинг'),
                               validators=[MinValueValidator(0)], blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')
    type = models.CharField(_('тип'), max_length=20)

    class Meta:
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')
        db_table = 'film_work'

    def __str__(self):
        return self.title


class PersonFilmwork(TimeStampedModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    role = models.TextField(_('роль'), blank=True)

    class Meta:
        verbose_name = _('актёр')
        verbose_name_plural = _('актёры')
        db_table = 'person_film_work'


class GenreFilmwork(TimeStampedModel):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')
        db_table = 'genre_film_work'
