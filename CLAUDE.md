# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **CareDian Home Assistant configuration** - a smart home system focused on care monitoring and home automation. The repository is part of the 2025 Embedded Software Contest project and contains a complete Home Assistant setup with custom components, sensors, and integrations.

## Architecture

### Core Structure
- **Configuration Files**: `configuration.yaml` is the main config file that includes other YAML files
- **Custom Components**: Located in `custom_components/` with several integrations:
  - `bestin/` - BESTIN home automation system integration 
  - `icloud3/` - Enhanced iCloud device tracking
  - `ble_monitor/` - Bluetooth Low Energy device monitoring
  - `google_home/` - Google Home integration
  - `hacs/` - Home Assistant Community Store
  - `smartthinq_sensors/` - LG SmartThinQ device integration
  - `kwh_to_won/` - Korean electricity cost calculator

### Data Collection & Storage
- **InfluxDB Integration**: Configured for time-series data collection with comprehensive sensor filtering
- **Database**: Uses SQLite (`home-assistant_v2.db`) for state storage
- **Logging**: Separate log files for main system (`home-assistant.log`) and iCloud3 (`icloud3.log`)

### Key Integrations Focus
The system is heavily configured for **environmental monitoring** with InfluxDB collecting:
- Temperature, humidity, pressure sensors
- Air quality (CO2, TVOC, PM2.5, PM10)
- Power consumption and energy monitoring  
- Motion, occupancy, and presence detection
- Device tracking and location services

## Common Commands

### Home Assistant Operations
```bash
# Restart Home Assistant
ha core restart

# Check configuration
ha core check

# View logs
tail -f /config/home-assistant.log
tail -f /config/icloud3.log
```

### Git Operations
```bash
# Pull latest configuration (automated script available)
./pull-config.sh

# Manual git operations
git pull origin main
git status
git add .
git commit -m "Update configuration"
git push origin main
```

### Custom Component Management
Most custom components are managed through HACS (Home Assistant Community Store) integration.

## Development Guidelines

### Configuration Files
- Main configuration is in `configuration.yaml`
- Secrets are stored in `secrets.yaml` (not committed to repo)
- Automations, scripts, and scenes are in separate YAML files
- InfluxDB configuration includes extensive filtering rules for optimal data collection

### Custom Components
- Each component has its own directory structure under `custom_components/`
- Components include `manifest.json` with dependencies and version info
- Translation files are provided for multiple languages
- Follow Home Assistant integration development patterns

### File Structure Conventions
- Static files served from `www/` directory
- ESPHome configurations in `esphome/` directory  
- Jupyter notebooks for data analysis in `notebooks/`
- TTS audio files cached in `tts/` directory

### Monitoring & Logging
- System uses structured logging with separate log files
- InfluxDB collects quantitative sensor data with smart filtering
- Binary sensors and state changes are tracked for automation triggers

## Repository Context

This is a **backend configuration repository** for the CareDian project (2025 Embedded Software Contest). The system appears to be designed for elderly care monitoring with emphasis on:
- Environmental monitoring (air quality, temperature, humidity)
- Presence and motion detection
- Device tracking and location services  
- Energy consumption monitoring
- Integration with Korean smart home systems (BESTIN, LG SmartThinQ)

The configuration is production-ready with comprehensive data collection, proper secret management, and automated deployment scripts.