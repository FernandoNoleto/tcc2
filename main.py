from PIL import Image, ImageFilter, ImageEnhance
from itertools import product
import numpy as np


import cv2

queimada = (168, 28, 13, 255) #vermelho
branco = (255,255,255, 255)
PONTOS = []
# LIMITE_INF = dict([('r',  63), ('g',  63), ('b', 40)]) #original
# LIMITE_SUP = dict([('r', 114), ('g', 117), ('b', 99)]) #original

LIMITE_INF = dict([('r',  60), ('g',  50), ('b', 40)]) 
LIMITE_SUP = dict([('r', 114), ('g', 117), ('b', 99)]) 

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
            r,g,b,a = pix[x,y]
            if(r > LIMITE_INF.get('r') and r < LIMITE_SUP.get('r') and g > LIMITE_INF.get('g') and
               g < LIMITE_SUP.get('g') and b > LIMITE_INF.get('b') and b < LIMITE_SUP.get('b')):
               PONTOS.append((x,y))
    
    #Segmentacao do resto
    if segmentacao == 2:
        for y, x in product(range(height), range(width)):
            r,g,b,a = pix[x,y]
            if(r > 80 and r < 190 and g > 35 and g < 132 and b > 110 and b < 215):
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

    for x,y in PONTOS:
        if(x > 0 and x < width-1 and y > 0 and y < height-1):
            r,g,b,a = pix[x+1,y]
            if(distancia(r, LIMITE_INF.get('r'))<= 5):
                print("entrou no if r inferior")
                limite_r = dict([('r', LIMITE_INF.get('r')-5)])
                LIMITE_INF.update(limite_r)
                PONTOS.append((x+1,y))
                pixels_acrescentados+=1
            
            # aumentando limite superior para r
            if(distancia(r, LIMITE_SUP.get('r'))<= 5):
                print("entrou no if r superior")
                limite_r = dict([('r', LIMITE_SUP.get('r')+5)])
                LIMITE_SUP.update(limite_r)
                PONTOS.append((x+1,y))
                pixels_acrescentados+=1
            
            # reduzindo limite inferior para g
            if(distancia(g, LIMITE_INF.get('g'))<= 5):
                print("entrou no if g inferior")
                limite_g = dict([('g', LIMITE_INF.get('g')-5)])
                LIMITE_INF.update(limite_g)
                PONTOS.append((x+1,y))
                pixels_acrescentados+=1
            
            # aumentando limite superior para g
            if(distancia(g, LIMITE_SUP.get('g'))<= 5):
                print("entrou no if g superior")
                limite_g = dict([('g', LIMITE_SUP.get('g')+5)])
                LIMITE_SUP.update(limite_g)
                PONTOS.append((x+1,y))
                pixels_acrescentados+=1
            
            # reduzindo limite inferior para b
            if(distancia(b, LIMITE_INF.get('b'))<= 5):
                print("entrou no if b inferior")
                limite_b = dict([('b', LIMITE_INF.get('b')-5)])
                LIMITE_INF.update(limite_b)
                PONTOS.append((x+1,y))
                pixels_acrescentados+=1
            
            # aumentando limite superior para b
            if(distancia(b, LIMITE_SUP.get('b'))<= 5):
                print("entrou no if b superior")
                limite_b = dict([('b', LIMITE_SUP.get('b')+5)])
                LIMITE_SUP.update(limite_b)
                PONTOS.append((x+1,y))
                pixels_acrescentados+=1
            
    #-----------------------------------------------------------------------#
        
    for x,y in PONTOS:
        if(x > 0 and x < width-1 and y > 0 and y < height-1):
            r,g,b,a = pix[x,y+1]
            if(distancia(r, LIMITE_INF.get('r'))<= 5):
                print("entrou no if r inferior")
                limite_r = dict([('r', LIMITE_INF.get('r')-5)])
                LIMITE_INF.update(limite_r)
                PONTOS.append((x,y+1))
                pixels_acrescentados+=1
            
            # aumentando limite superior para r
            if(distancia(r, LIMITE_SUP.get('r'))<= 5):
                print("entrou no if r superior")
                limite_r = dict([('r', LIMITE_SUP.get('r')+5)])
                LIMITE_SUP.update(limite_r)
                PONTOS.append((x,y+1))
                pixels_acrescentados+=1
            
            # reduzindo limite inferior para g
            if(distancia(g, LIMITE_INF.get('g'))<= 5):
                print("entrou no if g inferior")
                limite_g = dict([('g', LIMITE_INF.get('g')-5)])
                LIMITE_INF.update(limite_g)
                PONTOS.append((x,y+1))
                pixels_acrescentados+=1
            
            # aumentando limite superior para g
            if(distancia(g, LIMITE_SUP.get('g'))<= 5):
                print("entrou no if g superior")
                limite_g = dict([('g', LIMITE_SUP.get('g')+5)])
                LIMITE_SUP.update(limite_g)
                PONTOS.append((x,y+1))
                pixels_acrescentados+=1
            
            # reduzindo limite inferior para b
            if(distancia(b, LIMITE_INF.get('b'))<= 5):
                print("entrou no if b inferior")
                limite_b = dict([('b', LIMITE_INF.get('b')-5)])
                LIMITE_INF.update(limite_b)
                PONTOS.append((x,y+1))
                pixels_acrescentados+=1
            
            # aumentando limite superior para b
            if(distancia(b, LIMITE_SUP.get('b'))<= 5):
                print("entrou no if b superior")
                limite_b = dict([('b', LIMITE_SUP.get('b')+5)])
                LIMITE_SUP.update(limite_b)
                PONTOS.append((x,y+1))
                pixels_acrescentados+=1
            

        #-----------------------------------------------------------------------#

            # if(distancia(pix[x-1,y], LIMITE_INF.get('r'))<= 5):
            #     limite_r = dict([('r', LIMITE_INF.get('r')-5)])
            #     LIMITE_INF.update(limite_r)
            #     PONTOS.append(x-1,y)
            
            # # aumentando limite superior para r
            # if(distancia(pix[x-1,y], LIMITE_SUP.get('r'))<= 5):
            #     limite_r = dict([('r', LIMITE_SUP.get('r')-5)])
            #     LIMITE_SUP.update(limite_r)
            #     PONTOS.append(x-1,y)
            
            # # reduzindo limite inferior para g
            # if(distancia(pix[x-1,y], LIMITE_INF.get('g'))<= 5):
            #     limite_g = dict([('g', LIMITE_INF.get('g')-5)])
            #     LIMITE_INF.update(limite_g)
            #     PONTOS.append(x-1,y)
            
            # # aumentando limite superior para g
            # if(distancia(pix[x-1,y], LIMITE_SUP.get('g'))<= 5):
            #     limite_g = dict([('g', LIMITE_SUP.get('g')-5)])
            #     LIMITE_SUP.update(limite_g)
            #     PONTOS.append(x-1,y)
            
            # # reduzindo limite inferior para b
            # if(distancia(pix[x-1,y], LIMITE_INF.get('b'))<= 5):
            #     limite_b = dict([('b', LIMITE_INF.get('b')-5)])
            #     LIMITE_INF.update(limite_b)
            #     PONTOS.append(x-1,y)
            
            # # aumentando limite superior para b
            # if(distancia(pix[x-1,y], LIMITE_SUP.get('b'))<= 5):
            #     limite_b = dict([('b', LIMITE_SUP.get('b')-5)])
            #     LIMITE_SUP.update(limite_b)
            #     PONTOS.append(x-1,y)
            
           
            # if(pix[x,y-1]):
            #     pass
            # if(pix[x,y-1]):
            #     pass
            # if(pix[x+1,y+1]):
            #     pass
            # if(pix[x+1,y-1]):
            #     pass
            # if(pix[x-1,y-1]):
            #     pass
        
    for p in PONTOS:
        x,y = p
        pix[x,y] = queimada
    
    print(pixels_acrescentados)
        
    
    return img
    




