import os
import sys
import cv2
import numpy as np
from colorama import Fore
from potrace import Bitmap
from frr import FastReflectionRemoval


def get_edges_drawings(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
    diff = cv2.absdiff(dilate, thresh)

    edges = 255 - diff

    return edges


def get_edges_real_images(img):
    y, x = img.shape[0:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)
    edges = cv2.Canny(blurred, 20, 50)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_image = np.full((y, x), 255, dtype=np.uint8)
    
    cv2.drawContours(contour_image, contours, -1, (0, 0, 0), 2)

    return contour_image


def save_svg(edges, filename):
    y, x = edges.shape

    bitmap = Bitmap(edges)

    path = bitmap.trace()
    with open(f'./output/{filename}.svg', 'w') as fp:
        fp.write(
            f'''<svg version='1.1' xmlns='http://xw.w3.org/2000/svg' xmlns:xlink='http://xw.w3.org/1999/xlink' width='{x}' height='{y}' viewBox='0 0 {x} {y}'>''')
        parts = []
        for curve in path:
            fs = curve.start_point
            parts.append(f'M{fs.x},{fs.y}')
            for segment in curve.segments:
                if segment.is_corner:
                    a = segment.c
                    b = segment.end_point
                    parts.append(f'L{a.x},{a.y}L{b.x},{b.y}')
                else:
                    a = segment.c1
                    b = segment.c2
                    c = segment.end_point
                    parts.append(f'C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}')
            parts.append('z')
        fp.write(f'''<path stroke='none' fill='black' fill-rule='evenodd' d='{''.join(parts)}'/>''')
        fp.write('</svg>')


def main():
    files = os.listdir('./input')
    total_files = len(files)

    for i, file in enumerate(files):
        filename = file.split('.')[0]
        print(f'{Fore.YELLOW} Processando {file} ({i}/{total_files}) ...', end='', flush=True)

        img = cv2.imread(f'./input/{file}')
        
        if len(sys.argv) == 1 or sys.argv[1] == '0':
            alg = FastReflectionRemoval(h = 0.15)
            img = alg.remove_reflection(img/255.0)
            img = (img * 255).astype(np.uint8)

            edges = get_edges_real_images(img)
        
        elif sys.argv[1] == '1':
            edges = get_edges_drawings(img)

        else:
            print(f'{Fore.RED}Opção Inválida')
            break

        save_svg(edges, filename)

        print(f'\r{Fore.GREEN} Imagem {file} processada com sucesso ({i + 1}/{total_files})', flush=True)
    
    print(f'{Fore.GREEN} Todas as imagens foram processadas!')


if __name__ == '__main__':
    main()