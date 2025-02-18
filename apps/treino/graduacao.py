import math

order_faixas = {'Branca': 0, 'Azul': 1, 'Roxa': 2, 'Marrom': 3, 'Preta': 4 }

def calcular_qtd_aulas_evoluir_de_faixa(nivel_atual):
    if nivel_atual < 4:
        d = 1.47
        k = 30 / math.log(d)

        aulas_proximo_nivel = k * math.log(nivel_atual + d)
        
        return round(aulas_proximo_nivel)
    else:
        return 0
