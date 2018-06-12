'''
The flyweight pattern is used as a memory optimization. When we're creating
a large number of instances which all have majority of fields in common,
we can instantiate the common part just once.
The week reference dictionary is used to allow for garbage collection,
once no references (other then the one in the dictionary itself) are available.
'''
import weakref


class CarModel:
    '''This is the flyweight class'''
    _models = weakref.WeakValueDictionary()

    def __new__(cls, model_name,  *args, **kwargs):
        model = cls._models.get(model_name)
        if not model:
            # Construct a new object
            model = super().__new__(cls)
            cls._models[model_name] = model

        return model

    def __init__(self, model_name, air=False, tilt=False, cruise_control=False,
            power_locks=False, alloy_wheels=False, usb_charger=False):
        # Initiate only the first time this object is created
        if not hasattr(self, "initted"):
            self.model_name = model_name
            self.air = air
            self.tilt = tilt
            self.cruise_control = cruise_control
            self.power_locks = power_locks
            self.alloy_wheels = alloy_wheels
            self.usb_charger = usb_charger
            self.initted = True

''' We can now define a class that stores additional information as well as
a reference to the flyweight'''
class Car:

    def __init__(self, model, color, serial):
        self.model = model
        self.color = color
        self.serial = serial

    def check_serial(self):
        return self.model.check_serial(self.serial)



if __name__ == '__main__':
    import gc

    dx = CarModel("FIT DX")
    lx = CarModel("FIT LX", air=True, cruise_control=True, power_locks=True,
        tilt=True)
    car1 = Car(dx, "blue", "12345")
    car2 = Car(dx, "black", "12346")
    car3 = Car(lx, "red", "12347")

    print(id(lx))
    del lx
    del car3
    gc.collect()
    lx = CarModel("FIT LX", air=True, cruise_control=True, power_locks=True,
        tilt=True)
    print(id(lx))
    lx = CarModel("FIT LX")
    print(id(lx))
    print(lx.air)
