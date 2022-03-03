from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, null=False, verbose_name='Title', )
    parent_category_id = models.IntegerField(null=True, blank=True, verbose_name='Parent Category ID', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return "{} - {} - {} - {}".format(
            self.title,
            self.parent_category_id,
            self.created_at,
            self.updated_at,
        )


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )

    title = models.CharField(max_length=255, null=False, verbose_name='Title', )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', )

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(
            self.category,
            self.title,
            self.price,
            self.created_at,
            self.updated_at,
        )
