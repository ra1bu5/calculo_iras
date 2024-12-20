from django.shortcuts import render
import numpy as np

def calcular(request):
    if request.method == 'POST':
        # Campos para IPCSL
        percentis_IPCSL = list(map(float, request.POST['percentis_IPCSL'].split(',')))  #atual
        valores_IPCSL = list(map(float, request.POST['valores_IPCSL'].split(',')))      #atual
        valor_atual_IPCSL = float(request.POST['valor_atual_IPCSL'])                   #atual

        # Campos para PAV
        percentis_PAV = list(map(float, request.POST['percentis_PAV'].split(',')))      #atual
        valores_PAV = list(map(float, request.POST['valores_PAV'].split(',')))          #atual
        valor_atual_PAV = float(request.POST['valor_atual_PAV'])                       #atual

        # Campos para ITU
        percentis_ITU = list(map(float, request.POST['percentis_ITU'].split(',')))      #atual
        valores_ITU = list(map(float, request.POST['valores_ITU'].split(',')))          #atual
        valor_atual_ITU = float(request.POST['valor_atual_ITU'])                       #atual

        # Verifique se as listas têm o mesmo comprimento
        if len(percentis_IPCSL) != len(valores_IPCSL) or len(percentis_PAV) != len(valores_PAV) or len(percentis_ITU) != len(valores_ITU):
            return render(request, 'calculos/formulario.html', {'error': 'As listas de percentis e valores devem ter o mesmo comprimento.'})

        # Valores conhecidos IPCSL BR 2023
        percentis_BR_IPCSL = [50, 75]           # Percentis conhecidos  #2023
        valores_BR_IPCSL = [2.7, 5.4]           # Valores correspondentes #2023
        valor_BR_IPCSL = 4.11                   # Média Brasil 2023 #2023

        # Interpolação
        percentil_BR_IPCSL = np.interp(valor_BR_IPCSL, valores_BR_IPCSL, percentis_BR_IPCSL) #2023

        # Valores conhecidos PAV BR 2023
        percentis_BR_PAV = [50, 75]             # Percentis conhecidos #2023
        valores_BR_PAV = [7.5, 14.4]            # Valores correspondentes #2023
        valor_BR_PAV = 9.99                     # Média Brasil 2023 #2023

        # Interpolação
        percentil_BR_PAV = np.interp(valor_BR_PAV, valores_BR_PAV, percentis_BR_PAV) #2023

        # Valores conhecidos ITU
        percentis_BR_ITU = [50, 75]             # Percentis conhecidos #2023
        valores_BR_ITU = [1.5, 3.7]             # Valores correspondentes #2023
        valor_BR_ITU = 2.7                      # Média Brasil 2023 #2023

        # Interpolação
        percentil_BR_ITU = np.interp(valor_BR_ITU, valores_BR_ITU, percentis_BR_ITU) #2023

        # Interpolação dos valores atuais
        percentil_atual_IPCSL = np.interp(valor_atual_IPCSL, valores_IPCSL, percentis_IPCSL) #atual
        percentil_atual_PAV = np.interp(valor_atual_PAV, valores_PAV, percentis_PAV)        #atual
        percentil_atual_ITU = np.interp(valor_atual_ITU, valores_ITU, percentis_ITU)        #atual

        # Cálculo do resultado do KR
        resultado_KR = (
            ((percentil_BR_IPCSL - percentil_atual_IPCSL) / 15) * 
            (valor_atual_IPCSL / (valor_atual_IPCSL + valor_atual_PAV + valor_atual_ITU))
        ) + (
            ((percentil_BR_PAV - percentil_atual_PAV) / 15) * 
            (valor_atual_PAV / (valor_atual_IPCSL + valor_atual_PAV + valor_atual_ITU))
        ) + (
            ((percentil_BR_ITU - percentil_atual_ITU) / 15) * 
            (valor_atual_ITU / (valor_atual_IPCSL + valor_atual_PAV + valor_atual_ITU))
        )

        return render(request, 'calculos/resultado.html', {'resultado_KR': resultado_KR})

    return render(request, 'calculos/formulario.html')