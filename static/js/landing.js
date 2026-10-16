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
    const previewLiquorSelect = document.getElementById('previewLiquor');
    const previewAgeInput = document.getElementById('previewAge');
    const previewBmiInput = document.getElementById('previewBmi');
    const previewScenarioPrice = document.getElementById('previewScenarioPrice');
    const previewDeltaBadge = document.getElementById('previewDeltaBadge');

    function updatePreviewCalc() {
        if (!previewScenarioPrice || !previewDeltaBadge) return;
        const base = 28500;
        const isSmoker = previewSmokerSelect ? previewSmokerSelect.value === 'yes' : true;
        const isLiquor = previewLiquorSelect ? previewLiquorSelect.value === 'yes' : true;
        const age = previewAgeInput ? parseInt(previewAgeInput.value) || 35 : 35;
        const bmi = previewBmiInput ? parseFloat(previewBmiInput.value) || 28.5 : 28.5;

        let estimated = 1200 + (age * 260) + (bmi * 125);
        if (isSmoker) {
            estimated += 17500 + (age * 130);
            if (bmi >= 30) estimated += 2400;
        }
        if (isLiquor) {
            estimated += 2200 + (age * 20);
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
    if (previewLiquorSelect) previewLiquorSelect.addEventListener('change', updatePreviewCalc);
    if (previewAgeInput) previewAgeInput.addEventListener('input', updatePreviewCalc);
    if (previewBmiInput) previewBmiInput.addEventListener('input', updatePreviewCalc);

    // Initial calculation if present
    updatePreviewCalc();

    // =========================================================================
    // 4. Hero Quick-Quote Widget Interactive Engine (Care & Star Health Style)
    // =========================================================================
    const heroAgeSlider = document.getElementById('heroAge');
    const heroAgeDisplay = document.getElementById('heroAgeDisplay');
    const heroEstPrice = document.getElementById('heroEstPrice');
    const heroEstMonth = document.getElementById('heroEstMonth');
    const heroEstYear = document.getElementById('heroEstYear');
    const memberPills = document.querySelectorAll('.member-pill');
    let currentMember = 'self';

    // Member Pills Click Handler
    memberPills.forEach(pill => {
        pill.addEventListener('click', (e) => {
            e.preventDefault();
            memberPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            currentMember = pill.getAttribute('data-member');

            // Intelligently adjust default age for parents/family
            if (currentMember === 'parents' && heroAgeSlider) {
                if (parseInt(heroAgeSlider.value) < 50) {
                    heroAgeSlider.value = 58;
                }
            } else if (currentMember === 'self' && heroAgeSlider) {
                if (parseInt(heroAgeSlider.value) > 50) {
                    heroAgeSlider.value = 28;
                }
            }
            updateHeroQuote();
        });
    });

    // Segmented Pill Radio Toggles
    const setupSegmentedRadios = (name) => {
        const radios = document.querySelectorAll(`input[name="${name}"]`);
        radios.forEach(radio => {
            radio.addEventListener('change', () => {
                radios.forEach(r => {
                    const label = r.closest('.pill-choice');
                    if (label) {
                        label.classList.toggle('active', r.checked);
                        if (r.value === 'yes') {
                            label.classList.toggle('risk-active', r.checked);
                        }
                    }
                });
                updateHeroQuote();
            });
        });
    };
    setupSegmentedRadios('smoker');
    setupSegmentedRadios('liquor');

    // Dynamic Calculation Function
    function updateHeroQuote() {
        if (!heroEstPrice || !heroEstMonth || !heroEstYear) return;

        const age = heroAgeSlider ? parseInt(heroAgeSlider.value) || 28 : 28;
        if (heroAgeDisplay) {
            heroAgeDisplay.textContent = age + ' Yrs';
        }

        const smokerRadio = document.querySelector('input[name="smoker"]:checked');
        const liquorRadio = document.querySelector('input[name="liquor"]:checked');
        const isSmoker = smokerRadio ? smokerRadio.value === 'yes' : false;
        const isLiquor = liquorRadio ? liquorRadio.value === 'yes' : false;

        // Actuarial regression approximation for instant quotes
        let baseAnnual = 3200 + (age * 115);
        if (age > 45) {
            baseAnnual += (age - 45) * 160;
        }

        // Tobacco surcharge
        if (isSmoker) {
            baseAnnual += 14500 + (age * 80);
        }

        // Alcohol surcharge
        if (isLiquor) {
            baseAnnual += 1800 + (age * 15);
        }

        // Member multiplier
        if (currentMember === 'spouse') {
            baseAnnual *= 1.75;
        } else if (currentMember === 'family') {
            baseAnnual *= 2.15;
        } else if (currentMember === 'parents') {
            baseAnnual *= 1.85;
        }

        const annualRounded = Math.round(baseAnnual / 10) * 10;
        const dailyRate = Math.max(12, Math.round(annualRounded / 365));
        const monthlyRate = Math.round(annualRounded / 12);

        heroEstPrice.innerHTML = '₹' + dailyRate.toLocaleString('en-IN') + ' <span class="est-per-unit">/ day</span>';
        heroEstMonth.textContent = '₹' + monthlyRate.toLocaleString('en-IN') + ' / mo';
        heroEstYear.textContent = '₹' + annualRounded.toLocaleString('en-IN') + ' / yr';
    }

    if (heroAgeSlider) {
        heroAgeSlider.addEventListener('input', updateHeroQuote);
        updateHeroQuote();
    }
});
