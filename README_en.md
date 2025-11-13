[English](README_en.md) | [简体中文](README.md)

<div align="center">
  <img src="icons/icon.png" alt="icon" width="200"><br>
  <h1>ok-dna</h1>
  <p>An image-recognition-based automation tool for <em>Duet Night Abyss</em>, with background operation support.</p>
  <p>Developed based on the <a href="https://github.com/ok-oldking/ok-script">ok-script</a> framework.</p>
  
  <p>
    <img src="https://img.shields.io/badge/platform-Windows-blue" alt="Platform">
    <img src="https://img.shields.io/badge/python-3.12+-skyblue" alt="Python Version">
    <img src="https://img.shields.io/github/downloads/BnanZ0/ok-duet-night-abyss/total" alt="Total Downloads">
    <img src="https://img.shields.io/github/v/release/BnanZ0/ok-duet-night-abyss" alt="Latest Release">
    <a href="https://discord.gg/vVyCatEBgA"><img alt="Discord" src="https://img.shields.io/discord/296598043787132928?color=5865f2&label=%20Discord"></a>
  </p>
</div>

## ⚠️ Disclaimer

This software is an open-source, free external tool intended for learning and discussion purposes only. It aims to simplify the gameplay of *Duet Night Abyss* through simulated operations.

-   **How it Works**: The program interacts with the game solely by recognizing the existing user interface and does not modify any game files or code.
-   **Purpose**: It is designed to provide convenience to users and is not intended to disrupt the game's balance or provide any unfair advantage.
-   **Liability**: All issues and consequences arising from the use of this software are not related to this project or its development team. The development team reserves the final right of interpretation for this project.
-   **Commercial Use**: If you encounter vendors using this software for power-leveling services and charging a fee, this may cover their costs for equipment and time; this is not related to the software itself.

