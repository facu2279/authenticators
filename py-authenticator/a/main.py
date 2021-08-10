import random
from datetime import datetime

f = open ('datos.csv','w')

inicio = datetime(1990, 1, 1)
final =  datetime(2012, 8, 10)
binarios = ["true", "false"]
min_fact_anual = 100000
max_fact_anual = 1000000
min_metros = 10
max_metros = 100


for i in range(1, 10000):
    random_date = inicio + (final - inicio) * random.random()
    fact_anual = random.randrange(min_fact_anual, max_fact_anual, 100)
    fact_promedio = int(fact_anual / 12)
    metros = random.randrange(min_metros, max_metros, 1)
    conducta_pago = random.choice(binarios)
    cant_funcionarios = random.randrange(10, 500, 10)
    vip = random.choice(binarios)
    string = str(i) + "," + str(random_date) + "," + str(fact_anual) + "," + str(fact_promedio) + "," + str(metros) + "," + conducta_pago + "," + str(cant_funcionarios) + "," + vip + '\n'
    f.write(string)

f.close()