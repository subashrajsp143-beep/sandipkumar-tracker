/**
 * M/S SANDIP KUMAR - 19 Sites Material Tracker
 * Bilingual Translation Engine (Hindi / English)
 * 1-Tap Language Switcher controlled from the TAP ICON in UP LEFT
 */

const AppTranslations = {
    // Current active language: 'hi' (Hindi) or 'en' (English)
    currentLang: localStorage.getItem('sandip_app_lang') || 'hi',

    // Dictionary of translation keys
    dictionary: {
        hi: {
            // Header & Navigation
            app_title: "M/S SANDIP KUMAR",
            app_subtitle: "19 Sites Material Tracker",
            nav_dashboard: "डैशबोर्ड",
            nav_stock: "📦 साइट स्टॉक (रजिस्टर)",
            nav_stock_short: "स्टॉक",
            nav_store: "🛒 सामग्री स्टोर",
            nav_daily_entry: "📝 दैनिक एंट्री",
            nav_attendance: "👥 हाजिरी (मैनपावर)",
            nav_attendance_short: "हाजिरी",
            nav_site_report: "साइट रिपोर्ट",
            nav_daily_report: "दैनिक रिपोर्ट",
            nav_monthly_report: "माहवार रिपोर्ट",
            nav_material_report: "सामग्री अनुसार",
            nav_item_history: "कब इस्तेमाल हुआ? (तारीख)",
            nav_matrix_report: "साइट्स मैट्रिक्स",
            nav_sites: "साइट्स",
            nav_materials: "सामग्री",
            nav_backup: "बैकअप",
            owner_login: "मालिक लॉगिन",
            owner_active: "👑 मालिक",
            owner_title: "मालिक लॉगिन (Owner Mode)",
            owner_pin_desc: "मास्टर कंट्रोल, कुल खर्चे और स्टॉक बदलाव के लिए 4 अंकों का पिन डालें:",
            unlock_btn: "लॉगिन करें (Unlock)",
            cancel_btn: "रद्द करें",
            close_btn: "बंद करें",
            save_btn: "सुरक्षित करें",
            submit_btn: "दर्ज करें",
            delete_btn: "हटाएं",
            edit_btn: "संपादित करें",
            search_placeholder: "खोजें...",
            filter_btn: "फ़िल्टर करें",
            print_btn: "प्रिंट करें",
            export_excel: "एक्सेल डाउनलोड",
            online_status: "ऑनलाइन (लाइव सिंक)",
            offline_status: "ऑफलाइन (स्थानीय सुरक्षित)",

            // Dashboard
            dash_banner_badge: "M/S SANDIP KUMAR • 19 Sites Live Project Tracker",
            dash_banner_title: "सामग्री खपत एवं साइट ट्रैकिंग",
            dash_banner_desc: "मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।",
            dash_btn_store: "🛒 सामग्री स्टोर (+ आइटम जोड़ें)",
            dash_btn_entry: "नई दैनिक एंट्री करें",
            dash_btn_site_report: "साइट-वार हिसाब देखें",
            dash_btn_matrix: "साइट्स मैट्रिक्स",
            dash_stock_card_title: "साइट स्टॉक व बैलेंस (Site Stock)",
            dash_stock_card_sub: "भेजा गया माल, रोज़ का खर्च और बचा स्टॉक (तारीख-वार लेजर)",
            dash_stock_open: "स्टॉक रजिस्टर खोलें",
            dash_att_card_title: "दैनिक मैनपावर हाजिरी (Attendance)",
            dash_att_card_sub: "मिस्त्री, प्लंबर, हेल्पर और स्टाफ की 21 साइट्स की दैनिक हाजिरी शीट",
            dash_att_open: "हाजिरी शीट खोलें",
            dash_stat_sites: "कुल साइट्स",
            dash_stat_materials: "कुल सामग्री",
            dash_stat_today_entries: "आज की एंट्रीज",
            dash_stat_7days_entries: "अंतिम 7 दिन में एंट्रीज",
            dash_recent_entries: "हाल की दैनिक सामग्री एंट्रीज (Recent Entries)",
            dash_site_summary: "साइट-वार सामग्री सारांश (Site Quick View)",

            // Stock Register Page
            stock_page_title: "📦 साइट स्टॉक व बैलेंस रजिस्टर",
            stock_page_subtitle: "19 साइट्स पर भेजा गया माल (Inward), रोज़ का खर्च (Daily Consumption) और बचा हुआ स्टॉक (Live Balance)",
            stock_btn_inward: "➕ नया माल भेजें (स्टॉक आवक)",
            stock_btn_reset: "⚠️ स्टॉक 0 करें (Reset)",
            stock_filter_site: "सभी साइट्स (All Sites)",
            stock_filter_category: "सभी श्रेणियां (All Categories)",
            stock_th_site: "साइट का नाम",
            stock_th_material: "सामग्री का नाम",
            stock_th_category: "श्रेणी / प्रकार",
            stock_th_inward: "कुल भेजा गया (आवक)",
            stock_th_used: "कुल खर्च (दैनिक खपत)",
            stock_th_balance: "बचा हुआ स्टॉक (बैलेंस)",
            stock_th_unit: "इकाई",
            stock_th_history: "तारीख-वार लेजर",
            stock_inward_modal_title: "📦 नया माल भेजें (Stock Inward Entry)",
            stock_inward_modal_desc: "गोदाम या सप्लायर से साइट पर माल भेजने का रिकॉर्ड दर्ज करें।",
            stock_reset_modal_title: "⚠️ साइट स्टॉक 0 करें (Reset to Zero)",
            stock_reset_modal_desc: "चुनी गई साइट या सभी साइट्स का भेजा गया माल और खपत 0 पर सेट करें।",
            stock_ledger_modal_title: "📋 तारीख-वार स्टॉक लेजर (Date-wise Ledger)",
            stock_ledger_modal_desc: "किस तारीख को कितना माल आया और कितना खर्च हुआ का पूरा ब्यौरा।",
            stock_pin_label: "मालिक का 4 अंकों का गुप्त पिन:",

            // Daily Entry Page
            entry_page_title: "📝 दैनिक सामग्री इस्तेमाल एंट्री (Roj Ka Kharch)",
            entry_page_subtitle: "साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें",
            entry_form_site: "साइट चुनें:",
            entry_form_date: "तारीख (Date):",
            entry_form_material: "सामग्री (Material):",
            entry_form_qty: "आज कितनी मात्रा लगी:",
            entry_form_remarks: "विवरण / कहाँ लगाया गया (Remarks):",
            entry_form_submit: "एंट्री सुरक्षित करें",

            // Attendance Page
            att_page_title: "👥 दैनिक मैनपावर हाजिरी रजिस्टर (Daily Attendance)",
            att_page_subtitle: "साइट्स पर काम कर रहे मिस्त्री, प्लंबर, हेल्पर और स्टाफ की उपस्थिति दर्ज करें",
            att_date_label: "तारीख चुनें:",
            att_save_btn: "हाजिरी सुरक्षित करें",
            att_mistry: "मिस्त्री (Mason)",
            att_plumber: "प्लंबर (Plumber)",
            att_helper: "हेल्पर (Helper)",
            att_staff: "स्टाफ / सुपरवाइजर",

            // Language Selector texts
            lang_selector_title: "भाषा चुनें / Select Language",
            lang_hi_title: "हिंदी (Hindi)",
            lang_hi_sub: "पूरा सिस्टम हिंदी में",
            lang_en_title: "English",
            lang_en_sub: "Complete system in English",
            lang_switch_toast_hi: "✅ भाषा बदलकर 'हिंदी' कर दी गई है।",
            lang_switch_toast_en: "✅ Language switched to 'English'."
        },

        en: {
            // Header & Navigation
            app_title: "M/S SANDIP KUMAR",
            app_subtitle: "19 Sites Material Tracker",
            nav_dashboard: "Dashboard",
            nav_stock: "📦 Site Stock Register",
            nav_stock_short: "Stock",
            nav_store: "🛒 Material Store",
            nav_daily_entry: "📝 Daily Entry",
            nav_attendance: "👥 Attendance (Manpower)",
            nav_attendance_short: "Attendance",
            nav_site_report: "Site Report",
            nav_daily_report: "Daily Report",
            nav_monthly_report: "Monthly Report",
            nav_material_report: "Material Wise",
            nav_item_history: "Usage History (Date)",
            nav_matrix_report: "Sites Matrix",
            nav_sites: "Sites",
            nav_materials: "Materials",
            nav_backup: "Backup",
            owner_login: "Owner Login",
            owner_active: "👑 Owner",
            owner_title: "Owner Mode (Admin PIN)",
            owner_pin_desc: "Enter 4-digit PIN for master control, total costs, and stock modifications:",
            unlock_btn: "Login (Unlock)",
            cancel_btn: "Cancel",
            close_btn: "Close",
            save_btn: "Save",
            submit_btn: "Submit",
            delete_btn: "Delete",
            edit_btn: "Edit",
            search_placeholder: "Search...",
            filter_btn: "Filter",
            print_btn: "Print",
            export_excel: "Export Excel",
            online_status: "Online (Live Sync)",
            offline_status: "Offline (Saved locally)",

            // Dashboard
            dash_banner_badge: "M/S SANDIP KUMAR • 19 Sites Live Project Tracker",
            dash_banner_title: "Material Consumption & Site Tracking",
            dash_banner_desc: "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga.",
            dash_btn_store: "🛒 Material Store (+ Add Item)",
            dash_btn_entry: "New Daily Entry",
            dash_btn_site_report: "View Site-Wise Report",
            dash_btn_matrix: "Sites Matrix",
            dash_stock_card_title: "Site Stock & Balance Register",
            dash_stock_card_sub: "Dispatched stock, daily consumption, and remaining balance (Date-wise ledger)",
            dash_stock_open: "Open Stock Register",
            dash_att_card_title: "Daily Manpower Attendance",
            dash_att_card_sub: "Daily attendance sheet for Masons, Plumbers, Helpers, and Staff across 21 sites",
            dash_att_open: "Open Attendance Sheet",
            dash_stat_sites: "Total Sites",
            dash_stat_materials: "Master Materials",
            dash_stat_today_entries: "Today's Entries",
            dash_stat_7days_entries: "Last 7 Days Entries",
            dash_recent_entries: "Recent Material Entries",
            dash_site_summary: "Site-Wise Material Summary",

            // Stock Register Page
            stock_page_title: "📦 Site Stock & Balance Register",
            stock_page_subtitle: "Dispatched stock (Inward), daily consumption, and remaining stock (Live Balance) across all 19 sites",
            stock_btn_inward: "➕ Dispatch Inward Stock",
            stock_btn_reset: "⚠️ Reset Stock to 0",
            stock_filter_site: "All Sites",
            stock_filter_category: "All Categories",
            stock_th_site: "Site Name",
            stock_th_material: "Material Name",
            stock_th_category: "Category / Type",
            stock_th_inward: "Total Inward",
            stock_th_used: "Total Used (Consumed)",
            stock_th_balance: "Balance Stock",
            stock_th_unit: "Unit",
            stock_th_history: "Date-Wise Ledger",
            stock_inward_modal_title: "📦 Dispatch Inward Stock",
            stock_inward_modal_desc: "Record dispatch of materials from godown or supplier to site.",
            stock_reset_modal_title: "⚠️ Reset Site Stock to 0",
            stock_reset_modal_desc: "Reset inward and consumption quantities to 0 for selected site or all sites.",
            stock_ledger_modal_title: "📋 Date-Wise Stock Ledger",
            stock_ledger_modal_desc: "Complete history of material dispatches and daily consumptions with dates.",
            stock_pin_label: "Owner 4-digit Secret PIN:",

            // Daily Entry Page
            entry_page_title: "📝 Daily Material Consumption Entry",
            entry_page_subtitle: "Record material consumed at site with date, quantity, and work location",
            entry_form_site: "Select Site:",
            entry_form_date: "Date:",
            entry_form_material: "Material:",
            entry_form_qty: "Quantity Consumed Today:",
            entry_form_remarks: "Remarks / Location of Work:",
            entry_form_submit: "Save Entry",

            // Attendance Page
            att_page_title: "👥 Daily Manpower Attendance Register",
            att_page_subtitle: "Record daily attendance for Masons, Plumbers, Helpers, and Staff at sites",
            att_date_label: "Select Date:",
            att_save_btn: "Save Attendance",
            att_mistry: "Mason (Mistry)",
            att_plumber: "Plumber",
            att_helper: "Helper",
            att_staff: "Staff / Supervisor",

            // Language Selector texts
            lang_selector_title: "Select Language / भाषा चुनें",
            lang_hi_title: "हिंदी (Hindi)",
            lang_hi_sub: "Entire system in Hindi",
            lang_en_title: "English",
            lang_en_sub: "Complete system in English",
            lang_switch_toast_hi: "✅ भाषा बदलकर 'हिंदी' कर दी गई है।",
            lang_switch_toast_en: "✅ Language switched to 'English'."
        }
    },

    // Bilingual phrase pairs for automatic DOM text node replacement
    phrasePairs: [
        { en: "Dashboard", hi: "डैशबोर्ड" },
        { en: "Material Store", hi: "सामग्री स्टोर" },
        { en: "Daily Entry", hi: "दैनिक एंट्री" },
        { en: "Roj Ka Entry", hi: "दैनिक एंट्री" },
        { en: "Site Stock & Balance Register", hi: "साइट स्टॉक और बैलेंस रजिस्टर" },
        { en: "Site Stock & Balance", hi: "साइट स्टॉक व बैलेंस" },
        { en: "Site Stock", hi: "साइट स्टॉक" },
        { en: "Stock Register", hi: "स्टॉक रजिस्टर" },
        { en: "Daily Manpower Attendance", hi: "दैनिक साइट हाजिरी" },
        { en: "Attendance", hi: "हाजिरी" },
        { en: "Daily Report", hi: "दैनिक रिपोर्ट" },
        { en: "Site Report", hi: "साइट रिपोर्ट" },
        { en: "Monthly Report", hi: "माहवार रिपोर्ट" },
        { en: "Mahina-war", hi: "माहवार" },
        { en: "Material Wise", hi: "सामग्री अनुसार" },
        { en: "Usage History (Date)", hi: "कब इस्तेमाल हुआ? (तारीख)" },
        { en: "Kab Use Hua?", hi: "कब इस्तेमाल हुआ?" },
        { en: "Sites Matrix", hi: "साइट्स मैट्रिक्स" },
        { en: "Sites Directory", hi: "साइट्स सूची" },
        { en: "Material Master", hi: "सामग्री मास्टर" },
        { en: "Download Backup", hi: "बैकअप डाउनलोड" },
        { en: "Owner Login", hi: "मालिक लॉगिन" },
        { en: "Active Project Sites", hi: "सक्रिय प्रोजेक्ट साइट्स" },
        { en: "Total Sites", hi: "कुल साइट्स" },
        { en: "Kul Sites", hi: "कुल साइट्स" },
        { en: "Master Materials", hi: "कुल सामग्री" },
        { en: "Kul Samagri", hi: "कुल सामग्री" },
        { en: "Today's Entries", hi: "आज की एंट्रीज" },
        { en: "Aaj Ki Entries", hi: "आज की एंट्रीज" },
        { en: "Balance Stock", hi: "बचा हुआ स्टॉक" },
        { en: "Inward Stock", hi: "आवक स्टॉक" },
        { en: "Daily Consumption", hi: "दैनिक खपत" },
        { en: "Reset Stock to 0", hi: "स्टॉक 0 करें" },
        { en: "Date-wise Ledger", hi: "तारीख-वार लेजर" },
        { en: "View Date-wise Ledger", hi: "तारीख-वार लेजर देखें" },
        { en: "View Ledger", hi: "लेजर देखें" },
        { en: "Dispatch Inward Stock", hi: "साइट पर माल भेजें" },
        { en: "Dispatch stock to this site", hi: "इस साइट पर नया माल भेजें" },
        { en: "Export Excel", hi: "Excel डाउनलोड" },
        { en: "Select Site:", hi: "साइट चुनें:" },
        { en: "Search Material", hi: "सामान खोजें" },
        { en: "Total Inward", hi: "कुल भेजा गया (Inward)" },
        { en: "Total Used", hi: "कुल खर्च (Used)" },
        { en: "Site Balance", hi: "साइट पर शेष (Balance)" },
        { en: "Available %", hi: "उपलब्ध %" },
        { en: "Status", hi: "स्थिति" },
        { en: "Actions", hi: "एक्शन" },
        { en: "Material Name", hi: "सामग्री का नाम" },
        { en: "Site Name", hi: "साइट का नाम" },
        { en: "Category", hi: "श्रेणी" },
        { en: "Unit", hi: "इकाई" },
        { en: "Date", hi: "तारीख" },
        { en: "Quantity", hi: "मात्रा" },
        { en: "Remarks", hi: "विवरण" },
        { en: "Supervisor", hi: "सुपरवाइजर" },
        { en: "Total Manpower", hi: "कुल मैनपावर" },
        { en: "Mason & Plumber", hi: "मिस्त्री व प्लंबर" },
        { en: "Mason", hi: "मिस्त्री" },
        { en: "Plumber", hi: "प्लंबर" },
        { en: "Total Helpers", hi: "कुल हेल्पर्स" },
        { en: "Helper", hi: "हेल्पर" },
        { en: "Staff", hi: "स्टाफ" },
        { en: "Save Attendance", hi: "हाजिरी सेव करें" },
        { en: "All Sites", hi: "सभी साइट्स" },
        { en: "All 21 Sites", hi: "सभी 21 साइट्स" },
        { en: "Healthy Stock", hi: "पर्याप्त" },
        { en: "Low Stock", hi: "कम स्टॉक" },
        { en: "Out of Stock", hi: "खत्म" },
        { en: "Save", hi: "सुरक्षित करें" },
        { en: "Submit", hi: "दर्ज करें" },
        { en: "Cancel", hi: "रद्द करें" },
        { en: "Delete", hi: "हटाएं" },
        { en: "Edit", hi: "संपादित करें" },
        { en: "Print", hi: "प्रिंट करें" },
        { en: "Search", hi: "खोजें" },
        { en: "Online (Live Sync)", hi: "ऑनलाइन (लाइव सिंक)" },
        { en: "Offline (Saved locally)", hi: "ऑफलाइन (स्थानीय सुरक्षित)" }
    ],

    /**
     * Apply active language to the entire document
     */
    applyLanguage: function(lang) {
        if (!lang) lang = this.currentLang;
        if (lang !== 'hi' && lang !== 'en') lang = 'hi';

        this.currentLang = lang;
        localStorage.setItem('sandip_app_lang', lang);

        const dict = this.dictionary[lang];
        if (!dict) return;

        // 1. Update all elements with data-i18n
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key] !== undefined) {
                // If element has nested icon, preserve icon and update text
                const icon = el.querySelector('i');
                if (icon) {
                    const iconHTML = icon.outerHTML;
                    el.innerHTML = iconHTML + ' ' + dict[key];
                } else {
                    el.textContent = dict[key];
                }
            }
        });

        // 2. Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (dict[key]) el.placeholder = dict[key];
        });

        // 3. Update titles / tooltips
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            if (dict[key]) el.title = dict[key];
        });

        // 4. Update the Tap Icon in UP LEFT
        this.updateTapIconButton(lang);

        // 5. Automatic text walker for untagged elements
        this.walkAndTranslate(lang);

        // 6. Broadcast event for any page-specific custom tables/scripts
        window.dispatchEvent(new CustomEvent('appLanguageChanged', { detail: { lang } }));
    },

    /**
     * Update the visual display of the TAP ICON in UP LEFT
     */
    updateTapIconButton: function(lang) {
        const codeEl = document.getElementById('tapLangCode');
        const nameEl = document.getElementById('tapLangName');
        const checkHi = document.getElementById('langCheckHi');
        const checkEn = document.getElementById('langCheckEn');
        const optHi = document.getElementById('langOptHi');
        const optEn = document.getElementById('langOptEn');

        if (lang === 'hi') {
            if (codeEl) codeEl.textContent = 'HI';
            if (nameEl) nameEl.textContent = '🇮🇳 हिंदी';
            if (checkHi) checkHi.className = 'fa-solid fa-circle-check text-emerald-400 text-base';
            if (checkEn) checkEn.className = 'fa-regular fa-circle text-slate-500 text-base';
            if (optHi) optHi.className = 'w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-left text-xs font-bold transition bg-blue-900/80 border border-amber-400/70 text-white';
            if (optEn) optEn.className = 'w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-left text-xs font-bold transition hover:bg-slate-800 text-slate-300 border border-transparent';
        } else {
            if (codeEl) codeEl.textContent = 'EN';
            if (nameEl) nameEl.textContent = '🇬🇧 English';
            if (checkHi) checkHi.className = 'fa-regular fa-circle text-slate-500 text-base';
            if (checkEn) checkEn.className = 'fa-solid fa-circle-check text-emerald-400 text-base';
            if (optHi) optHi.className = 'w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-left text-xs font-bold transition hover:bg-slate-800 text-slate-300 border border-transparent';
            if (optEn) optEn.className = 'w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-left text-xs font-bold transition bg-blue-900/80 border border-amber-400/70 text-white';
        }
    },

    /**
     * Walk text nodes to translate common phrases automatically
     */
    walkAndTranslate: function(targetLang) {
        // Build regex / replacement mapping based on target language
        const pairs = this.phrasePairs;
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    // Skip script, style, input, textarea, and language selector dropdown
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    const tag = parent.tagName.toLowerCase();
                    if (tag === 'script' || tag === 'style' || tag === 'textarea' || tag === 'input') return NodeFilter.FILTER_REJECT;
                    if (parent.closest('#tapLangContainer') || parent.closest('#tapLangDropdown')) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let node;
        while (node = walker.nextNode()) {
            let val = node.nodeValue;
            if (!val || val.trim().length === 0) continue;

            for (let i = 0; i < pairs.length; i++) {
                const pair = pairs[i];
                if (targetLang === 'hi') {
                    // Replace English with Hindi
                    if (val.includes(pair.en)) {
                        val = val.replaceAll(pair.en, pair.hi);
                    }
                } else {
                    // Replace Hindi with English
                    if (val.includes(pair.hi)) {
                        val = val.replaceAll(pair.hi, pair.en);
                    }
                }
            }
            if (node.nodeValue !== val) {
                node.nodeValue = val;
            }
        }
    },

    /**
     * Show a quick non-intrusive toast notification
     */
    showToast: function(msg) {
        let toast = document.getElementById('langToastNotification');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'langToastNotification';
            toast.className = 'fixed top-20 left-1/2 transform -translate-x-1/2 bg-slate-900/95 border-2 border-amber-400 text-white px-5 py-2.5 rounded-2xl shadow-2xl z-50 text-xs font-bold flex items-center gap-2 transition-all duration-300';
            document.body.appendChild(toast);
        }
        toast.innerHTML = `<i class="fa-solid fa-language text-amber-300 text-base"></i> <span>${msg}</span>`;
        toast.style.display = 'flex';
        toast.style.opacity = '1';

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => { toast.style.display = 'none'; }, 300);
        }, 2200);
    }
};

