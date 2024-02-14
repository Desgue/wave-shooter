# Wave Shooter Game Development Project

## Overview:

Developing a wave shooter game has proven to be a challenging yet rewarding journey. Building upon the experience gained from the Pong2 project, this game involves rendering multiple sprites, managing complex collision scenarios, implementing animations, and delving into more complicate vector math. The addition of character states further increases the complexity.

## Current Features:

- **Player Character:**
  - Hitpoints, ammo, and shooting functionality.
  - Shooting directed at mouse click with reload using the R key.
  - Reload cooldown prevents shooting during this time.

- **Enemy AI:**
  - Computer AI follows the player's center position.
  - Inflicts damage on collision.
  - Two different enemy sprites with unique hitpoints, damage, and speed.

- **Game Assets**
  - Utilizing a free asset pack from Itch.io
    - *I lost the link to the asset pack, will update when I find it*

- **Game Map:**
  - Utilizes Tiled, an open-source project, to create the game map and export it as a TMX file.
  - Reads TMX file to draw sprites at correct positions.

- **Basic States:**
  - Very basic menu, pause, and game over states and screens.

## Ongoing Development:

- **AI Enhancement:**
  - Implementing the A* algorithm for pathfinding to enhance computer AI behavior.

- **UI/UX Improvement:**
  - Focusing on polishing UI and UX elements.
  - Adding sound effects, better UI sprites, and more animations for character and enemy interactions.

## Future Plans:

- **Core Game Features:**
  - Introducing waves of enemies for an engaging gameplay experience.
  - Incorporating power-ups that persist after each wave.

- **Database Integration:**
  - Implementing SQLite for game save preservation.

- **Character Selection:**
  - Introducing different starting weapons for character selection.

## Development Approach:

- **Object-Oriented Programming (OOP):**
  - Utilizing Python for its simplicity in creating relationships between different game components.
  - Leveraging the base classes provided by Pygame-CE for efficient sprite manipulation.

## Project Status:

This is a passion project that receives attention whenever time allows. The development progress focuses on building a solid foundation before delving into more advanced features. The journey involves a balance between learning, experimentation, and the joy of creating a game from scratch.
