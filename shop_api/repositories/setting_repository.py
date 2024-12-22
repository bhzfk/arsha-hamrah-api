from shop_api.models import Setting


class SettingRepo :
    
    
    def get_setting_by_name(name) :
        return Setting.objects.filter(name=name).values()
    def get_all_settings() :
        return Setting.objects.values()
    def get_all_settings_dic() :
        settings =  Setting.objects.values()
        print("settings")
        print(settings)
        dic={}
        for a in  settings :
            dic[a["name"]]=a["val"]
        
        print("settings")
        print(settings)
        return dic
        


