# Flappy Bird AI 🐦🤖

A versatile Flappy Bird clone featuring two gameplay modes and adjustable difficulty, all configurable via the in-game menu.

* **Manual Mode**: Take direct control of the bird with intuitive keyboard inputs.
* **AI Mode**: Watch neural networks evolve using NEAT to master the game over generations.
* **Difficulty Levels**: Switch between Normal for casual play and Hard for a true challenge.

---

## Project Overview

Flappy Bird AI is built in Python using Pygame. It combines interactive gameplay with advanced neuroevolution: in AI Mode, agents learn by tuning parameters like pipe speed and gap size. All settings—mode selection and difficulty—are adjusted through the app’s graphical menu before you start playing or training.

---

## Key Features

* **In-Game Menu**: Seamlessly switch between Manual and AI modes and choose Normal or Hard difficulty without touching the command line.
* **Real-Time Training Visualization**: During AI sessions, view generation count, top fitness score, and population size on-screen.
* **Configurable Hyperparameters**: Tweak NEAT settings by editing `config-feedforward.txt` before launching.
* **Performance Optimization**: Enjoy smooth simulations even at accelerated training speeds.
* **Modular Codebase**: Clear separation of game logic, AI routines, and configuration for easy maintenance.

---

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/narayansubedi/FlappyBirdAI.git
   cd FlappyBirdAI
   ```
2. **Install Pygame**

   ```bash
   pip install pygame
   ```
3. **Run the Game**

   ```bash
   python FlappyBirdAI.py
   ```

Use the in-game menu to set your preferred mode (Manual or AI) and difficulty (Normal or Hard), then press **Start**.

---

## Skills & Concepts Learned

* **NEAT Algorithm**: Setting up genomes, species, crossover, and mutation processes.
* **Genetic Algorithms**: Designing fitness functions and evolutionary cycles.
* **Pygame Development**: Creating game loops, handling events, and sprite management.
* **Dynamic Difficulty Scaling**: Adjusting game parameters for different player skill levels.
* **Live Visualization**: Overlaying AI training metrics in real time.
* **Optimization & Debugging**: Profiling for performance to support fast-forward training.

---

Enjoy experimenting with both manual play and AI evolution—all from the comfort of your game’s menu!
