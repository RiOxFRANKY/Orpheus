# App.java Documentation

## Location
`Java/src/main/java/com/speech/App.java`

## Overview
This is the main entry point for the Java GUI application. It sets up the global look and feel (FlatMacDarkLaf), enforces a custom default font ("Anticyclone"), and launches the `MainDashboard` on the Swing Event Dispatch Thread.

## Key Responsibilities
- Sets the default font globally using `UIManager.put()`.
- Initializes the `FlatMacDarkLaf` Look and Feel for modern dark theme aesthetics.
- Instantiates and displays `MainDashboard` asynchronously using `SwingUtilities.invokeLater()`.
