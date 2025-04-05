from pygame import Vector2
import pygame
import utils
G = utils.G

screen = pygame.display.set_mode((1280, 1280))
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000

class Particle:
    def __init__(self, x, y, vx, vy, m, r, color = "blue"):
        self.position = Vector2(x, y)
        self.velocity = Vector2(vx, vy)
        self.acceleration = Vector2(0, 0)
        self.mass = m
        self.r = r
        self.color = color


    def update(self):
        self.velocity += self.acceleration * dt
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
        self.acceleration += force / self.mass


    def apply_newtonian_gravity(self, particle):
        direction = particle.position - self.position
        distance = self.position.distance_to(particle.position)
        f_magnitude = G * ((self.mass * particle.mass) / distance ** 2)
        f  = direction.normalize() * f_magnitude
        self.apply_force(f)
        particle.apply_force(-f)

    
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