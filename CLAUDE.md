# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monika After Story (MAS) is a Ren'Py mod for Doki Doki Literature Club that allows players to interact with Monika after the game's events. This is a Chinese localization fork of the main project.

## Development Commands

### Testing and Validation
- **Sprite Validation**: `python tools/ghactions.py` - Validates sprite definitions and catches mismatches
- **Ren'Py Linting**: Requires Ren'Py SDK (see CI workflow for setup) - `./renpy.sh "<path_to_game>" lint`

### Running the Game
- **Linux/macOS**: `./DDLC.sh` (from `Monika After Story/` directory)
- **Direct Python**: `python DDLC.py` (from `Monika After Story/` directory)

### Development Tools
- **Sprite Checker**: `python tools/spritechecker.py` - Comprehensive sprite validation
- **Menu Utils**: `python tools/menutils.py` - Development menu utilities

## Architecture

### Core Structure
- **`Monika After Story/game/`**: Main game directory containing all Ren'Py scripts
- **`script-ch30.rpy`**: Main idle/conversation flow - the core loop of the mod
- **`definitions.rpy`**: Core definitions, constants, and early initialization
- **`event-handler.rpy`** & **`event-rules.rpy`**: Event system architecture

### Content Organization
- **`script-topics.rpy`**: Random and pool dialogue topics
- **`script-greetings.rpy`**: Game startup greetings 
- **`script-farewells.rpy`**: Game exit dialogues
- **`script-moods.rpy`**: Mood system interactions
- **`script-stories.rpy`**: Story content
- **`script-*.rpy`**: Various content modules (holidays, anniversaries, etc.)

### Systems Architecture
- **`zz_*.rpy`**: Core systems (backgrounds, music, overlays, sprites, etc.)
- **Event System**: Uses `Event` objects with categories, prompts, and conditions
- **Store System**: Ren'Py stores for namespacing (prefix with `mas_`)
- **Persistent Data**: Prefixed with `_mas_` for save data

### Asset Organization
- **`mod_assets/`**: All mod-specific assets (required location for new assets)
- **`images/`**: Character sprites and backgrounds
- **`gui/`**: UI elements and interface assets

## Coding Conventions

### Label Naming
- Lowercase with underscores: `monika_example_topic`
- Reserved prefixes: `greeting`, `monika`, `mas_`, `bye`, `ch30`, `game`
- Event labels must be unique across the entire codebase

### Event Definition Template
```renpy
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_unique_label",
            category=["category"],
            prompt="Button Text",
            random=True,
            pool=True
        )
    )

label monika_unique_label:
    m "Dialogue here"
    return
```

### Style Requirements
- Four-space indentation
- Functions: prefix globals with `mas_`
- Constants: UPPERCASE_UNDERSCORES
- Variables: lowercase_underscores  
- Persistent data: prefix with `_mas_`
- Store names: prefix with `mas_`

### Development Files
- **`dev/`**: Development and testing scripts (not included in distribution)
- **`dev/*.rpy`**: Development tools and test dialogues

## File Exclusions
The `.vscode/settings.json` excludes compiled files:
- `*.rpyc` (compiled Ren'Py scripts)
- `*.rpa` (Ren'Py archives)  
- `*.rpymc` (compiled Ren'Py macros)
- `cache/` directories

## CI/CD Pipeline
GitHub Actions workflow validates:
1. Sprite definitions using custom tools
2. Ren'Py linting (filters out known sprite attribute warnings)
3. Linux distribution building with Ren'Py 8.1.1

## Chinese Localization Notes
This is the Chinese localization repository - text content translations are managed separately at Mon1-innovation/MAS-Simplified-Chinese-Patch.