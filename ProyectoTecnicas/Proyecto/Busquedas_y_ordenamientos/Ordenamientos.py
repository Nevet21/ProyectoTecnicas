# Ordenamientos.py

def burbuja(lista, clave):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if getattr(lista[j], clave) < getattr(lista[j + 1], clave):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def seleccion(lista, clave):
    n = len(lista)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if getattr(lista[j], clave) > getattr(lista[max_idx], clave):
                max_idx = j
        lista[i], lista[max_idx] = lista[max_idx], lista[i]
    return lista

def insercion(lista, clave):
    for i in range(1, len(lista)):
        key = lista[i]
        j = i - 1
        while j >= 0 and getattr(lista[j], clave) < getattr(key, clave):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = key
    return lista

def mezcla(lista, clave):
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2
    left = mezcla(lista[:mid], clave)
    right = mezcla(lista[mid:], clave)
    return merge(left, right, clave)

def merge(left, right, clave):
    result = []
    while left and right:
        if getattr(left[0], clave) >= getattr(right[0], clave):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result