/**
 * Toggle the Language Dropdown from the Tap Icon
 */
function toggleLanguageDropdown(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    const dropdown = document.getElementById('tapLangDropdown');
    const chevron = document.getElementById('tapLangChevron');
    if (!dropdown) return;

    const isHidden = dropdown.classList.contains('hidden');
    if (isHidden) {
        dropdown.classList.remove('hidden');
        if (chevron) chevron.style.transform = 'rotate(180deg)';
    } else {
        dropdown.classList.add('hidden');
        if (chevron) chevron.style.transform = 'rotate(0deg)';
    }
}

/**
 * Set application language to 'hi' or 'en'
 */
function setAppLanguage(lang, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    AppTranslations.applyLanguage(lang);

    // Close dropdown
    const dropdown = document.getElementById('tapLangDropdown');
    const chevron = document.getElementById('tapLangChevron');
    if (dropdown) dropdown.classList.add('hidden');
    if (chevron) chevron.style.transform = 'rotate(0deg)';

    // Show toast feedback
    const toastMsg = lang === 'hi' 
        ? AppTranslations.dictionary.hi.lang_switch_toast_hi 
        : AppTranslations.dictionary.en.lang_switch_toast_en;
    AppTranslations.showToast(toastMsg);
}

// Close language dropdown when clicking outside
document.addEventListener('click', function(e) {
    const container = document.getElementById('tapLangContainer');
    const dropdown = document.getElementById('tapLangDropdown');
    const chevron = document.getElementById('tapLangChevron');
    if (container && dropdown && !container.contains(e.target)) {
        dropdown.classList.add('hidden');
        if (chevron) chevron.style.transform = 'rotate(0deg)';
    }
});

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    const savedLang = localStorage.getItem('sandip_app_lang') || 'hi';
    AppTranslations.applyLanguage(savedLang);
});
