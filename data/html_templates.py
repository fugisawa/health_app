"""HTML templates for custom components."""

def get_timer_template(state_class: str = "", time_display: str = "00:00") -> str:
    """Return HTML template for timer component."""
    return f"""
    <div class="timer-container">
        <div class="timer-display {state_class}">{time_display}</div>
        <div class="timer-controls">
            <button class="primary-button">Iniciar</button>
            <button class="secondary-button">Pausar</button>
        </div>
    </div>
    """

def get_exercise_card_template(
    title: str,
    badges: list[str],
    details: dict,
    controls: dict,
    notes: str = ""
) -> str:
    """Return HTML template for exercise card component."""
    badges_html = "".join([
        f'<span class="exercise-badge">{badge}</span>'
        for badge in badges
    ])
    
    details_html = "".join([
        f'<div class="detail-item"><span class="label">{k}:</span> {v}</div>'
        for k, v in details.items()
    ])
    
    return f"""
    <div class="exercise-card">
        <div class="exercise-header">
            <h3>{title}</h3>
            <div class="exercise-badges">{badges_html}</div>
        </div>
        <div class="exercise-content">
            <div class="exercise-details">{details_html}</div>
            <div class="exercise-controls">
                <button class="{controls.get('primary_class', 'primary-button')}">{controls.get('primary_text', 'Iniciar')}</button>
                <button class="{controls.get('secondary_class', 'secondary-button')}">{controls.get('secondary_text', 'Pular')}</button>
            </div>
        </div>
        {f'<div class="exercise-notes">{notes}</div>' if notes else ''}
    </div>
    """

def get_progress_bar_template(label: str, value: float) -> str:
    """Return HTML template for progress bar component."""
    return f"""
    <div class="progress-container">
        <div class="progress-label">
            <span>{label}</span>
            <span>{value}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {value}%"></div>
        </div>
    </div>
    """

def get_metric_card_template(
    icon: str,
    title: str,
    value: str,
    delta: str = "",
    description: str = ""
) -> str:
    """Return HTML template for metric card component."""
    delta_class = "positive" if delta.startswith("+") else "negative" if delta.startswith("-") else ""
    
    return f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-icon">{icon}</div>
            <h4>{title}</h4>
        </div>
        <div class="metric-value">
            {value}
            {f'<span class="metric-delta {delta_class}">{delta}</span>' if delta else ''}
        </div>
        {f'<div class="metric-footer">{description}</div>' if description else ''}
    </div>
    """

def get_session_summary_template(
    date: str,
    metrics: list[dict],
    notes: str = "",
    footer_buttons: list[dict] = None
) -> str:
    """Return HTML template for session summary component."""
    metrics_html = "".join([
        get_metric_card_template(**metric)
        for metric in metrics
    ])
    
    footer_html = ""
    if footer_buttons:
        buttons_html = "".join([
            f'<button class="{btn.get("class", "secondary-button")}">{btn.get("text", "")}</button>'
            for btn in footer_buttons
        ])
        footer_html = f'<div class="summary-footer">{buttons_html}</div>'
    
    return f"""
    <div class="session-summary">
        <div class="summary-header">
            <h3>Resumo da Sessão</h3>
            <span class="summary-date">{date}</span>
        </div>
        <div class="summary-metrics">{metrics_html}</div>
        {f'<div class="summary-notes"><h4>Notas</h4><p>{notes}</p></div>' if notes else ''}
        {footer_html}
    </div>
    """ 