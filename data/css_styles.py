"""CSS styles for custom components."""

def get_component_styles() -> str:
    """Return CSS styles for custom components."""
    return """
    /* Timer Styles */
    .timer-container {
        background: var(--surface-primary);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .timer-display {
        font-family: 'Inter', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        letter-spacing: 0.05em;
    }
    
    .timer-display.warning {
        color: #FFA726;
    }
    
    .timer-display.danger {
        color: #EF5350;
    }
    
    .timer-controls {
        display: flex;
        gap: 1rem;
        justify-content: center;
    }
    
    /* Exercise Card Styles */
    .exercise-card {
        background: var(--surface-primary);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .exercise-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .exercise-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .exercise-badges {
        display: flex;
        gap: 0.5rem;
    }
    
    .exercise-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .exercise-content {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .exercise-notes {
        background: var(--surface-secondary);
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* Progress Bar Styles */
    .progress-container {
        margin-bottom: 1rem;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .progress-bar {
        height: 6px;
        background: var(--surface-secondary);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: var(--primary-button-bg);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Metric Card Styles */
    .metric-card {
        background: var(--surface-primary);
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid var(--border-color);
    }
    
    .metric-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .metric-icon {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--surface-secondary);
        border-radius: 8px;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }
    
    .metric-delta.positive {
        color: var(--success-button-bg);
    }
    
    .metric-delta.negative {
        color: #EF5350;
    }
    
    .metric-footer {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* Session Summary Styles */
    .session-summary {
        background: var(--surface-primary);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    .summary-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .summary-date {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .summary-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .summary-notes {
        background: var(--surface-secondary);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .summary-notes h4 {
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .summary-notes p {
        font-size: 0.875rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    .summary-footer {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
    }
    """ 