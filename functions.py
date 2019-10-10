from PIL import Image, ImageFilter
import numpy as np
from itertools import product
import sys

class Pixel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Abre uma imagem
def abrir_imagem(nome_img):
    img = Image.open(nome_img)
    return img

def converter_para_escala_de_cinza(img):     
    return img.convert('L')

def binarizar_imagem(img):
    img = converter_para_escala_de_cinza(img)
    pix = img.load()
    
    for i in range(img.width):
        for j in range(img.height):
            if pix[i,j] >= 100:
                pix[i,j] = 255
            else:
                pix[i,j] = 0
    return img
    


#Imprime a matriz da imagem passada como parâmetro
def imprimir_matriz(img):
    print(np.asarray(img.convert('L')))


def dilatacao(img):
    pix = img.load()

    pixels_to_paint = []
    
    width, height = img.size
    for j, i in product(range(height-1), range(width-1)):
        if i > 0 and j > 0:
            if pix[i-1,j] == 255 or pix[i+1, j] == 255 or pix[i,j+1] == 255 or pix[i,j-1] == 255:
                pixels_to_paint.append(Pixel(i,j))
    
    for p in pixels_to_paint:
        # p = pixels_to_paint.pop()
        pix[p.x, p.y] = 255
    
    return img

def erosao(img):
    pix = img.load()

    pixels_to_paint = []
    
    width, height = img.size
    for j, i in product(range(height-1), range(width-1)):
        if i > 0 and j > 0:
            if pix[i-1,j] == 255 and pix[i+1, j] == 255 and pix[i,j+1] == 255 and pix[i,j-1] == 255:
                pixels_to_paint.append(Pixel(i,j))
    
    # for j, i in product(range(height), range(width)):
    #     pix[i,j] = 0
    
    for p in pixels_to_paint:
        # p = pixels_to_paint.pop()
        pix[p.x, p.y] = 0


    return img

def abertura(img):
    img = erosao(img)
    img = dilatacao(img)
    return img

def fechamento(img):
    #img = binarizar_imagem(img)
    img = dilatacao(img)
    img = erosao(img)
    return img

def extracaoContorno(img):
    new_img = Image.new('L', (img.width, img.height), color = 'black')
    imgOriginal = converter_para_escala_de_cinza(img)
    img = binarizar_imagem(img)
    imgErosao = erosao(img)
    pixOriginal = imgOriginal.load()
    pixErosao = imgErosao.load()
    pixNovo = new_img.load()

    for j in range(img.height):
        for i in range(img.width):
            pixNovo[i,j] = pixOriginal[i,j] - pixErosao[i,j]

    return new_img

def main(operacao, nome_da_imagem):
    
    # img = abrir_imagem('word.png')
    # img = abrir_imagem('Google_logo.png')
    # img = abrir_imagem('BolsoSimpson.jpg')

    img = abrir_imagem(nome_da_imagem)
    img = binarizar_imagem(img)
    img.show()

    if operacao == 'dilatacao':
        img = dilatacao(img)
    elif operacao == 'erosao':
        img = erosao(img)
    elif operacao == 'abertura':
        img = abertura(img)
    elif operacao == 'fechamento':
        img = fechamento(img)
    elif operacao == 'extracaoContorno':
        img = extracaoContorno(img)
    else:
        print("Algo deu errado!")
    img.show()
    
    
    

if __name__ == '__main__':
    # main()
    if len(sys.argv) < 3 or (sys.argv[1] != 'dilatacao' and sys.argv[1] != 'erosao' and sys.argv[1] != 'abertura' and sys.argv[1] != 'fechamento' and sys.argv[1] != 'extracaoContorno'):
        print("Execute assim: 'python dilatacao\&erosao.py dilatacao|erosao nomeDaImagem'")
    else:
        main(sys.argv[1], sys.argv[2])
