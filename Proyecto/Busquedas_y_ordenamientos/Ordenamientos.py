# Ordenamientos.py

def burbuja(lista, clave):
    """Bubble sort implementation (sorts in descending order)"""
    n = len(lista)
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if current element is less than next
            if getattr(lista[j], clave) < getattr(lista[j + 1], clave):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def seleccion(lista, clave):
    """Selection sort implementation (sorts in descending order)"""
    n = len(lista)
    for i in range(n):
        # Find the maximum element in remaining unsorted array
        max_idx = i
        for j in range(i + 1, n):
            if getattr(lista[j], clave) > getattr(lista[max_idx], clave):
                max_idx = j
        # Swap the found maximum element with first element
        lista[i], lista[max_idx] = lista[max_idx], lista[i]
    return lista

def insercion(lista, clave):
    """Insertion sort implementation (sorts in descending order)"""
    for i in range(1, len(lista)):
        key = lista[i]
        j = i - 1
        # Move elements that are less than key to one position ahead
        while j >= 0 and getattr(lista[j], clave) < getattr(key, clave):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = key
    return lista

def mezcla(lista, clave):
    """Merge sort implementation (sorts in descending order)"""
    if len(lista) <= 1:
        return lista
    # Divide the list into two halves
    mid = len(lista) // 2
    left = mezcla(lista[:mid], clave)
    right = mezcla(lista[mid:], clave)
    # Merge the sorted halves
    return merge(left, right, clave)

def merge(left, right, clave):
    """Helper function for merge sort (merges two sorted lists)"""
    result = []
    while left and right:
        # Append the larger element first (for descending order)
        if getattr(left[0], clave) >= getattr(right[0], clave):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    # Append remaining elements (if any)
    result.extend(left or right)
    return result