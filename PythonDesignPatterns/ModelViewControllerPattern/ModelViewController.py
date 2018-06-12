#! python3

class Model:
    def logic(self):
        data = "Got it!"
        print("Model: Crunching data as per business logic")
        return data

class View:
    def update(self, data):
        print("View: Updating the view with results: ", data)

class Controller:
    def __init__(self):
        self._model = Model()
        self._view = View()

    def interface(self):
        print("Controller: Relayed the Client asks")
        data = self._model.logic()
        self._view.update(data)

class Client:
    print("Client: asks for certain infromation")
    controller = Controller()
    controller.interface()
