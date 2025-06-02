def busquedaLineal(objetivo, lista, nombreDato, contador=0):
    """Linear search implementation (recursive)"""
    
    if len(lista) >= contador:  # Base case: reached end of list
        print("Target player not found")
        return None
    
    if getattr(lista[contador], nombreDato) == objetivo:  # Base case: target found
        return lista[contador]   
    
    # Recursive call with incremented counter
    return busquedaLineal(objetivo, lista, nombreDato, contador+1)


def busquedaBinaria(objetivo, lista, nombreDato):
    """Binary search implementation (recursive)"""
    valor = len(lista) // 2  # Get middle index
    
    if len(lista) < 1:  # Base case: empty list
        print("Data not found")
        return None
    
    if getattr(lista[valor], nombreDato) == objetivo:  # Base case: target found
        return lista[valor]
    
    # Determine which sublist to search next
    if objetivo < getattr(lista[valor], nombreDato):
        sublista = lista[0:valor]  # Search left half
    else:
        sublista = lista[valor+1:len(lista)]  # Search right half
    
    # Recursive call with new sublist
    return busquedaBinaria(objetivo, sublista, nombreDato)