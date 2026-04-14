# ThemeSwitch.java Documentation

## Location
`Java/src/main/java/com/speech/ui/ThemeSwitch.java`

## Overview
A custom animated toggle component that allows the user to switch between "Dark Mode" and "Light Mode" seamlessly. 

## Key Responsibilities
- Visually draws an interactive pill-shaped toggle switch using Java 2D Graphics.
- Fades background colors and icon opacities (sun and moon SVGs) based on linear interpolation state.
- Utilizes `javax.swing.Timer` to orchestrate smooth transition animations over time.
- Uses `FlatAnimatedLafChange` APIs to dynamically re-paint the global frame Look & Feel synchronously with the toggle animation.
