# Pygame Multiplayer Game

This project is a multiplayer game built using Pygame, featuring real-time gameplay and networking capabilities. The game includes various features such as QR code invitations, customizable settings, and sound effects. This README will guide you through setting up, running, and understanding the project.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Running the Game](#running-the-game)
5. [Project Structure](#project-structure)
6. [Customization](#customization)
7. [Known Issues](#known-issues)
8. [Contributing](#contributing)
9. [License](#license)

## Features

- **Multiplayer Gameplay:** Connect and play with other players over a network.
- **QR Code Invitations:** Generate and display a QR code for easy game invitations.
- **Customizable Settings:** Configure game settings such as screen size, colors, and captions.
- **Sound Effects and Music:** Enjoy background music and sound effects during gameplay.
- **Real-time Updates:** Experience smooth and real-time updates for game states and player actions.

## Requirements

- Python 3.x
- Pygame
- qrcode
- pyperclip
- Required libraries for networking and JSON handling

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/pygame-multiplayer-game.git
   cd pygame-multiplayer-game
   ```

2. **Install Required Libraries:**
   ```bash
   pip install pygame qrcode pyperclip mido
   ```

## Running the Game

1. **Start the Game Server:**
   Ensure you have a server running that can handle game connections. You may need to modify the `SERVER_IP` and `SERVER_PORT` constants in the code to match your server setup.

2. **Run the Main Script:**

   ```bash
   python scripts/main.py
   ```

3. **Configure Game Settings:**
   The settings page will appear, allowing you to configure game settings and input your username. You can also invite players by generating a QR code.

4. **Start the Game:**
   Click the "Start" button to begin the game after configuring your settings.

## Project Structure

```
.
├── assets/                 # Assets such as images and sounds
├── scripts/
│   ├── game.py             # Main game logic
│   ├── main.py             # Entry point of the application
│   ├── settings_page.py    # Settings page with QR code functionality
│   ├── connection.py       # Networking and connection handling
│   ├── fighter.py          # Fighter class
│   ├── alien.py            # Alien class
│   ├── ball.py             # Ball class
│   ├── game_music.py       # Music and sound effects handling
│   └── generate_midi.py    # MIDI file generation for sound effects
├── README.md               # This README file
└── requirements.txt        # List of dependencies
```

## Customization

### Changing Game Settings

You can customize various game settings by modifying the `settings_page.py` file. This includes screen dimensions, colors, and game captions.

### Adding New Features

To add new features or game elements, create new Python classes or scripts in the `scripts/` directory and integrate them with the existing game logic.

### Changing Assets

Replace or add new assets such as images and sound files in the `assets/` directory. Ensure the paths in your scripts are updated accordingly.

## Known Issues

- Ensure `pygame.font.init()` is called before using any font-related functionalities to avoid initialization errors.
- Verify the server IP and port settings to ensure proper connectivity.

## Contributing

We welcome contributions to this project! If you have suggestions or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch to your fork.
4. Create a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Thank you for using and contributing to our Pygame Multiplayer Game project! If you have any questions or need further assistance, feel free to open an issue on GitHub. Enjoy the game!
