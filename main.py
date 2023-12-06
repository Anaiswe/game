import tkinter as tk

class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.hungry = 0
        self.humor = 100
        self.body_color = "white"
        self.eyes_color = "black"
        self.nose_color = "brown"
        self.eyes_open = True
        self.position_x = 100
        self.direction = 1
        self.legs_up = False
        self.whisker_length = 30
        self.normal_state = True

    def feed(self):
        if self.hungry >= 20:
            self.hungry -= 20
            self.humor += 10
            self.health += 5
        else:
            print(f"{self.name} is not hungry!")

    def play(self):
        self.humor += 20
        self.hungry += 10
        self.health -= 5
        self.normal_state = False  # Transition to "rolling up" state
        dessiner_personnage()
        fenetre.after(3000, self.return_to_normal_state)  # Return to normal state after 3000 ms (3 seconds)

    def pass_time(self):
        self.hungry += 5
        self.health -= 2
        self.humor -= 2

    def is_dead(self):
        return self.health <= 0 or self.hungry >= 100 or self.humor <= 0

    def walk(self):
        self.position_x += 5 * self.direction
        self.direction *= -1
        self.legs_up = not self.legs_up
        dessiner_personnage()
        fenetre.after(500, self.walk)  # Call the walk function every 500 ms

    def return_to_normal_state(self):
        self.normal_state = True
        dessiner_personnage()

def blink_eyes():
    pet.eyes_open = not pet.eyes_open
    dessiner_personnage()
    delay = 300 if pet.eyes_open else 100
    fenetre.after(delay, blink_eyes)

def feed_pet():
    pet.feed()
    update_ui()

def play_with_pet():
    pet.play()
    update_ui()

def pass_time():
    pet.pass_time()
    update_ui()
    if pet.is_dead():
        game_over_label.config(text=f"{pet.name} is in pet heaven...")

def update_ui():
    name_label.config(text=f"Name: {pet.name}")
    health_label.config(text=f"Health: {pet.health}")
    hungry_label.config(text=f"Hungry: {pet.hungry}")
    humor_label.config(text=f"Humor: {pet.humor}")

    if pet.is_dead():
        game_over_label.config(text=f"{pet.name} is in pet heaven...")

    dessiner_personnage()

def dessiner_personnage():
    canvas.delete("character")
    x, y = pet.position_x, 200
    size = 60

    # Light blue background
    canvas.create_rectangle(0, 0, 300, 300, fill="lightblue")

    if pet.normal_state:
        # Body
        canvas.create_oval(x, y, x + size, y + size, fill=pet.body_color, tags="character")

        # Eyes
        size_eyes = 20
        eyes_offset = size // 3
        for i in range(2):
            pos_x = x + eyes_offset * (i + 1) - size_eyes / 2
            pos_y = y + size // 3

            if pet.eyes_open:
                # Open eyes
                canvas.create_oval(pos_x, pos_y, pos_x + size_eyes, pos_y + size_eyes, fill=pet.eyes_color, tags="character")
                # White spot in the eyes
                canvas.create_oval(pos_x + 5, pos_y + 5, pos_x + 10, pos_y + 10, fill="white", tags="character")
            else:
                # Closed eyes
                canvas.create_rectangle(pos_x, pos_y + size_eyes // 2, pos_x + size_eyes, pos_y + size_eyes // 2 + 5, fill=pet.eyes_color, tags="character")

        # Nose (inverted triangle)
        points = [x + size // 2, y + size // 2,
                  x + size // 2 - 5, y + size // 2 + 10,
                  x + size // 2 + 5, y + size // 2 + 10]
        canvas.create_polygon(points, fill=pet.nose_color, tags="character")

        # Whiskers
        whisker_length = pet.whisker_length
        for i in [-1, 1]:
            start_x = x + size // 2 + i * 10
            start_y = y + size // 2 + 10
            canvas.create_line(start_x, start_y, start_x + i * whisker_length, start_y - 5, fill="black", tags="character")
            canvas.create_line(start_x, start_y, start_x + i * whisker_length, start_y, fill="black", tags="character")
            canvas.create_line(start_x, start_y, start_x + i * whisker_length, start_y + 5, fill="black", tags="character")

        # Legs
        legs_offset = size // 4
        legs_size = 15
        for i in range(2):
            pos_x = x + legs_offset * (i + 1)
            pos_y = y + size
            if pet.legs_up:
                pos_y += 5  # Simulate leg movement
            canvas.create_oval(pos_x, pos_y, pos_x + legs_size, pos_y + legs_size, fill=pet.body_color, tags="character")
    else:
        # When not in normal state (rolling up)
        canvas.create_oval(x, y + 20, x + size, y + size - 20, fill=pet.body_color, tags="character")
        canvas.create_text(x + size // 2, y + size // 2, text="^^", font=("Arial", 20, "bold"), fill="black", tags="character")

pet = VirtualPet("Virtual Pet")

fenetre = tk.Tk()
fenetre.title("Virtual Pet")

name_label = tk.Label(fenetre, text=f"Name: {pet.name}")
health_label = tk.Label(fenetre, text=f"Health: {pet.health}")
hungry_label = tk.Label(fenetre, text=f"Hungry: {pet.hungry}")
humor_label = tk.Label(fenetre, text=f"Humor: {pet.humor}")

feed_button = tk.Button(fenetre, text="Feed", command=feed_pet)
play_button = tk.Button(fenetre, text="Play", command=play_with_pet)
pass_time_button = tk.Button(fenetre, text="Pass Time", command=pass_time)

game_over_label = tk.Label(fenetre, text="")

name_label.pack()
health_label.pack()
hungry_label.pack()
humor_label.pack()
feed_button.pack()
play_button.pack()
pass_time_button.pack()
game_over_label.pack()

canvas = tk.Canvas(fenetre, width=300, height=300, bg='white')
canvas.pack()

update_ui()
blink_eyes()
pet.walk()  # Automatically make the pet walk

fenetre.mainloop()
