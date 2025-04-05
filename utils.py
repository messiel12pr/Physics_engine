from pygame import Vector2

G = 1
gravity_vector = Vector2(0, 5)

def vector_abs(v):
    return Vector2(abs(v.x), abs(v.y))

def vector_pow(v, e):
    return Vector2(v.x**e, v.y**e)

def vector_mult(v1, v2):
    return Vector2(v1.x * v2.x, v1.y * v2.y)

def vector_div(v1, v2):
    return Vector2(v1.x / v2.x, v1.y / v2.y)