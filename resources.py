import pygame
import sys
from random import *
from resources import *
import math




motds = [
    "In the darkest corners of the cosmos, your presence has been noted. Beware what lurks just beyond the veil. But don’t worry, the gelatinous blobs are still just as squishy.",
    "Reality is a fragile construct. With every breath you take, you draw closer to the horrors that await. Meanwhile, don’t forget to collect your daily rations!",
    "The whispers of the abyss grow louder with each passing moment. Do you dare to listen to what lies beyond? Just make sure you don’t forget to upgrade your gear!",
    "Time itself is but a twisted jest in the hands of ancient beings. Your sanity is the price of their amusement. In the meantime, enjoy the new in-game events.",
    "The gelatinous entities that slither through the shadows are beyond your comprehension. Their motives are as inscrutable as the void. Speaking of which, have you checked out the latest challenges?",
    "You have disturbed forces older than humanity. Their wrath is a slow and inexorable tide that will consume you. But before that happens, take a moment to upgrade your character!",
    "Every step you take brings you closer to the horrors that slumber beneath the surface. There is no escape from the madness. However, you can always take a break with our latest mini-games.",
    "The cosmic entities that watch over you are indifferent to your suffering. Their gaze is eternal and unfeeling. On a brighter note, there’s a new cosmetic item available in the shop.",
    "In the silence of the night, listen for the echoes of forgotten gods. Their murmurs are a harbinger of doom. For now, focus on completing your current quests.",
    "The fabric of reality is unraveling. Each moment spent in this world is a step further into the abyss. At least the new leaderboard is up and running!",

    "The abyss gazes back, and your soul trembles in its shadow. Yet, the crafting station is still operational—don’t forget to use it!",
    "Ancient cosmic entities stir in their slumber, their dreams affecting your reality. At least the daily login rewards are still waiting for you.",
    "Every corner of the universe hides unspeakable horrors. For now, focus on gathering resources to enhance your defenses.",
    "As the stars align in patterns of dread, remember that the in-game shop has new items to help you face the darkness.",
    "The unfathomable void beckons, promising madness. However, the quest for more kludges is still within reach.",
    "Your mind reels as the fabric of reality unravels. Take solace in the fact that your in-game achievements still stand.",
    "In the realm of the unknown, sanity is a fleeting illusion. Meanwhile, the latest patch has fixed some bugs—enjoy smoother gameplay!",
    "The nameless horrors of the cosmos watch your every move. On a brighter note, the new community event has just begun.",
    "Darkness encroaches upon your senses, but the game’s leaderboard is still accessible for you to track your progress.",
    "The endless void whispers of doom, but remember, the in-game marketplace has just restocked with valuable items.",

    "The whispers of Andy Lowe echo through the void, promising ancient terrors. But don’t worry—he’s also a fan of your new character’s outfit!",
    "Andy Lowe’s presence stirs the cosmic balance, his gaze cold and unyielding. Yet, even he can’t resist the charm of your latest in-game achievement.",
    "As you wander the shadowy realms, remember that Andy Lowe’s influence is ever-present. Take a moment to enjoy the tranquility of your in-game garden.",
    "The eldritch tendrils of Andy Lowe reach into your world, warping reality itself. On the bright side, your pet monster has just learned a new trick!",
    "Andy Lowe’s dark laughter reverberates through the cosmos, a reminder of his unfathomable power. Still, your new quest rewards are sure to lift your spirits.",
    "In the grip of Andy Lowe’s cosmic dread, your courage shines bright. Celebrate with a joyful feast in your in-game home, and forget the shadows for a while.",
    "The unfathomable presence of Andy Lowe looms near, his motives as inscrutable as the void. Yet, your latest in-game puzzle has just been solved!",
    "Andy Lowe’s ancient power weaves through the fabric of reality, but so does the warmth of your in-game community. Enjoy a moment of camaraderie with friends!",
    "Even as Andy Lowe’s chilling whispers reach your ears, there’s always time to appreciate the whimsical decorations in your virtual space.",
    "The abyssal influence of Andy Lowe is a reminder of the vast unknown. Meanwhile, don’t miss out on the latest cheerful event and in-game celebrations!",

    "Why did the gelatinous kludge go to school? To improve its `jelly-cation`!",
    "What do you call a kludge that can play music? A `jam`-ming kludge!",
    "Why don`t kludges get lost? Because they always stick to their `jelly` of the road!",
    "What`s a kludge`s favorite type of exercise? `Jelly-cise`!",
    "How do kludges prefer their eggs? Over `easy`—just like their `gelatin`!",
    "Why was the kludge always calm? It had a lot of `gelatin` patience!",
    "What do you get when you cross a kludge with a comedian? A real `gelatinous` laugh!",
    "Why did the kludge go to therapy? It had too many `unstable` feelings!",
    "How do kludges stay cool? They use a `gel`-based air conditioner!",
    "Why don`t kludges play hide and seek? Because they always leave a `jelly` trail!",

    "Welcome to Gelatinous Kludge—where the only thing more flexible than our gameplay is our hero’s vampire-themed career choices!",
    "Remember: In Gelatinous Kludge, being slimy is a feature, not a bug. Just ask our nocturnal scientist!",
    "We hope you’re ready for a gooey good time—after all, everyone needs a hobby between transforming into a dark, brooding antihero!",
    "In Gelatinous Kludge, it’s not about the bloodsucking. It’s about how many gelatinous blobs you can consume before calling it a night!",
    "Our game is like a blockbuster hit: unpredictable, slightly awkward, and with a lot of goo. Dive in and embrace the weird!",
    "Don’t worry about the slimy mess; it’s just our way of paying tribute to a certain scientifically ambitious nocturnal character!",
    "Gelatinous Kludge: Where even our gelatinous blobs have a more interesting backstory than a certain misunderstood scientist!",
    "You may not have superpowers, but at least you’re not trying to reinvent the wheel after a few bad experiments!",
    "Welcome to the only game where the gooey texture is intentional and every game session feels like a wild, cinematic experiment!",
    "In Gelatinous Kludge, we’ve perfected the art of being a sticky, ungraspable mess. Sort of like how our hero handled those messy experiments!"
]
_colours = [
    (234, 118, 203), # Pink
    (136, 57, 239),  # Mauve
    (210, 15, 57),   # Red
    (230, 69, 83),   # Maroon
    (254, 100, 75),  # Peach
    (223, 142, 29),  # Yellow
    (64, 160, 43),   # Green
    (23, 146, 153),  # Teal
    (4, 165, 229),   # Sky
    (32, 159, 181),  # Sapphire
    (30, 102, 245),  # Blue
    (114, 135, 253)  # Lavender
]

