from shop_api.models import Brand


class BrandRepo:
    
    def get_all(self):
        return Brand.objects.values()
