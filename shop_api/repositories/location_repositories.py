from shop_api.models import City, State


class LocationRepositpry:
    
    def add_state(self,name):
        state = State(name=name)
        state.save()
        return state
    
    def get_state(self,id):
        states = State.objects.filter(id=id).values()
        if states.count()==0:
            return None
        return states[0]
    def state_exist_by_name(self,name):
        states = State.objects.filter(name=name).values()
        if states.count()==0:
            return None
        return states[0]
    
    
    def add_city(self,name,state_id):
        city = City(name=name,state_id=state_id)
        city.save()
        return city
    
    def city_exist_by_name_and_state(self,name,state_id):
        cities = City.objects.filter(name=name).filter(state_id=state_id).values()
        if cities.count()==0:
            return None
        return cities[0]
    
    def get_city(self,id):
        cities = City.objects.filter(id=id).values()
        if cities.count()==0:
            return None
        return cities[0]