> **Please Note: According to the [*Duet Night Abyss* Fair Play Declaration](https://dna.yingxiong.com/#/news/list?id=14453&type=2523):**
>
> > "The use of any cheats, third-party tools, or other behaviors that undermine game fairness is strictly prohibited."
> > "Once verified, the operations team will take measures such as deducting illicit gains, freezing, or permanently banning the game account, depending on the severity and frequency of the violation, to protect the fair rights of players."
>
> **You should fully understand and voluntarily assume all potential risks associated with using this tool.**

## ✨ Main Features

<img width="1586" height="1142" alt="QQ_1763005086472" src="https://github.com/user-attachments/assets/c78b5acc-b08a-4dfe-98c9-49389711a7a8" />

*   **Automated Dungeon Farming**
    *   Supports fully automatic and semi-automatic modes
    *   Auto-repeat battles
    *   Compatible with external movement logic (Mods)
*   **Auto-Fishing** (Core logic original author: Bilibili @无敌大蜜瓜)
*   **Fast Travel**
    *   Auto-triggers Resonance Traversal
*   **Auto-charge for Inflorescence Bow**
*   **Background Operation**
    *   Supports automation while the PC game is running in the background

## 🖥️ System Requirements & Compatibility

*   **Operating System**: Windows
*   **Game Resolution**: 1600x900 or higher (16:9 aspect ratio recommended)
*   **Game Language**: Simplified Chinese / English

## 🚀 Installation Guide

### Method 1: Using the Installer (Recommended)

This method is suitable for most users. It's simple, fast, and supports automatic updates.

1.  Go to the [**Releases**](https://github.com/BnanZ0/ok-duet-night-abyss/releases) page.
2.  Download the latest `ok-dna-win32-Global-setup.exe` file.
3.  Double-click the installer and follow the prompts to complete the installation.

### Method 2: Running from Source (For Developers)

This method requires a Python environment and is suitable for users who want to contribute, modify, or debug the code.

1.  **Prerequisites**: Ensure you have **Python 3.12** or a newer version installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/BnanZ0/ok-duet-night-abyss.git
    cd ok-duet-night-abyss
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt --upgrade
    ```
    *Tip: After pulling new code, it's recommended to run this command again to ensure all dependencies are up to date.*
4.  **Run the application**:
    ```bash
    # Run the standard version
    python main.py
    
    # Run the debug version (outputs more detailed logs)
    python main_debug.py
    ```

## 📖 Usage Guide & FAQ

To ensure the program runs stably, please carefully read the following configuration requirements and frequently asked questions before use.

### 1. Pre-use Configuration (Required)

Before starting the automation, please check and confirm the following settings:

*   **Graphics Settings**
    *   **Graphics Filters**: **Disable** all graphics card filters and sharpening effects (e.g., NVIDIA Freestyle, AMD FidelityFX).
    *   **Game Brightness**: Use the **default** in-game brightness.
    *   **UI Scaling**: Use the **default 100%** UI scale.
*   **Resolution**
    *   Recommended to use **1600x900** or other common 16:9 resolutions.
*   **Keybindings**
    *   Please use the game's **default** keybindings.
*   **Third-party Software**
    *   Disable any overlays that display information on the game screen, such as the **framerate counter** from MSI Afterburner.
*   **Window and System State**
    *   **Mouse Interference**: When the game window is in the **foreground**, do not move your mouse, as it will interfere with the program's simulated clicks.
    *   **Window State**: The game window can be in the background but **must not be minimized**.
    *   **System State**: Do not let your computer **turn off the display** or **lock the screen**, as this will interrupt the program.

### 2. Quick Start

1.  Navigate to the level or scene you want to automate.
2.  Click the **"Start"** button in the program's interface.

### 3. Installing External Logic (Mods)

You can install community-developed external logic modules to extend the program's functionality.

1.  From the program's main interface, click the **"Installation Directory"** button to open the program folder.
2.  Place the downloaded Mod files into the `mod` folder.
3.  Restart the program to load them.

### 4. Frequently Asked Questions (FAQ)

**Q1: My character often runs into walls or fails to reach the target location.**

*   **Reason**: The game engine's movement speed is strongly tied to the frame rate (FPS).
*   **Solution**:
    1.  **Adjust Game FPS**: In the game's settings, try setting the frame rate limit to **60 FPS**, **120 FPS**, and **Unlimited** to see which one performs most consistently.
    2.  **Adjust Key Press Duration**: In the settings for the relevant task or Mod, fine-tune the **"Key Press Duration"** parameter.
    3.  **Wait for Official Patches**: This issue may need to be addressed in a future official game update.

**Q2: My installed Mod isn't working or isn't being recognized correctly.**

*   **Reason**: The image assets used for recognition within the Mod may not be compatible with all screen resolutions.
*   **Solution**:
    1.  **Change Resolution**: Try switching to a common resolution like 1920x1080 or 1600x900.
    2.  **Update Assets Manually**: If you are familiar with Mod creation, you can re-capture the necessary screenshots for image recognition at your current resolution.

**Q3: The program gets stuck on the results screen and stops running.**

*   **Reason**: Unintentional mouse movement has likely interfered with the program's image recognition.
*   **Solution**:
    1.  Click **"Settings"** in the bottom-left corner of the program.
    2.  Switch to the **"Farming Settings"** tab.
    3.  Check and enable the **"Prevent Mouse Interference"** feature.

### 5. Bug Reports & Feedback

If the solutions above do not resolve your issue, feel free to report it via [**Issues**](https://github.com/BnanZ0/ok-duet-night-abyss/issues). To help us quickly identify the problem, please provide the following information in your report:

*   **Screenshot**: A clear image of the error or unusual behavior.
*   **Log File**: Attach the `.log` file from the program's directory.
*   **Detailed Description**: What were you doing? What exactly happened? Can you reproduce the issue consistently, or does it happen randomly?

## 💬 Community

*   **Discord**: [https://discord.gg/vVyCatEBgA](https://discord.gg/vVyCatEBgA)

## 🔗 Projects developed using [ok-script](https://github.com/ok-oldking/ok-script):

*   Wuthering Waves: [https://github.com/ok-oldking/ok-wuthering-waves](https://github.com/ok-oldking/ok-wuthering-waves)
*   Genshin Impact (discontinued, but background story progression is still usable): [https://github.com/ok-oldking/ok-genshin-impact](https://github.com/ok-oldking/ok-genshin-impact)
*   Girls' Frontline 2: [https://github.com/ok-oldking/ok-gf2](https://github.com/ok-oldking/ok-gf2)
*   Honkai: Star Rail: [https://github.com/Shasnow/ok-starrailassistant](https://github.com/Shasnow/ok-starrailassistant)
*   Star-Resonance: [https://github.com/Sanheiii/ok-star-resonance](https://github.com/Sanheiii/ok-star-resonance)
*   Duet Night Abyss: [https://github.com/BnanZ0/ok-duet-night-abyss](https://github.com/BnanZ0/ok-duet-night-abyss)
*   Ash Echoes (discontinued): [https://github.com/ok-oldking/ok-baijing](https://github.com/ok-oldking/ok-baijing)
