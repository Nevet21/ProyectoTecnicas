def busquedaLineal(objetivo,lista,nombreDato,contador=0):
    
    if len(lista)>=contador:## caso limite,  si sse llega al final de la lista se termina el llamado recursivvo
        print("El jugador objetivo no existe")
        return None
    
    if getattr(lista[contador], nombreDato) == objetivo: ## getAttr me permite volver la funcion mas dinamica para todos los atributos de ese objeto
        return lista[contador]   ##caso Base cuando en la lista se encuentra el obejtivo se finaliza el llamado recursivo
    
    
    
    return busquedaLineal(objetivo,lista,nombreDato, contador+1) ## llamada recursiva incrementando en 1 el contador para una nueva busqueda


def busquedaBinaria(objetivo,lista,nombreDato):
    valor=len(lista)//2 ##se busca el valor de la mitad de la lista
    
    if len(lista)<1:
        print("no se encontro el dato")  ## caso limite cuando la lista essta vacia
        return None
    
    if getattr(lista[valor], nombreDato)== objetivo: ##  caso base cuando encontramos el valor objetivo
        return lista[valor]
    
    if objetivo < getattr(lista[valor],nombreDato):   ## se mira si se divide la lissta izquierda o derecha dependiendo si valor es mayor o menor a objetivo
        sublista=lista[0:valor] 
    else:
        sublista=lista[valor+1:len(lista)]
    
    return busquedaBinaria(objetivo,sublista,nombreDato)

    
    