# AnimatedButton.java Documentation

## Location
`Java/src/main/java/com/speech/ui/components/AnimatedButton.java`

## Overview
A customized Swing `JButton` utilizing custom 2D Graphics to orchestrate modern UI aesthetics like smooth hover fading and animated alpha press effects natively, decoupled from basic Look & Feel limits.

## Key Responsibilities
- Modifies button painting semantics to use custom alpha compositing (fading).
- Listens to Mouse Events locally to spin up `javax.swing.Timer` events for `hoverAlpha` and `pressAlpha` values.
- Supports a toggleable `SpecialGlow` property specifically used for primary call-to-action buttons (like the Run Matrix button).
