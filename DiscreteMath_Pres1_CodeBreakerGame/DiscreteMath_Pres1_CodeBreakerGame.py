import pygame # Import the Pygame library

# Initialization 
pygame.init() # Initialize Pygame

# Display setup
screen = pygame.display.set_mode((800, 600)) # Set the window size
pygame.display.set_caption("Code Breaker Game") # Set the window title
font = pygame.font.Font(None, 48) # Set the font and size

# Parameters
running = True # Main loop flag

# Main loop
while running: # Main loop
    for event in pygame.event.get():    # Event handling
        if event.type == pygame.QUIT:   # Quit event
            running = False             # Exit the main loop
            
    screen.fill((240,240,240))  # Fill the screen with a light gray color   
    pygame.display.flip()       # Update the display
 
# Close Game    
pygame.quit()   # Quit Pygame