package com.speech;

import com.formdev.flatlaf.themes.FlatMacDarkLaf;
import com.speech.ui.MainDashboard;

import javax.swing.*;

public class App {
    public static void main(String[] args) {
        // Enforce Anticyclone globally for absolutely all generic fonts (excluding customly overridden ones like headings!)
        // Set Global Default Font natively into UIManager for UIResource scaling
        UIManager.put("defaultFont", new javax.swing.plaf.FontUIResource(
            com.speech.util.FontHelper.getAnticycloneFont(java.awt.Font.PLAIN, 12f)
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
