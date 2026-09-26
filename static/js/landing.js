/**
 * HealthSecure - Landing Page Interactive Scripts
 * Handles mobile drawer, FAQ accordion, smooth scrolling, and live simulation preview.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Navigation Toggle
    const mobileToggle = document.getElementById('navMobileToggle');
    const mobileMenu = document.getElementById('navMobileMenu');

    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
            const isOpen = mobileMenu.classList.contains('open');
            mobileToggle.setAttribute('aria-expanded', isOpen);
            mobileToggle.innerHTML = isOpen 
                ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>'
                : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>';
        });

        // Close menu on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                mobileToggle.setAttribute('aria-expanded', 'false');
                mobileToggle.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>';
            });
        });
    }

    // 2. FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const questionBtn = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');

        if (questionBtn && answer) {
            questionBtn.addEventListener('click', () => {
                const isOpen = item.classList.contains('open');

                // Close other items for single-accordion effect
                faqItems.forEach(other => {
                    if (other !== item && other.classList.contains('open')) {
                        other.classList.remove('open');
                        const otherAnswer = other.querySelector('.faq-answer');
                        if (otherAnswer) otherAnswer.style.maxHeight = null;
                    }
                });

                if (isOpen) {
                    item.classList.remove('open');
                    answer.style.maxHeight = null;
                } else {
                    item.classList.add('open');
                    answer.style.maxHeight = answer.scrollHeight + 30 + 'px';
                }
            });
        }
    });

    // 3. Interactive Scenario Simulation Preview Toggle
    const previewSmokerSelect = document.getElementById('previewSmoker');
    const previewAgeInput = document.getElementById('previewAge');
    const previewBmiInput = document.getElementById('previewBmi');
    const previewScenarioPrice = document.getElementById('previewScenarioPrice');
    const previewDeltaBadge = document.getElementById('previewDeltaBadge');

    function updatePreviewCalc() {
        if (!previewScenarioPrice || !previewDeltaBadge) return;
        const base = 28500;
        const isSmoker = previewSmokerSelect ? previewSmokerSelect.value === 'yes' : true;
        const age = previewAgeInput ? parseInt(previewAgeInput.value) || 35 : 35;
        const bmi = previewBmiInput ? parseFloat(previewBmiInput.value) || 28.5 : 28.5;

        let estimated = 1200 + (age * 260) + (bmi * 125);
        if (isSmoker) {
            estimated += 17500 + (age * 130);
            if (bmi >= 30) estimated += 2400;
        }

        estimated = Math.round(estimated);
        const diff = estimated - base;
        const diffPct = Math.round((diff / base) * 100);

        previewScenarioPrice.innerHTML = 'INR ' + estimated.toLocaleString('en-IN') + ' <span>/ year</span>';
        if (diff >= 0) {
            previewDeltaBadge.className = 'sim-delta-badge' + (diff > 5000 ? ' surcharge' : '');
            previewDeltaBadge.innerHTML = '▲ +INR ' + Math.abs(diff).toLocaleString('en-IN') + ' (' + (diffPct > 0 ? '+' : '') + diffPct + '%)';
        } else {
            previewDeltaBadge.className = 'sim-delta-badge savings';
            previewDeltaBadge.innerHTML = '▼ -INR ' + Math.abs(diff).toLocaleString('en-IN') + ' (' + diffPct + '%)';
        }
    }

    if (previewSmokerSelect) previewSmokerSelect.addEventListener('change', updatePreviewCalc);
    if (previewAgeInput) previewAgeInput.addEventListener('input', updatePreviewCalc);
    if (previewBmiInput) previewBmiInput.addEventListener('input', updatePreviewCalc);

    // Initial calculation if present
    updatePreviewCalc();
});
