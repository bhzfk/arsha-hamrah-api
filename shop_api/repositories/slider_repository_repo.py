from shop_api.models import Slider


class SliderRepository:
    def get_front_list():
        return Slider.objects.values()