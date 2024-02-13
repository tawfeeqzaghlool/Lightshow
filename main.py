from machine import Pin
import time
import random

# Seed the random number generator (adjust as needed)
random.seed()  # Use current time as the seed (different each run)

# Create an array of pins and corresponding colors
leds = [(28, "red"), (27, "green"), (26, "blue"), (22, "yellow"),
        (21, "orange"), (20, "white"), (19, "purple"), (18, "pink"),
        (17, "lightgreen"), (16, "cyan")]

# Define a function to turn on/off a single LED
def led_control(pin, color, state):
    led = Pin(pin, Pin.OUT)
    led.value(1 if state == "on" else 0)  # Set value based on state
    time.sleep(0.2)  # Adjust delay as needed


# Define delays and randomization parameters (adjust as needed)
base_delay = 0.2
shift_amount = 1
random_delay_range = 0.1
# Define functions for each pattern:

def forward_pattern():
    for pin, color in leds:  # Iterate through each LED in the array
        led_control(pin, color, "on")  # Turn LED on
        time.sleep(0.2)  # Adjust delay as needed
        led_control(pin, color, "off")  # Turn LED off
        time.sleep(0.2)  # Adjust delay as needed

def reverse_pattern():
    for pin, color in reversed(leds):  # Iterate in reverse order using reversed()
        led_control(pin, color, "on")
        time.sleep(0.2)
        led_control(pin, color, "off")
        time.sleep(0.2)

def shifting_pattern():
    global leds  # Access global leds array
    shifted_leds = leds[shift_amount:] + leds[:shift_amount]
    for pin, color in shifted_leds:
        led_control(pin, color, "on")
        time.sleep(base_delay)
        led_control(pin, color, "off")
        time.sleep(base_delay)

def mirrored_pattern():
    global leds
    for i in range(len(leds)):
        pin1, color1 = leds[i]
        pin2, color2 = leds[len(leds) - 1 - i]  # Access mirrored element directly
        # Turn both LEDs on simultaneously:
        led_control(pin1, color1, "on")
        led_control(pin2, color2, "on")
        time.sleep(base_delay)  # Wait for specified duration
        # Turn both LEDs off simultaneously:
        led_control(pin1, color1, "off")
        led_control(pin2, color2, "off")
        time.sleep(base_delay)  # Wait for specified duration

current_pos = 0  # Initialize current LED position
def spiral_pattern():
    global leds, current_pos

    # Choose a random spiral path
    clockwise_spiral = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
    counterclockwise_spiral = reversed(clockwise_spiral)
    square_spiral = clockwise_spiral * 4  # Repeat clockwise path 4 times for a square
    spiral_paths = [clockwise_spiral, counterclockwise_spiral, square_spiral]
    chosen_path = random.choice(spiral_paths)

    # Choose the desired spiral path (optional)
    if random.random() < 0.5:
        chosen_path = chosen_path[::-1]  # Reverse the path randomly

    # Center LED blink at the beginning (assuming `led_control` exists)
    if current_pos == 0:
        led_control(leds[0][0], "white", "on")  # Access LED 0 directly
        time.sleep(base_delay)
        led_control(leds[0][0], "white", "off")
        time.sleep(base_delay)

    # Loop through the chosen spiral path
    for x, y in chosen_path:
        num_leds = 10  # Adjust if the number changes

        # Address edge cases and update current_pos
        new_pos = (current_pos + x * num_leds + y) % num_leds  # Handle wraparound
        current_pos = new_pos

        # Turn on the LED at the current position with its color
        led_control(leds[current_pos][0], leds[current_pos][1], "on")
        time.sleep(base_delay + random.random() * random_delay_range)
        led_control(leds[current_pos][0], leds[current_pos][1], "off")
        time.sleep(base_delay + random.random() * random_delay_range)

def waves_pattern():
    global leds

    num_leds = len(leds)

    # Choose random starting point, direction, initial group size, and color
    start_index = random.randrange(num_leds)
    direction = random.choice([-1, 1])
    group_size = random.randrange(2, 5)
    color = random.choice(range(256)) * 3  # RGB color triplet (0-255)

    while True:
        # Turn on LEDs in the current group
        for i in range(start_index, start_index + group_size):
            index = (i + direction * num_leds) % num_leds
            led_control(leds[index][0], color, "on")

        # Randomly change direction or group size at intervals
        if random.random() < 0.2:  # 20% chance of change
            if random.random() < 0.5:  # 50% chance to change direction
                direction *= -1
            else:
                group_size = random.randrange(2, 5)

        # Delay and turn off previous group
        time.sleep(random.uniform(0.1, 0.5))  # Random delay 0.1-0.5 seconds
        for i in range(start_index, start_index + group_size):
            index = (i + direction * num_leds) % num_leds
            led_control(leds[index][0], leds[index][1], "off")  # Include color argument

        # Shift starting point for the next group
        start_index = (start_index + direction * group_size) % num_leds

        # Break out of loop after some iterations (optional)
        if random.random() < 0.01:  # 1% chance to stop
            break

pattern_names = {
    forward_pattern: "Forward",
    reverse_pattern: "Reverse",
    shifting_pattern: "Shifting",
    mirrored_pattern: "Mirrored",
    spiral_pattern: "Spiral",
    waves_pattern: "Waves",
}
# Main loop with random pattern selection:

while True:
    random.seed()
    pattern_choice = random.choice([forward_pattern, reverse_pattern, shifting_pattern, mirrored_pattern, spiral_pattern, waves_pattern])
    # print(f"Running pattern: {pattern_names[pattern_choice]}")
    pattern_choice()
    time.sleep(1)  # Adjust delay between patterns if desired