def main():
    abertura = int(input("Digite a abertura: 1-5. Padrão: \'3\'"))
    segmentacao = int(input("Digite a segmentacao: 1-2. Padrão: \'1\'"))
    nome_imagem = "area-queimada.png"
    
    print("Nome image: {}".format(nome_imagem))
    print("Open par: {}".format(abertura))
    print("Segm par: {}".format(segmentacao))
    
    img = abrir_imagem(nome_imagem)
    

    #pontos vermelhos
    img2 = encontrar_pixels_de_queimadas(img, segmentacao)
    img2.save("segmentada-cores.png")


    #crescimento de regiao
    img3 = crescimento_de_regiao(img)
    img3.save('crescimento.png')
    # img3.show()

    # #pontos brancos
    # img4 = diferenca(img3)
    # img4.save('diferenca.png')
    
    # #abertura
    # img5 = cv2.imread('diferenca.png',0)
    # kernel = np.ones((abertura,abertura),np.uint8)
    # opening = cv2.morphologyEx(img4, cv2.MORPH_OPEN, kernel)
    
    # #salvando imagem final
    # nome = str(abertura)+str(segmentacao)+nome_imagem
    # print("Nome local salvar: {}".format(nome))
    # cv2.imwrite(nome, opening)
    
    # img5 = abrir_imagem(nome)
    # area = area_de_queimada(abrir_imagem(nome))
    # print("Area de queimada: {}m²".format(area))

    # cv2.imshow('iamge', opening)
    # cv2.waitKey(0)

    
    

    # return 'static/resultado_final.png'

    
    # mostrar_imagem(nome_imagem+"-segmentada"+".png")

if __name__ == '__main__':
    # print(LIMITE_SUP.get('b'))
    main()