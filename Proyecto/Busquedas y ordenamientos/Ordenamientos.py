def bubbleSort(lista):
    for x in range(0,len(lista)-1): ##cada iteracion de estas se encarga de recorrer toda la lista y subir un unico numero desde abajo hasta arriba
        for j in range(0,len(lista)-1):
            if lista[j]>lista[j+1]:##en cada iteracion de esta se mira el numero contiguo y en el condicional si es mayor se intercambia en la lista
                aux=lista[j+1]   
                lista[j+1]=lista[j]
                lista[j]=aux
                
    return lista
        
def selectionSort(lista):
    
    for x in range(0,len(lista)):## en este ciclo se lleva la cuenta de la posicion de ordenamiento
        menor=lista[x]  ## aqui me aseguro de que el menor nunca sera el menor encontrado en el ciclo anterior
        for j in range(x,len(lista)):##en este ciclo encuentro el numero menor, en un rango que no incluye el numero menor anterior
            if lista[j]<menor:
                menor=lista[j]
                                ## guardo la posicion en donde tengo que intercambiar el menor con el numero no ordenado
                aux=j
        if lista[x]!=menor:
            lista[aux]=lista[x] ##actualizo la lista si es el caso, osea cuando el numero no ordenado y el menor no estan en la misma posicion
            lista[x]=menor
            print(lista)
    return lista

print(selectionSort([5,4,3,2,1,-2]))