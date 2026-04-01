package com.speech.ui;

import javax.swing.*;
import javax.swing.border.TitledBorder;
import net.miginfocom.swing.MigLayout;
import java.awt.Font;

public abstract class AbstractDashboardSection implements DashboardSection {
    
    protected JPanel panel;

    @Override
    public JPanel buildPanel() {
        if (panel == null) {
            panel = new JPanel(new MigLayout("wrap 1, fill, insets 5"));
            
            // Explicitly use an EtchedBorder to ensure top/bottom lines are prominently visible regardless of the LAF style
            TitledBorder border = BorderFactory.createTitledBorder(
                BorderFactory.createEtchedBorder(javax.swing.border.EtchedBorder.LOWERED),
                getSectionTitle()
            );
            // Use a regular Font (not UIResource) to ensure the Glonto header is PERSISTENT across theme changes!
            border.setTitleFont(com.speech.util.FontHelper.getGlontoFont(Font.BOLD, 14f));
            
            // Apply a CompoundBorder to add exactly 10px of high-end spacing between the heading title and the actual content!
            panel.setBorder(BorderFactory.createCompoundBorder(
                border,
                BorderFactory.createEmptyBorder(10, 5, 5, 5)
            ));
            
            initializeComponents();
        }
        return panel;
    }

    protected abstract void initializeComponents();
}
