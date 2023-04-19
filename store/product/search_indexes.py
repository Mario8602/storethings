from haystack import indexes
from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # id = indexes.IntegerField(model_attr='product_id')
    name = indexes.CharField(model_attr='name')
    body = indexes.CharField(model_attr='body')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()