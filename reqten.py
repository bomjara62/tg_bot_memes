import numpy as np
import cv2

txt = str(input())

# Создание пустого изображения
image = cv2.imread(r'4.png', )


# Задание координат и размеров прямоугольника
x, y = 250, 100
width, height = 250, 125

# Задание радиуса закругления углов
borderRadius = 20

# Рисование прямоугольника с закругленными углами
cv2.rectangle(image, (x + borderRadius, y), (x + width - borderRadius, y + height), (255, 255, 255), -1)
cv2.rectangle(image, (x, y + borderRadius), (x + width, y + height - borderRadius), (255, 255, 255), -1)
cv2.ellipse(image, (x + borderRadius, y + borderRadius), (borderRadius, borderRadius), 180, 0, 90, (255, 255, 255), -1)
cv2.ellipse(image, (x + width - borderRadius, y + borderRadius), (borderRadius, borderRadius), 270, 0, 90, (255, 255, 255), -1)
cv2.ellipse(image, (x + width - borderRadius, y + height - borderRadius), (borderRadius, borderRadius), 0, 0, 90, (255, 255, 255), -1)
cv2.ellipse(image, (x + borderRadius, y + height - borderRadius), (borderRadius, borderRadius), 90, 0, 90, (255, 255, 255), -1)

cv2.putText(image, f"{txt}", (260, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 255), 2)

#img = np.full((300, 400, 3), 255, dtype=np.uint8)

cv2.imwrite('image11.png', image)

cv2.waitKey(0)
cv2.destroyAllWindows()