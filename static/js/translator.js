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
        document.cookie = name + '=' + encodeURIComponent(val) + expires + '; path=/;';
        if (host && host.indexOf('.') !== -1) {
            document.cookie = name + '=' + encodeURIComponent(val) + expires + '; path=/; domain=' + host + ';';
        }
    }

    function clearCookie(name) {
        var host = window.location.hostname;
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + host + ';';
        if (host && host.indexOf('.') !== -1) {
            var domainParts = host.split('.');
            if (domainParts.length >= 2) {
                var rootDomain = '.' + domainParts.slice(-2).join('.');
                document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + rootDomain + ';';
            }
        }
    }

    // Determine target initial language (localStorage > cookie > default 'en')
    var savedLang = 'en';
    try {
        savedLang = localStorage.getItem(STORAGE_KEY) || 'en';
    } catch (e) {
        savedLang = 'en';
    }

    var cookieVal = getCookie(COOKIE_KEY);
    if (cookieVal) {
        var parts = cookieVal.split('/');
        if (parts.length >= 3 && parts[2]) {
            savedLang = parts[2];
        }
    }

    // If a saved non-English language is set, guarantee cookie is primed before Google script loads
    if (savedLang && savedLang !== 'en') {
        setCookie(COOKIE_KEY, '/en/' + savedLang, 30);
        setCookie(COOKIE_KEY, '/auto/' + savedLang, 30);
    } else {
        clearCookie(COOKIE_KEY);
    }

    // 3. Define Google Translate Element Init Callback
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

    // 4. Inject Google Translate Library
    function initGoogleTranslate() {
        // Ensure container exists
        if (!document.getElementById('google_translate_element')) {
            var div = document.createElement('div');
            div.id = 'google_translate_element';
            div.style.display = 'none';
            document.body.appendChild(div);
        }

        // Add script if not already added
        if (!document.getElementById('google-translate-script')) {
            var s = document.createElement('script');
            s.id = 'google-translate-script';
            s.type = 'text/javascript';
            s.async = true;
            s.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
            document.head.appendChild(s);
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

    // 5. Global API: Change Language Programmatically
    window.changeLanguage = function(langCode, event) {
        if (event && event.preventDefault) {
            event.preventDefault();
        }

        langCode = (langCode || 'en').toLowerCase();
        var prevLang = savedLang;
        savedLang = langCode;

        try {
            localStorage.setItem(STORAGE_KEY, langCode);
        } catch (e) {}

        // Keep backend in sync asynchronously without full page navigation
        try {
            fetch('/set-language/' + langCode, { credentials: 'same-origin' }).catch(function() {});
        } catch (e) {}

        if (langCode === 'en') {
            clearCookie(COOKIE_KEY);
            setCookie(COOKIE_KEY, '', -1);
            
            // Trigger combo reset or reload if translating from another language
            var combo = document.querySelector('.goog-te-combo');
            if (combo) {
                combo.value = '';
                combo.dispatchEvent(new Event('change'));
            }
            if (prevLang && prevLang !== 'en') {
                // Smooth reload to guarantee complete restoration of English text nodes
                window.location.reload();
                return;
            }
        } else {
            setCookie(COOKIE_KEY, '/en/' + langCode, 30);
            setCookie(COOKIE_KEY, '/auto/' + langCode, 30);
            var combo = document.querySelector('.goog-te-combo');
            if (combo) {
                combo.value = langCode;
                combo.dispatchEvent(new Event('change'));
            } else {
                // If combo not ready yet, reload so Google reads the cookie on boot
                window.location.reload();
                return;
            }
        }

        updateCustomUI(langCode);
    };

    // 6. Update Custom HealthSecure Dropdown UI
    function updateCustomUI(langCode) {
        var title = LANG_NAMES[langCode] || 'English';
        var dropbtns = document.querySelectorAll('.lang-dropbtn, .landing-lang-btn');
        dropbtns.forEach(function(btn) {
            btn.innerHTML = '🌐 ' + title;
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

    // 7. Initialize once DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initGoogleTranslate();
            updateCustomUI(savedLang);
        });
    } else {
        initGoogleTranslate();
        updateCustomUI(savedLang);
    }
})();
