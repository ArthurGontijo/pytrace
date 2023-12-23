## Funcionamento do Programa

Todas as imagens contidas na pasta input serão vetorizadas e salvas na pasta output. 

O argv serve para informar qual tipo de imagem está sendo processada:
    
    - 0 para imagens reais
    - 1 para desenhos/blueprints

## Vetorização de Blueprints

```python
python ./main.py 1
```
### Imagem Original
![](./input/march.jpg)

### Imagem Vetorizada
![](./output/march.svg)

## Vetorização de Images Reais

```python
python ./main.py 0
```
### Imagem Original
![](./input/gol.jpg)

### Imagem Vetorizada.
![](./output/gol.svg)