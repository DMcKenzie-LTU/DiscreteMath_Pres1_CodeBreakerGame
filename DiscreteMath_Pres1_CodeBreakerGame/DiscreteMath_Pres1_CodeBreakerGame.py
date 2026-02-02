import pygame # Import the Pygame library

# Initialization 
pygame.init() # Initialize Pygame

# Display setup
screen = pygame.display.set_mode((800, 600)) # Set the window size
pygame.display.set_caption("Code Breaker Game") # Set the window title
font = pygame.font.Font(None, 48) # Set the font and size

# Main Loop
running = True # Main loop flag
while running: # Main loop
    for event in pygame.event.get():    # Event handling
        if event.type == pygame.QUIT:   # Quit event
            running = False             # Exit the main loop
            
    screen.fill((240,240,240))  # Fill the screen with a light gray color
    title = font.render("Code Breaker", True, (0, 0, 0)) # Render the title text
    screen.blit(title, (30, 30)) # Draw the title on the screen
    
    pygame.display.flip()       # Update the display
 
# Close Game    
pygame.quit()   # Quit Pygame