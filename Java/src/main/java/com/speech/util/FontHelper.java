package com.speech.util;

import java.awt.Font;
import java.io.InputStream;
import java.awt.GraphicsEnvironment;

public class FontHelper {
    private static Font glontoFont;
    private static Font anticycloneFont;

    public static Font getGlontoFont(int style, float size) {
        if (glontoFont == null) {
            try {
                // Read the physical font file bundled in our Maven resources
                InputStream is = FontHelper.class.getResourceAsStream("/fonts/Glonto-Regular.otf");
                if (is != null) {
                    glontoFont = Font.createFont(Font.TRUETYPE_FONT, is);
                    // Register the font globally to ensure HTML tags and native Swing rendering engine locks onto it
                    GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
                    ge.registerFont(glontoFont);
                } else {
                    System.err.println("Could not load Glonto from resources! Falling back to generic font.");
                    glontoFont = new Font("SansSerif", Font.BOLD, 12);
                }
            } catch (Exception e) {
                e.printStackTrace();
                glontoFont = new Font("SansSerif", Font.BOLD, 12);
            }
        }
        // Generate the properly sized & styled variant
        return glontoFont.deriveFont(style, size);
    }

    public static Font getAnticycloneFont(int style, float size) {
        if (anticycloneFont == null) {
            try {
                // Read the physical font file bundled in our Maven resources
                InputStream is = FontHelper.class.getResourceAsStream("/fonts/Anticyclone-VariableVF.ttf");
                if (is != null) {
                    anticycloneFont = Font.createFont(Font.TRUETYPE_FONT, is);
                    GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
                    ge.registerFont(anticycloneFont);
                } else {
                    System.err.println("Could not load Anticyclone from resources! Falling back to generic font.");
                    anticycloneFont = new Font("SansSerif", Font.PLAIN, 13);
                }
            } catch (Exception e) {
                e.printStackTrace();
                anticycloneFont = new Font("SansSerif", Font.PLAIN, 13);
            }
        }
        // Generate the properly sized & styled variant
        return anticycloneFont.deriveFont(style, size);
    }
}
