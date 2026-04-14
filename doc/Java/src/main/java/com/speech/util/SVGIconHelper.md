# SVGIconHelper.java Documentation

## Location
`Java/src/main/java/com/speech/util/SVGIconHelper.java`

## Overview
A streamlined graphical utility wrapper facilitating robust, pixel-perfect dynamic icons for Swing Buttons utilizing the third-party SVG library (SVG Salamander).

## Key Responsibilities
- Avoids blurry `.png` artifacting on scaled monitors by exclusively rendering resolution-independent `.svg` files located dynamically under `/icons/`.
- Abstracts complicated `SVGIcon` loading logic into a simple `getIcon(String)` helper.
- Overrides basic failing behavior securely by constructing dynamic code-drawn placeholder polygons dynamically if a file trace fails locally, preventing total UI collapse.
