package com.speech.ui;

import net.miginfocom.swing.MigLayout;
import com.speech.ui.sections.*;
import javax.swing.*;
import java.awt.*;

public class MainDashboard extends JFrame {

    public MainDashboard() {
        setTitle("Orpheus");
        
        // Dynamically locate and bind the user's custom logo to the Window/Taskbar icon slots natively
        try {
            java.net.URL iconURL = getClass().getResource("/icons/logo.png");
            if (iconURL != null) {
                setIconImage(new ImageIcon(iconURL).getImage());
            } else {
                System.err.println("Warning: logo.png not found, falling back to default icon.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // Made the height smaller so it comfortably fits above the taskbar on 1080p / scaled displays
        setSize(1000, 700);
        // Start maximized
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        setLocationRelativeTo(null);
        
        // Set a hard minimum window size to prevent squashing the layout beyond 800x600
        setMinimumSize(new Dimension(800, 600));

        // Note: Dynamic resize font-event listener completely deleted to guarantee relative flex bounds instead of absolute font hacks
        
        initializeUI();
    }

    private void initializeUI() {
        // Master Panel with Custom Scrollable Properties
        class ScrollablePanel extends JPanel implements Scrollable {
            public ScrollablePanel(LayoutManager layout) { super(layout); }
            @Override public Dimension getPreferredSize() {
                Dimension d = super.getPreferredSize();
                // When we stop tracking the viewport width (below 800px), 
                // we lock the preferred width to a STABLE 1000px floor to prevent infinite layout-drift.
                if (getParent() != null && getParent().getWidth() < 800) {
                    d.width = Math.max(d.width, 1000);
                }
                // Same for height - lock to 700px floor to prevent vertical jitter
                if (getParent() != null && getParent().getHeight() < 600) {
                    d.height = Math.max(d.height, 700);
                }
                return d;
            }
            @Override public Dimension getPreferredScrollableViewportSize() { return getPreferredSize(); }
            @Override public int getScrollableUnitIncrement(Rectangle visibleRect, int orientation, int direction) { return 16; }
            @Override public int getScrollableBlockIncrement(Rectangle visibleRect, int orientation, int direction) { return 100; }
            @Override public boolean getScrollableTracksViewportWidth() { 
                // Tracking is true by default (responsive squash). 
                // We only return false (switch to scroll) if the window is crushed below 800px.
                return getParent().getWidth() > 800; 
            }
            @Override public boolean getScrollableTracksViewportHeight() { 
                // Tracking is true by default (no scrollbars).
                // We only allow vertical scrolling if the window goes below 600px height.
                return getParent().getHeight() > 600;
            }
        }

        // We cleanly use MigLayout Size Groups (sg) to mathematically link Row 1 and Row 2. 
        // This guarantees Sections 1,2,3,4 identically square out and match the tallest required height equally.
        // And Section 5 (Row 3) still retains 100px of minimum bottom space automatically.
        // Increase insets to 15 and row gaps to 10 to ensure all section borders (top/bottom) are perfectly visible
        JPanel mainPanel = new ScrollablePanel(new MigLayout("wrap 2, fill, insets 15", "[50%, fill][50%, fill]", "[sg 1, grow, fill]10[sg 1, grow, fill]10[100::, grow, fill]"));

        // Master Panel Content Sections
        InputSection inputSection = new InputSection();
        PreprocessingSection prepSection = new PreprocessingSection();
        FeatureSelectionSection featureSection = new FeatureSelectionSection();
        // The ExecutionSection now natively requires references to its sibling sections to extract their data for JSON generation
        ExecutionSection executionSection = new ExecutionSection(inputSection, prepSection, featureSection);
        
        // Reactive Link: Disable Run button if no files are selected
        inputSection.setOnFileChangeListener(() -> {
            boolean hasFiles = inputSection.hasFiles();
            executionSection.updateRunButtonState(hasFiles);
        });
        
        OutputSection outputSection = new OutputSection();

        // Connect Execution section to Output section so it can enable the buttons
        executionSection.setOutputSection(outputSection);

        // Map components perfectly back using un-distorted standard MigLayout proportional rules over raw grid spans
        mainPanel.add(inputSection.buildPanel(), "grow, shrink 100, h 0::");
        mainPanel.add(prepSection.buildPanel(), "grow, shrink 100, h 0::");

        mainPanel.add(featureSection.buildPanel(), "grow, shrink 100, h 0::");
        mainPanel.add(executionSection.buildPanel(), "grow, shrink 100, h 0::");

        mainPanel.add(outputSection.buildPanel(), "span 2, grow, shrink 0");

        JScrollPane scrollPane = new JScrollPane(mainPanel);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        
        // Restore master scrollbars (AS_NEEDED) to prevent content being lost when window is crushed
        scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        
        // Header Panel for Top-Right animated switch
        JPanel headerPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 20, 10));
        
        // Add our custom animated smooth pill switch
        ThemeSwitch themeSwitch = new ThemeSwitch();
        headerPanel.add(themeSwitch);

        // Composite wrapper to hold header on top, scrolling dashboard directly beneath
        JPanel wrapperPanel = new JPanel(new BorderLayout());
        wrapperPanel.add(headerPanel, BorderLayout.NORTH);
        wrapperPanel.add(scrollPane, BorderLayout.CENTER);

        setContentPane(wrapperPanel);
    }
}
