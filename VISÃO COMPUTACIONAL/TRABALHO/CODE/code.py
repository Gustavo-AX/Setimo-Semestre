import cv2

import numpy as np

from matplotlib import pyplot as plt


# 1. Leitura da imagem

img = cv2.imread('../IMAGES/synthetic_045_images/20GRAY.tif')

img_original = img.copy()


# 2. Conversão para escala de cinza

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# 3. Suavização para redução de ruído

blur = cv2.GaussianBlur(gray, (5, 5), 0)


# 4. Binarização adaptativa

ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


# 5. Operações morfológicas

kernel = np.ones((3, 3), np.uint8)

opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)


#======================================================================


# 6. Transformada da distância

dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)

dist_norm = cv2.normalize(dist_transform, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


# 7. Threshold nos picos da transformada

"""ret, sure_fg = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)

sure_fg = np.uint8(sure_fg)"""

value = np.percentile(dist_transform[dist_transform > 0], 95)  # só valores > 0
ret, sure_fg = cv2.threshold(dist_transform, value, 255, 0)
sure_fg = np.uint8(sure_fg)


# 8. Background certo com dilatação

sure_bg = cv2.dilate(closing, kernel, iterations=3)


# 9. Regiões de incerteza

unknown = cv2.subtract(sure_bg, sure_fg)


# 10. Rotulagem dos marcadores

ret, markers = cv2.connectedComponents(sure_fg)


# Ajustar rótulos: fundo = 1, células ≥ 2

markers = markers + 1


# Áreas de incerteza marcadas como 0

markers[unknown == 255] = 0


# 11. Aplicar Watershed (modifica a imagem original!)

markers_ws = cv2.watershed(img, markers.copy())

output = img.copy()

output[markers_ws == -1] = [0, 0, 255]  # bordas vermelhas



# 12. Contagem de células

# Pegamos os rótulos únicos, ignorando fundo (1) e bordas (-1)

unique_labels = np.unique(markers)

num_cells = len(unique_labels[(unique_labels > 1)])


print(f"Total de células detectadas: {num_cells}")

# 13. Colorir cada célula detectada com uma cor diferente
color_map = np.zeros_like(img)

for label in np.unique(markers_ws):
    if label <= 1:
        continue  

    mask = markers_ws == label

    color = np.random.randint(0, 255, size=3, dtype=np.uint8)

    color_map[mask] = color

color_map[markers_ws == -1] = [0, 0, 255]


# 14. Visualização das etapas

plt.figure(figsize=(16, 10))


plt.subplot(2, 4, 1)

plt.title("1. Original")

plt.imshow(cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB))

plt.axis('off')


plt.subplot(2, 4, 2)

plt.title("2. Escala de Cinza")

plt.imshow(gray, cmap='gray')

plt.axis('off')


plt.subplot(2, 4, 3)

plt.title("3. Binarização Otsu")

plt.imshow(thresh, cmap='gray')

plt.axis('off')


plt.subplot(2, 4, 4)

plt.title("4. Pós-Morfologia")

plt.imshow(closing, cmap='gray')

plt.axis('off')


plt.subplot(2, 4, 5)

plt.title("5. Transformada Distância")

plt.imshow(dist_norm, cmap='gray')

plt.axis('off')


plt.subplot(2, 4, 6)

plt.title("6. Foreground (sure_fg)")

plt.imshow(sure_fg, cmap='gray')

plt.axis('off')


plt.subplot(2, 4, 7)

plt.title("7. Resultado Watershed")

plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))

plt.axis('off')

plt.subplot(2, 4, 8)
plt.title("8. Células Coloridas")
plt.imshow(cv2.cvtColor(color_map, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.tight_layout()
plt.show() 
