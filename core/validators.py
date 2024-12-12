import re
from django.core.exceptions import ValidationError

# RUT

class RutChile:
    def __init__(self, ver_rut):
        self.rut = ""
        self.es_rut = False
        self.verifica_rut(ver_rut)
        if self.es_rut:
            self.rut = self.formatear_rut(self.rut)

    def verifica_rut(self, rut_raw):
        rut = ""
        pre_rut = "" 
        cuenta = 0

        # Eliminar puntos y guiones del RUT
        rut_raw = re.sub(r"[.-]", "", rut_raw)

        # Separar el número del dígito verificador
        numero_raw = rut_raw[:-1]
        digito_verificador = rut_raw[-1]

        if len(numero_raw) < 7 or len(numero_raw) > 8:
            raise ValidationError("El número del RUT debe tener entre 7 y 8 dígitos")

        # Validar que el número y el dígito verificador sean correctos
        if not numero_raw.isdigit() or not (digito_verificador.isdigit() or digito_verificador.lower() == 'k'):
            raise ValidationError("El valor ingresado no es un RUT válido")

        # Formatear el RUT
        self.rut = f"{numero_raw}-{digito_verificador}"
        self.digito_verificador()

        return self.rut

    def digito_verificador(self):
        rut_separado = self.rut.split("-")
        numero = rut_separado[0][::-1]
        digito = rut_separado[1]
        l = len(numero)
        valor = 0
        serie = [2, 3, 4, 5, 6, 7]
        for x in range(l):
            i = x % len(serie)
            valor += serie[i] * int(numero[x])
        division = float(valor) / 11
        resto = valor - int(division) * 11
        diferencia = 11 - resto
        if diferencia == 11:
            test = 0
        elif diferencia == 10:
            test = "k"
        else:
            test = diferencia
        if digito.isdigit():
            if int(digito) == int(test):
                self.es_rut = True
            else:
                self.es_rut = False
                raise ValidationError("El digito verificador no concuerda")
        elif digito == "k":
            self.es_rut = True
        else:
            self.es_rut = False
            raise ValidationError("El digito verificador no concuerda")

        return self.es_rut

    def formatear_rut(self, rut):
        rut_separado = rut.split("-")
        numero = rut_separado[0]
        digito = rut_separado[1]
        numero_formateado = "{:,}".format(int(numero)).replace(",", ".")
        return f"{numero_formateado}-{digito}"
    

#nombre

def validar_nombre(value):
    # Verificar que el nombre solo contenga letras y espacios
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError("El nombre solo debe contener letras. No se permiten números ni caracteres especiales.")
    
    # Verificar que el nombre no tenga más de 40 caracteres
    if len(value) > 40:
        raise ValidationError("El nombre no debe tener más de 40 caracteres.")
    
    # Transformar la primera letra en mayúscula
    return value.title()
    
def validar_apellido(value):
    # Verificar que el apellido solo contenga letras y espacios
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError("El apellido solo debe contener letras. No se permiten números ni caracteres especiales.")
    # Verificar que el apellido no tenga más de 40 caracteres
    if len(value) > 40:
        raise ValidationError("El apellido no debe tener más de 40 caracteres.")
    
    # Transformar la primera letra en mayúscula
    return value.title()

#numero de telefono

def validar_telefono(telefono):
    # Eliminar cualquier espacio en blanco
    telefono = telefono.strip()

    # Verificar que el teléfono sea numérico y tenga 9 dígitos
    if not re.match(r'^\d{9}$', telefono):
        raise ValidationError("El teléfono debe contener 9 dígitos numéricos.")

    # Agregar el prefijo +56
    return f'+56{telefono}'


