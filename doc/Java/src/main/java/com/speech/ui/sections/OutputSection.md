# OutputSection.java Documentation

## Location
`Java/src/main/java/com/speech/ui/sections/OutputSection.java`

## Overview
The Dashboard component utilized strictly *after* the Python Pipeline finishes. It enables the downloading of results directly back to the Local OS via HTTP Streams.

## Key Responsibilities
- Houses dual download trigger buttons utilizing SVG Icons natively for "Download CSV" and "Download ZIP" operations.
- Intercepts clicks and natively opens `JFileChooser` save dialogs securely.
- Initiates `SwingWorker` instances to handle asynchronous HTTP GET streams natively fetching ZIP and CSV binaries dynamically from the `127.0.0.1:9999/api/download/` endpoints.
- Leverages standard library `Files.copy` protocols to directly dump incoming web streams right to hard disk files reliably to bypass generic RAM limits.
