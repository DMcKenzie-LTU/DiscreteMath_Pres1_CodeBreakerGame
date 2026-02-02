import pygame  # Import the Pygame library

# Initialization
pygame.init()

# Display setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Code Breaker Game")
font = pygame.font.Font(None, 48)

# ---------- Draw functions ----------
def draw_button(rect, label, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    bg = (220, 220, 220) if hovered else (200, 200, 200)
    pygame.draw.rect(screen, bg, rect, border_radius=12)
    pygame.draw.rect(screen, (80, 80, 80), rect, width=2, border_radius=12)
    text = font.render(label, True, (20, 20, 20))
    screen.blit(text, text.get_rect(center=rect.center))

def draw_NumPad(rect, label, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    bg = (0, 255, 0) if hovered else (0, 200, 0)
    pygame.draw.rect(screen, bg, rect, border_radius=12)
    pygame.draw.rect(screen, (40, 40, 0), rect, width=2, border_radius=12)
    text = font.render(label, True, (20, 20, 20))
    screen.blit(text, text.get_rect(center=rect.center))

def draw_YesBtn(rect, label, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    bg = (0, 0, 255) if hovered else (0, 0, 200)
    pygame.draw.rect(screen, bg, rect, border_radius=12)
    pygame.draw.rect(screen, (0, 0, 80), rect, width=2, border_radius=12)
    text = font.render(label, True, (20, 20, 20))
    screen.blit(text, text.get_rect(center=rect.center))

def draw_NoBtn(rect, label, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    bg = (255, 0, 0) if hovered else (200, 0, 0)
    pygame.draw.rect(screen, bg, rect, border_radius=12)
    pygame.draw.rect(screen, (80, 0, 0), rect, width=2, border_radius=12)
    text = font.render(label, True, (20, 20, 20))
    screen.blit(text, text.get_rect(center=rect.center))

def draw_EnterBtn(rect, label, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    bg = (255, 255, 0) if hovered else (200, 200, 0)
    pygame.draw.rect(screen, bg, rect, border_radius=12)
    pygame.draw.rect(screen, (80, 80, 0), rect, width=2, border_radius=12)
    text = font.render(label, True, (20, 20, 20))
    screen.blit(text, text.get_rect(center=rect.center))

# ---------- UI Rectangles ----------
button_rect = pygame.Rect(30, 120, 160, 60)  # "Submit" (we'll use as CLEAR for now)
button_Yes = pygame.Rect((30 + 5 * (60 + 10)), 380, 100, 60)
button_No = pygame.Rect((30 + 5 * (60 + 10)), 450, 100, 60)
button_Enter = pygame.Rect((140 + 5 * (60 + 10)), 380, 160, 130)

# ---------- Build numpad ONCE ----------
numpad_buttons = []  # list of (rect, label)
count = 0
x_pos = 30
y_pos = 380
btn_w = 60
btn_h = 60
gap = 10

for row in range(2):
    for col in range(5):
        rect = pygame.Rect(
            x_pos + col * (btn_w + gap),
            y_pos + row * (btn_h + gap),
            btn_w,
            btn_h
        )
        numpad_buttons.append((rect, str(count)))
        count += 1

# ---------- Game state ----------
message = "Click numpad to type"
input_text = ""  # what the player is "entering"

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Numpad clicks -> add digit
            for rect, label in numpad_buttons:
                if rect.collidepoint(event.pos):
                    input_text += label

            # Clear button (reusing Submit for now)
            if button_rect.collidepoint(event.pos):
                input_text = ""
                message = "Cleared."

            # Enter button -> "submit"
            if button_Enter.collidepoint(event.pos):
                message = f"You entered: {input_text}"
                # Later this is where we check answers
                input_text = ""

            # YES/NO buttons -> append y/n
            if button_Yes.collidepoint(event.pos):
                input_text += "y"
            if button_No.collidepoint(event.pos):
                input_text += "n"

    # Draw
    screen.fill((240, 240, 240))

    title = font.render("Code Breaker", True, (0, 0, 0))
    screen.blit(title, (30, 30))

    # show message
    msg_text = font.render(message, True, (0, 0, 0))
    screen.blit(msg_text, (30, 220))

    # input display box
    pygame.draw.rect(screen, (255, 255, 255), (30, 270, 740, 60), border_radius=12)
    pygame.draw.rect(screen, (80, 80, 80), (30, 270, 740, 60), width=2, border_radius=12)
    input_render = font.render(input_text, True, (0, 0, 0))
    screen.blit(input_render, (40, 285))

    # draw buttons
    draw_button(button_rect, "CLEAR", mouse_pos)

    for rect, label in numpad_buttons:
        draw_NumPad(rect, label, mouse_pos)

    draw_YesBtn(button_Yes, "YES", mouse_pos)
    draw_NoBtn(button_No, "NO", mouse_pos)
    draw_EnterBtn(button_Enter, "ENTER", mouse_pos)

    pygame.display.flip()

pygame.quit()
