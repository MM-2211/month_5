from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title



STARS = (
    (1, "1/5"),
    (2, "2/5"),
    (3, "3/5"),
    (4, "4/5"),
    (5, "5/5")

)

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')

    stars = models.IntegerField(default='1/5', choices=STARS)

    def __str__(self):
        return self.text

