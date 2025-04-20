import random
import time
import matplotlib.pyplot as plt

def generar_arreglo(n):
    return [random.randint(10_000_000, 99_999_999) for _ in range(n)]

def bubble_sort(arr):
    n = len(arr)
    if n<=100001:
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def stooge_sort(arr, i=0, j=None):
    if j is None:
        j = len(arr) - 1
    if arr[i] > arr[j]:
        arr[i], arr[j] = arr[j], arr[i]
    if j - i + 1 > 2:
        t = (j - i + 1) // 3
        stooge_sort(arr, i, j - t)
        stooge_sort(arr, i + t, j)
        stooge_sort(arr, i, j - t)

def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    for i in range(1, 10):
        count[i] += count[i-1]
    
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index]-1] = arr[i]
        count[index] -= 1
        i -= 1
    
    for i in range(n):
        arr[i] = output[i]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def bitonic_sort(arr, up=True):
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr) // 2
        first = bitonic_sort(arr[:mid], True)
        second = bitonic_sort(arr[mid:], False)
        return bitonic_merge(first + second, up)

def bitonic_merge(arr, up):
    if len(arr) == 1:
        return arr
    else:
        bitonic_compare(arr, up)
        mid = len(arr) // 2
        first = bitonic_merge(arr[:mid], up)
        second = bitonic_merge(arr[mid:], up)
        return first + second

def bitonic_compare(arr, up):
    dist = len(arr) // 2
    for i in range(dist):
        if (arr[i] > arr[i + dist]) == up:
            arr[i], arr[i + dist] = arr[i + dist], arr[i]

def medir_tiempo(func, arr):
    start = time.time()
    if func in [quick_sort, stooge_sort, bitonic_sort]:
        arr = func(arr.copy())
    else:
        func(arr.copy())
    end = time.time()
    return end - start

def guardar_arreglo_en_archivo(arr, nombre_archivo):
    with open(nombre_archivo, 'w') as f:
        for num in arr:
            f.write(f"{num}\n")

def cargar_arreglo_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]



def main_ordenamiento():
    tamanos = [10_000, 100_000, 1_000_000]
    metodos = [
        ("Bubble Sort", bubble_sort, "O(n²)"),
        ("Quick Sort", quick_sort, "O(n log n)"),
        #("Stooge Sort", stooge_sort, "O(n^(log 3/log 1.5))"),
        ("Radix Sort", radix_sort, "O(nk)"),
        ("Merge Sort", merge_sort, "O(n log n)"),
        ("Bitonic Sort", bitonic_sort, "O(n log² n)")
    ]
    
    resultados = {nombre: [] for nombre, _, _ in metodos}
    
    for tam in tamanos:
        nombre_archivo = f"arreglo_{tam}.txt"

        # Solo generar y guardar si no existe el archivo
        try:
            arr = cargar_arreglo_desde_archivo(nombre_archivo)
        except FileNotFoundError:
            arr = generar_arreglo(tam)
            guardar_arreglo_en_archivo(arr, nombre_archivo)

        for nombre, func, _ in metodos:
            tiempo = medir_tiempo(func, arr)
            resultados[nombre].append(tiempo)
            print(f"{nombre} con {tam} elementos: {tiempo:.4f} segundos")
    
    # Mostrar tabla
    print("\nTabla 1. Análisis de datos enteros")
    print("|Método de ordenamiento|Tamaño 1|Tiempo|Tamaño 2|Tiempo|Tamaño 3|Tiempo|")
    print("|---|---|---|---|---|---|---|")
    for nombre, _, complejidad in metodos:
        tiempos = resultados[nombre]
        print(f"|{nombre} {complejidad}|{tamanos[0]}|{tiempos[0]:.4f}|{tamanos[1]}|{tiempos[1]:.4f}|{tamanos[2]}|{tiempos[2]:.4f}|")
    
   # Gráfico mejorado
    plt.figure(figsize=(14, 8))

    for nombre, _, _ in metodos:
        tiempos = resultados[nombre]
        plt.plot(tamanos, tiempos, marker='o', linestyle='-', linewidth=2, markersize=6, label=nombre)

        # Añadir etiquetas a cada punto
        for x, y in zip(tamanos, tiempos):
            plt.text(x, y + 0.05, f"{y:.2f}s", ha='center', fontsize=8)

    plt.xlabel('Tamaño del arreglo (n)', fontsize=12)
    plt.ylabel('Tiempo de ejecución (segundos)', fontsize=12)
    plt.title('Comparación de Algoritmos de Ordenamiento - Datos Enteros', fontsize=14)
    plt.xticks(tamanos, [f'{x:,}' for x in tamanos])
    plt.yscale('log')  # Escala logarítmica si hay mucha diferencia entre algoritmos
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.legend(title="Algoritmo", fontsize=10)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main_ordenamiento()