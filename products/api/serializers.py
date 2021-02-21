from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.response import Response

from products.models import Product, Option, Category, ProductImages, Brand, CartProduct, Cart, WishList, ProductReview


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
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'name_ar', 'description', 'description_ar', 'price',
                  'stock', 'weight', 'main_image', 'images', 'categories', 'options', 'brand', 'reviews', 'rate',
                  'rate_count']

    def get_reviews(self, obj):
        reviews = obj.reviews.all()[:5]
        return ReviewSerializer(reviews, many=True, context={'request': self.context.get('view').request}).data

    def to_internal_value(self, data):
        # override many to many field by get from form-data as string separated by ',' and split it to list and set
        # it in query dec by same name like it came as list
        data._mutable = True
        categories = data.getlist('categories')
        options = data.getlist('options')
        del_img = data.getlist('del_img')
        if len(categories) == 1:
            categories = categories[0].split(',')
            if categories[-1] == '':
                categories.pop()
            data.setlist('categories', categories)
        if len(options) == 1:
            options = options[0].split(',')
            if options[-1] == '':
                options.pop()
            data.setlist('options', options)
        if len(del_img) == 1:
            del_img = del_img[0].split(',')
            if del_img[-1] == '':
                del_img.pop()
            data.setlist('del_img', del_img)
        data._mutable = False
        return super(ProductSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        # overwrite to_representation to be nested in show
        self.fields['categories'] = CategorySerializer(many=True)
        self.fields['options'] = OptionSerializer(many=True)
        self.fields['brand'] = BrandSerializer()
        return super(ProductSerializer, self).to_representation(instance)

    def create(self, validated_data):
        images = self.context.get('view').request.FILES.getlist('images')
        product = super(ProductSerializer, self).create(validated_data)
        for image in images:
            ProductImages.objects.create(product_id=product, image=image)
        return product

    def update(self, instance, validated_data):
        images = self.initial_data.getlist('images')
        del_img = self.initial_data.getlist('del_img')
        product = super(ProductSerializer, self).update(instance, validated_data)
        for image in images:
            ProductImages.objects.create(product_id=product, image=image)
        if del_img:
            img = ProductImages.objects.filter(Q(id__in=del_img) & Q(product_id=product))
            for p in img:
                p.delete()
        return product


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']

    def to_representation(self, instance):
        # overwrite to_representation to be nested in show
        self.fields['product'] = ProductSerializer(read_only=True)
        return super(CartProductSerializer, self).to_representation(instance)


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['products']

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request:
            if request.user.is_authenticated:
                cart = Cart.objects.get_or_create(user=request.user)[0]
            else:
                if not request.session.exists(request.session.session_key):
                    request.session.create()
                cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]

            # because  cart and product_id is unique together and if add product more than one time just update
            # quantity
            for c in validated_data['products']:
                try:
                    cart_product, flag = CartProduct.objects.get_or_create(cart=cart, product=c['product'])
                    if c.get('quantity', None):
                        if c['quantity'] == 'plus':
                            if not flag:
                                cart_product.quantity = cart_product.quantity + 1
                            else:
                                cart_product.quantity = 1
                        else:
                            cart_product.quantity = c['quantity']
                    else:
                        cart_product.quantity = 1
                    cart_product.save()
                except:
                    pass
            return cart
        raise Response(status=status.HTTP_404_NOT_FOUND)


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['products']

    def to_internal_value(self, data):
        # override many to many field by get from form-data as string separated by ',' and split it to list and set
        # it in query dec by same name like it came as list
        data._mutable = True
        products = data.getlist('products')
        if len(products) == 1:
            products = products[0].split(',')
            if products[-1] == '':
                products.pop()
            data.setlist('products', products)
        data._mutable = False
        return super(WishSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        # overwrite to_representation to be nested in show
        self.fields['products'] = ProductSerializer(many=True, read_only=True)
        return super(WishSerializer, self).to_representation(instance)

    def create(self, validated_data):
        product = validated_data.get('products', None)
        request = self.context.get("request", None)
        if product and request:
            # Add to WishList in database if user is authenticated
            if request.user.is_authenticated:
                wish = WishList.objects.get_or_create(user=request.user)[0]
            else:
                if not request.session.exists(request.session.session_key):
                    request.session.create()
                wish = WishList.objects.get_or_create(session_key=request.session.session_key)[0]
            for p in product:
                if p not in wish.products.all():
                    wish.products.add(product)
            return wish
        else:
            raise Response(status=status.HTTP_404_NOT_FOUND)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = ['user', 'product', 'rate', 'comment', 'created_at']
        extra_kwargs = {'product': {'write_only': True}}

    def get_user(self, obj):
        request = self.context.get("request", None)

        return {'name': obj.user.get_full_name(), 'image': request.build_absolute_uri(obj.user.image.url)}

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request:
            review = ProductReview.objects.create(user=request.user, rate=validated_data['rate'],
                                                  comment=validated_data['comment'], product=validated_data['product'])
            return review
        raise Response(status=status.HTTP_404_NOT_FOUND)
