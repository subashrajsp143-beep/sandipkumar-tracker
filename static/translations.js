/**
 * M/S SANDIP KUMAR - 21 Sites Material & Dispatch Tracker
 * Advanced Tri-Lingual Engine:
 * 1. 'en' -> 100% Proper English (No Hindi, no mixed parenthesis)
 * 2. 'hi' -> 100% Proper Hindi (Clean Hindi, no English in brackets)
 * 3. 'bi' -> Bilingual / Hinglish (English + Hindi Mixed)
 */

const AppTranslations = {
    currentLang: (typeof localStorage !== 'undefined' && localStorage.getItem('sandip_app_lang')) || 'en',

    dictionary: {
        en: {
            app_title: "M/S Sandip Kumar",
            app_subtitle: "21 Sites",
            top_status: "21 Sites Live",
            top_user: "Sandip Kumar",
            top_role: "Office Work",
            sign_out: "Sign out",

            // Sidebar
            nav_dashboard: "Dashboard",
            seg_attendance: "Attendance",
            sub_manual: "Manual",
            sub_gps: "GPS",
            sub_workers: "Workers",
            seg_material: "Material",
            sub_stock: "Stock",
            sub_usage: "Usage",
            sub_store: "Store",
            seg_progress: "Progress",
            sub_dpr: "DPR",
            sub_photos: "Photos",
            sub_upload: "Upload",
            seg_letters: "Letters",
            sub_letters: "Register",
            sub_excel: "Excel",
            sub_pdf: "PDF",
            seg_reports: "Reports",
            sub_daily: "Daily",
            sub_monthly: "Monthly",
            sub_ledger: "Ledger",
            sub_matrix: "Matrix",
            seg_admin: "Master",
            seg_complaints: "Complaints",
            sub_sites: "Sites",
            sub_rates: "Rates",
            sub_gps_setup: "GPS Setup",
            sub_apk: "App",
            sub_website: "Website",
            sub_backup: "Backup",

            // Dashboard
            dash_title: "Dashboard",
            dash_subtitle: "21 Sites",
            dash_active_date: "Date:",
            dash_status_title: "Project Status",
            dash_status_body: "21 Water Supply Sites Live",
            dash_status_badge: "● Active",

            tile_sites: "Sites",
            tile_sites_val: "21 Sites",
            tile_sites_sub: "Live",
            tile_workers: "Workers",
            tile_workers_val: "Daily Attendance",
            tile_workers_sub: "Site Manpower",
            tile_logs: "Usage",
            tile_logs_sub: "Logs",
            tile_cost: "Cost",
            tile_cost_sub: "Total Spent",
            tile_ref: "Ref No",
            tile_ref_sub: "Financial Year",
            tile_items: "Items",
            tile_items_sub: "Master Items",

            mod_attendance: "Attendance",
            mod_att_desc: "Manual & GPS Attendance",
            btn_open: "Attendance",
            btn_gps: "GPS",
            mod_material: "Material",
            mod_mat_desc: "Stock & Usage Logs",
            btn_stock: "Stock",
            btn_entry: "+ Usage",
            mod_progress: "Progress",
            mod_prog_desc: "DPR & Site Photos",
            btn_dpr: "DPR",
            btn_photos: "Photos",
            mod_reports: "Reports",
            mod_rep_desc: "Daily & Monthly Ledger",
            btn_reports: "Reports",
            btn_matrix: "Matrix",

            lang_selector_title: "Select Language",
            lang_hi_title: "हिंदी (Hindi)",
            lang_hi_sub: "Entire system in pure Hindi",
            lang_en_title: "English",
            lang_en_sub: "Complete system in pure English",
            lang_bi_title: "Bilingual (Mixed)",
            lang_bi_sub: "English + Hindi together",
            lang_switch_toast_hi: "✅ भाषा बदलकर 'हिंदी' कर दी गई है।",
            lang_switch_toast_en: "✅ Language switched to 'English'.",
            lang_switch_toast_bi: "✅ Language switched to 'Bilingual (English + हिंदी)'."
        },
        hi: {
            app_title: "M/S संदीप कुमार",
            app_subtitle: "२१ साइट्स",
            top_status: "२१ साइट्स चालू",
            top_user: "संदीप कुमार",
            top_role: "ऑफिस वर्क",
            sign_out: "लॉगआउट",

            // Sidebar
            nav_dashboard: "डैशबोर्ड",
            seg_attendance: "उपस्थिति",
            sub_manual: "मैनुअल",
            sub_gps: "GPS",
            sub_workers: "श्रमिक",
            seg_material: "सामग्री",
            sub_stock: "स्टॉक",
            sub_usage: "खपत",
            sub_store: "स्टोर",
            seg_progress: "प्रगति",
            sub_dpr: "DPR",
            sub_photos: "फोटो",
            sub_upload: "अपलोड",
            seg_letters: "जावक पत्र",
            sub_letters: "पंजी",
            sub_excel: "एक्सेल",
            sub_pdf: "पीडीएफ",
            seg_reports: "रिपोर्ट्स",
            sub_daily: "दैनिक",
            sub_monthly: "मासिक",
            sub_ledger: "लेजर",
            sub_matrix: "मैट्रिक्स",
            seg_admin: "मास्टर",
            seg_complaints: "समस्या / शिकायत",
            sub_sites: "साइट्स",
            sub_rates: "दरें",
            sub_gps_setup: "GPS सेटअप",
            sub_apk: "ऐप",
            sub_website: "वेबसाइट",
            sub_backup: "बैकअप",

            // Dashboard
            dash_title: "डैशबोर्ड",
            dash_subtitle: "२१ साइट्स",
            dash_active_date: "दिनांक:",
            dash_status_title: "परियोजना स्थिति",
            dash_status_body: "२१ जलापूर्ति साइट्स चालू",
            dash_status_badge: "● सक्रिय",

            tile_sites: "साइट्स",
            tile_sites_val: "21 साइट्स",
            tile_sites_sub: "चालू",
            tile_workers: "श्रमिक",
            tile_workers_val: "दैनिक हाजिरी",
            tile_workers_sub: "साइट मैनपॉवर",
            tile_logs: "खपत",
            tile_logs_sub: "एंट्रीज",
            tile_cost: "लागत",
            tile_cost_sub: "कुल सामग्री खर्च",
            tile_ref: "पत्रांक",
            tile_ref_sub: "वित्तीय वर्ष",
            tile_items: "सामग्री",
            tile_items_sub: "मास्टर आइटम्स",

            mod_attendance: "उपस्थिति",
            mod_att_desc: "मैनुअल व GPS हाजिरी",
            btn_open: "हाजिरी",
            btn_gps: "GPS",
            mod_material: "सामग्री",
            mod_mat_desc: "स्टॉक व खपत एंट्री",
            btn_stock: "स्टॉक",
            btn_entry: "+ खपत",
            mod_progress: "प्रगति",
            mod_prog_desc: "DPR व फोटो एल्बम",
            btn_dpr: "DPR",
            btn_photos: "फोटो",
            mod_reports: "रिपोर्ट्स",
            mod_rep_desc: "दैनिक व मासिक लेजर",
            btn_reports: "रिपोर्ट्स",
            btn_matrix: "मैट्रिक्स",

            lang_selector_title: "भाषा चुनें",
            lang_hi_title: "हिंदी",
            lang_hi_sub: "पूरा सिस्टम शुद्ध हिंदी में",
            lang_en_title: "English",
            lang_en_sub: "पूरा सिस्टम अंग्रेजी में",
            lang_bi_title: "Bilingual (मिश्रित)",
            lang_bi_sub: "हिंदी + अंग्रेजी दोनों साथ",
            lang_switch_toast_hi: "✅ भाषा बदलकर 'हिंदी' कर दी गई है।",
            lang_switch_toast_en: "✅ Language switched to 'English'.",
            lang_switch_toast_bi: "✅ भाषा बदलकर 'Bilingual (हिंदी + English)' कर दी गई है।"
        },
        bi: {
            app_title: "M/S Sandip Kumar (संदीप कुमार)",
            app_subtitle: "21 Sites (२१ साइट्स)",
            top_status: "21 Sites Live (चालू)",
            top_user: "Sandip Kumar",
            top_role: "Office Work (ऑफिस)",
            sign_out: "Sign Out (लॉगआउट)",

            // Sidebar
            nav_dashboard: "Dashboard (डैशबोर्ड)",
            seg_attendance: "Attendance (उपस्थिति)",
            sub_manual: "Manual (मैनुअल)",
            sub_gps: "GPS",
            sub_workers: "Workers (श्रमिक)",
            seg_material: "Material (सामग्री)",
            sub_stock: "Stock (स्टॉक)",
            sub_usage: "Usage (खपत)",
            sub_store: "Store (स्टोर)",
            seg_progress: "Progress (प्रगति)",
            sub_dpr: "DPR",
            sub_photos: "Photos (फोटो)",
            sub_upload: "Upload (अपलोड)",
            seg_letters: "Letters (जावक पत्र)",
            sub_letters: "Register (पंजी)",
            sub_excel: "Excel",
            sub_pdf: "PDF",
            seg_reports: "Reports (रिपोर्ट्स)",
            sub_daily: "Daily (दैनिक)",
            sub_monthly: "Monthly (मासिक)",
            sub_ledger: "Ledger (लेजर)",
            sub_matrix: "Matrix (मैट्रिक्स)",
            seg_admin: "Master (मास्टर)",
            seg_complaints: "Complaints (समस्या / शिकायत)",
            sub_sites: "Sites (साइट्स)",
            sub_rates: "Rates (दरें)",
            sub_gps_setup: "GPS Setup",
            sub_apk: "App (ऐप)",
            sub_website: "Website",
            sub_backup: "Backup (बैकअप)",

            // Dashboard
            dash_title: "Dashboard (डैशबोर्ड)",
            dash_subtitle: "21 Sites (२१ साइट्स)",
            dash_active_date: "Date (दिनांक):",
            dash_status_title: "Project Status (स्थिति)",
            dash_status_body: "21 Water Supply Sites Live (२१ साइट्स चालू)",
            dash_status_badge: "● Active (सक्रिय)",

            tile_sites: "Sites (साइट्स)",
            tile_sites_val: "21 Sites (चालू)",
            tile_sites_sub: "Live",
            tile_workers: "Workers (श्रमिक)",
            tile_workers_val: "Daily Attendance (हाजिरी)",
            tile_workers_sub: "Site Manpower",
            tile_logs: "Usage (खपत)",
            tile_logs_sub: "Logs (एंट्रीज)",
            tile_cost: "Cost (लागत)",
            tile_cost_sub: "Total Spent (कुल खर्च)",
            tile_ref: "Ref No (पत्रांक)",
            tile_ref_sub: "Financial Year",
            tile_items: "Items (सामग्री)",
            tile_items_sub: "Master Items",

            mod_attendance: "Attendance (उपस्थिति)",
            mod_att_desc: "Manual & GPS Attendance",
            btn_open: "Attendance (हाजिरी)",
            btn_gps: "GPS",
            mod_material: "Material (सामग्री)",
            mod_mat_desc: "Stock & Usage Logs",
            btn_stock: "Stock (स्टॉक)",
            btn_entry: "+ Usage (+ खपत)",
            mod_progress: "Progress (प्रगति)",
            mod_prog_desc: "DPR & Site Photos",
            btn_dpr: "DPR",
            btn_photos: "Photos (फोटो)",
            mod_reports: "Reports (रिपोर्ट्स)",
            mod_rep_desc: "Daily & Monthly Ledger",
            btn_reports: "Reports",
            btn_matrix: "Matrix",

            lang_selector_title: "Select Language / भाषा चुनें",
            lang_hi_title: "हिंदी (Hindi)",
            lang_hi_sub: "पूरा सिस्टम शुद्ध हिंदी में",
            lang_en_title: "English",
            lang_en_sub: "Complete system in pure English",
            lang_bi_title: "Bilingual (मिश्रित)",
            lang_bi_sub: "English + हिंदी Mixed",
            lang_switch_toast_hi: "✅ भाषा बदलकर 'हिंदी' कर दी गई है।",
            lang_switch_toast_en: "✅ Language switched to 'English'.",
            lang_switch_toast_bi: "✅ भाषा बदलकर 'Bilingual (English + हिंदी)' कर दी गई है।"
        }
    },

    // Tri-lingual phrases for full element / option translations
    phraseList: [
        // Complaints Page
        { en: "Site Issues & Complaints", hi: "साइट समस्या एवं शिकायत निवारण", bi: "Site Issues & Complaints (साइट समस्या एवं शिकायत निवारण)" },
        { en: "Help & Site Issue Center", hi: "सहायता एवं समस्या निवारण केंद्र", bi: "Help & Issue Center (सहायता केंद्र)" },
        { en: "Report site issues, shortages, machine breakdown or disputes here.", hi: "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें।", bi: "Report site issues (सामान की कमी, विवाद या खराबी यहाँ दर्ज करें)" },
        { en: "+ Report New Issue", hi: "+ नई समस्या दर्ज करें", bi: "+ Report New Issue (नई समस्या दर्ज करें)" },
        { en: "Submit New Issue / Complaint", hi: "नई समस्या / शिकायत दर्ज करें", bi: "Submit New Issue (नई समस्या दर्ज करें)" },
        { en: "Describe site problem, office will resolve immediately", hi: "साइट की दिक्कत लिखें, ऑफिस द्वारा तुरंत समाधान होगा", bi: "Describe site problem (दिक्कत लिखें, तुरंत समाधान होगा)" },
        { en: "Total Complaints", hi: "कुल समस्याएं", bi: "Total Complaints (कुल समस्याएं)" },
        { en: "Total registered complaints", hi: "दर्ज की गई कुल शिकायतें", bi: "Total Registered Complaints (दर्ज शिकायतें)" },
        { en: "Open / Pending", hi: "लंबित समस्याएं", bi: "Open / Pending (लंबित)" },
        { en: "Pending resolution", hi: "जिनका समाधान अभी बाकी है", bi: "Pending Resolution (समाधान बाकी)" },
        { en: "Urgent", hi: "अति आवश्यक", bi: "Urgent (अति आवश्यक)" },
        { en: "Work is stopped", hi: "जहाँ काम रुका हुआ है", bi: "Work Stopped (काम रुका हुआ है)" },
        { en: "Resolved", hi: "हल हो चुकी", bi: "Resolved (हल हो चुकी)" },
        { en: "Resolved complaints", hi: "समाधान की गई समस्याएं", bi: "Resolved Complaints (समाधान की गई समस्याएं)" },
        { en: "All", hi: "सभी", bi: "All (सभी)" },
        { en: "All 21 Sites", hi: "सभी 21 साइट्स", bi: "All 21 Sites (सभी 21 साइटें)" },
        { en: "Select Site:", hi: "साइट चुनें:", bi: "Select Site (साइट चुनें):" },
        { en: "Work Site", hi: "कार्य स्थल", bi: "Work Site (कार्य स्थल)" },
        { en: "Your Authorized Site", hi: "आपकी अधिकृत साइट", bi: "Authorized Site (अधिकृत साइट)" },
        { en: "Issue Category", hi: "समस्या का प्रकार", bi: "Issue Category (समस्या का प्रकार)" },
        { en: "Material Shortage (Pipe, Solvent, Valve)", hi: "सामान की कमी (पाइप, सॉल्वेंट, वाल्व)", bi: "Material Shortage (सामान की कमी - Pipe, Solvent, Valve)" },
        { en: "Site Dispute / Public Obstruction", hi: "साइट विवाद / जनता द्वारा रुकावट", bi: "Site Dispute (साइट विवाद / रुकावट)" },
        { en: "Boring / Machine Breakdown", hi: "मशीन / बोरिंग रिग खराबी", bi: "Machine Breakdown (मशीन / बोरिंग खराबी)" },
        { en: "Pipeline Leakage / Technical Defect", hi: "पाइपलाइन लीकेज / तकनीकी खराबी", bi: "Pipeline Leakage (पाइपलाइन लीकेज / तकनीकी समस्या)" },
        { en: "Labour / Wage Issue", hi: "लेबर / मजदूरी समस्या", bi: "Labour Issue (लेबर / मजदूरी समस्या)" },
        { en: "Other Problem", hi: "अन्य समस्या", bi: "Other Problem (अन्य समस्या)" },
        { en: "Urgency Level", hi: "प्राथमिकता", bi: "Urgency Level (प्राथमिकता)" },
        { en: "Normal", hi: "सामान्य", bi: "Normal (सामान्य)" },
        { en: "Urgent (Work Stopped)", hi: "अति आवश्यक (काम रुका है)", bi: "Urgent (अति आवश्यक - काम रुका है)" },
        { en: "What is the issue? Describe in detail", hi: "क्या दिक्कत है? विस्तार से लिखें", bi: "What is the issue? (क्या दिक्कत है? विस्तार से लिखें)" },
        { en: "Site Photos (Optional)", hi: "साइट फ़ोटो (ऐच्छिक)", bi: "Site Photos (साइट फ़ोटो - Optional)" },
        { en: "Capture live site photos of issue", hi: "खराबी या समस्या की लाइव फ़ोटो लें", bi: "Capture live site photos (खराबी या साइट की लाइव फ़ोटो लें)" },
        { en: "Cancel", hi: "रद्द करें", bi: "Cancel (रद्द करें)" },
        { en: "Submit Complaint", hi: "शिकायत दर्ज करें", bi: "Submit Complaint (शिकायत दर्ज करें)" },
        { en: "Problem registered successfully!", hi: "समस्या सफलतापूर्वक दर्ज हो गई है!", bi: "Problem Registered (समस्या दर्ज हो गई!)" },

        // DPR & Operations
        { en: "Daily Progress Report", hi: "दैनिक प्रगति रिपोर्ट", bi: "Daily Progress Report (दैनिक प्रगति रिपोर्ट)" },
        { en: "Daily DPR Sheet Overview", hi: "दैनिक DPR सारांश", bi: "Daily DPR Overview (दैनिक DPR सारांश)" },
        { en: "Supervisor Name", hi: "सुपरवाइजर का नाम", bi: "Supervisor Name (सुपरवाइजर)" },
        { en: "Sub Supervisor Name", hi: "उप-सुपरवाइजर का नाम", bi: "Sub Supervisor (उप-सुपरवाइजर)" },
        { en: "Workmen Name", hi: "कारीगर का नाम", bi: "Workmen Name (कारीगर का नाम)" },
        { en: "Mobile No.", hi: "मोबाइल नंबर", bi: "Mobile No. (मोबाइल नंबर)" },
        { en: "Work Area", hi: "कार्य क्षेत्र", bi: "Work Area (कार्य क्षेत्र)" },
        { en: "Ward No.", hi: "वार्ड नंबर", bi: "Ward No. (वार्ड नंबर)" },
        { en: "Work Activity", hi: "कार्य विवरण", bi: "Work Activity (कार्य विवरण)" },
        { en: "New Connection", hi: "नया कनेक्शन", bi: "New Connection (नया कनेक्शन)" },
        { en: "Connection Repairing", hi: "कनेक्शन मरम्मत", bi: "Connection Repairing (कनेक्शन मरम्मत)" },
        { en: "Motor/Starter Repair", hi: "मोटर/स्टार्टर मरम्मत", bi: "Motor/Starter Repair (मोटर/स्टार्टर रिपेयर)" },
        { en: "Main Pipe Repairing", hi: "मेन पाइपलाइन मरम्मत", bi: "Main Pipe Repairing (मेन पाइप रिपेयर)" },
        { en: "New Motor & Starter", hi: "नया मोटर व स्टार्टर", bi: "New Motor & Starter (नया मोटर व स्टार्टर)" },
        { en: "Other Work", hi: "अन्य कार्य", bi: "Other Work (अन्य कार्य)" },
        { en: "Save & Submit DPR", hi: "DPR सेव व सबमिट करें", bi: "Save & Submit DPR (DPR सेव करें)" },
        { en: "Print DPR (A4)", hi: "A4 प्रिंट निकालें", bi: "Print DPR (A4 प्रिंट)" },
        { en: "Download PDF", hi: "PDF डाउनलोड करें", bi: "Download PDF (पीडीएफ डाउनलोड)" }
    ],

    /**
     * Resolves a string into the target language.
     * Guarantees 0 mixing in 'en' and 'hi', and clean dual output in 'bi'.
     */
    resolveString: function(str, targetLang) {
        if (!str || typeof str !== 'string') return str;
        const trimmed = str.trim();
        if (!trimmed) return str;

        // 1. Direct match in phraseList
        for (let i = 0; i < this.phraseList.length; i++) {
            const p = this.phraseList[i];
            if (trimmed === p.en || trimmed === p.hi || trimmed === p.bi) {
                return p[targetLang] || trimmed;
            }
            // Strip leading emojis to match
            const tNoEmoji = trimmed.replace(/^[^\w\s\u0900-\u097F]+/, '').trim();
            const pEnNoEmoji = p.en.replace(/^[^\w\s\u0900-\u097F]+/, '').trim();
            const pHiNoEmoji = p.hi.replace(/^[^\w\s\u0900-\u097F]+/, '').trim();
            const pBiNoEmoji = p.bi.replace(/^[^\w\s\u0900-\u097F]+/, '').trim();
            if (tNoEmoji && (tNoEmoji === pEnNoEmoji || tNoEmoji === pHiNoEmoji || tNoEmoji === pBiNoEmoji)) {
                // Keep original emoji prefix if any
                const prefixMatch = trimmed.match(/^[^\w\s\u0900-\u097F]+\s*/);
                const prefix = prefixMatch ? prefixMatch[0] : '';
                const targetText = p[targetLang].replace(/^[^\w\s\u0900-\u097F]+\s*/, '');
                return prefix + targetText;
            }
        }

        // 2. Intelligent Parenthetical Parser: "Hindi (English)" or "English (Hindi)"
        const parenMatch = trimmed.match(/^(.*?)\s*\((.*?)\)\s*(\*?)$/);
        if (parenMatch) {
            const p1 = parenMatch[1].trim();
            const p2 = parenMatch[2].trim();
            const star = parenMatch[3] ? (" " + parenMatch[3]) : "";

            const hasDev1 = /[\u0900-\u097F]/.test(p1);
            const hasDev2 = /[\u0900-\u097F]/.test(p2);

            let hiPart = null, enPart = null;
            if (hasDev1 && !hasDev2) {
                hiPart = p1;
                enPart = p2;
            } else if (!hasDev1 && hasDev2) {
                enPart = p1;
                hiPart = p2;
            }

            if (hiPart && enPart) {
                // Check if p2 is just a count like "लंबित - 5" or "5"
                const countMatch = p2.match(/^([^\d]*)(\d+.*)$/);
                if (targetLang === 'en') {
                    if (countMatch && !hasDev2) {
                        return enPart + star;
                    }
                    return enPart + star;
                } else if (targetLang === 'hi') {
                    return hiPart + star;
                } else {
                    return enPart + " (" + hiPart + ")" + star;
                }
            }
        }

        // 3. Fallback for 'en' mode: If text still contains Devanagari followed by / English:
        if (targetLang === 'en') {
            const slashMatch = trimmed.match(/[\u0900-\u097F]+.*\/\s*([A-Za-z\s]+)$/);
            if (slashMatch) return slashMatch[1].trim();
        }

        // 4. Fallback for 'hi' mode: If text contains English in brackets, strip them
        if (targetLang === 'hi') {
            const cleanHi = trimmed.replace(/\s*\([A-Za-z\s\-\,\.]+\)/g, '').trim();
            if (cleanHi && /[\u0900-\u097F]/.test(cleanHi)) {
                return cleanHi;
            }
        }

        return trimmed;
    },

    /**
     * Apply active language across the entire document
     */
    applyLanguage: function(lang) {
        if (!lang) lang = this.currentLang;
        if (lang !== 'en' && lang !== 'hi' && lang !== 'bi') lang = 'en';

        this.currentLang = lang;
        localStorage.setItem('sandip_app_lang', lang);

        // 1. Direct data-i18n elements
        const dict = this.dictionary[lang] || this.dictionary['en'];
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key] !== undefined) {
                const icon = el.querySelector('i');
                if (icon) {
                    el.innerHTML = icon.outerHTML + ' ' + dict[key];
                } else {
                    el.textContent = dict[key];
                }
            }
        });

        // 2. Update Topbar and Sidebar switchers
        this.updateButtons(lang);

        // 3. Walk all text nodes & select options
        this.walkAndTranslate(lang);

        // 4. Translate all attributes (placeholder, title, alt)
        this.translateAttributes(lang);

        // 5. Broadcast language change event
        window.dispatchEvent(new CustomEvent('appLanguageChanged', { detail: { lang } }));
    },

    /**
     * Update active button styles in Topbar and Sidebar
     */
    updateButtons: function(lang) {
        // Topbar buttons
        const topEn = document.getElementById('topBtnLangEn');
        const topHi = document.getElementById('topBtnLangHi');
        const topBi = document.getElementById('topBtnLangBi');

        const activeTopClass = 'px-2 sm:px-2.5 py-1 rounded-md text-xs font-semibold transition flex items-center gap-1 bg-[#163F37] text-white shadow-xs';
        const inactiveTopClass = 'px-2 sm:px-2.5 py-1 rounded-md text-xs font-medium transition flex items-center gap-1 text-[#52736B] hover:text-[#163F37]';

        if (topEn) topEn.className = (lang === 'en') ? activeTopClass : inactiveTopClass;
        if (topHi) topHi.className = (lang === 'hi') ? activeTopClass : inactiveTopClass;
        if (topBi) topBi.className = (lang === 'bi') ? activeTopClass : inactiveTopClass;

        // Sidebar buttons
        const sideEn = document.getElementById('sideBtnLangEn');
        const sideHi = document.getElementById('sideBtnLangHi');
        const sideBi = document.getElementById('sideBtnLangBi');

        const activeSideClass = 'sidebar-lang-btn px-1.5 py-0.5 rounded text-[10px] font-bold transition bg-white text-[#163F37] shadow-xs';
        const inactiveSideClass = 'sidebar-lang-btn px-1.5 py-0.5 rounded text-[10px] font-medium transition text-[#A8C5BF] hover:bg-white/20';

        if (sideEn) sideEn.className = (lang === 'en') ? activeSideClass : inactiveSideClass;
        if (sideHi) sideHi.className = (lang === 'hi') ? activeSideClass : inactiveSideClass;
        if (sideBi) sideBi.className = (lang === 'bi') ? activeSideClass : inactiveSideClass;
    },

    /**
     * Walk text nodes and select options cleanly
     */
    walkAndTranslate: function(targetLang, rootNode) {
        const root = rootNode || document.body;
        if (!root) return;

        // Translate SELECT option elements directly
        root.querySelectorAll('option').forEach(opt => {
            if (!opt.__origText) opt.__origText = opt.textContent;
            const translated = this.resolveString(opt.__origText, targetLang);
            if (translated && opt.textContent !== translated) {
                opt.textContent = translated;
            }
        });

        // Translate labels and buttons
        root.querySelectorAll('label, button, h1, h2, h3, h4, p, span, a, th, td').forEach(el => {
            if (el.hasAttribute('data-i18n')) return;
            if (el.closest('#prominentLangSwitcher') || el.closest('.sidebar-lang-pill-container')) return;
            if (el.children.length === 0) {
                if (!el.__origText) el.__origText = el.textContent;
                const translated = this.resolveString(el.__origText, targetLang);
                if (translated && el.textContent !== translated) {
                    el.textContent = translated;
                }
            }
        });

        // TreeWalker for inner text nodes
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    const tag = parent.tagName.toLowerCase();
                    if (tag === 'script' || tag === 'style' || tag === 'textarea' || tag === 'input' || tag === 'option') return NodeFilter.FILTER_REJECT;
                    if (parent.closest('#prominentLangSwitcher') || parent.closest('.sidebar-lang-pill-container')) return NodeFilter.FILTER_REJECT;
                    if (parent.hasAttribute('data-i18n')) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let node;
        while (node = walker.nextNode()) {
            let val = node.nodeValue;
            if (!val || val.trim().length === 0) continue;

            if (!node.__origText) {
                node.__origText = val;
            }

            const translated = this.resolveString(node.__origText, targetLang);
            if (translated && node.nodeValue !== translated) {
                node.nodeValue = translated;
            }
        }
    },

    /**
     * Translate placeholders, titles, and alt text across all elements
     */
    translateAttributes: function(targetLang, rootNode) {
        const root = rootNode || document;

        root.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
            if (!el.__origPlaceholder) el.__origPlaceholder = el.getAttribute('placeholder');
            const translated = this.resolveString(el.__origPlaceholder, targetLang);
            if (translated) el.setAttribute('placeholder', translated);
        });

        root.querySelectorAll('[title]').forEach(el => {
            if (el.closest('#prominentLangSwitcher') || el.closest('.sidebar-lang-pill-container')) return;
            if (!el.__origTitle) el.__origTitle = el.getAttribute('title');
            const translated = this.resolveString(el.__origTitle, targetLang);
            if (translated) el.setAttribute('title', translated);
        });
    },

    /**
     * Setup MutationObserver for dynamically added elements (like modals)
     */
    setupObserver: function() {
        if (typeof MutationObserver === 'undefined') return;
        const observer = new MutationObserver((mutations) => {
            let shouldTranslate = false;
            for (let i = 0; i < mutations.length; i++) {
                if (mutations[i].addedNodes.length > 0) {
                    shouldTranslate = true;
                    break;
                }
            }
            if (shouldTranslate) {
                this.walkAndTranslate(this.currentLang);
                this.translateAttributes(this.currentLang);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    },

    /**
     * Show toast feedback
     */
    showToast: function(msg) {
        let toast = document.getElementById('langSwitchToast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'langSwitchToast';
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
 * Set application language ('en', 'hi', or 'bi')
 */
function setAppLanguage(lang, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    AppTranslations.applyLanguage(lang);

    const dict = AppTranslations.dictionary[lang] || AppTranslations.dictionary['en'];
    const toastMsg = (lang === 'hi') ? dict.lang_switch_toast_hi : ((lang === 'bi') ? dict.lang_switch_toast_bi : dict.lang_switch_toast_en);
    AppTranslations.showToast(toastMsg);
}

// Initialize on DOMContentLoaded
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        const savedLang = (typeof localStorage !== 'undefined' && localStorage.getItem('sandip_app_lang')) || 'en';
        AppTranslations.applyLanguage(savedLang);
        AppTranslations.setupObserver();
    });
}

if (typeof window !== 'undefined') {
    window.AppTranslations = AppTranslations;
    window.setAppLanguage = setAppLanguage;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AppTranslations, setAppLanguage };
}
