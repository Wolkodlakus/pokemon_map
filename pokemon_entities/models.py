from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название по русски', max_length=200)
    title_en = models.CharField(verbose_name='Название по английски',max_length=200, default='', blank=True, null=True)
    title_jp = models.CharField(verbose_name='Название по японски',max_length=200, default='', blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', blank=True,null=True)
    description = models.TextField(verbose_name='Описание', default='', blank=True, null=True)
    evolved_from = models.ForeignKey('self', verbose_name='Из кого эволюционировал',
                                     blank=True, on_delete=models.SET_NULL, null=True,
                                     related_name='evolves_into')

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появление', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения', blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень', default=0, blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', default=0, blank=True, null=True)
    strength = models.IntegerField(verbose_name='Сила', default=0, blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', default=0, blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', default=0, blank=True, null=True)

    def __str__(self):
        return f'{self.id}-{self.pokemon.title}'
