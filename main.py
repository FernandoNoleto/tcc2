from PIL import Image, ImageFilter, ImageEnhance
from itertools import product
import numpy as np


import cv2

queimada = (168, 28, 13) #vermelho
branco = (255,255,255, 255)
PONTOS = []

#limite inferior para a imagem de Palmas
LIMITE_INF_P = dict([('r',  1), ('g',  0), ('b', 28)]) 
#limite superior para a imagem de Palmas
LIMITE_SUP_P = dict([('r', 255), ('g', 112), ('b', 255)]) 

#limite inferior para o resto das imagens
LIMITE_INF_R = dict([('r',  80), ('g',  35), ('b', 110)]) 
#limite superior para a imagem de Palmas
LIMITE_SUP_R = dict([('r', 190), ('g', 132), ('b', 215)]) 

#Abre uma imagem
def abrir_imagem(nome_img):
    return Image.open(nome_img)

#Converte a imagem para escala de cinza
def escala_de_cinza(img):
    return img.convert('L')

def gerar_matriz (n_linhas, n_colunas):
    matriz = np.zeros((n_linhas, n_colunas), dtype=np.str)
    return matriz

def imprimir_matriz(matriz):
    print(np.asarray(matriz))

def matriz_da_imagem(img):
    return np.asarray(img.convert('L'))

def nova_imagem(img):
    new_img = Image.new('RGB', (img.width, img.height), color='black')
    # new_img.save('nova_imagem.png')
    # new_img.show()
    return new_img

def imprimir_valores(img):
    pix = img.load()
    width, height = img.size
    for y, x in product(range(height), range(width)):
        if pix[x,y] != 0:
            time.sleep(0.1)
        print("x: {}| y: {} = {}".format(x, y, pix[x,y]))

def mostrar_imagem(nome_img):
    call(["ristretto", nome_img])

#função auxiliar de modulo para calcular distancia
def distancia(valor1, valor2):
    if (valor1 >= valor2):
        return valor1-valor2
    else:
        return valor2-valor1




# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------




# Binarizar com regras
def encontrar_pixels_de_queimadas(img, segmentacao):
    pix = img.load()

    width, height = img.size
    # pixels_queimadas = []
    
    #Segmentacao de Palmas
    if segmentacao == 1:
        for y, x in product(range(height), range(width)):
            r,g,b = pix[x,y]
            if(r > LIMITE_INF_P.get('r') and r < LIMITE_SUP_P.get('r') and g > LIMITE_INF_P.get('g') and
               g < LIMITE_SUP_P.get('g') and b > LIMITE_INF_P.get('b') and b < LIMITE_SUP_P.get('b')):
               PONTOS.append((x,y))
    
    #Segmentacao do resto
    if segmentacao == 2:
        for y, x in product(range(height), range(width)):
            r,g,b = pix[x,y]
            if(r > LIMITE_INF_R.get('r') and r < LIMITE_SUP_R.get('r') and g > LIMITE_INF_R.get('g') and
            g < LIMITE_SUP_R.get('g') and b > LIMITE_INF_R.get('b') and b < LIMITE_SUP_R.get('b')):
                PONTOS.append((x,y))
    

    # crescimento_de_regiao(img)
    
    for pixel in PONTOS:
        x,y = pixel
        pix[x,y] = queimada
    

    return img

def diferenca(img):
    new_img = nova_imagem(img)
    pix  = img.load()
    pix2 = new_img.load()

    width, height = img.size
    
    for y, x in product(range(height), range(width)):
        if pix[x,y] == queimada:
            pix2[x,y] = (255,255,255)
        else:
            pix2[x,y] = (0,0,0)
    
    # new_img.save('diferenca.png')

    # img.show()


    return new_img

def area_de_queimada(img):
    pix = img.load()
    width, height = img.size
    qtd_pontos = 0
    
    for y, x in product(range(height), range(width)):
        # print ("pix[x,y] {}".format(pix[x,y]))
        if pix[x,y] == 255: # se for uma area detectada com regiao de queimada
            qtd_pontos +=1
            PONTOS.append([x,y])

    #cada pixel equivale a 73 metros²
    return qtd_pontos*7

