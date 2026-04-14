# test_client.py Documentation

## Location
`Python/test_client.py`

## Overview
A lightweight secondary developer toolkit utilized manually for validating Python Engine boundaries via console loops rather than firing the heavy Java GUI.

## Key Responsibilities
- Compiles a mocked static configuration dictionary mapped identically matching exactly what Java's GSON outputs dynamically.
- Triggers standard TCP JSON exports mapping payload directly via HTTP POST to the running `FastAPI` port.
- Excellent tool primarily dedicated to simulating exact user payloads to trigger `ExtractionService` executions.
