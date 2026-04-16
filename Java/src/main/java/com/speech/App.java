package com.speech;

import com.formdev.flatlaf.themes.FlatMacDarkLaf;
import com.speech.ui.MainDashboard;

import com.speech.util.FontHelper;

import javax.swing.*;
import javax.swing.plaf.FontUIResource;
import java.awt.Font;

public class App {
    public static void main(String[] args) {
        // Enforce Anticyclone globally for absolutely all generic fonts (excluding customly overridden ones like headings!)
        // Set Global Default Font natively into UIManager for UIResource scaling
        UIManager.put("defaultFont", new FontUIResource(
            FontHelper.getAnticycloneFont(Font.PLAIN, 12f)
        ));

        // Initialize FlatLaf Dark theme
        try {
            UIManager.setLookAndFeel(new FlatMacDarkLaf());
        } catch (Exception ex) {
            System.err.println("Failed to initialize FlatLaf");
            ex.printStackTrace();
        }

        SwingUtilities.invokeLater(() -> {
            MainDashboard dashboard = new MainDashboard();
            dashboard.setVisible(true);
        });
    }
}
