# Acronym Expander Integration

This integration expands acronyms in messages entering a Telex channel, replacing them with their full forms.

## Table of Contents
1. [Description](#description)
2. [Setup](#setup)
3. [Testing](#testing)
4. [Deployment](#deployment)
5. [Usage](#usage)
6. [Screenshots](#screenshots)

## Description
The Acronym Expander integration is a Modifier Integration for the Telex platform. It scans messages for commonly used acronyms and expands them to their full forms to enhance readability.

## Setup

### Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/telex_integrations/acronym_expander.git
    cd acronym_expander
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
1. Create a JSON file named `acronym.json` in the root directory with the acronyms and their full forms.
    ```json
    {
        "fyi": "For your information",
        "lol": "Laugh out loud",
        "idk": "I don't know"
    }
    ```

2. Create a JSON file named `integration.json` in the root directory with the integration settings.
    ```json
    {
        "label": "modifier",
        "type": "text",
        "required": true,
        "default": ""
    }
    ```

## Testing
To run the tests, use the following command:
```bash
pytest