colours = [
    (242, 205, 205),  # Flamingo
    (245, 194, 231),  # Pink
    (203, 166, 247),  # Mauve
    (243, 139, 168),  # Red
    (235, 160, 172),  # Maroon
    (250, 179, 135),  # Peach
    (249, 226, 175),  # Yellow
    (166, 227, 161),  # Green
    (148, 226, 213),  # Teal
    (137, 220, 235),  # Sky
    (116, 199, 236),  # Sapphire
    (137, 180, 250),  # Blue
    (180, 190, 254)   # Lavender
]

title ="""   
  ___  ____  __      __   ____  ____  _  _  _____  __  __  ___    _  _  __    __  __  ____    ___  ____ 
 / __)( ___)(  )    /__\ (_  _)(_  _)( \( )(  _  )(  )(  )/ __)  ( )/ )(  )  (  )(  )(  _ \  / __)( ___)
( (_-. )__)  )(__  /(__)\  )(   _)(_  )  (  )(_)(  )(__)( \__ \   )  (  )(__  )(__)(  )(_) )( (_-. )__) 
 \___/(____)(____)(__)(__)(__) (____)(_)\_)(_____)(______)(___/  (_)\_)(____)(______)(____/  \___/(____)"""

def angle_to_velocities(angle_degrees, velocity=5):
    """
    Converts an angle in degrees to x and y velocities with a given velocity magnitude.

    Parameters:
    - angle_degrees: Angle in degrees.
    - velocity: Magnitude of the velocity. Default is 5.

    Returns:
    - A tuple (x_velocity, y_velocity) where x_velocity and y_velocity are the
      components of the velocity vector.
    """
    # Convert angle from degrees to radians
    angle_radians = math.radians(angle_degrees)
    
    # Calculate x and y velocities
    x_velocity = velocity * math.cos(angle_radians)
    y_velocity = velocity * math.sin(angle_radians)
    
    return (x_velocity, y_velocity)

def get_random_item(list):
    item = list[randint(0,len(list)-1)]
    return item

