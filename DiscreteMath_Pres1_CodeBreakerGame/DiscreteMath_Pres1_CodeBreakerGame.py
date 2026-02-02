import pygame  # Import the Pygame library
import csv
import os
import random

# Initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Code Breaker")
font = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 28)

# Settings
CSV_FileName = "questions.csv"
Total_Questions = 6
Tries_Per_Question = 2
Max_Wrong_Questions = 3

# ---------- Draw functions ----------
def draw_ClearBtn(rect, label, mouse_pos):
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
button_Clear = pygame.Rect(30, 120, 160, 60)  # "Submit" (we'll use as CLEAR for now)
button_Yes = pygame.Rect((30 + 5 * (60 + 10)), 380, 100, 60)
button_No = pygame.Rect((30 + 5 * (60 + 10)), 450, 100, 60)
button_Enter = pygame.Rect((140 + 5 * (60 + 10)), 380, 160, 130)

# ---------- Build numpad ----------
numpad_buttons = []  # list of (rect, label)
count = 0
x_pos = 30
y_pos = 380
btn_w = 60
btn_h = 60
gap = 10

for row in range(2):
    for col in range(5):
        rect = pygame.Rect(x_pos + col * (btn_w + gap),y_pos + row * (btn_h + gap), btn_w, btn_h)
        numpad_buttons.append((rect, str(count)))
        count += 1

# ---------- Build Hex Buttons -----------
hex_buttons = []
hex_labels = ["A","B","C","D","E","F"]
hex_y = y_pos + 2 * (btn_h + gap)

for i, lab in enumerate(hex_labels):
    rect = pygame.Rect(x_pos + i * (btn_w + gap), hex_y, btn_w, btn_h)
    hex_buttons.append((rect,lab))

# ---------- Load CSV ------------
def load_questions_from_csv(filename):
    questions = []
    if not os.path.exists(filename):
        return questions

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chapter = (row.get("chapter") or "").strip()
            question = (row.get("question") or "").strip()
            answer = (row.get("answer") or "").strip()
            if question and answer:
                questions.append({
                    "chapter": chapter,
                    "question": question,
                    "answer": answer
                })
    return questions

def six_questions(pool):
    if len(pool) >= Total_Questions:
        return random.sample(pool, Total_Questions)
    return [random.choice(pool) for _ in range(Total_Questions)]

def normalize(s):
    return s.strip().lower()

def check_answer(user_input, actual_answer):
    u = normalize(user_input)
    e = normalize(actual_answer)

    if e == "y":
        return u in ("y","yes")
    if e == "n":
        return u in ("n","no")
    return u == e

def wrap_text(text, max_chars = 34):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 > max_chars:
            lines.append(current)
            current = w
        else:
            current = w if current == "" else current + " " + w
    if current:
        lines.append(current)
    return lines

# ---------- Run State -----------
pool = load_questions_from_csv(CSV_FileName)
if not pool:
    # fallback so it runs even if CSV missing
    pool = [
        {"chapter": "1", "question": "type 47", "answer": "47"},
        {"chapter": "2", "question": "type 45", "answer": "45"},
        {"chapter": "3", "question": "press yes", "answer": "y"},
        {"chapter": "4", "question": "type 12", "answer": "12"},
        {"chapter": "5", "question": "type 41", "answer": "41"},
        {"chapter": "6", "question": "press no", "answer": "n"},
    ]

def restart_run():
    return {
        "questions_run": six_questions(pool),
        "q_index": 0,
        "tries_left": Tries_Per_Question,
        "wrong_questions": 0,
        "input_text": "",
        "message": "New run started!"
    }

state = restart_run()

