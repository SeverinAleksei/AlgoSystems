'''
1. Написать умножение матриц случайной размерности
2. Написать перемножение каждой матрицы из списка друг с другом 
3. Распараллелить второй пункт с помощью multiprocessing
4. Вывести сравнение времени работы распараллеленного кода и не распараллеленного
'''

import numpy as np
from timeit import timeit
import multiprocessing 
from random import randint


# Перемножение матриц через numpy
def mmul_native(matrix1, matrix2):
    '''
    Функция перемножения 2-ух матриц
    Пункт 1
    '''
    result = []
    '''Ваш код'''
    try :
        
        m1 = np.array(matrix1)
        m2 = np.array(matrix2)
        
        y1,x1 = m1.shape
        y2,x2 = m2.shape
        #print(y1,x1,y2,x2)
        for i in range(y1):
            row = []
            for j in range(x2):
                row.append(np.sum(m1[i,:] * m2[:,j]))
            result.append(row)
        
    except:
        return "Неподходящий размер матриц"
    
    return result


# Перемножает все пары матриц через numpy
def mmul(matrixs):
    '''
    Функция перемножения каждой матрицы с каждой
    Пункт 2
    '''
    result = []
    '''Ваш код'''
    
    for i in matrixs:
        for j in matrixs:
            result.append(mmul_native(i,j))
    
    return result

# Просто функция для отладки перемножения
def print_matrix(matrix):
    for row in matrix:
        print(row)

# Перемножение матриц без использования numpy
def mmul_native_without_np(matrix1, matrix2):
    try :
        x1 = len(matrix1[0])
        y1 = len(matrix1)

        x2 = len(matrix2[0])
        result = [[0 for i in range(x2)] for j in range(y1)]
        #print(y1,x1,y2,x2)
        for i in range(y1):
            for j in range(x2):
                for k in range(x1):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]
        
    except:
        print("Error")
        return "Неподходящий размер матриц"
    
    return result

# Перемножение пар матриц без использования numpy
def mmul_without_np(matrixs):
    result = []
    
    for i in matrixs:
        for j in matrixs:
            result.append(mmul_native_without_np(i,j))
    
    return result

if __name__ == '__main__':
    '''
    Точка входа в программу
    '''

    matrices = []
    for z in range(4):
        matrices.append([[randint(1, 100) for i in range(10)] for j in range(10)]) # Создание матриц
    '''
    3 и 4 пункты
    '''
    '''Ваш код'''
    n_iterations = 10
    # 3ий пункт 
    # Numpy лучше подходит для перемножения больших матриц
    # Например для матриц 100*100 он работает в 4 раза быстрее, чем через списки
    print("Время расчета 3-ий пункт через numpy:", timeit('mmul(matrices)', globals=globals(), number = n_iterations))
    print("Время расчета 3-ий пункт без numpy:  ", timeit('mmul_without_np(matrices)', globals=globals(), number = n_iterations))
    #print(mmul(matrices))
    # 4ый пункт
    # Есть два варианта как можно действовать
    # 1) Делать параллельные вычисления перемножения рядов и столбоцов для двух матриц 
    # 2) Параллельно считать произведения различных пар матриц

    # Я реализовал второй вариант, так как считаю что он должен дать больше прибавки к скорости
    product = [[i,j] for i in matrices for j in matrices]
    pool =  multiprocessing.Pool(4)
    print("Время расчета 4-ый пункт мульт:      ", timeit(lambda: pool.starmap(mmul_native_without_np, product), number=n_iterations))
    
    #Ниже вариант с итератором, по идее это экономит время генерации листа product
    print("Время расчета 4-ый пункт мульт:      ", timeit(lambda: pool.starmap(mmul_native_without_np, ([i,j] for i in matrices for j in matrices)), number=n_iterations))
    
    # Однако я не смог добится увелечения скорости
    # Почитав форумы на эту тему я не смог найти решения
    # Хотя на форумах также писали что один и тот же код у одних и тех же людей на разных машинах показывал разные результаты