# FontHelper.java Documentation

## Location
`Java/src/main/java/com/speech/util/FontHelper.java`

## Overview
A global utility class heavily utilized dynamically to enforce strict typography aesthetics inside the Java App independently of OS defaults. 

## Key Responsibilities
- Dynamically loads uninstalled standard ".otf" and ".ttf" physical web fonts from inside the secured compiled Maven `.jar` resources (`/fonts/`).
- Registers specific premium aesthetic fonts like 'Glonto' (for Title headers) and 'Anticyclone' (for general text mapping) strictly into the local `GraphicsEnvironment` dynamically for pristine UI rendering.
- Handles robust fallbacks gracefully in the event physical files are corrupt or restricted on-device.
