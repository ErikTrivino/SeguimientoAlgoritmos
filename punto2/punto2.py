import random
import time
import matplotlib.pyplot as plt

def generar_arreglo(n):
    return [random.randint(10_000_000, 99_999_999) for _ in range(n)]

def busqueda_lineal(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

def busqueda_binaria(arr, x):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

def busqueda_ternaria(arr, x):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        if arr[mid1] == x:
            return mid1
        if arr[mid2] == x:
            return mid2
            
        if x < arr[mid1]:
            right = mid1 - 1
        elif x > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1
    return -1

def busqueda_saltos(arr, x):
    n = len(arr)
    step = int(n ** 0.5)
    prev = 0
    
    while prev < n and arr[min(step, n)-1] < x:
        prev = step
        step += int(n ** 0.5)
        if prev >= n:
            return -1
    
    while prev < n and arr[prev] < x:
        prev += 1
        if prev == min(step, n):
            return -1
    
    if prev < n and arr[prev] == x:
        return prev
    return -1

def medir_tiempo_busqueda(func, arr, x):
    start = time.perf_counter()
    func(arr, x)
    end = time.perf_counter()
    return (end - start) * 1000  # milisegundos

def main_busqueda():
    tamanos = [10_000, 100_000, 1_000_000]
    metodos = [
        ("Busqueda Lineal", busqueda_lineal, "O(n)"),
        ("Busqueda Binaria", busqueda_binaria, "O(log n)"),
        ("Busqueda Ternaria", busqueda_ternaria, "O(log3 n)"),
        ("Busqueda por saltos", busqueda_saltos, "O(sqrt(n))")
    ]
    
    resultados = {nombre: [] for nombre, _, _ in metodos}
    
    for tam in tamanos:
        arr = sorted(generar_arreglo(tam))
        x = arr[tam // 2]
        for nombre, func, _ in metodos:
            tiempo = medir_tiempo_busqueda(func, arr, x)
            resultados[nombre].append(tiempo)
            print(f"{nombre} con {tam} elementos: {tiempo:.4f} ms")
    
    # Tabla
    print("\nTabla 2. Analisis de datos enteros (tiempo en milisegundos)")
    print("|Metodo de busqueda|Tamano 1|Tiempo (ms)|Tamano 2|Tiempo (ms)|Tamano 3|Tiempo (ms)|")
    print("|---|---|---|---|---|---|---|")
    for nombre, _, complejidad in metodos:
        tiempos = resultados[nombre]
        print(f"|{nombre} {complejidad}|{tamanos[0]}|{tiempos[0]:.4f}|{tamanos[1]}|{tiempos[1]:.4f}|{tamanos[2]}|{tiempos[2]:.4f}|")
    
    # Gráfico con etiquetas detalladas
    plt.figure(figsize=(12, 7))
    colores = ['#e74c3c', '#2ecc71', '#3498db', '#9b59b6']
    estilos = ['-', '--', '-.', ':']
    
    for i, (nombre, _, _) in enumerate(metodos):
        tiempos = resultados[nombre]
        plt.plot(tamanos, tiempos, label=nombre, marker='o', color=colores[i], linestyle=estilos[i])
        for j, tiempo in enumerate(tiempos):
            offset = tiempo * 0.03 + 0.3  # Ajuste dinámico
            plt.text(tamanos[j], tiempo + offset, f"{tiempo:.2f} ms", 
                    fontsize=9, ha='center', va='bottom', 
                    bbox=dict(facecolor='white', edgecolor='none', pad=1))
    
    plt.xlabel('Tamaño del arreglo', fontsize=12)
    plt.ylabel('Tiempo (milisegundos)', fontsize=12)
    plt.title('Comparación detallada de algoritmos de búsqueda', fontsize=14)
    plt.xticks(tamanos, [f"{tam:,}" for tam in tamanos], fontsize=10)
    plt.yscale('log')  # Escala log para claridad
    plt.legend()
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main_busqueda()
