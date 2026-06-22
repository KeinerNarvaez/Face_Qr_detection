import os
import shutil

class DashboardPerson:
    def __init__(self):
        self.data_path = "Data/recognition/"

    def folders(self):
        try:
            self.people_list = []
            #Hago un recorrido para identificar las carpetas ignorando los documentos
            for path in os.listdir(self.data_path):
                #Uno de forma segura para evitar errores entre dispositivos
                data = os.path.join(self.data_path, path)
                if os.path.isdir(data):
                    #Se agrega los nombres al arreglo evitando agregar el de documentos, ejemplo .gitkeep
                    self.people_list.append(path)
            return self.people_list
        except Exception as ex:
            return f'Error al detectar nombres de personas: {ex}'

    def modify_name(self,current_name,new_name):
        try:
            os.rename(
                os.path.join(self.data_path, current_name),
                os.path.join(self.data_path, new_name)
            )
        except Exception as ex:
            return f'Error al realizar modificar nombre: {ex}'

    def delete_person(self,name):
        try:
            shutil.rmtree(
                os.path.join(self.data_path, name)
            )
        except Exception as ex:
            return f'Error al delectar nombres de personas: {ex}'