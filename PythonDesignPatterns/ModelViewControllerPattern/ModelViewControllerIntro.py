#! python3

class Model:
    services = {
                'email': {'number': 1000, 'price': 2},
                'sms'  : {'number': 1000, 'price': 2},
                'voice': {'number': 1000, 'price': 2}
    }

class View:
    def list_services(self, services):
        for svc in services:
            print(svc, ' ')

    def list_pricing(self, services):
        for svc in services:
            print("For", Model.services[svc]['number'], svc,
            'message you pay $', Model.services[svc]['price'])

class Controller:
    def __init__(self):
        self._model = Model()
        self._view = View()

    def get_services(self):
        services = self._model.services.keys()
        return(self._view.list_services(services))

    def get_pricing(self):
        services = self._model.services.keys()
        return(self._view.list_pricing(services))

class Client:
    controller = Controller()
    print("Services Provided:")
    controller.get_services()
    print("Pricing for Services:")
    controller.get_pricing()
