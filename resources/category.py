import cv2



class Resource:
    namespace: str

    def __init__(self, name):
        self._name = name
        # print(name)




class Image_rs(Resource):
    def __init__(self, name):
        super().__init__(name)
        path = pathutil.from_resource(self)
        self.image =cv2.cvtColor(cv2.imread(path, cv2.IMREAD_COLOR),cv2.COLOR_RGBA2RGB)


class Button_rs(Image_rs): pass


class realm_rs(Resource): pass


class strom_rs(realm_rs): pass


class GreatEmpire_rs(realm_rs): pass


class Nomad_rs(Image_rs): pass


class FirePeak_rs(Image_rs): pass


class String_rs(Resource): pass


class DisplayName_rs(String_rs): pass

class Popup_rs(Image_rs): pass


class unit_rs(Image_rs):
    def __init__(self, name):
        super().__init__(name)
        # TODO these infos also should be loaded from resources
        self._displayName:str



from utils import pathutil