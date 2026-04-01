package com.speech.ui;

import javax.swing.JPanel;

public interface DashboardSection {
    JPanel buildPanel();
    String getSectionTitle();
}
