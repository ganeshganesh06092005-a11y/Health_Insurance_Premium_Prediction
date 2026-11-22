/**
 * HealthSecure Google Translate Integration & Multi-Language Optimization
 * 
 * Provides automated client-side translation across all webpage texts (Tamil, Hindi, English)
 * without altering backend routes, models, or database schemas.
 * Suppresses default Google banners and integrates directly with HealthSecure's custom UI dropdown.
 */
(function() {
    'use strict';

    var STORAGE_KEY = 'healthsecure_lang';
    var COOKIE_KEY = 'googtrans';

    var LANG_NAMES = {
        'en': 'English',
        'ta': 'தமிழ் (Tamil)',
        'hi': 'हिन्दी (Hindi)'
    };

    // 1. Helper to read cookie
    function getCookie(name) {
        var match = document.cookie.match(new RegExp('(^|;\\s*)(' + name + ')=([^;]*)'));
        return match ? decodeURIComponent(match[3]) : null;
    }

    // 2. Helper to set cookie across root and host domain
    function setCookie(name, val, days) {
        var expires = '';
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = '; expires=' + date.toUTCString();
        }
        var host = window.location.hostname;
        document.cookie = name + '=' + val + expires + '; path=/;';
        if (host && host.indexOf('.') !== -1) {
            document.cookie = name + '=' + val + expires + '; path=/; domain=' + host + ';';
        }
    }

    // 3. Clear googtrans cookies comprehensively across all domains and paths
    function clearAllGoogTransCookies() {
        var host = window.location.hostname;
        var domains = ['', host, '.' + host];
        if (host && host.indexOf('.') !== -1) {
            var parts = host.split('.');
            if (parts.length >= 2) {
                domains.push('.' + parts.slice(-2).join('.'));
            }
        }
        var paths = ['/', window.location.pathname];

        ['googtrans', 'googtrans_saved'].forEach(function(cname) {
            domains.forEach(function(d) {
                paths.forEach(function(p) {
                    var s = cname + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=' + p + ';';
                    if (d) s += ' domain=' + d + ';';
                    document.cookie = s;
                });
            });
        });
    }

    // Determine target initial language (localStorage is the source of truth)
    var savedLang = 'en';
    try {
        savedLang = localStorage.getItem(STORAGE_KEY) || 'en';
    } catch (e) {
        savedLang = 'en';
    }

    // If English, immediately eradicate any lingering googtrans cookies
    if (savedLang === 'en') {
        clearAllGoogTransCookies();
    } else {
        var cookieVal = getCookie(COOKIE_KEY);
        if (cookieVal) {
            var parts = cookieVal.split('/');
            if (parts.length >= 3 && parts[2]) {
                savedLang = parts[2];
            }
        }
        setCookie(COOKIE_KEY, '/en/' + savedLang, 30);
        setCookie(COOKIE_KEY, '/auto/' + savedLang, 30);
    }

    // 4. Define Google Translate Element Init Callback
    window.googleTranslateElementInit = function() {
        if (!window.google || !window.google.translate) return;
        new window.google.translate.TranslateElement({
            pageLanguage: 'en',
            includedLanguages: 'en,ta,hi',
            autoDisplay: false,
            layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE
        }, 'google_translate_element');

        // Apply saved language once combo box is available
        applyWhenComboReady(savedLang);
    };

    // 5. Inject Google Translate Library (loaded when a translation is requested)
    function initGoogleTranslate() {
        // Ensure container exists
        if (!document.getElementById('google_translate_element')) {
            var div = document.createElement('div');
            div.id = 'google_translate_element';
            div.style.display = 'none';
            document.body.appendChild(div);
        }

        // Only inject Google script if non-English translation is active
        if (savedLang !== 'en') {
            if (!document.getElementById('google-translate-script')) {
                var s = document.createElement('script');
                s.id = 'google-translate-script';
                s.type = 'text/javascript';
                s.async = true;
                s.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
                document.head.appendChild(s);
            }
        }
    }

    function applyWhenComboReady(lang, attempts) {
        attempts = attempts || 0;
        if (attempts > 50) return; // 5 seconds max

        var combo = document.querySelector('.goog-te-combo');
        if (combo) {
            if (lang && lang !== 'en') {
                if (combo.value !== lang) {
                    combo.value = lang;
                    combo.dispatchEvent(new Event('change'));
                }
            } else if (lang === 'en') {
                if (combo.value && combo.value !== 'en') {
                    combo.value = '';
                    combo.dispatchEvent(new Event('change'));
                }
            }
            updateCustomUI(lang || 'en');
        } else {
            setTimeout(function() {
                applyWhenComboReady(lang, attempts + 1);
            }, 100);
        }
    }

    // 6. Global API: Change Language Programmatically
    window.changeLanguage = function(langCode, event) {
        if (event && event.preventDefault) {
            event.preventDefault();
        }

        langCode = (langCode || 'en').toLowerCase();
        savedLang = langCode;

        try {
            localStorage.setItem(STORAGE_KEY, langCode);
        } catch (e) {}

        // Close any open dropdowns immediately
        document.querySelectorAll('.lang-dropdown.open').forEach(function(d) {
            d.classList.remove('open');
        });

        // Immediate visual update on button
        updateCustomUI(langCode);

        if (langCode === 'en') {
            clearAllGoogTransCookies();

            var combo = document.querySelector('.goog-te-combo');
            if (combo) {
                combo.value = '';
                combo.dispatchEvent(new Event('change'));
            }

            // Sync with backend session and cleanly reload in English
            fetch('/set-language/en', { credentials: 'same-origin' })
                .then(function() {
                    clearAllGoogTransCookies();
                    window.location.reload();
                })
                .catch(function() {
                    clearAllGoogTransCookies();
                    window.location.href = '/set-language/en';
                });
        } else {
            setCookie(COOKIE_KEY, '/en/' + langCode, 30);
            setCookie(COOKIE_KEY, '/auto/' + langCode, 30);

            // Sync with backend session and cleanly reload in target language
            fetch('/set-language/' + langCode, { credentials: 'same-origin' })
                .then(function() {
                    window.location.reload();
                })
                .catch(function() {
                    window.location.href = '/set-language/' + langCode;
                });
        }
    };

    // 7. Update Custom HealthSecure Dropdown UI
    function updateCustomUI(langCode) {
        var title = LANG_NAMES[langCode] || 'English';
        var dropbtns = document.querySelectorAll('.lang-dropbtn, .landing-lang-btn');
        dropbtns.forEach(function(btn) {
            btn.innerHTML = '🌐 ' + title + ' <span class="lang-chevron">▾</span>';
        });

        // Update active class on dropdown links
        var links = document.querySelectorAll('.lang-dropdown-content a, .landing-lang-dropdown a');
        links.forEach(function(link) {
            var href = link.getAttribute('href') || '';
            var onclickVal = link.getAttribute('onclick') || '';
            if (href.indexOf('/' + langCode) !== -1 || onclickVal.indexOf("'" + langCode + "'") !== -1) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // 8. Interactive Dropdown Toggle Setup (Click, Touch, Outside Click, Keyboard)
    function setupDropdownToggles() {
        document.querySelectorAll('.lang-dropbtn').forEach(function(btn) {
            btn.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                var parent = btn.closest('.lang-dropdown');
                if (!parent) return;
                var isOpen = parent.classList.contains('open');
                document.querySelectorAll('.lang-dropdown.open').forEach(function(d) {
                    if (d !== parent) d.classList.remove('open');
                });
                parent.classList.toggle('open', !isOpen);
            };
        });

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.lang-dropdown')) {
                document.querySelectorAll('.lang-dropdown.open').forEach(function(d) {
                    d.classList.remove('open');
                });
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.lang-dropdown.open').forEach(function(d) {
                    d.classList.remove('open');
                });
            }
        });
    }

    // 9. Initialize once DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initGoogleTranslate();
            setupDropdownToggles();
            updateCustomUI(savedLang);
        });
    } else {
        initGoogleTranslate();
        setupDropdownToggles();
        updateCustomUI(savedLang);
    }
})();