def submit_answer(state, current):
    user = state["input_text"]
    expected = current["answer"]

    if check_answer(user, expected):
        state["message"] = "Correct!"
        state["q_index"] += 1
        state["tries_left"] = Tries_Per_Question
    else:
        state["tries_left"] -= 1
        if state["tries_left"] > 0:
            state["message"] = f"Wrong. {state['tries_left']} try left."
        else:
            state["wrong_questions"] += 1
            state["message"] = f"Wrong question! ({state['wrong_questions']}/{Max_Wrong_Questions})"
            state["q_index"] += 1
            state["tries_left"] = Tries_Per_Question

            # fail run after 3 wrong questions
            if state["wrong_questions"] >= Max_Wrong_Questions:
                state["message"] = "FAIL: 3 wrong questions. Restarting run..."
                return restart_run()

    state["input_text"] = ""

    # finished 6 questions -> restart run
    if state["q_index"] >= Total_Questions:
        state["message"] = "Run complete! Restarting..."
        return restart_run()

    return state

# ---------- Game state ----------
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    
    # Current Question
    questions_run = state["questions_run"]
    q_index = state["q_index"]
    current = questions_run[q_index]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Numpad clicks -> add digit
            for rect, label in numpad_buttons:
                if rect.collidepoint(event.pos):
                    state["input_text"] += label

            # Clear button (reusing Submit for now)
            if button_Clear.collidepoint(event.pos):
                state["input_text"] = ""
                state["message"] = "Cleared."

            # Enter button -> "submit"
            if button_Enter.collidepoint(event.pos):
                if button_Enter.collidepoint(event.pos):
                    state = submit_answer(state, current)
                    continue

            # YES/NO buttons -> append y/n
            if button_Yes.collidepoint(event.pos):
                state["input_text"] = "y"
                state = submit_answer(state, current)
                continue

            if button_No.collidepoint(event.pos):
                state["input_text"] = "n"
                state = submit_answer(state, current)
                continue

            # Hex buttons
            for rect, lab in hex_buttons:
                if rect.collidepoint(event.pos):
                    state["input_text"] += lab
                    break

    # Draw
    screen.fill((240, 240, 240))

    # Title
    title = font.render("Code Breaker", True, (0, 0, 0))
    screen.blit(title, (30, 30))
    
    # Status line
    status = f"Q {state['q_index']+1}/{Total_Questions}   Tries: {state['tries_left']}   Wrong: {state['wrong_questions']}/{Max_Wrong_Questions}"
    status_surf = font_small.render(status, True, (0, 0, 0))
    screen.blit(status_surf, (30, 85))

    # Chapter + question prompt
    chap = f"Chapter: {current['chapter']}" if current["chapter"] else "Chapter: -"
    chap_surf = font_small.render(chap, True, (0, 0, 0))
    screen.blit(chap_surf, (260, 120))

    q_lines = wrap_text(current["question"], max_chars=40)
    y = 150
    for line in q_lines[:5]:
        line_surf = font_small.render(line, True, (0, 0, 0))
        screen.blit(line_surf, (260, y))
        y += 28

    # show message
    msg_text = font.render(state["message"], True, (0, 0, 0))
    screen.blit(msg_text, (30, 220))

    # input display box
    pygame.draw.rect(screen, (255, 255, 255), (30, 270, 740, 60), border_radius=12)
    pygame.draw.rect(screen, (80, 80, 80), (30, 270, 740, 60), width=2, border_radius=12)
    input_render = font.render(state["input_text"], True, (0, 0, 0))
    screen.blit(input_render, (40, 285))

    # draw buttons
    draw_ClearBtn(button_Clear, "CLEAR", mouse_pos)

    for rect, label in numpad_buttons:
        draw_NumPad(rect, label, mouse_pos)
    
    for rect, lab in hex_buttons:
        draw_NumPad(rect, lab, mouse_pos)

    draw_YesBtn(button_Yes, "YES", mouse_pos)
    draw_NoBtn(button_No, "NO", mouse_pos)
    draw_EnterBtn(button_Enter, "ENTER", mouse_pos)


    pygame.display.flip()

pygame.quit()
