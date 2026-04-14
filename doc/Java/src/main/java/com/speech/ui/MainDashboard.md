# MainDashboard.java Documentation

## Location
`Java/src/main/java/com/speech/ui/MainDashboard.java`

## Overview
The primary GUI window (`JFrame`) that acts as the container for all the individual modular sub-components (Input, Preprocessing, Feature Selection, Execution, and Output sections). 

## Key Responsibilities
- Configures the root `JFrame`, enforcing min/max sizing, taskbar icons, and default close operations.
- Implements a custom `ScrollablePanel` wrapper to handle responsive resizing gracefully without layout breaking on small resolutions.
- Uses `MigLayout` to systematically arrange `DashboardSection` components logically across a grid.
- Links reactive behavior across sections (e.g. Disabling Run button dynamically depending on "OnFileChangeListener" events).
- Mounts the `ThemeSwitch` component into a dynamic header bar.
