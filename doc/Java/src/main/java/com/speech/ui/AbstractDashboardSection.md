# AbstractDashboardSection.java Documentation

## Location
`Java/src/main/java/com/speech/ui/AbstractDashboardSection.java`

## Overview
An abstract base class that implements the `DashboardSection` interface. It provides standard boilerplate for scaffolding GUI sections in the Orpheus Dashboard.

## Key Responsibilities
- Creates a `JPanel` utilizing `MigLayout` as a unified layout engine.
- Sets up consistent Etched-Titled borders utilizing a dedicated title font (Glonto).
- Implements `buildPanel()` utilizing a Singleton pattern to initialize components exactly once.
- Declares the abstract method `initializeComponents()` to be implemented by child classes.
