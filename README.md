---
title: Gemini 3 Web Search
emoji: 🏢
colorFrom: green
colorTo: red
sdk: gradio
sdk_version: 6.5.1
app_file: app.py
pinned: false
short_description: An app for grounded response
---
# Gemini Web Search Application

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)

## Overview

A Gradio-based web application that combines Google Search with Gemini AI to provide grounded, contextual responses with real-time web information.

## Features

- Real-time Google Search integration
- Gemini AI-powered responses
- Customizable chat interface
- Environment-based configuration
- Professional assistant mode

## Project Structure

```
web-search/
├── app.py
├── requirements.txt
└── README.md
```

## Setup

1. Clone or download this project
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables (see Configuration section)
4. Run: `python app.py`

## Configuration

Set the following environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | — | API key for Gemini |
| `CHATBOT_NAME` | No | Assistant | Name displayed in chat |
| `DEFAULT_MODEL_ID` | No | `gemini-2.0-flash` | Gemini model version |
| `DEFAULT_TEMPERATURE` | No | `0.7` | Response creativity (0-1) |
| `SYSTEM_INSTRUCTION` | No | Professional assistant | System prompt |

## Usage

Launch the app and interact with the chat interface. Searches are performed automatically for grounded responses.

