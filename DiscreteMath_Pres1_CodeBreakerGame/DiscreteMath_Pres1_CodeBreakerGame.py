from telnetlib import GA
import pygame # Import the Pygame library

# Initialization 
pygame.init() # Initialize Pygame

# Display setup
screen = pygame.display.set_mode((800, 600)) # Set the window size
pygame.display.set_caption("Code Breaker Game") # Set the window title
font = pygame.font.Font(None, 48) # Set the font and size

# Definitions
def draw_button(rect, label, mouse_pos):    # Function to draw a button
    hovered = rect.collidepoint(mouse_pos)  # Check if mouse is over the button
    bg = (220, 220, 220) if hovered else (200, 200, 200)    # Button background color
    pygame.draw.rect(screen, bg, rect, border_radius = 12)  # Draw button background
    pygame.draw.rect(screen,(80, 80, 80), rect, width = 2, border_radius = 12)  # Draw button border
    text = font.render(label, True, (20, 20, 20))   # Render button label
    screen.blit(text, text.get_rect(center = rect.center))  # Draw button label

def draw_NumPad(rect, label, mouse_pos):    # Function to draw a number pad button
    hovered = rect.collidepoint(mouse_pos)  # Check if mouse is over the button
    bg = (0, 255, 0) if hovered else (0, 200, 0)    # Button background color
    pygame.draw.rect(screen, bg, rect, border_radius = 12)  # Draw button background
    pygame.draw.rect(screen,(40, 40, 0), rect, width = 2, border_radius = 12)  # Draw button border
    text = font.render(label, True, (20, 20, 20))   # Render button label
    screen.blit(text, text.get_rect(center = rect.center))  # Draw button label

# Main Loop
button_NumPad = pygame.Rect(30, 300, 60, 60) # Define number pad button rectangle
button_rect = pygame.Rect(30, 120, 160, 60) # Define button rectangle
message = "Click the Button"    # Button label
running = True # Main loop flag
while running: # Main loop
    mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
    for event in pygame.event.get():    # Event handling
        if event.type == pygame.QUIT:   # Quit event
            running = False             # Exit the main loop
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button click
            if button_rect.collidepoint(event.pos): # Check if click is within button
                message = "Button Clicked!" # Update message on button click
            
    screen.fill((240,240,240))  # Fill the screen with a light gray color
    title = font.render("Code Breaker", True, (0, 0, 0)) # Render the title text
    screen.blit(title, (30, 30)) # Draw the title on the screen
    
    draw_button(button_rect, "Submit", mouse_pos) # Draw the button
    msg_text = font.render(message, True, (0,0,0)) # Render the message text
    screen.blit(msg_text, (30, 220)) # Draw the message on the screen
    
    count = 0
    x_pos = 30
    y_pos = 380
    btn_w = 60
    btn_h = 60
    gap = 10
    for y in range(2):          # Draw number pad buttons
        for x in range(5):
            rect = pygame.Rect(x_pos + x * (btn_w + gap),y_pos + y * (btn_h + gap), btn_w, btn_h)
            draw_NumPad(rect, str(count), mouse_pos) # Draw number pad button
            count += 1
            
    pygame.display.flip()       # Update the display
 
# Close Game    
pygame.quit()   # Quit Pygame