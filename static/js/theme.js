/**
 * HealthSecure Dark / Light Mode Theme Engine
 * 
 * Automatically applies saved theme prior to DOM render to eliminate FOUC (flash of unstyled content).
 * Persists user preference to localStorage and updates theme toggle buttons.
 */
(function() {
    'use strict';

    var STORAGE_KEY = 'healthsecure_theme';

    // 1. Immediate theme application before DOM renders
    var savedTheme = 'light';
    try {
        savedTheme = localStorage.getItem(STORAGE_KEY) || 'light';
    } catch (e) {
        savedTheme = 'light';
    }
    document.documentElement.setAttribute('data-theme', savedTheme);

    // 2. Global toggle function
    window.toggleTheme = function() {
        var current = document.documentElement.getAttribute('data-theme') || 'light';
        var next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        try {
            localStorage.setItem(STORAGE_KEY, next);
        } catch (e) {}
        updateThemeUI(next);

        // Also notify any chart components to re-render if present
        if (window.dispatchEvent) {
            window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: next } }));
        }
    };

    function updateThemeUI(theme) {
        var toggles = document.querySelectorAll('.theme-toggle-btn, .landing-theme-btn');
        toggles.forEach(function(btn) {
            var icon = btn.querySelector('.theme-icon') || btn;
            var text = btn.querySelector('.theme-text');
            if (theme === 'dark') {
                btn.setAttribute('title', 'Switch to Light Mode');
                btn.setAttribute('aria-label', 'Switch to Light Mode');
                if (icon) icon.innerHTML = '☀️';
                if (text) text.textContent = 'Light Mode';
            } else {
                btn.setAttribute('title', 'Switch to Dark Mode');
                btn.setAttribute('aria-label', 'Switch to Dark Mode');
                if (icon) icon.innerHTML = '🌙';
                if (text) text.textContent = 'Dark Mode';
            }
        });
    }

    // 3. Initialize button states when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            updateThemeUI(document.documentElement.getAttribute('data-theme') || 'light');
        });
    } else {
        updateThemeUI(savedTheme);
    }
})();
