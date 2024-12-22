from shop_api.tools.melipayamak import Api

class SMSRepository:
    
    def send_sms(self,mobile,text):
        username = '09113400016'
        password = '3c28d31b-553f-4dbc-93cc-872691fce726'
        api = Api(username,password)
        sms = api.sms()
        to = mobile
        _from = '90005763'
        text = text
        response = sms.send(to,_from,text)
        print(response)