
import random

def generate_prediction():
    """
    Gera uma previsão para o jogo Aviator
   
    Returns:
        tuple: (prediction, wait_time)
            - prediction (float): Valor previsto entre 1.00 e 100.59
            - wait_time (int): Tempo de espera em segundos
    """
    # Define a distribuição dos números com predominância de números baixos
    rand_value = random.random()
   
    if rand_value < 0.5:  # 50% de chance para números entre 1.00 e 1.59
        prediction = round(random.uniform(1.00, 1.59), 2)
        wait_time = 6  # 6 segundos para números de 1.00 a 1.59
       
    elif rand_value < 0.8:  # 30% de chance para números entre 2.00 e 5.37
        prediction = round(random.uniform(2.00, 5.37), 2)
        wait_time = 12  # 12 segundos para números de 2.00 a 9.59
       
    elif rand_value < 0.9:  # 10% de chance para números entre 5.38 e 9.59
        prediction = round(random.uniform(5.38, 9.59), 2)
        wait_time = 12  # 12 segundos para números de 2.00 a 9.59
       
    else:  # 10% de chance para números entre 10.00 e 100.59
        prediction = round(random.uniform(10.00, 100.59), 2)
        wait_time = 30  # 30 segundos para números de 10.00 a 100.59
   
    # Formata o número para sempre ter 2 casas decimais
    prediction = format(prediction, '.2f')
   
    return prediction, wait_time
