from rest_framework import serializers
from products.models import Product, Option, Category, ProductImages, Brand


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'name', 'name_ar', 'description', 'description_ar']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'description', 'description_ar', 'image']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'name_ar', 'description', 'description_ar', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'name_ar', 'description', 'description_ar', 'price',
                  'stock', 'weight', 'main_image', 'images', 'categories', 'options', 'brand']

    def to_internal_value(self, data):
        # override many to many field by get from form-data as string separated by ',' and split it to list and set
        # it in query dec by same name like it came as list
        c = data.getlist('categories')
        o = data.getlist('options')
        if len(c) == 1:
            c = c[0].split(',')
            data.setlist('categories', c)
        if len(o) == 1:
            o = o[0].split(',')
            data.setlist('options', o)
        return super(ProductSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        self.fields['categories'] = CategorySerializer(many=True)
        self.fields['options'] = OptionSerializer(many=True)
        return super(ProductSerializer, self).to_representation(instance)

    def create(self, validated_data):
        images = self.context.get('view').request.FILES.getlist('images')
        product = super(ProductSerializer, self).create(validated_data)
        for image in images:
            ProductImages.objects.create(product_id=product, image=image)
        return product

    def update(self, instance, validated_data):
        images = self.context.get('view').request.FILES.getlist('images')
        product = super(ProductSerializer, self).create(validated_data)
        for image in images:
            ProductImages.objects.create(product_id=product, image=image)
        return product