def crescimento_de_regiao(img):
    
    pixels_acrescentados = 0
    width, height = img.size
    pix = img.load()  

    flag = 0
    #primeiro
    while 1:
        print("Limite superior: {}".format(LIMITE_SUP_P))
        print("Limite inferior: {}".format(LIMITE_INF_P))
        flag = 0
        for x,y in PONTOS:
            if(x > 0 and x < width-1 and y > 0 and y < height-1):
                r,g,b,a = pix[x+1,y]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x+1,y))
                    pixels_acrescentados+=1
                    flag = 1
                    print("Limite superior: {}".format(LIMITE_SUP_P))
                    print("Limite inferior: {}".format(LIMITE_INF_P))
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x+1,y))
                    pixels_acrescentados+=1
                    flag = 1
                    print("Limite superior: {}".format(LIMITE_SUP_P))
                    print("Limite inferior: {}".format(LIMITE_INF_P))
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x+1,y))
                    pixels_acrescentados+=1
                    flag = 1
                    print("Limite superior: {}".format(LIMITE_SUP_P))
                    print("Limite inferior: {}".format(LIMITE_INF_P))
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x+1,y))
                    pixels_acrescentados+=1
                    flag = 1
                    print("Limite superior: {}".format(LIMITE_SUP_P))
                    print("Limite inferior: {}".format(LIMITE_INF_P))
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x+1,y))
                    pixels_acrescentados+=1
                    flag = 1
                    print("Limite superior: {}".format(LIMITE_SUP_P))
                    print("Limite inferior: {}".format(LIMITE_INF_P))
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x+1,y))
                    pixels_acrescentados+=1
                    print("Limite superior: {}".format(LIMITE_SUP_P))
                    print("Limite inferior: {}".format(LIMITE_INF_P))
                
        

            
                r,g,b,a = pix[x,y+1]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                

        
            
                r,g,b,a = pix[x-1,y]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x-1,y))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x-1,y))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x-1,y))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x-1,y))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x-1,y))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x-1,y))
                    pixels_acrescentados+=1
                    flag = 1
                
            
        
                
                r,g,b,a = pix[x,y-1]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x,y-1))
                    pixels_acrescentados+=1
                    flag = 1
        
        
        
            
                r,g,b,a = pix[x+1,y+1]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x+1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x+1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x+1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x+1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x+1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x+1,y+1))
                    pixels_acrescentados+=1
                    flag = 1

                    

            
                r,g,b,a = pix[x+1,y-1]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x+1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x+1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x+1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x+1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x+1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x+1,y-1))
                    pixels_acrescentados+=1
                    flag = 1

        
        
            
                r,g,b,a = pix[x-1,y+1]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x-1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x-1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x-1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x-1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x-1,y+1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x-1,y+1))
                    pixels_acrescentados+=1
                    flag = 1



            
                r,g,b,a = pix[x-1,y-1]
                if(distancia(r, LIMITE_INF_P.get('r'))<= 5):
                    print("entrou no if r inferior")
                    limite_r = dict([('r', LIMITE_INF_P.get('r')-5)])
                    LIMITE_INF_P.update(limite_r)
                    PONTOS.append((x-1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para r
                if(distancia(r, LIMITE_SUP_P.get('r'))<= 5):
                    print("entrou no if r superior")
                    limite_r = dict([('r', LIMITE_SUP_P.get('r')+5)])
                    LIMITE_SUP_P.update(limite_r)
                    PONTOS.append((x-1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para g
                if(distancia(g, LIMITE_INF_P.get('g'))<= 5):
                    print("entrou no if g inferior")
                    limite_g = dict([('g', LIMITE_INF_P.get('g')-5)])
                    LIMITE_INF_P.update(limite_g)
                    PONTOS.append((x-1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para g
                if(distancia(g, LIMITE_SUP_P.get('g'))<= 5):
                    print("entrou no if g superior")
                    limite_g = dict([('g', LIMITE_SUP_P.get('g')+5)])
                    LIMITE_SUP_P.update(limite_g)
                    PONTOS.append((x-1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # reduzindo limite inferior para b
                if(distancia(b, LIMITE_INF_P.get('b'))<= 5):
                    print("entrou no if b inferior")
                    limite_b = dict([('b', LIMITE_INF_P.get('b')-5)])
                    LIMITE_INF_P.update(limite_b)
                    PONTOS.append((x-1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
                
                # aumentando limite superior para b
                if(distancia(b, LIMITE_SUP_P.get('b'))<= 5):
                    print("entrou no if b superior")
                    limite_b = dict([('b', LIMITE_SUP_P.get('b')+5)])
                    LIMITE_SUP_P.update(limite_b)
                    PONTOS.append((x-1,y-1))
                    pixels_acrescentados+=1
                    flag = 1
        
        
        print("pixels acrescentados: {}".format(pixels_acrescentados))
        print("flag = {}".format(flag))
        if flag == 0:
            break
        
    for p in PONTOS:
        x,y = p
        pix[x,y] = queimada
    
    # print("pixels acrescentados: {}".format(pixels_acrescentados))
        
    
    return img
    




def main():
    
    #para escolher o nome de imagem mude a string abaixo:
    nome="palmas2009.png"

    abertura = int(input("Digite a abertura: 1-5. Padrão: \'3\'"))
    segmentacao = int(input("Digite a segmentacao: 1-2. Padrão: \'1\'"))
    nome_imagem = "imagens-satelite/"+nome
    
    print("Nome image: {}".format(nome_imagem))
    print("Open par: {}".format(abertura))
    print("Segm par: {}".format(segmentacao))
    
    img = abrir_imagem(nome_imagem)
    img.save(nome)
    

    #pontos vermelhos
    img = encontrar_pixels_de_queimadas(img, segmentacao)
    img.save("segmentada-cores.png")


    #crescimento de regiao
    # img = crescimento_de_regiao(img)
    # img.save('crescimento.png')
    # img3.show()

    #pontos brancos
    img = diferenca(img) #pegando img3
    img.save('diferenca.png')
    
    #abertura
    img = cv2.imread('diferenca.png',0) #pegando img4
    kernel = np.ones((abertura,abertura),np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    
    #salvando imagem final
    nome = str(abertura)+str(segmentacao)+nome
    print("Nome local salvar: {}".format(nome))
    cv2.imwrite(nome, opening)
    


    ## -------------------------------- parte que usa flask ----------------------------------##

    # img5 = abrir_imagem(nome)
    # area = area_de_queimada(abrir_imagem(nome))
    # print("Area de queimada: {}m²".format(area))

    # cv2.imshow('iamge', opening)
    # cv2.waitKey(0)

    
    

    # return 'static/resultado_final.png'

    
    # mostrar_imagem(nome_imagem+"-segmentada"+".png")

if __name__ == '__main__':
    # print(LIMITE_SUP_P.get('b'))
    main()