# InputSection.java Documentation

## Location
`Java/src/main/java/com/speech/ui/sections/InputSection.java`

## Overview
The Dashboard component responsible for ingesting Raw Audio files from the user's filesystem dynamically.

## Key Responsibilities
- Instantiates a secure user `JFileChooser` restricted heavily to verified audio extension types (wav, mp3, ogg, etc).
- Displays selected ingest data neatly inside a managed `JTable` / `DefaultTableModel`.
- Maintains the internal reference state natively for all tracked absolute filesystem `Path` values for target raw files.
- Provides an `onFileChangeListener` listener system allowing it to securely communicate outwards, for example, strictly disabling the 'RUN' button if the filetable becomes void.
