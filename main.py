import os
import cv2
import numpy as np
from colorama import Fore
from potrace import Bitmap


def get_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
    diff = cv2.absdiff(dilate, thresh)

    edges = 255 - diff

    return edges


def save_svg(edges, filename):
    y, x = edges.shape

    bitmap = Bitmap(edges)

    path = bitmap.trace()
    with open(f'./output/{filename}.svg', 'w') as fp:
        fp.write(
            f'''<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='{x}' height='{y}' viewBox='0 0 {x} {y}'>''')
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

        edges = get_edges(img)
        save_svg(edges, filename)

        print(f'\r{Fore.GREEN} Imagem {file} processada com sucesso ({i + 1}/{total_files})', flush=True)
    
    print(f'{Fore.GREEN} Todas as imagens foram processadas!')


if __name__ == '__main__':
    main()