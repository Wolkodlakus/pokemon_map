from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(default=0, blank=True, null=True)
    health = models.IntegerField(default=0, blank=True, null=True)
    strength = models.IntegerField(default=0, blank=True, null=True)
    defence = models.IntegerField(default=0, blank=True, null=True)
    stamina = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f'{self.id}-{self.pokemon.title}'
