# Example file showing a circle moving on screen
import math
import random
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280//2, 720//2))
clock = pygame.time.Clock()
running = True
dt = 0
gravity = pygame.Vector2(0, 0.1)


def vector_abs(v):
    return pygame.Vector2(abs(v.x), abs(v.y))

def vector_pow(v, e):
    return pygame.Vector2(v.x**e, v.y**e)

def vector_mult(v1, v2):
    return pygame.Vector2(v1.x * v2.x, v1.y * v2.y)

def vector_div(v1, v2):
    return pygame.Vector2(v1.x / v2.x, v1.y / v2.y)


class Particle:
    def __init__(self, x, y, vx, vy, m, color = "blue"):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(vx, vy)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = m
        self.r = math.sqrt(self.mass) * 20
        self.color = color


    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0


    def edges(self):
        if self.position.x > screen.get_width() - self.r:
            self.position.x = screen.get_width() - self.r
            self.velocity.x *= -1

        elif self.position.x < self.r:
            self.position.x = self.r
            self.velocity.x *= -1

        if self.position.y > screen.get_height() - self.r:
            self.position.y = screen.get_height() - self.r
            self.velocity.y *= -1

        elif self.position.y < self.r:
            self.position.y = self.r
            self.velocity.y *= -1


    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, self.r)
    
    
    def apply_force(self, force):
        self.acceleration += force

    
    def collide(self, particle):
        return self.position.distance_to(particle.position) < self.r + particle.r
    
    
    def resolve_collision(self, particle):
        distance = self.position.distance_to(particle.position)
        normal = (particle.position - self.position).normalize()
        overlap = (self.r + particle.r) - distance
        if overlap > 0:
            correction = normal * overlap * 0.5  # 0.5 for equal separation
            self.position -= correction
            particle.position += correction
            distance = self.r + particle.r

        # calculating self.velocity
        velocity_diff = particle.velocity - self.velocity
        position_diff = particle.position - self.position
        numerator = (2*particle.mass) * velocity_diff.dot(position_diff) 
        denominator = (self.mass + particle.mass) * distance * distance
        self.velocity += position_diff * (numerator/denominator)

        # calculating particle.velocity
        velocity_diff *= -1
        position_diff *= -1
        numerator = (2*self.mass) * velocity_diff.dot(position_diff) 
        particle.velocity += position_diff * (numerator/denominator)




blue_particles = [Particle(random.randrange(1, 600), random.randrange(1, 300), -1, -3, .2) for _ in range(30)]
red_particles = [Particle(random.randrange(1, 600), random.randrange(1, 300), -1, -3, .2, "red") for _ in range(30)]
particles = blue_particles + red_particles

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    #p.apply_force(gravity)
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i] 
            p2 = particles[j]
            if p2 != p1 and p1.collide(p2):
                p1.resolve_collision(p2)

    #total_k_energy = 0
    for p in particles:
        p.update()
        p.edges()
        p.draw()
        p.apply_force(gravity)
        #total_k_energy += 0.5 * p.mass * p.velocity.magnitude()**2

    #print(total_k_energy)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()