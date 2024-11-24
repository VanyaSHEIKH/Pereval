from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=50)
    fam = models.CharField(max_length=50, default='Иванов')
    name = models.CharField(max_length=50, default='Иван')
    otc = models.CharField(max_length=50, default='Иванович')
    phone = models.CharField(max_length=17, default='8 999 999 99 99')

    def __str__(self):
        return f'{self.email}, {self.name}, {self.fam}, {self.otc}'


class Coordinates(models.Model):
    latitude = models.DecimalField(max_digits=15, decimal_places=2)
    longitude = models.DecimalField(max_digits=15, decimal_places=2)
    height = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'Широта: {self.latitude}, Долгота: {self.longitude}, Высота: {self.height}'


class Level(models.Model):
    #"А" русская
    LEVEL = (
        ('1А', '1А'),
        ('2А', '2А'),
        ('3А', '3А'),
        ('1B', '1Б'),
        ('2B', '2Б'),
        ('3B', '3Б'),
        ('3B*', '3Б*'),
    )
    winter = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)
    summer = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)
    autumn = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)
    spring = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)

    def __str__(self):
        return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, весна: {self.spring}'

class Pereval(models.Model):
    STATUS_TYPES = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('new', 'new'),
    )
    beauty_title = models.CharField(max_length=255, default="пер.")
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, null=True, blank=True)
    connect = models.CharField(max_length=255, null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    coords = models.ForeignKey(Coordinates, on_delete=models.CASCADE, related_name='coords')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='level')
    status = models.CharField(choices=STATUS_TYPES, default='new', max_length=15)


def get_path_upload_images(instance, file):
    return f'photos-{instance.pereval.id}/{file}'


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, related_name='images', on_delete=models.CASCADE)
    data = models.ImageField(upload_to=get_path_upload_images, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)


