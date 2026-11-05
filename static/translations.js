/**
 * M/S SANDIP KUMAR - 21 Sites Material & Dispatch Tracker
 * Comprehensive Tri-Lingual Engine (All 21 Sites & All Segments)
 * 1. 'en' -> 100% Proper English (Zero Hindi, zero Devanagari in English mode)
 * 2. 'hi' -> 100% Proper Hindi (Clean Hindi, zero English in parens)
 * 3. 'bi' -> Bilingual (English + Hindi Mixed)
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

    // 1600+ Exact Phrase & Keyword Mappings across All Segments
    dictMap: {
  "m/s sandip kumar": {
    "en": "M/S Sandip Kumar",
    "hi": "मेसर्स संदीप कुमार",
    "bi": "M/S Sandip Kumar (मेसर्स संदीप कुमार)"
  },
  "मेसर्स संदीप कुमार": {
    "en": "M/S Sandip Kumar",
    "hi": "मेसर्स संदीप कुमार",
    "bi": "M/S Sandip Kumar (मेसर्स संदीप कुमार)"
  },
  "m/s sandip kumar (मेसर्स संदीप कुमार)": {
    "en": "M/S Sandip Kumar",
    "hi": "मेसर्स संदीप कुमार",
    "bi": "M/S Sandip Kumar (मेसर्स संदीप कुमार)"
  },
  "21 sites": {
    "en": "21 Sites",
    "hi": "21 साइट्स",
    "bi": "21 Sites (21 साइट्स)"
  },
  "21 साइट्स": {
    "en": "21 Sites",
    "hi": "21 साइट्स",
    "bi": "21 Sites (21 साइट्स)"
  },
  "21 sites (21 साइट्स)": {
    "en": "21 Sites",
    "hi": "21 साइट्स",
    "bi": "21 Sites (21 साइट्स)"
  },
  "21 sites live": {
    "en": "21 Sites Live",
    "hi": "21 साइट्स चालू",
    "bi": "21 Sites Live (21 साइट्स चालू)"
  },
  "21 साइट्स चालू": {
    "en": "21 Sites Live",
    "hi": "21 साइट्स चालू",
    "bi": "21 Sites Live (21 साइट्स चालू)"
  },
  "21 sites live (21 साइट्स चालू)": {
    "en": "21 Sites Live",
    "hi": "21 साइट्स चालू",
    "bi": "21 Sites Live (21 साइट्स चालू)"
  },
  "office work": {
    "en": "Office Work",
    "hi": "ऑफिस वर्क",
    "bi": "Office Work (कार्यालय कार्य)"
  },
  "ऑफिस वर्क": {
    "en": "Office Work",
    "hi": "ऑफिस वर्क",
    "bi": "Office Work (कार्यालय कार्य)"
  },
  "office work (कार्यालय कार्य)": {
    "en": "Office Work",
    "hi": "ऑफिस वर्क",
    "bi": "Office Work (कार्यालय कार्य)"
  },
  "sign out": {
    "en": "Sign out",
    "hi": "लॉगआउट",
    "bi": "Sign Out (लॉगआउट)"
  },
  "लॉगआउट": {
    "en": "Sign out",
    "hi": "लॉगआउट",
    "bi": "Sign Out (लॉगआउट)"
  },
  "sign out (लॉगआउट)": {
    "en": "Sign out",
    "hi": "लॉगआउट",
    "bi": "Sign Out (लॉगआउट)"
  },
  "language": {
    "en": "Language",
    "hi": "भाषा",
    "bi": "Language (भाषा)"
  },
  "भाषा": {
    "en": "Language",
    "hi": "भाषा",
    "bi": "Language (भाषा)"
  },
  "language (भाषा)": {
    "en": "Language",
    "hi": "भाषा",
    "bi": "Language (भाषा)"
  },
  "active": {
    "en": "Active",
    "hi": "सक्रिय",
    "bi": "Active (सक्रिय)"
  },
  "सक्रिय": {
    "en": "Active",
    "hi": "सक्रिय",
    "bi": "Active (सक्रिय)"
  },
  "active (सक्रिय)": {
    "en": "Active",
    "hi": "सक्रिय",
    "bi": "Active (सक्रिय)"
  },
  "inactive": {
    "en": "Inactive",
    "hi": "निष्क्रिय",
    "bi": "Inactive (निष्क्रिय)"
  },
  "निष्क्रिय": {
    "en": "Inactive",
    "hi": "निष्क्रिय",
    "bi": "Inactive (निष्क्रिय)"
  },
  "inactive (निष्क्रिय)": {
    "en": "Inactive",
    "hi": "निष्क्रिय",
    "bi": "Inactive (निष्क्रिय)"
  },
  "save": {
    "en": "Save",
    "hi": "सुरक्षित करें",
    "bi": "Save (सुरक्षित करें)"
  },
  "सुरक्षित करें": {
    "en": "Save",
    "hi": "सुरक्षित करें",
    "bi": "Save (सुरक्षित करें)"
  },
  "save (सुरक्षित करें)": {
    "en": "Save",
    "hi": "सुरक्षित करें",
    "bi": "Save (सुरक्षित करें)"
  },
  "submit": {
    "en": "Submit",
    "hi": "जमा करें",
    "bi": "Submit (जमा करें)"
  },
  "जमा करें": {
    "en": "Submit",
    "hi": "जमा करें",
    "bi": "Submit (जमा करें)"
  },
  "submit (जमा करें)": {
    "en": "Submit",
    "hi": "जमा करें",
    "bi": "Submit (जमा करें)"
  },
  "save & submit": {
    "en": "Save & Submit",
    "hi": "सुरक्षित व जमा करें",
    "bi": "Save & Submit (सुरक्षित व जमा करें)"
  },
  "सुरक्षित व जमा करें": {
    "en": "Save & Submit",
    "hi": "सुरक्षित व जमा करें",
    "bi": "Save & Submit (सुरक्षित व जमा करें)"
  },
  "save & submit (सुरक्षित व जमा करें)": {
    "en": "Save & Submit",
    "hi": "सुरक्षित व जमा करें",
    "bi": "Save & Submit (सुरक्षित व जमा करें)"
  },
  "cancel": {
    "en": "Cancel",
    "hi": "रद्द करें (Cancel)",
    "bi": "Cancel (रद्द करें)"
  },
  "रद्द करें": {
    "en": "Cancel",
    "hi": "रद्द करें",
    "bi": "Cancel (रद्द करें)"
  },
  "cancel (रद्द करें)": {
    "en": "Cancel",
    "hi": "रद्द करें (Cancel)",
    "bi": "Cancel (रद्द करें)"
  },
  "close": {
    "en": "Close",
    "hi": "बंद करें",
    "bi": "Close (बंद करें)"
  },
  "बंद करें": {
    "en": "Close",
    "hi": "बंद करें",
    "bi": "Close (बंद करें)"
  },
  "close (बंद करें)": {
    "en": "Close",
    "hi": "बंद करें",
    "bi": "Close (बंद करें)"
  },
  "delete": {
    "en": "Delete",
    "hi": "हटाएं",
    "bi": "Delete (हटाएं)"
  },
  "हटाएं": {
    "en": "Delete",
    "hi": "हटाएं",
    "bi": "Delete (हटाएं)"
  },
  "delete (हटाएं)": {
    "en": "Delete",
    "hi": "हटाएं",
    "bi": "Delete (हटाएं)"
  },
  "edit": {
    "en": "Edit",
    "hi": "संपादित करें",
    "bi": "Edit (बदलें)"
  },
  "संपादित करें": {
    "en": "Edit",
    "hi": "संपादित करें",
    "bi": "Edit (बदलें)"
  },
  "edit (बदलें)": {
    "en": "Edit",
    "hi": "संपादित करें",
    "bi": "Edit (बदलें)"
  },
  "actions": {
    "en": "Actions",
    "hi": "कार्रवाई",
    "bi": "Actions (कार्रवाई)"
  },
  "कार्रवाई": {
    "en": "Actions",
    "hi": "कार्रवाई",
    "bi": "Actions (कार्रवाई)"
  },
  "actions (कार्रवाई)": {
    "en": "Actions",
    "hi": "कार्रवाई",
    "bi": "Actions (कार्रवाई)"
  },
  "status": {
    "en": "Status",
    "hi": "स्थिति",
    "bi": "Status (स्थिति)"
  },
  "स्थिति": {
    "en": "Status",
    "hi": "स्थिति",
    "bi": "Status (स्थिति)"
  },
  "status (स्थिति)": {
    "en": "Status",
    "hi": "स्थिति",
    "bi": "Status (स्थिति)"
  },
  "date": {
    "en": "Date",
    "hi": "तारीख",
    "bi": "Date (तारीख)"
  },
  "तारीख": {
    "en": "Date",
    "hi": "तारीख",
    "bi": "Date (तारीख)"
  },
  "date (तारीख)": {
    "en": "Date",
    "hi": "तारीख",
    "bi": "Date (तारीख)"
  },
  "month": {
    "en": "Month",
    "hi": "महीना",
    "bi": "Month (महीना)"
  },
  "महीना": {
    "en": "Month",
    "hi": "महीना",
    "bi": "Month (महीना)"
  },
  "month (महीना)": {
    "en": "Month",
    "hi": "महीना",
    "bi": "Month (महीना)"
  },
  "all": {
    "en": "All",
    "hi": "सभी",
    "bi": "All (सभी)"
  },
  "सभी": {
    "en": "All",
    "hi": "सभी",
    "bi": "All (सभी)"
  },
  "all (सभी)": {
    "en": "All",
    "hi": "सभी",
    "bi": "All (सभी)"
  },
  "all sites": {
    "en": "All Sites",
    "hi": "सभी साइट्स",
    "bi": "All Sites (सभी साइट्स)"
  },
  "सभी साइट्स": {
    "en": "All Sites",
    "hi": "सभी साइट्स",
    "bi": "All Sites (सभी साइट्स)"
  },
  "all sites (सभी साइट्स)": {
    "en": "All Sites",
    "hi": "सभी साइट्स",
    "bi": "All Sites (सभी साइट्स)"
  },
  "all 21 sites": {
    "en": "All 21 Sites",
    "hi": "सभी 21 साइट्स",
    "bi": "All 21 Sites (सभी 21 साइट्स)"
  },
  "सभी 21 साइट्स": {
    "en": "All 21 Sites",
    "hi": "सभी 21 साइट्स",
    "bi": "All 21 Sites (सभी 21 साइट्स)"
  },
  "all 21 sites (सभी 21 साइट्स)": {
    "en": "All 21 Sites",
    "hi": "सभी 21 साइट्स",
    "bi": "All 21 Sites (सभी 21 साइट्स)"
  },
  "select site": {
    "en": "Select Site",
    "hi": "साइट चुनें",
    "bi": "Select Site (साइट चुनें)"
  },
  "साइट चुनें": {
    "en": "Select Site",
    "hi": "साइट चुनें",
    "bi": "Select Site (साइट चुनें)"
  },
  "select site (साइट चुनें)": {
    "en": "Select Site",
    "hi": "साइट चुनें",
    "bi": "Select Site (साइट चुनें)"
  },
  "-- select site --": {
    "en": "-- Select Site --",
    "hi": "-- साइट चुनें --",
    "bi": "-- Select Site (साइट चुनें) --"
  },
  "-- साइट चुनें --": {
    "en": "-- Select Site --",
    "hi": "-- साइट चुनें --",
    "bi": "-- Select Site (साइट चुनें) --"
  },
  "-- select site (साइट चुनें) --": {
    "en": "-- Select Site --",
    "hi": "-- साइट चुनें --",
    "bi": "-- Select Site (साइट चुनें) --"
  },
  "download pdf": {
    "en": "Download PDF",
    "hi": "PDF डाउनलोड करें",
    "bi": "Download PDF (PDF डाउनलोड)"
  },
  "pdf डाउनलोड करें": {
    "en": "Download PDF",
    "hi": "PDF डाउनलोड करें",
    "bi": "Download PDF (PDF डाउनलोड)"
  },
  "download pdf (pdf डाउनलोड)": {
    "en": "Download PDF",
    "hi": "PDF डाउनलोड करें",
    "bi": "Download PDF (PDF डाउनलोड)"
  },
  "export excel": {
    "en": "Export Excel",
    "hi": "Excel निकालें",
    "bi": "Export Excel (Excel निकालें)"
  },
  "excel निकालें": {
    "en": "Export Excel",
    "hi": "Excel निकालें",
    "bi": "Export Excel (Excel निकालें)"
  },
  "export excel (excel निकालें)": {
    "en": "Export Excel",
    "hi": "Excel निकालें",
    "bi": "Export Excel (Excel निकालें)"
  },
  "print": {
    "en": "Print",
    "hi": "प्रिंट निकालें",
    "bi": "Print (प्रिंट निकालें)"
  },
  "प्रिंट निकालें": {
    "en": "Print",
    "hi": "प्रिंट निकालें",
    "bi": "Print (प्रिंट निकालें)"
  },
  "print (प्रिंट निकालें)": {
    "en": "Print",
    "hi": "प्रिंट निकालें",
    "bi": "Print (प्रिंट निकालें)"
  },
  "search site...": {
    "en": "Search site...",
    "hi": "साइट खोजें...",
    "bi": "Search site (साइट खोजें)..."
  },
  "साइट खोजें...": {
    "en": "Search site...",
    "hi": "साइट खोजें...",
    "bi": "Search site (साइट खोजें)..."
  },
  "search site (साइट खोजें)...": {
    "en": "Search site...",
    "hi": "साइट खोजें...",
    "bi": "Search site (साइट खोजें)..."
  },
  "remarks": {
    "en": "Remarks",
    "hi": "टिप्पणी",
    "bi": "Remarks (टिप्पणी)"
  },
  "टिप्पणी": {
    "en": "Remarks",
    "hi": "टिप्पणी",
    "bi": "Remarks (टिप्पणी)"
  },
  "remarks (टिप्पणी)": {
    "en": "(Remarks)",
    "hi": "(टिप्पणी)",
    "bi": "Remarks (टिप्पणी)"
  },
  "notes": {
    "en": "Notes",
    "hi": "निर्देश",
    "bi": "Notes (निर्देश)"
  },
  "निर्देश": {
    "en": "Notes",
    "hi": "निर्देश",
    "bi": "Notes (निर्देश)"
  },
  "notes (निर्देश)": {
    "en": "Notes",
    "hi": "निर्देश",
    "bi": "Notes (निर्देश)"
  },
  "quantity": {
    "en": "Quantity",
    "hi": "मात्रा",
    "bi": "Quantity (मात्रा)"
  },
  "मात्रा": {
    "en": "Quantity",
    "hi": "मात्रा",
    "bi": "Quantity (मात्रा)"
  },
  "quantity (मात्रा)": {
    "en": "Quantity",
    "hi": "मात्रा",
    "bi": "Quantity (मात्रा)"
  },
  "unit": {
    "en": "Unit",
    "hi": "इकाई",
    "bi": "Unit (इकाई)"
  },
  "इकाई": {
    "en": "Unit",
    "hi": "इकाई",
    "bi": "Unit (इकाई)"
  },
  "unit (इकाई)": {
    "en": "Unit",
    "hi": "इकाई",
    "bi": "Unit (इकाई)"
  },
  "rate": {
    "en": "Rate",
    "hi": "दर",
    "bi": "Rate (दर)"
  },
  "दर": {
    "en": "Rate",
    "hi": "दर",
    "bi": "Rate (दर)"
  },
  "rate (दर)": {
    "en": "Rate",
    "hi": "दर",
    "bi": "Rate (दर)"
  },
  "amount": {
    "en": "Amount",
    "hi": "राशि",
    "bi": "Amount (राशि)"
  },
  "राशि": {
    "en": "Amount",
    "hi": "राशि",
    "bi": "Amount (राशि)"
  },
  "amount (राशि)": {
    "en": "Amount",
    "hi": "राशि",
    "bi": "Amount (राशि)"
  },
  "total": {
    "en": "Total",
    "hi": "कुल",
    "bi": "Total (कुल)"
  },
  "कुल": {
    "en": "Total",
    "hi": "कुल",
    "bi": "Total (कुल)"
  },
  "total (कुल)": {
    "en": "Total",
    "hi": "कुल",
    "bi": "Total (कुल)"
  },
  "success": {
    "en": "Success",
    "hi": "सफल",
    "bi": "Success (सफल)"
  },
  "सफल": {
    "en": "Success",
    "hi": "सफल",
    "bi": "Success (सफल)"
  },
  "success (सफल)": {
    "en": "Success",
    "hi": "सफल",
    "bi": "Success (सफल)"
  },
  "error": {
    "en": "Error",
    "hi": "त्रुटि",
    "bi": "Error (त्रुटि)"
  },
  "त्रुटि": {
    "en": "Error",
    "hi": "त्रुटि",
    "bi": "Error (त्रुटि)"
  },
  "error (त्रुटि)": {
    "en": "Error",
    "hi": "त्रुटि",
    "bi": "Error (त्रुटि)"
  },
  "warning": {
    "en": "Warning",
    "hi": "चेतावनी",
    "bi": "Warning (चेतावनी)"
  },
  "चेतावनी": {
    "en": "Warning",
    "hi": "चेतावनी",
    "bi": "Warning (चेतावनी)"
  },
  "warning (चेतावनी)": {
    "en": "Warning",
    "hi": "चेतावनी",
    "bi": "Warning (चेतावनी)"
  },
  "site issues & complaints": {
    "en": "Site Issues & Complaints",
    "hi": "साइट समस्या एवं शिकायत निवारण",
    "bi": "Site Issues & Complaints (साइट समस्या एवं शिकायत निवारण)"
  },
  "साइट समस्या एवं शिकायत निवारण": {
    "en": "Site Issues & Complaints",
    "hi": "साइट समस्या एवं शिकायत निवारण",
    "bi": "Site Issues & Complaints (साइट समस्या एवं शिकायत निवारण)"
  },
  "site issues & complaints (साइट समस्या एवं शिकायत निवारण)": {
    "en": "Site Issues & Complaints",
    "hi": "साइट समस्या एवं शिकायत निवारण",
    "bi": "Site Issues & Complaints (साइट समस्या एवं शिकायत निवारण)"
  },
  "help & site issue center": {
    "en": "Help & Site Issue Center",
    "hi": "सहायता एवं समस्या निवारण केंद्र",
    "bi": "Help & Site Issue Center (सहायता केंद्र)"
  },
  "सहायता एवं समस्या निवारण केंद्र": {
    "en": "Help & Site Issue Center",
    "hi": "सहायता एवं समस्या निवारण केंद्र",
    "bi": "Help & Site Issue Center (सहायता केंद्र)"
  },
  "help & site issue center (सहायता केंद्र)": {
    "en": "Help & Site Issue Center",
    "hi": "सहायता एवं समस्या निवारण केंद्र",
    "bi": "Help & Site Issue Center (सहायता केंद्र)"
  },
  "report site issues, shortages, machine breakdown or disputes here.": {
    "en": "Report site issues, shortages, machine breakdown or disputes here.",
    "hi": "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें।",
    "bi": "Report site issues (सामान की कमी, विवाद या खराबी यहाँ दर्ज करें)"
  },
  "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें।": {
    "en": "Report site issues, shortages, machine breakdown or disputes here.",
    "hi": "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें।",
    "bi": "Report site issues (सामान की कमी, विवाद या खराबी यहाँ दर्ज करें)"
  },
  "report site issues (सामान की कमी, विवाद या खराबी यहाँ दर्ज करें)": {
    "en": "Report site issues, shortages, machine breakdown or disputes here.",
    "hi": "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें।",
    "bi": "Report site issues (सामान की कमी, विवाद या खराबी यहाँ दर्ज करें)"
  },
  "+ report new issue": {
    "en": "+ Report New Issue",
    "hi": "+ नई समस्या दर्ज करें",
    "bi": "+ Report New Issue (नई समस्या दर्ज करें)"
  },
  "+ नई समस्या दर्ज करें": {
    "en": "+ Report New Issue",
    "hi": "+ नई समस्या दर्ज करें",
    "bi": "+ Report New Issue (नई समस्या दर्ज करें)"
  },
  "+ report new issue (नई समस्या दर्ज करें)": {
    "en": "+ Report New Issue",
    "hi": "+ नई समस्या दर्ज करें",
    "bi": "+ Report New Issue (नई समस्या दर्ज करें)"
  },
  "submit new issue / complaint": {
    "en": "Submit New Issue / Complaint",
    "hi": "नई समस्या / शिकायत दर्ज करें",
    "bi": "Submit New Issue (नई समस्या दर्ज करें)"
  },
  "नई समस्या / शिकायत दर्ज करें": {
    "en": "Submit New Issue / Complaint",
    "hi": "नई समस्या / शिकायत दर्ज करें",
    "bi": "Submit New Issue (नई समस्या दर्ज करें)"
  },
  "submit new issue (नई समस्या दर्ज करें)": {
    "en": "Submit New Issue / Complaint",
    "hi": "नई समस्या / शिकायत दर्ज करें",
    "bi": "Submit New Issue (नई समस्या दर्ज करें)"
  },
  "describe site problem, office will resolve immediately": {
    "en": "Describe site problem, office will resolve immediately",
    "hi": "साइट की दिक्कत लिखें, ऑफिस द्वारा तुरंत समाधान होगा",
    "bi": "Describe site problem (दिक्कत लिखें, तुरंत समाधान होगा)"
  },
  "साइट की दिक्कत लिखें, ऑफिस द्वारा तुरंत समाधान होगा": {
    "en": "Describe site problem, office will resolve immediately",
    "hi": "साइट की दिक्कत लिखें, ऑफिस द्वारा तुरंत समाधान होगा",
    "bi": "Describe site problem (दिक्कत लिखें, तुरंत समाधान होगा)"
  },
  "describe site problem (दिक्कत लिखें, तुरंत समाधान होगा)": {
    "en": "Describe site problem, head office will resolve immediately",
    "hi": "साइट की दिक्कत लिखें, ऑफिस तक तुरंत पहुँचेगी",
    "bi": "Describe site problem (दिक्कत लिखें, तुरंत समाधान होगा)"
  },
  "total complaints": {
    "en": "Total Complaints",
    "hi": "कुल समस्याएं",
    "bi": "Total Complaints (कुल समस्याएं)"
  },
  "कुल समस्याएं": {
    "en": "Total Complaints",
    "hi": "कुल समस्याएं",
    "bi": "Total Complaints (कुल समस्याएं)"
  },
  "total complaints (कुल समस्याएं)": {
    "en": "Total Complaints",
    "hi": "कुल समस्याएं",
    "bi": "Total Complaints (कुल समस्याएं)"
  },
  "total registered complaints": {
    "en": "Total registered complaints",
    "hi": "दर्ज की गई कुल शिकायतें",
    "bi": "Total Registered Complaints (दर्ज शिकायतें)"
  },
  "दर्ज की गई कुल शिकायतें": {
    "en": "Total registered complaints",
    "hi": "दर्ज की गई कुल शिकायतें",
    "bi": "Total Registered Complaints (दर्ज शिकायतें)"
  },
  "total registered complaints (दर्ज शिकायतें)": {
    "en": "Total registered complaints",
    "hi": "दर्ज की गई कुल शिकायतें",
    "bi": "Total Registered Complaints (दर्ज शिकायतें)"
  },
  "open / pending": {
    "en": "Open / Pending",
    "hi": "लंबित समस्याएं",
    "bi": "Open / Pending (लंबित)"
  },
  "लंबित समस्याएं": {
    "en": "Open / Pending",
    "hi": "लंबित समस्याएं",
    "bi": "Open / Pending (लंबित)"
  },
  "open / pending (लंबित)": {
    "en": "Open / Pending",
    "hi": "लंबित समस्याएं",
    "bi": "Open / Pending (लंबित)"
  },
  "pending resolution": {
    "en": "Pending resolution",
    "hi": "जिनका समाधान अभी बाकी है",
    "bi": "Pending Resolution (समाधान बाकी)"
  },
  "जिनका समाधान अभी बाकी है": {
    "en": "Pending resolution",
    "hi": "जिनका समाधान अभी बाकी है",
    "bi": "Pending Resolution (समाधान बाकी)"
  },
  "pending resolution (समाधान बाकी)": {
    "en": "Pending resolution",
    "hi": "जिनका समाधान अभी बाकी है",
    "bi": "Pending Resolution (समाधान बाकी)"
  },
  "urgent": {
    "en": "Urgent",
    "hi": "जरूरी",
    "bi": "Urgent (जरूरी)"
  },
  "अति आवश्यक": {
    "en": "Urgent",
    "hi": "अति आवश्यक",
    "bi": "Urgent (अति आवश्यक)"
  },
  "urgent (अति आवश्यक)": {
    "en": "Urgent",
    "hi": "अति आवश्यक",
    "bi": "Urgent (अति आवश्यक)"
  },
  "high priority issues": {
    "en": "High priority issues",
    "hi": "तुरंत ध्यान देने योग्य",
    "bi": "High Priority (तुरंत समाधान)"
  },
  "तुरंत ध्यान देने योग्य": {
    "en": "High priority issues",
    "hi": "तुरंत ध्यान देने योग्य",
    "bi": "High Priority (तुरंत समाधान)"
  },
  "high priority (तुरंत समाधान)": {
    "en": "High priority issues",
    "hi": "तुरंत ध्यान देने योग्य",
    "bi": "High Priority (तुरंत समाधान)"
  },
  "resolved": {
    "en": "Resolved",
    "hi": "हल हो चुकी",
    "bi": "Resolved (हल हो चुकी)"
  },
  "हल हो चुकी": {
    "en": "Resolved",
    "hi": "हल हो चुकी",
    "bi": "Resolved (हल हो चुकी)"
  },
  "resolved (हल हो चुकी)": {
    "en": "Resolved",
    "hi": "हल हो चुकी",
    "bi": "Resolved (हल हो चुकी)"
  },
  "resolved issues": {
    "en": "Resolved issues",
    "hi": "समाधान की गई समस्याएं",
    "bi": "Resolved Issues (हल की गई समस्याएं)"
  },
  "समाधान की गई समस्याएं": {
    "en": "Resolved issues",
    "hi": "समाधान की गई समस्याएं",
    "bi": "Resolved Issues (हल की गई समस्याएं)"
  },
  "resolved issues (हल की गई समस्याएं)": {
    "en": "Resolved issues",
    "hi": "समाधान की गई समस्याएं",
    "bi": "Resolved Issues (हल की गई समस्याएं)"
  },
  "work site": {
    "en": "Work Site",
    "hi": "कार्य स्थल (साइट)",
    "bi": "Work Site (साइट)"
  },
  "कार्य स्थल (साइट)": {
    "en": "Work Site",
    "hi": "कार्य स्थल (साइट)",
    "bi": "Work Site (साइट)"
  },
  "work site (साइट)": {
    "en": "Work Site",
    "hi": "कार्य स्थल (साइट)",
    "bi": "Work Site (साइट)"
  },
  "site name": {
    "en": "Site Name",
    "hi": "साइट का नाम",
    "bi": "Site Name (साइट का नाम)"
  },
  "साइट का नाम": {
    "en": "Site Name",
    "hi": "साइट का नाम",
    "bi": "Site Name (साइट का नाम)"
  },
  "site name (साइट का नाम)": {
    "en": "Site Name",
    "hi": "साइट का नाम",
    "bi": "Site Name (साइट का नाम)"
  },
  "issue category": {
    "en": "Issue Category",
    "hi": "समस्या का प्रकार",
    "bi": "Issue Category (समस्या का प्रकार)"
  },
  "समस्या का प्रकार": {
    "en": "Issue Category",
    "hi": "समस्या का प्रकार",
    "bi": "Issue Category (समस्या का प्रकार)"
  },
  "issue category (समस्या का प्रकार)": {
    "en": "Issue Category",
    "hi": "समस्या का प्रकार",
    "bi": "Issue Category (समस्या का प्रकार)"
  },
  "material shortage (pipe, solvent, valve)": {
    "en": "Material Shortage (Pipe, Solvent, Valve)",
    "hi": "सामान की कमी (पाइप, सॉल्वेंट, वाल्व)",
    "bi": "Material Shortage (सामान की कमी - Pipe, Solvent, Valve)"
  },
  "सामान की कमी (पाइप, सॉल्वेंट, वाल्व)": {
    "en": "Material Shortage (Pipe, Solvent, Valve)",
    "hi": "सामान की कमी (पाइप, सॉल्वेंट, वाल्व)",
    "bi": "Material Shortage (सामान की कमी - Pipe, Solvent, Valve)"
  },
  "material shortage (सामान की कमी - pipe, solvent, valve)": {
    "en": "Material Shortage (Pipe, Solvent, Valve)",
    "hi": "सामान की कमी (पाइप, सॉल्वेंट, वाल्व)",
    "bi": "Material Shortage (सामान की कमी - Pipe, Solvent, Valve)"
  },
  "site dispute / obstruction": {
    "en": "Site Dispute / Obstruction",
    "hi": "साइट विवाद / जनता द्वारा रुकावट",
    "bi": "Site Dispute (साइट विवाद / रुकावट)"
  },
  "साइट विवाद / जनता द्वारा रुकावट": {
    "en": "Site Dispute / Obstruction",
    "hi": "साइट विवाद / जनता द्वारा रुकावट",
    "bi": "Site Dispute (साइट विवाद / रुकावट)"
  },
  "site dispute (साइट विवाद / रुकावट)": {
    "en": "Site Dispute / Obstruction",
    "hi": "साइट विवाद / जनता द्वारा रुकावट",
    "bi": "Site Dispute (साइट विवाद / रुकावट)"
  },
  "machine / boring rig issue": {
    "en": "Machine / Boring Rig Issue",
    "hi": "मशीन / बोरिंग रिग खराबी",
    "bi": "Machine Issue (मशीन / बोरिंग रिग खराबी)"
  },
  "मशीन / बोरिंग रिग खराबी": {
    "en": "Machine / Boring Rig Issue",
    "hi": "मशीन / बोरिंग रिग खराबी",
    "bi": "Machine Issue (मशीन / बोरिंग रिग खराबी)"
  },
  "machine issue (मशीन / बोरिंग रिग खराबी)": {
    "en": "Machine / Boring Rig Issue",
    "hi": "मशीन / बोरिंग रिग खराबी",
    "bi": "Machine Issue (मशीन / बोरिंग रिग खराबी)"
  },
  "pipeline leakage / technical defect": {
    "en": "Pipeline Leakage / Technical Defect",
    "hi": "पाइपलाइन लीकेज / तकनीकी खराबी",
    "bi": "Pipeline Leakage (पाइपलाइन लीकेज / खराबी)"
  },
  "पाइपलाइन लीकेज / तकनीकी खराबी": {
    "en": "Pipeline Leakage / Technical Defect",
    "hi": "पाइपलाइन लीकेज / तकनीकी खराबी",
    "bi": "Pipeline Leakage (पाइपलाइन लीकेज / खराबी)"
  },
  "pipeline leakage (पाइपलाइन लीकेज / खराबी)": {
    "en": "Pipeline Leakage / Technical Defect",
    "hi": "पाइपलाइन लीकेज / तकनीकी खराबी",
    "bi": "Pipeline Leakage (पाइपलाइन लीकेज / खराबी)"
  },
  "labour / payment issue": {
    "en": "Labour / Payment Issue",
    "hi": "लेबर / मजदूरी समस्या",
    "bi": "Labour / Payment (लेबर / मजदूरी समस्या)"
  },
  "लेबर / मजदूरी समस्या": {
    "en": "Labour / Payment Issue",
    "hi": "लेबर / मजदूरी समस्या",
    "bi": "Labour / Payment (लेबर / मजदूरी समस्या)"
  },
  "labour / payment (लेबर / मजदूरी समस्या)": {
    "en": "Labour / Payment Issue",
    "hi": "लेबर / मजदूरी समस्या",
    "bi": "Labour / Payment (लेबर / मजदूरी समस्या)"
  },
  "other problem": {
    "en": "Other Problem",
    "hi": "अन्य समस्या",
    "bi": "Other Problem (अन्य समस्या)"
  },
  "अन्य समस्या": {
    "en": "Other Problem",
    "hi": "अन्य समस्या",
    "bi": "Other Problem (अन्य समस्या)"
  },
  "other problem (अन्य समस्या)": {
    "en": "Other Problem",
    "hi": "अन्य समस्या",
    "bi": "Other Problem (अन्य समस्या)"
  },
  "urgency level": {
    "en": "Urgency Level",
    "hi": "प्राथमिकता स्तर",
    "bi": "Urgency Level (प्राथमिकता स्तर)"
  },
  "प्राथमिकता स्तर": {
    "en": "Urgency Level",
    "hi": "प्राथमिकता स्तर",
    "bi": "Urgency Level (प्राथमिकता स्तर)"
  },
  "urgency level (प्राथमिकता स्तर)": {
    "en": "Urgency Level",
    "hi": "प्राथमिकता स्तर",
    "bi": "Urgency Level (प्राथमिकता स्तर)"
  },
  "normal": {
    "en": "Normal",
    "hi": "सामान्य",
    "bi": "Normal (सामान्य)"
  },
  "सामान्य": {
    "en": "Normal",
    "hi": "सामान्य",
    "bi": "Normal (सामान्य)"
  },
  "normal (सामान्य)": {
    "en": "Normal",
    "hi": "सामान्य",
    "bi": "Normal (सामान्य)"
  },
  "problem description": {
    "en": "Problem Description",
    "hi": "समस्या का विवरण",
    "bi": "Problem Description (समस्या का विवरण)"
  },
  "समस्या का विवरण": {
    "en": "Problem Description",
    "hi": "समस्या का विवरण",
    "bi": "Problem Description (समस्या का विवरण)"
  },
  "problem description (समस्या का विवरण)": {
    "en": "Problem Description",
    "hi": "समस्या का विवरण",
    "bi": "Problem Description (समस्या का विवरण)"
  },
  "describe the exact problem at site...": {
    "en": "Describe the exact problem at site...",
    "hi": "साइट पर क्या दिक्कत आ रही है, विस्तार से लिखें...",
    "bi": "Describe the exact problem at site... (विस्तार से लिखें...)"
  },
  "साइट पर क्या दिक्कत आ रही है, विस्तार से लिखें...": {
    "en": "Describe the exact problem at site...",
    "hi": "साइट पर क्या दिक्कत आ रही है, विस्तार से लिखें...",
    "bi": "Describe the exact problem at site... (विस्तार से लिखें...)"
  },
  "describe the exact problem at site... (विस्तार से लिखें...)": {
    "en": "Describe the exact problem at site...",
    "hi": "साइट पर क्या दिक्कत आ रही है, विस्तार से लिखें...",
    "bi": "Describe the exact problem at site... (विस्तार से लिखें...)"
  },
  "take live site photos": {
    "en": "Take live site photos",
    "hi": "खराबी या साइट का लाइव फोटो लें",
    "bi": "Take Live Site Photos (लाइव फोटो लें)"
  },
  "खराबी या साइट का लाइव फोटो लें": {
    "en": "Take live photo of defect or site",
    "hi": "खराबी या साइट का लाइव फोटो लें",
    "bi": "Take live site photo (साइट का लाइव फोटो लें)"
  },
  "take live site photos (लाइव फोटो लें)": {
    "en": "Take live site photos",
    "hi": "खराबी या साइट का लाइव फोटो लें",
    "bi": "Take Live Site Photos (लाइव फोटो लें)"
  },
  "site photos (optional)": {
    "en": "Site Photos (Optional)",
    "hi": "साइट फोटो (वैकल्पिक)",
    "bi": "Site Photos (साइट फोटो - वैकल्पिक)"
  },
  "साइट फोटो (वैकल्पिक)": {
    "en": "Site Photos (Optional)",
    "hi": "साइट फोटो (वैकल्पिक)",
    "bi": "Site Photos (साइट फोटो - वैकल्पिक)"
  },
  "site photos (साइट फोटो - वैकल्पिक)": {
    "en": "Site Photos (Optional)",
    "hi": "साइट फोटो (वैकल्पिक)",
    "bi": "Site Photos (साइट फोटो - वैकल्पिक)"
  },
  "choose file": {
    "en": "Choose File",
    "hi": "फाइल चुनें",
    "bi": "Choose File (फाइल चुनें)"
  },
  "फाइल चुनें": {
    "en": "Choose File",
    "hi": "फाइल चुनें",
    "bi": "Choose File (फाइल चुनें)"
  },
  "choose file (फाइल चुनें)": {
    "en": "Choose File",
    "hi": "फाइल चुनें",
    "bi": "Choose File (फाइल चुनें)"
  },
  "no file chosen": {
    "en": "No file chosen",
    "hi": "कोई फाइल नहीं चुनी",
    "bi": "No file chosen (कोई फाइल नहीं चुनी)"
  },
  "कोई फाइल नहीं चुनी": {
    "en": "No file chosen",
    "hi": "कोई फाइल नहीं चुनी",
    "bi": "No file chosen (कोई फाइल नहीं चुनी)"
  },
  "no file chosen (कोई फाइल नहीं चुनी)": {
    "en": "No file chosen",
    "hi": "कोई फाइल नहीं चुनी",
    "bi": "No file chosen (कोई फाइल नहीं चुनी)"
  },
  "submit complaint": {
    "en": "Submit Complaint",
    "hi": "शिकायत दर्ज करें",
    "bi": "Submit Complaint (शिकायत दर्ज करें)"
  },
  "शिकायत दर्ज करें": {
    "en": "Submit Complaint",
    "hi": "शिकायत दर्ज करें",
    "bi": "Submit Complaint (शिकायत दर्ज करें)"
  },
  "submit complaint (शिकायत दर्ज करें)": {
    "en": "Submit Complaint",
    "hi": "शिकायत दर्ज करें",
    "bi": "Submit Complaint (शिकायत दर्ज करें)"
  },
  "no complaints registered": {
    "en": "No complaints registered",
    "hi": "कोई समस्या या शिकायत दर्ज नहीं है",
    "bi": "No complaints registered (कोई शिकायत दर्ज नहीं है)"
  },
  "कोई समस्या या शिकायत दर्ज नहीं है": {
    "en": "No complaints registered",
    "hi": "कोई समस्या या शिकायत दर्ज नहीं है",
    "bi": "No complaints registered (कोई शिकायत दर्ज नहीं है)"
  },
  "no complaints registered (कोई शिकायत दर्ज नहीं है)": {
    "en": "No complaints registered",
    "hi": "कोई समस्या या शिकायत दर्ज नहीं है",
    "bi": "No complaints registered (कोई शिकायत दर्ज नहीं है)"
  },
  "all is running smoothly!": {
    "en": "All is running smoothly!",
    "hi": "इस समय कोई भी खुली समस्या नहीं है। सब कुछ ठीक चल रहा है!",
    "bi": "All is running smoothly! (सब कुछ ठीक चल रहा है!)"
  },
  "इस समय कोई भी खुली समस्या नहीं है। सब कुछ ठीक चल रहा है!": {
    "en": "All is running smoothly!",
    "hi": "इस समय कोई भी खुली समस्या नहीं है। सब कुछ ठीक चल रहा है!",
    "bi": "All is running smoothly! (सब कुछ ठीक चल रहा है!)"
  },
  "all is running smoothly! (सब कुछ ठीक चल रहा है!)": {
    "en": "All is running smoothly!",
    "hi": "इस समय कोई भी खुली समस्या नहीं है। सब कुछ ठीक चल रहा है!",
    "bi": "All is running smoothly! (सब कुछ ठीक चल रहा है!)"
  },
  "mark as resolved": {
    "en": "Mark as Resolved",
    "hi": "हल हो गया मार्क करें",
    "bi": "Mark as Resolved (हल मार्क करें)"
  },
  "हल हो गया मार्क करें": {
    "en": "Mark as Resolved",
    "hi": "हल हो गया मार्क करें",
    "bi": "Mark as Resolved (हल मार्क करें)"
  },
  "mark as resolved (हल मार्क करें)": {
    "en": "Mark as Resolved",
    "hi": "हल हो गया मार्क करें",
    "bi": "Mark as Resolved (हल मार्क करें)"
  },
  "resolved by office": {
    "en": "Resolved by Office",
    "hi": "कार्यालय द्वारा समाधान",
    "bi": "Resolved by Office (कार्यालय समाधान)"
  },
  "कार्यालय द्वारा समाधान": {
    "en": "Resolved by Office",
    "hi": "कार्यालय द्वारा समाधान",
    "bi": "Resolved by Office (कार्यालय समाधान)"
  },
  "resolved by office (कार्यालय समाधान)": {
    "en": "Resolved by Office",
    "hi": "कार्यालय द्वारा समाधान",
    "bi": "Resolved by Office (कार्यालय समाधान)"
  },
  "resolution remarks": {
    "en": "Resolution Remarks",
    "hi": "समाधान विवरण",
    "bi": "Resolution Remarks (समाधान विवरण)"
  },
  "समाधान विवरण": {
    "en": "Resolution Remarks",
    "hi": "समाधान विवरण",
    "bi": "Resolution Remarks (समाधान विवरण)"
  },
  "resolution remarks (समाधान विवरण)": {
    "en": "Resolution Remarks",
    "hi": "समाधान विवरण",
    "bi": "Resolution Remarks (समाधान विवरण)"
  },
  "save resolution": {
    "en": "Save Resolution",
    "hi": "समाधान सुरक्षित करें",
    "bi": "Save Resolution (समाधान सुरक्षित करें)"
  },
  "समाधान सुरक्षित करें": {
    "en": "Save Resolution",
    "hi": "समाधान सुरक्षित करें",
    "bi": "Save Resolution (समाधान सुरक्षित करें)"
  },
  "save resolution (समाधान सुरक्षित करें)": {
    "en": "Save Resolution",
    "hi": "समाधान सुरक्षित करें",
    "bi": "Save Resolution (समाधान सुरक्षित करें)"
  },
  "21 sites bill status": {
    "en": "21 Sites Bill Status",
    "hi": "21 साइट्स बिल स्थिति",
    "bi": "21 Sites Bill Status (21 साइट्स बिल स्थिति)"
  },
  "21 साइट्स बिल स्थिति": {
    "en": "21 Sites Bill Status",
    "hi": "21 साइट्स बिल स्थिति",
    "bi": "21 Sites Bill Status (21 साइट्स बिल स्थिति)"
  },
  "21 sites bill status (21 साइट्स बिल स्थिति)": {
    "en": "21 Sites Bill Status",
    "hi": "21 साइट्स बिल स्थिति",
    "bi": "21 Sites Bill Status (21 साइट्स बिल स्थिति)"
  },
  "21 sites bill clearance checklist": {
    "en": "21 Sites Bill Clearance Checklist",
    "hi": "21 साइट्स बिल क्लीयरेंस चेकलिस्ट",
    "bi": "21 Sites Bill Clearance Checklist (21 साइट्स बिल क्लीयरेंस चेकलिस्ट)"
  },
  "21 साइट्स बिल क्लीयरेंस चेकलिस्ट": {
    "en": "21 Sites Bill Clearance Checklist",
    "hi": "21 साइट्स बिल क्लीयरेंस चेकलिस्ट",
    "bi": "21 Sites Bill Clearance Checklist (21 साइट्स बिल क्लीयरेंस चेकलिस्ट)"
  },
  "21 sites bill clearance checklist (21 साइट्स बिल क्लीयरेंस चेकलिस्ट)": {
    "en": "21 Sites Bill Clearance Checklist",
    "hi": "21 साइट्स बिल क्लीयरेंस चेकलिस्ट",
    "bi": "21 Sites Bill Clearance Checklist (21 साइट्स बिल क्लीयरेंस चेकलिस्ट)"
  },
  "every site's current bill status & stage progression across the 9-step cycle": {
    "en": "Every site's current bill status & stage progression across the 9-step cycle",
    "hi": "सभी साइट्स के बिल की वर्तमान स्थिति एवं 9 चरणों की प्रगति",
    "bi": "Every site's current bill status (सभी साइट्स के बिल की 9 चरणों में स्थिति)"
  },
  "सभी साइट्स के बिल की वर्तमान स्थिति एवं 9 चरणों की प्रगति": {
    "en": "Every site's current bill status & stage progression across the 9-step cycle",
    "hi": "सभी साइट्स के बिल की वर्तमान स्थिति एवं 9 चरणों की प्रगति",
    "bi": "Every site's current bill status (सभी साइट्स के बिल की 9 चरणों में स्थिति)"
  },
  "every site's current bill status (सभी साइट्स के बिल की 9 चरणों में स्थिति)": {
    "en": "Every site's current bill status & stage progression across the 9-step cycle",
    "hi": "सभी साइट्स के बिल की वर्तमान स्थिति एवं 9 चरणों की प्रगति",
    "bi": "Every site's current bill status (सभी साइट्स के बिल की 9 चरणों में स्थिति)"
  },
  "+ add bill": {
    "en": "+ Add Bill",
    "hi": "+ नया बिल जोड़ें",
    "bi": "+ Add Bill (नया बिल जोड़ें)"
  },
  "+ नया बिल जोड़ें": {
    "en": "+ Add Bill",
    "hi": "+ नया बिल जोड़ें",
    "bi": "+ Add Bill (नया बिल जोड़ें)"
  },
  "+ add bill (नया बिल जोड़ें)": {
    "en": "+ Add Bill",
    "hi": "+ नया बिल जोड़ें",
    "bi": "+ Add Bill (नया बिल जोड़ें)"
  },
  "prep form": {
    "en": "Prep Form",
    "hi": "तैयारी फॉर्म",
    "bi": "Prep Form (तैयारी फॉर्म)"
  },
  "तैयारी फॉर्म": {
    "en": "Prep Form",
    "hi": "तैयारी फॉर्म",
    "bi": "Prep Form (तैयारी फॉर्म)"
  },
  "prep form (तैयारी फॉर्म)": {
    "en": "Prep Form",
    "hi": "तैयारी फॉर्म",
    "bi": "Prep Form (तैयारी फॉर्म)"
  },
  "open supervisor prep form": {
    "en": "Open Supervisor Prep Form",
    "hi": "सुपरवाइजर तैयारी फॉर्म खोलें",
    "bi": "Open Prep Form (तैयारी फॉर्म खोलें)"
  },
  "सुपरवाइजर तैयारी फॉर्म खोलें": {
    "en": "Open Supervisor Prep Form",
    "hi": "सुपरवाइजर तैयारी फॉर्म खोलें",
    "bi": "Open Prep Form (तैयारी फॉर्म खोलें)"
  },
  "open prep form (तैयारी फॉर्म खोलें)": {
    "en": "Open Supervisor Prep Form",
    "hi": "सुपरवाइजर तैयारी फॉर्म खोलें",
    "bi": "Open Prep Form (तैयारी फॉर्म खोलें)"
  },
  "search site, bill no, diary no, token...": {
    "en": "Search site, bill no, diary no, token...",
    "hi": "साइट, बिल नं, डायरी नं, टोकन से खोजें...",
    "bi": "Search site, bill no, diary no (साइट या बिल नं से खोजें)..."
  },
  "साइट, बिल नं, डायरी नं, टोकन से खोजें...": {
    "en": "Search site, bill no, diary no, token...",
    "hi": "साइट, बिल नं, डायरी नं, टोकन से खोजें...",
    "bi": "Search site, bill no, diary no (साइट या बिल नं से खोजें)..."
  },
  "search site, bill no, diary no (साइट या बिल नं से खोजें)...": {
    "en": "Search site, bill no, diary no, token...",
    "hi": "साइट, बिल नं, डायरी नं, टोकन से खोजें...",
    "bi": "Search site, bill no, diary no (साइट या बिल नं से खोजें)..."
  },
  "sites checklist": {
    "en": "Sites Checklist",
    "hi": "साइट्स चेकलिस्ट",
    "bi": "Sites Checklist (साइट्स चेकलिस्ट)"
  },
  "साइट्स चेकलिस्ट": {
    "en": "Sites Checklist",
    "hi": "साइट्स चेकलिस्ट",
    "bi": "Sites Checklist (साइट्स चेकलिस्ट)"
  },
  "sites checklist (साइट्स चेकलिस्ट)": {
    "en": "Sites Checklist",
    "hi": "साइट्स चेकलिस्ट",
    "bi": "Sites Checklist (साइट्स चेकलिस्ट)"
  },
  "month view": {
    "en": "Month View",
    "hi": "माह अनुसार",
    "bi": "Month View (माह अनुसार)"
  },
  "माह अनुसार": {
    "en": "Month View",
    "hi": "माह अनुसार",
    "bi": "Month View (माह अनुसार)"
  },
  "month view (माह अनुसार)": {
    "en": "Month View",
    "hi": "माह अनुसार",
    "bi": "Month View (माह अनुसार)"
  },
  "fy cleared matrix": {
    "en": "FY Cleared Matrix",
    "hi": "वित्तीय वर्ष मैट्रिक्स",
    "bi": "FY Cleared Matrix (वित्तीय वर्ष मैट्रिक्स)"
  },
  "वित्तीय वर्ष मैट्रिक्स": {
    "en": "FY Cleared Matrix",
    "hi": "वित्तीय वर्ष मैट्रिक्स",
    "bi": "FY Cleared Matrix (वित्तीय वर्ष मैट्रिक्स)"
  },
  "fy cleared matrix (वित्तीय वर्ष मैट्रिक्स)": {
    "en": "FY Cleared Matrix",
    "hi": "वित्तीय वर्ष मैट्रिक्स",
    "bi": "FY Cleared Matrix (वित्तीय वर्ष मैट्रिक्स)"
  },
  "all bills table": {
    "en": "All Bills Table",
    "hi": "सभी बिल तालिका",
    "bi": "All Bills Table (सभी बिल तालिका)"
  },
  "सभी बिल तालिका": {
    "en": "All Bills Table",
    "hi": "सभी बिल तालिका",
    "bi": "All Bills Table (सभी बिल तालिका)"
  },
  "all bills table (सभी बिल तालिका)": {
    "en": "All Bills Table",
    "hi": "सभी बिल तालिका",
    "bi": "All Bills Table (सभी बिल तालिका)"
  },
  "active bill": {
    "en": "Active Bill",
    "hi": "सक्रिय बिल",
    "bi": "Active Bill (सक्रिय बिल)"
  },
  "सक्रिय बिल": {
    "en": "Active Bill",
    "hi": "सक्रिय बिल",
    "bi": "Active Bill (सक्रिय बिल)"
  },
  "active bill (सक्रिय बिल)": {
    "en": "Active Bill",
    "hi": "सक्रिय बिल",
    "bi": "Active Bill (सक्रिय बिल)"
  },
  "bill amount": {
    "en": "Bill Amount",
    "hi": "बिल राशि",
    "bi": "Bill Amount (बिल राशि)"
  },
  "बिल राशि": {
    "en": "Bill Amount",
    "hi": "बिल राशि",
    "bi": "Bill Amount (बिल राशि)"
  },
  "bill amount (बिल राशि)": {
    "en": "Bill Amount",
    "hi": "बिल राशि",
    "bi": "Bill Amount (बिल राशि)"
  },
  "current status & details": {
    "en": "Current Status & Details",
    "hi": "वर्तमान स्थिति एवं विवरण",
    "bi": "Current Status & Details (वर्तमान स्थिति एवं विवरण)"
  },
  "वर्तमान स्थिति एवं विवरण": {
    "en": "Current Status & Details",
    "hi": "वर्तमान स्थिति एवं विवरण",
    "bi": "Current Status & Details (वर्तमान स्थिति एवं विवरण)"
  },
  "current status & details (वर्तमान स्थिति एवं विवरण)": {
    "en": "Current Status & Details",
    "hi": "वर्तमान स्थिति एवं विवरण",
    "bi": "Current Status & Details (वर्तमान स्थिति एवं विवरण)"
  },
  "quick actions": {
    "en": "Quick Actions",
    "hi": "त्वरित कार्रवाई",
    "bi": "Quick Actions (त्वरित कार्रवाई)"
  },
  "त्वरित कार्रवाई": {
    "en": "Quick Actions",
    "hi": "त्वरित कार्रवाई",
    "bi": "Quick Actions (त्वरित कार्रवाई)"
  },
  "quick actions (त्वरित कार्रवाई)": {
    "en": "Quick Actions",
    "hi": "त्वरित कार्रवाई",
    "bi": "Quick Actions (त्वरित कार्रवाई)"
  },
  "next step": {
    "en": "Next Step",
    "hi": "अगला चरण",
    "bi": "Next Step (अगला चरण)"
  },
  "अगला चरण": {
    "en": "Next Step",
    "hi": "अगला चरण",
    "bi": "Next Step (अगला चरण)"
  },
  "next step (अगला चरण)": {
    "en": "Next Step",
    "hi": "अगला चरण",
    "bi": "Next Step (अगला चरण)"
  },
  "done": {
    "en": "Done",
    "hi": "ठीक है (Done)",
    "bi": "Done (ठीक है)"
  },
  "पूर्ण": {
    "en": "Done",
    "hi": "पूर्ण",
    "bi": "Done (पूर्ण)"
  },
  "done (पूर्ण)": {
    "en": "Done",
    "hi": "पूर्ण",
    "bi": "Done (पूर्ण)"
  },
  "step 1: gps photo printout": {
    "en": "Step 1: GPS Photo Printout",
    "hi": "चरण 1: जीपीएस फोटो प्रिंटआउट",
    "bi": "Step 1: GPS Photo Printout (जीपीएस फोटो प्रिंटआउट)"
  },
  "चरण 1: जीपीएस फोटो प्रिंटआउट": {
    "en": "Step 1: GPS Photo Printout",
    "hi": "चरण 1: जीपीएस फोटो प्रिंटआउट",
    "bi": "Step 1: GPS Photo Printout (जीपीएस फोटो प्रिंटआउट)"
  },
  "step 1: gps photo printout (जीपीएस फोटो प्रिंटआउट)": {
    "en": "Step 1: GPS Photo Printout",
    "hi": "चरण 1: जीपीएस फोटो प्रिंटआउट",
    "bi": "Step 1: GPS Photo Printout (जीपीएस फोटो प्रिंटआउट)"
  },
  "step 2: complain register maintained": {
    "en": "Step 2: Complain Register Maintained",
    "hi": "चरण 2: शिकायत रजिस्टर संधारण",
    "bi": "Step 2: Complain Register (शिकायत रजिस्टर)"
  },
  "चरण 2: शिकायत रजिस्टर संधारण": {
    "en": "Step 2: Complain Register Maintained",
    "hi": "चरण 2: शिकायत रजिस्टर संधारण",
    "bi": "Step 2: Complain Register (शिकायत रजिस्टर)"
  },
  "step 2: complain register (शिकायत रजिस्टर)": {
    "en": "Step 2: Complain Register Maintained",
    "hi": "चरण 2: शिकायत रजिस्टर संधारण",
    "bi": "Step 2: Complain Register (शिकायत रजिस्टर)"
  },
  "step 3: field rough estimate calculated": {
    "en": "Step 3: Field Rough Estimate Calculated",
    "hi": "चरण 3: फील्ड रफ एस्टीमेट तैयार",
    "bi": "Step 3: Rough Estimate (रफ एस्टीमेट)"
  },
  "चरण 3: फील्ड रफ एस्टीमेट तैयार": {
    "en": "Step 3: Field Rough Estimate Calculated",
    "hi": "चरण 3: फील्ड रफ एस्टीमेट तैयार",
    "bi": "Step 3: Rough Estimate (रफ एस्टीमेट)"
  },
  "step 3: rough estimate (रफ एस्टीमेट)": {
    "en": "Step 3: Field Rough Estimate Calculated",
    "hi": "चरण 3: फील्ड रफ एस्टीमेट तैयार",
    "bi": "Step 3: Rough Estimate (रफ एस्टीमेट)"
  },
  "step 4: ra bill created in mb": {
    "en": "Step 4: RA Bill Created in MB",
    "hi": "चरण 4: MB में बिल तैयार हुआ",
    "bi": "Step 4: RA Bill Created (MB में बिल तैयार)"
  },
  "चरण 4: mb में बिल तैयार हुआ": {
    "en": "Step 4: RA Bill Created in MB",
    "hi": "चरण 4: MB में बिल तैयार हुआ",
    "bi": "Step 4: RA Bill Created (MB में बिल तैयार)"
  },
  "step 4: ra bill created (mb में बिल तैयार)": {
    "en": "Step 4: RA Bill Created in MB",
    "hi": "चरण 4: MB में बिल तैयार हुआ",
    "bi": "Step 4: RA Bill Created (MB में बिल तैयार)"
  },
  "step 5: submitted to head clerk": {
    "en": "Step 5: Submitted to Head Clerk",
    "hi": "चरण 5: हेड क्लर्क को जमा",
    "bi": "Step 5: Head Clerk (हेड क्लर्क को जमा)"
  },
  "चरण 5: हेड क्लर्क को जमा": {
    "en": "Step 5: Submitted to Head Clerk",
    "hi": "चरण 5: हेड क्लर्क को जमा",
    "bi": "Step 5: Head Clerk (हेड क्लर्क को जमा)"
  },
  "step 5: head clerk (हेड क्लर्क को जमा)": {
    "en": "Step 5: Submitted to Head Clerk",
    "hi": "चरण 5: हेड क्लर्क को जमा",
    "bi": "Step 5: Head Clerk (हेड क्लर्क को जमा)"
  },
  "step 6: verified by je / sdo": {
    "en": "Step 6: Verified by JE / SDO",
    "hi": "चरण 6: JE / SDO द्वारा सत्यापित",
    "bi": "Step 6: JE / SDO Verified (JE/SDO सत्यापन)"
  },
  "चरण 6: je / sdo द्वारा सत्यापित": {
    "en": "Step 6: Verified by JE / SDO",
    "hi": "चरण 6: JE / SDO द्वारा सत्यापित",
    "bi": "Step 6: JE / SDO Verified (JE/SDO सत्यापन)"
  },
  "step 6: je / sdo verified (je/sdo सत्यापन)": {
    "en": "Step 6: Verified by JE / SDO",
    "hi": "चरण 6: JE / SDO द्वारा सत्यापित",
    "bi": "Step 6: JE / SDO Verified (JE/SDO सत्यापन)"
  },
  "step 7: forwarded to treasury": {
    "en": "Step 7: Forwarded to Treasury",
    "hi": "चरण 7: ट्रेजरी को अग्रसारित",
    "bi": "Step 7: Treasury (ट्रेजरी अग्रसारित)"
  },
  "चरण 7: ट्रेजरी को अग्रसारित": {
    "en": "Step 7: Forwarded to Treasury",
    "hi": "चरण 7: ट्रेजरी को अग्रसारित",
    "bi": "Step 7: Treasury (ट्रेजरी अग्रसारित)"
  },
  "step 7: treasury (ट्रेजरी अग्रसारित)": {
    "en": "Step 7: Forwarded to Treasury",
    "hi": "चरण 7: ट्रेजरी को अग्रसारित",
    "bi": "Step 7: Treasury (ट्रेजरी अग्रसारित)"
  },
  "step 8: bill cleared / passed": {
    "en": "Step 8: Bill Cleared / Passed",
    "hi": "चरण 8: बिल पास / स्वीकृत",
    "bi": "Step 8: Bill Cleared (बिल पास)"
  },
  "चरण 8: बिल पास / स्वीकृत": {
    "en": "Step 8: Bill Cleared / Passed",
    "hi": "चरण 8: बिल पास / स्वीकृत",
    "bi": "Step 8: Bill Cleared (बिल पास)"
  },
  "step 8: bill cleared (बिल पास)": {
    "en": "Step 8: Bill Cleared / Passed",
    "hi": "चरण 8: बिल पास / स्वीकृत",
    "bi": "Step 8: Bill Cleared (बिल पास)"
  },
  "step 9: payment received": {
    "en": "Step 9: Payment Received",
    "hi": "चरण 9: भुगतान प्राप्त",
    "bi": "Step 9: Payment Received (भुगतान प्राप्त)"
  },
  "चरण 9: भुगतान प्राप्त": {
    "en": "Step 9: Payment Received",
    "hi": "चरण 9: भुगतान प्राप्त",
    "bi": "Step 9: Payment Received (भुगतान प्राप्त)"
  },
  "step 9: payment received (भुगतान प्राप्त)": {
    "en": "Step 9: Payment Received",
    "hi": "चरण 9: भुगतान प्राप्त",
    "bi": "Step 9: Payment Received (भुगतान प्राप्त)"
  },
  "ra bill": {
    "en": "RA Bill",
    "hi": "रनिंग बिल",
    "bi": "RA Bill (रनिंग बिल)"
  },
  "रनिंग बिल": {
    "en": "RA Bill",
    "hi": "रनिंग बिल",
    "bi": "RA Bill (रनिंग बिल)"
  },
  "ra bill (रनिंग बिल)": {
    "en": "RA Bill",
    "hi": "रनिंग बिल",
    "bi": "RA Bill (रनिंग बिल)"
  },
  "final bill": {
    "en": "Final Bill",
    "hi": "फाइनल बिल",
    "bi": "Final Bill (फाइनल बिल)"
  },
  "फाइनल बिल": {
    "en": "Final Bill",
    "hi": "फाइनल बिल",
    "bi": "Final Bill (फाइनल बिल)"
  },
  "final bill (फाइनल बिल)": {
    "en": "Final Bill",
    "hi": "फाइनल बिल",
    "bi": "Final Bill (फाइनल बिल)"
  },
  "claimed amount": {
    "en": "Claimed Amount",
    "hi": "दावा की गई राशि",
    "bi": "Claimed Amount (दावा राशि)"
  },
  "दावा की गई राशि": {
    "en": "Claimed Amount",
    "hi": "दावा की गई राशि",
    "bi": "Claimed Amount (दावा राशि)"
  },
  "claimed amount (दावा राशि)": {
    "en": "Claimed Amount",
    "hi": "दावा की गई राशि",
    "bi": "Claimed Amount (दावा राशि)"
  },
  "passed amount": {
    "en": "Passed Amount",
    "hi": "स्वीकृत राशि",
    "bi": "Passed Amount (स्वीकृत राशि)"
  },
  "स्वीकृत राशि": {
    "en": "Passed Amount",
    "hi": "स्वीकृत राशि",
    "bi": "Passed Amount (स्वीकृत राशि)"
  },
  "passed amount (स्वीकृत राशि)": {
    "en": "Passed Amount",
    "hi": "स्वीकृत राशि",
    "bi": "Passed Amount (स्वीकृत राशि)"
  },
  "received amount": {
    "en": "Received Amount",
    "hi": "प्राप्त राशि",
    "bi": "Received Amount (प्राप्त राशि)"
  },
  "प्राप्त राशि": {
    "en": "Received Amount",
    "hi": "प्राप्त राशि",
    "bi": "Received Amount (प्राप्त राशि)"
  },
  "received amount (प्राप्त राशि)": {
    "en": "Received Amount",
    "hi": "प्राप्त राशि",
    "bi": "Received Amount (प्राप्त राशि)"
  },
  "pending token": {
    "en": "Pending Token",
    "hi": "पेंडिंग टोकन",
    "bi": "Pending Token (पेंडिंग टोकन)"
  },
  "पेंडिंग टोकन": {
    "en": "Pending Token",
    "hi": "पेंडिंग टोकन",
    "bi": "Pending Token (पेंडिंग टोकन)"
  },
  "pending token (पेंडिंग टोकन)": {
    "en": "Pending Token",
    "hi": "पेंडिंग टोकन",
    "bi": "Pending Token (पेंडिंग टोकन)"
  },
  "under scrutiny": {
    "en": "Under Scrutiny",
    "hi": "जांच में",
    "bi": "Under Scrutiny (जांच में)"
  },
  "जांच में": {
    "en": "Under Scrutiny",
    "hi": "जांच में",
    "bi": "Under Scrutiny (जांच में)"
  },
  "under scrutiny (जांच में)": {
    "en": "Under Scrutiny",
    "hi": "जांच में",
    "bi": "Under Scrutiny (जांच में)"
  },
  "mb verification": {
    "en": "MB Verification",
    "hi": "एमबी सत्यापन",
    "bi": "MB Verification (एमबी सत्यापन)"
  },
  "एमबी सत्यापन": {
    "en": "MB Verification",
    "hi": "एमबी सत्यापन",
    "bi": "MB Verification (एमबी सत्यापन)"
  },
  "mb verification (एमबी सत्यापन)": {
    "en": "MB Verification",
    "hi": "एमबी सत्यापन",
    "bi": "MB Verification (एमबी सत्यापन)"
  },
  "attendance": {
    "en": "Attendance",
    "hi": "हाजिरी",
    "bi": "Attendance (हाजिरी)"
  },
  "हाजिरी": {
    "en": "Attendance",
    "hi": "हाजिरी",
    "bi": "Attendance (हाजिरी)"
  },
  "attendance (हाजिरी)": {
    "en": "Attendance",
    "hi": "हाजिरी",
    "bi": "Attendance (हाजिरी)"
  },
  "attendance register": {
    "en": "Attendance Register",
    "hi": "हाजिरी रजिस्टर",
    "bi": "Attendance Register (हाजिरी रजिस्टर)"
  },
  "हाजिरी रजिस्टर": {
    "en": "Attendance Register",
    "hi": "हाजिरी रजिस्टर",
    "bi": "Attendance Register (हाजिरी रजिस्टर)"
  },
  "attendance register (हाजिरी रजिस्टर)": {
    "en": "Attendance Register",
    "hi": "हाजिरी रजिस्टर",
    "bi": "Attendance Register (हाजिरी रजिस्टर)"
  },
  "daily attendance": {
    "en": "Daily Attendance",
    "hi": "दैनिक हाजिरी",
    "bi": "Daily Attendance (दैनिक हाजिरी)"
  },
  "दैनिक हाजिरी": {
    "en": "Daily Attendance",
    "hi": "दैनिक हाजिरी",
    "bi": "Daily Attendance (दैनिक हाजिरी)"
  },
  "daily attendance (दैनिक हाजिरी)": {
    "en": "Daily Attendance",
    "hi": "दैनिक हाजिरी",
    "bi": "Daily Attendance (दैनिक हाजिरी)"
  },
  "manual attendance": {
    "en": "Manual Attendance",
    "hi": "मैन्युअल हाजिरी",
    "bi": "Manual Attendance (मैन्युअल हाजिरी)"
  },
  "मैन्युअल हाजिरी": {
    "en": "Manual Attendance",
    "hi": "मैन्युअल हाजिरी",
    "bi": "Manual Attendance (मैन्युअल हाजिरी)"
  },
  "manual attendance (मैन्युअल हाजिरी)": {
    "en": "Manual Attendance",
    "hi": "मैन्युअल हाजिरी",
    "bi": "Manual Attendance (मैन्युअल हाजिरी)"
  },
  "gps attendance": {
    "en": "GPS Attendance",
    "hi": "जीपीएस हाजिरी",
    "bi": "GPS Attendance (जीपीएस हाजिरी)"
  },
  "जीपीएस हाजिरी": {
    "en": "GPS Attendance",
    "hi": "जीपीएस हाजिरी",
    "bi": "GPS Attendance (जीपीएस हाजिरी)"
  },
  "gps attendance (जीपीएस हाजिरी)": {
    "en": "GPS Attendance",
    "hi": "जीपीएस हाजिरी",
    "bi": "GPS Attendance (जीपीएस हाजिरी)"
  },
  "geo attendance": {
    "en": "Geo Attendance",
    "hi": "जियो हाजिरी",
    "bi": "Geo Attendance (जियो हाजिरी)"
  },
  "जियो हाजिरी": {
    "en": "Geo Attendance",
    "hi": "जियो हाजिरी",
    "bi": "Geo Attendance (जियो हाजिरी)"
  },
  "geo attendance (जियो हाजिरी)": {
    "en": "Geo Attendance",
    "hi": "जियो हाजिरी",
    "bi": "Geo Attendance (जियो हाजिरी)"
  },
  "workers": {
    "en": "Workers",
    "hi": "श्रमिक",
    "bi": "Workers (श्रमिक)"
  },
  "श्रमिक": {
    "en": "Workers",
    "hi": "श्रमिक",
    "bi": "Workers (श्रमिक)"
  },
  "workers (श्रमिक)": {
    "en": "Workers",
    "hi": "श्रमिक",
    "bi": "Workers (श्रमिक)"
  },
  "workers list": {
    "en": "Workers List",
    "hi": "श्रमिक सूची",
    "bi": "Workers List (श्रमिक सूची)"
  },
  "श्रमिक सूची": {
    "en": "Workers List",
    "hi": "श्रमिक सूची",
    "bi": "Workers List (श्रमिक सूची)"
  },
  "workers list (श्रमिक सूची)": {
    "en": "Workers List",
    "hi": "श्रमिक सूची",
    "bi": "Workers List (श्रमिक सूची)"
  },
  "+ add worker": {
    "en": "+ Add Worker",
    "hi": "+ नया श्रमिक जोड़ें",
    "bi": "+ Add Worker (नया श्रमिक जोड़ें)"
  },
  "+ नया श्रमिक जोड़ें": {
    "en": "+ Add Worker",
    "hi": "+ नया श्रमिक जोड़ें",
    "bi": "+ Add Worker (नया श्रमिक जोड़ें)"
  },
  "+ add worker (नया श्रमिक जोड़ें)": {
    "en": "+ Add Worker",
    "hi": "+ नया श्रमिक जोड़ें",
    "bi": "+ Add Worker (नया श्रमिक जोड़ें)"
  },
  "worker name": {
    "en": "Worker Name",
    "hi": "कारीगर का नाम",
    "bi": "Worker Name (कारीगर का नाम)"
  },
  "श्रमिक का नाम": {
    "en": "Worker Name",
    "hi": "श्रमिक का नाम",
    "bi": "Worker Name (श्रमिक का नाम)"
  },
  "worker name (श्रमिक का नाम)": {
    "en": "Worker Name",
    "hi": "श्रमिक का नाम",
    "bi": "Worker Name (श्रमिक का नाम)"
  },
  "worker category": {
    "en": "Worker Category",
    "hi": "श्रमिक वर्ग",
    "bi": "Worker Category (श्रमिक वर्ग)"
  },
  "श्रमिक वर्ग": {
    "en": "Worker Category",
    "hi": "श्रमिक वर्ग",
    "bi": "Worker Category (श्रमिक वर्ग)"
  },
  "worker category (श्रमिक वर्ग)": {
    "en": "Worker Category",
    "hi": "श्रमिक वर्ग",
    "bi": "Worker Category (श्रमिक वर्ग)"
  },
  "mason / mistry": {
    "en": "Mason / Mistry",
    "hi": "मिस्त्री",
    "bi": "Mason (मिस्त्री)"
  },
  "मिस्त्री": {
    "en": "Mason / Mistry",
    "hi": "मिस्त्री",
    "bi": "Mason (मिस्त्री)"
  },
  "mason (मिस्त्री)": {
    "en": "Mason / Mistry",
    "hi": "मिस्त्री",
    "bi": "Mason (मिस्त्री)"
  },
  "plumber": {
    "en": "Plumber",
    "hi": "प्लंबर",
    "bi": "Plumber (प्लंबर)"
  },
  "प्लंबर": {
    "en": "Plumber",
    "hi": "प्लंबर",
    "bi": "Plumber (प्लंबर)"
  },
  "plumber (प्लंबर)": {
    "en": "Plumber",
    "hi": "प्लंबर",
    "bi": "Plumber (प्लंबर)"
  },
  "helper": {
    "en": "Helper",
    "hi": "हेल्पर",
    "bi": "Helper (हेल्पर)"
  },
  "हेल्पर": {
    "en": "Helper",
    "hi": "हेल्पर",
    "bi": "Helper (हेल्पर)"
  },
  "helper (हेल्पर)": {
    "en": "Helper",
    "hi": "हेल्पर",
    "bi": "Helper (हेल्पर)"
  },
  "staff / supervisor": {
    "en": "Staff / Supervisor",
    "hi": "स्टाफ / सुपरवाइजर",
    "bi": "Staff (स्टाफ / सुपरवाइजर)"
  },
  "स्टाफ / सुपरवाइजर": {
    "en": "Staff / Supervisor",
    "hi": "स्टाफ / सुपरवाइजर",
    "bi": "Staff (स्टाफ / सुपरवाइजर)"
  },
  "staff (स्टाफ / सुपरवाइजर)": {
    "en": "Staff / Supervisor",
    "hi": "स्टाफ / सुपरवाइजर",
    "bi": "Staff (स्टाफ / सुपरवाइजर)"
  },
  "electrician": {
    "en": "Electrician",
    "hi": "इलेक्ट्रीशियन",
    "bi": "Electrician (इलेक्ट्रीशियन)"
  },
  "इलेक्ट्रीशियन": {
    "en": "Electrician",
    "hi": "इलेक्ट्रीशियन",
    "bi": "Electrician (इलेक्ट्रीशियन)"
  },
  "electrician (इलेक्ट्रीशियन)": {
    "en": "Electrician",
    "hi": "इलेक्ट्रीशियन",
    "bi": "Electrician (इलेक्ट्रीशियन)"
  },
  "present": {
    "en": "Present",
    "hi": "उपस्थित",
    "bi": "Present (उपस्थित)"
  },
  "उपस्थित": {
    "en": "Present",
    "hi": "उपस्थित",
    "bi": "Present (उपस्थित)"
  },
  "present (उपस्थित)": {
    "en": "Present",
    "hi": "उपस्थित",
    "bi": "Present (उपस्थित)"
  },
  "absent": {
    "en": "Absent",
    "hi": "अनुपस्थित",
    "bi": "Absent (अनुपस्थित)"
  },
  "अनुपस्थित": {
    "en": "Absent",
    "hi": "अनुपस्थित",
    "bi": "Absent (अनुपस्थित)"
  },
  "absent (अनुपस्थित)": {
    "en": "Absent",
    "hi": "अनुपस्थित",
    "bi": "Absent (अनुपस्थित)"
  },
  "half day": {
    "en": "Half Day",
    "hi": "आधा दिन",
    "bi": "Half Day (आधा दिन)"
  },
  "आधा दिन": {
    "en": "Half Day",
    "hi": "आधा दिन",
    "bi": "Half Day (आधा दिन)"
  },
  "half day (आधा दिन)": {
    "en": "Half Day",
    "hi": "आधा दिन",
    "bi": "Half Day (आधा दिन)"
  },
  "total workers": {
    "en": "Total Workers",
    "hi": "कुल श्रमिक",
    "bi": "Total Workers (कुल श्रमिक)"
  },
  "कुल श्रमिक": {
    "en": "Total Workers",
    "hi": "कुल श्रमिक",
    "bi": "Total Workers (कुल श्रमिक)"
  },
  "total workers (कुल श्रमिक)": {
    "en": "Total Workers",
    "hi": "कुल श्रमिक",
    "bi": "Total Workers (कुल श्रमिक)"
  },
  "total present": {
    "en": "Total Present",
    "hi": "कुल उपस्थित",
    "bi": "Total Present (कुल उपस्थित)"
  },
  "कुल उपस्थित": {
    "en": "Total Present",
    "hi": "कुल उपस्थित",
    "bi": "Total Present (कुल उपस्थित)"
  },
  "total present (कुल उपस्थित)": {
    "en": "Total Present",
    "hi": "कुल उपस्थित",
    "bi": "Total Present (कुल उपस्थित)"
  },
  "total absent": {
    "en": "Total Absent",
    "hi": "कुल अनुपस्थित",
    "bi": "Total Absent (कुल अनुपस्थित)"
  },
  "कुल अनुपस्थित": {
    "en": "Total Absent",
    "hi": "कुल अनुपस्थित",
    "bi": "Total Absent (कुल अनुपस्थित)"
  },
  "total absent (कुल अनुपस्थित)": {
    "en": "Total Absent",
    "hi": "कुल अनुपस्थित",
    "bi": "Total Absent (कुल अनुपस्थित)"
  },
  "daily wage": {
    "en": "Daily Wage",
    "hi": "दैनिक मजदूरी",
    "bi": "Daily Wage (दैनिक मजदूरी)"
  },
  "दैनिक मजदूरी": {
    "en": "Daily Wage",
    "hi": "दैनिक मजदूरी",
    "bi": "Daily Wage (दैनिक मजदूरी)"
  },
  "daily wage (दैनिक मजदूरी)": {
    "en": "Daily Wage",
    "hi": "दैनिक मजदूरी",
    "bi": "Daily Wage (दैनिक मजदूरी)"
  },
  "total wage": {
    "en": "Total Wage",
    "hi": "कुल मजदूरी",
    "bi": "Total Wage (कुल मजदूरी)"
  },
  "कुल मजदूरी": {
    "en": "Total Wage",
    "hi": "कुल मजदूरी",
    "bi": "Total Wage (कुल मजदूरी)"
  },
  "total wage (कुल मजदूरी)": {
    "en": "Total Wage",
    "hi": "कुल मजदूरी",
    "bi": "Total Wage (कुल मजदूरी)"
  },
  "mark all present": {
    "en": "Mark All Present",
    "hi": "सभी को उपस्थित करें",
    "bi": "Mark All Present (सभी उपस्थित)"
  },
  "सभी को उपस्थित करें": {
    "en": "Mark All Present",
    "hi": "सभी को उपस्थित करें",
    "bi": "Mark All Present (सभी उपस्थित)"
  },
  "mark all present (सभी उपस्थित)": {
    "en": "Mark All Present",
    "hi": "सभी को उपस्थित करें",
    "bi": "Mark All Present (सभी उपस्थित)"
  },
  "save attendance": {
    "en": "Save Attendance",
    "hi": "हाजिरी सुरक्षित करें",
    "bi": "Save Attendance (हाजिरी सुरक्षित करें)"
  },
  "हाजिरी सुरक्षित करें": {
    "en": "Save Attendance",
    "hi": "हाजिरी सुरक्षित करें",
    "bi": "Save Attendance (हाजिरी सुरक्षित करें)"
  },
  "save attendance (हाजिरी सुरक्षित करें)": {
    "en": "Save Attendance",
    "hi": "हाजिरी सुरक्षित करें",
    "bi": "Save Attendance (हाजिरी सुरक्षित करें)"
  },
  "material": {
    "en": "Material",
    "hi": "सामग्री",
    "bi": "Material (सामग्री)"
  },
  "सामग्री": {
    "en": "Material",
    "hi": "सामग्री",
    "bi": "Material (सामग्री)"
  },
  "material (सामग्री)": {
    "en": "Material",
    "hi": "सामग्री",
    "bi": "Material (सामग्री)"
  },
  "material management": {
    "en": "Material Management",
    "hi": "सामग्री प्रबंधन",
    "bi": "Material Management (सामग्री प्रबंधन)"
  },
  "सामग्री प्रबंधन": {
    "en": "Material Management",
    "hi": "सामग्री प्रबंधन",
    "bi": "Material Management (सामग्री प्रबंधन)"
  },
  "material management (सामग्री प्रबंधन)": {
    "en": "Material Management",
    "hi": "सामग्री प्रबंधन",
    "bi": "Material Management (सामग्री प्रबंधन)"
  },
  "stock": {
    "en": "Stock",
    "hi": "स्टॉक",
    "bi": "Stock (स्टॉक)"
  },
  "स्टॉक": {
    "en": "Stock",
    "hi": "स्टॉक",
    "bi": "Stock (स्टॉक)"
  },
  "stock (स्टॉक)": {
    "en": "Stock",
    "hi": "स्टॉक",
    "bi": "Stock (स्टॉक)"
  },
  "stock overview": {
    "en": "Stock Overview",
    "hi": "स्टॉक विवरण",
    "bi": "Stock Overview (स्टॉक विवरण)"
  },
  "स्टॉक विवरण": {
    "en": "Stock Overview",
    "hi": "स्टॉक विवरण",
    "bi": "Stock Overview (स्टॉक विवरण)"
  },
  "stock overview (स्टॉक विवरण)": {
    "en": "Stock Overview",
    "hi": "स्टॉक विवरण",
    "bi": "Stock Overview (स्टॉक विवरण)"
  },
  "usage": {
    "en": "Usage",
    "hi": "खपत",
    "bi": "Usage (खपत)"
  },
  "खपत": {
    "en": "Usage",
    "hi": "खपत",
    "bi": "Usage (खपत)"
  },
  "usage (खपत)": {
    "en": "Usage",
    "hi": "खपत",
    "bi": "Usage (खपत)"
  },
  "daily usage": {
    "en": "Daily Usage",
    "hi": "दैनिक खपत",
    "bi": "Daily Usage (दैनिक खपत)"
  },
  "दैनिक खपत": {
    "en": "Daily Usage",
    "hi": "दैनिक खपत",
    "bi": "Daily Usage (दैनिक खपत)"
  },
  "daily usage (दैनिक खपत)": {
    "en": "Daily Usage",
    "hi": "दैनिक खपत",
    "bi": "Daily Usage (दैनिक खपत)"
  },
  "daily entry": {
    "en": "Daily Entry",
    "hi": "दैनिक प्रविष्टि",
    "bi": "Daily Entry (दैनिक प्रविष्टि)"
  },
  "दैनिक प्रविष्टि": {
    "en": "Daily Entry",
    "hi": "दैनिक प्रविष्टि",
    "bi": "Daily Entry (दैनिक प्रविष्टि)"
  },
  "daily entry (दैनिक प्रविष्टि)": {
    "en": "Daily Entry",
    "hi": "दैनिक प्रविष्टि",
    "bi": "Daily Entry (दैनिक प्रविष्टि)"
  },
  "+ usage entry": {
    "en": "+ Usage Entry",
    "hi": "+ खपत प्रविष्टि",
    "bi": "+ Usage Entry (+ खपत प्रविष्टि)"
  },
  "+ खपत प्रविष्टि": {
    "en": "+ Usage Entry",
    "hi": "+ खपत प्रविष्टि",
    "bi": "+ Usage Entry (+ खपत प्रविष्टि)"
  },
  "+ usage entry (+ खपत प्रविष्टि)": {
    "en": "+ Usage Entry",
    "hi": "+ खपत प्रविष्टि",
    "bi": "+ Usage Entry (+ खपत प्रविष्टि)"
  },
  "store": {
    "en": "Store",
    "hi": "स्टोर",
    "bi": "Store (स्टोर)"
  },
  "स्टोर": {
    "en": "Store",
    "hi": "स्टोर",
    "bi": "Store (स्टोर)"
  },
  "store (स्टोर)": {
    "en": "Store",
    "hi": "स्टोर",
    "bi": "Store (स्टोर)"
  },
  "central store": {
    "en": "Central Store",
    "hi": "केंद्रीय स्टोर",
    "bi": "Central Store (केंद्रीय स्टोर)"
  },
  "केंद्रीय स्टोर": {
    "en": "Central Store",
    "hi": "केंद्रीय स्टोर",
    "bi": "Central Store (केंद्रीय स्टोर)"
  },
  "central store (केंद्रीय स्टोर)": {
    "en": "Central Store",
    "hi": "केंद्रीय स्टोर",
    "bi": "Central Store (केंद्रीय स्टोर)"
  },
  "inward stock": {
    "en": "Inward Stock",
    "hi": "सामग्री आवक",
    "bi": "Inward Stock (सामग्री आवक)"
  },
  "सामग्री आवक": {
    "en": "Inward Stock",
    "hi": "सामग्री आवक",
    "bi": "Inward Stock (सामग्री आवक)"
  },
  "inward stock (सामग्री आवक)": {
    "en": "Inward Stock",
    "hi": "सामग्री आवक",
    "bi": "Inward Stock (सामग्री आवक)"
  },
  "+ inward entry": {
    "en": "+ Inward Entry",
    "hi": "+ नई आवक दर्ज करें",
    "bi": "+ Inward Entry (नई आवक दर्ज करें)"
  },
  "+ नई आवक दर्ज करें": {
    "en": "+ Inward Entry",
    "hi": "+ नई आवक दर्ज करें",
    "bi": "+ Inward Entry (नई आवक दर्ज करें)"
  },
  "+ inward entry (नई आवक दर्ज करें)": {
    "en": "+ Inward Entry",
    "hi": "+ नई आवक दर्ज करें",
    "bi": "+ Inward Entry (नई आवक दर्ज करें)"
  },
  "current balance": {
    "en": "Current Balance",
    "hi": "वर्तमान शेष",
    "bi": "Current Balance (वर्तमान शेष)"
  },
  "वर्तमान शेष": {
    "en": "Current Balance",
    "hi": "वर्तमान शेष",
    "bi": "Current Balance (वर्तमान शेष)"
  },
  "current balance (वर्तमान शेष)": {
    "en": "Current Balance",
    "hi": "वर्तमान शेष",
    "bi": "Current Balance (वर्तमान शेष)"
  },
  "total inward": {
    "en": "Total Inward",
    "hi": "कुल आवक",
    "bi": "Total Inward (कुल आवक)"
  },
  "कुल आवक": {
    "en": "Total Inward",
    "hi": "कुल आवक",
    "bi": "Total Inward (कुल आवक)"
  },
  "total inward (कुल आवक)": {
    "en": "Total Inward",
    "hi": "कुल आवक",
    "bi": "Total Inward (कुल आवक)"
  },
  "total outward": {
    "en": "Total Outward",
    "hi": "कुल निर्गम",
    "bi": "Total Outward (कुल निर्गम)"
  },
  "कुल निर्गम": {
    "en": "Total Outward",
    "hi": "कुल निर्गम",
    "bi": "Total Outward (कुल निर्गम)"
  },
  "total outward (कुल निर्गम)": {
    "en": "Total Outward",
    "hi": "कुल निर्गम",
    "bi": "Total Outward (कुल निर्गम)"
  },
  "opening balance": {
    "en": "Opening Balance",
    "hi": "प्रारंभिक शेष",
    "bi": "Opening Balance (प्रारंभिक शेष)"
  },
  "प्रारंभिक शेष": {
    "en": "Opening Balance",
    "hi": "प्रारंभिक शेष",
    "bi": "Opening Balance (प्रारंभिक शेष)"
  },
  "opening balance (प्रारंभिक शेष)": {
    "en": "Opening Balance",
    "hi": "प्रारंभिक शेष",
    "bi": "Opening Balance (प्रारंभिक शेष)"
  },
  "closing balance": {
    "en": "Closing Balance",
    "hi": "अंतिम शेष",
    "bi": "Closing Balance (अंतिम शेष)"
  },
  "अंतिम शेष": {
    "en": "Closing Balance",
    "hi": "अंतिम शेष",
    "bi": "Closing Balance (अंतिम शेष)"
  },
  "closing balance (अंतिम शेष)": {
    "en": "Closing Balance",
    "hi": "अंतिम शेष",
    "bi": "Closing Balance (अंतिम शेष)"
  },
  "material name": {
    "en": "Material Name",
    "hi": "सामग्री का नाम",
    "bi": "Material Name (सामग्री का नाम)"
  },
  "सामग्री का नाम": {
    "en": "Material Name",
    "hi": "सामग्री का नाम",
    "bi": "Material Name (सामग्री का नाम)"
  },
  "material name (सामग्री का नाम)": {
    "en": "Material Name",
    "hi": "सामग्री का नाम",
    "bi": "Material Name (सामग्री का नाम)"
  },
  "material category": {
    "en": "Material Category",
    "hi": "सामग्री श्रेणी",
    "bi": "Material Category (सामग्री श्रेणी)"
  },
  "सामग्री श्रेणी": {
    "en": "Material Category",
    "hi": "सामग्री श्रेणी",
    "bi": "Material Category (सामग्री श्रेणी)"
  },
  "material category (सामग्री श्रेणी)": {
    "en": "Material Category",
    "hi": "सामग्री श्रेणी",
    "bi": "Material Category (सामग्री श्रेणी)"
  },
  "pipes": {
    "en": "Pipes",
    "hi": "पाइप",
    "bi": "Pipes (पाइप)"
  },
  "पाइप": {
    "en": "Pipes",
    "hi": "पाइप",
    "bi": "Pipes (पाइप)"
  },
  "pipes (पाइप)": {
    "en": "Pipes",
    "hi": "पाइप",
    "bi": "Pipes (पाइप)"
  },
  "motors & starters": {
    "en": "Motors & Starters",
    "hi": "मोटर एवं स्टार्टर",
    "bi": "Motors & Starters (मोटर व स्टार्टर)"
  },
  "मोटर एवं स्टार्टर": {
    "en": "Motors & Starters",
    "hi": "मोटर एवं स्टार्टर",
    "bi": "Motors & Starters (मोटर व स्टार्टर)"
  },
  "motors & starters (मोटर व स्टार्टर)": {
    "en": "Motors & Starters",
    "hi": "मोटर एवं स्टार्टर",
    "bi": "Motors & Starters (मोटर व स्टार्टर)"
  },
  "cables & wires": {
    "en": "Cables & Wires",
    "hi": "केबल एवं तार",
    "bi": "Cables & Wires (केबल व तार)"
  },
  "केबल एवं तार": {
    "en": "Cables & Wires",
    "hi": "केबल एवं तार",
    "bi": "Cables & Wires (केबल व तार)"
  },
  "cables & wires (केबल व तार)": {
    "en": "Cables & Wires",
    "hi": "केबल एवं तार",
    "bi": "Cables & Wires (केबल व तार)"
  },
  "fittings & valves": {
    "en": "Fittings & Valves",
    "hi": "फिटिंग एवं वाल्व",
    "bi": "Fittings & Valves (फिटिंग व वाल्व)"
  },
  "फिटिंग एवं वाल्व": {
    "en": "Fittings & Valves",
    "hi": "फिटिंग एवं वाल्व",
    "bi": "Fittings & Valves (फिटिंग व वाल्व)"
  },
  "fittings & valves (फिटिंग व वाल्व)": {
    "en": "Fittings & Valves",
    "hi": "फिटिंग एवं वाल्व",
    "bi": "Fittings & Valves (फिटिंग व वाल्व)"
  },
  "civil materials": {
    "en": "Civil Materials",
    "hi": "सिविल सामग्री",
    "bi": "Civil Materials (सिविल सामग्री)"
  },
  "सिविल सामग्री": {
    "en": "Civil Materials",
    "hi": "सिविल सामग्री",
    "bi": "Civil Materials (सिविल सामग्री)"
  },
  "civil materials (सिविल सामग्री)": {
    "en": "Civil Materials",
    "hi": "सिविल सामग्री",
    "bi": "Civil Materials (सिविल सामग्री)"
  },
  "tools & equipment": {
    "en": "Tools & Equipment",
    "hi": "उपकरण एवं औजार",
    "bi": "Tools & Equipment (उपकरण व औजार)"
  },
  "उपकरण एवं औजार": {
    "en": "Tools & Equipment",
    "hi": "उपकरण एवं औजार",
    "bi": "Tools & Equipment (उपकरण व औजार)"
  },
  "tools & equipment (उपकरण व औजार)": {
    "en": "Tools & Equipment",
    "hi": "उपकरण एवं औजार",
    "bi": "Tools & Equipment (उपकरण व औजार)"
  },
  "progress": {
    "en": "Progress",
    "hi": "प्रगति",
    "bi": "Progress (प्रगति)"
  },
  "प्रगति": {
    "en": "Progress",
    "hi": "प्रगति",
    "bi": "Progress (प्रगति)"
  },
  "progress (प्रगति)": {
    "en": "Progress",
    "hi": "प्रगति",
    "bi": "Progress (प्रगति)"
  },
  "dpr": {
    "en": "DPR",
    "hi": "दैनिक कार्य पर्चा",
    "bi": "DPR (दैनिक कार्य पर्चा)"
  },
  "दैनिक कार्य पर्चा (dpr)": {
    "en": "DPR",
    "hi": "दैनिक कार्य पर्चा",
    "bi": "DPR (दैनिक कार्य पर्चा)"
  },
  "दैनिक कार्य पर्चा": {
    "en": "DPR",
    "hi": "दैनिक कार्य पर्चा",
    "bi": "DPR (दैनिक कार्य पर्चा)"
  },
  "dpr (दैनिक कार्य पर्चा)": {
    "en": "DPR",
    "hi": "दैनिक कार्य पर्चा",
    "bi": "DPR (दैनिक कार्य पर्चा)"
  },
  "daily progress report": {
    "en": "Daily Progress Report",
    "hi": "दैनिक कार्य प्रगति विवरणी",
    "bi": "Daily Progress Report (दैनिक कार्य प्रगति विवरणी)"
  },
  "दैनिक कार्य प्रगति विवरणी": {
    "en": "Daily Progress Report",
    "hi": "दैनिक कार्य प्रगति विवरणी",
    "bi": "Daily Progress Report (दैनिक कार्य प्रगति विवरणी)"
  },
  "daily progress report (दैनिक कार्य प्रगति विवरणी)": {
    "en": "Daily Progress Report",
    "hi": "दैनिक कार्य प्रगति विवरणी",
    "bi": "Daily Progress Report (दैनिक कार्य प्रगति विवरणी)"
  },
  "daily progress report (dpr)": {
    "en": "Daily Progress Report (DPR)",
    "hi": "दैनिक कार्य प्रगति विवरणी",
    "bi": "Daily Progress Report (दैनिक कार्य प्रगति विवरणी - DPR)"
  },
  "दैनिक कार्य प्रगति विवरणी (dpr)": {
    "en": "Daily Progress Report (DPR)",
    "hi": "दैनिक कार्य प्रगति विवरणी",
    "bi": "Daily Progress Report (दैनिक कार्य प्रगति विवरणी - DPR)"
  },
  "daily progress report (दैनिक कार्य प्रगति विवरणी - dpr)": {
    "en": "Daily Progress Report (DPR)",
    "hi": "दैनिक कार्य प्रगति विवरणी",
    "bi": "Daily Progress Report (दैनिक कार्य प्रगति विवरणी - DPR)"
  },
  "supervisor work area": {
    "en": "Supervisor Work Area",
    "hi": "सुपरवाइजर कार्य क्षेत्र",
    "bi": "Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "सुपरवाइजर कार्य क्षेत्र": {
    "en": "Supervisor Work Area",
    "hi": "सुपरवाइजर कार्य क्षेत्र",
    "bi": "Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "supervisor work area (सुपरवाइजर कार्य क्षेत्र)": {
    "en": "(Supervisor Work Area)",
    "hi": "(सुपरवाइजर कार्य क्षेत्र)",
    "bi": "Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "site photos": {
    "en": "Site Photos",
    "hi": "साइट फोटो",
    "bi": "Site Photos (साइट फोटो)"
  },
  "साइट फोटो": {
    "en": "Site Photos",
    "hi": "साइट फोटो",
    "bi": "Site Photos (साइट फोटो)"
  },
  "site photos (साइट फोटो)": {
    "en": "Site Photos",
    "hi": "साइट फोटो",
    "bi": "Site Photos (साइट फोटो)"
  },
  "upload photos": {
    "en": "Upload Photos",
    "hi": "फोटो अपलोड करें",
    "bi": "Upload Photos (फोटो अपलोड करें)"
  },
  "फोटो अपलोड करें": {
    "en": "Upload Photos",
    "hi": "फोटो अपलोड करें",
    "bi": "Upload Photos (फोटो अपलोड करें)"
  },
  "upload photos (फोटो अपलोड करें)": {
    "en": "Upload Photos",
    "hi": "फोटो अपलोड करें",
    "bi": "Upload Photos (फोटो अपलोड करें)"
  },
  "ward no.": {
    "en": "Ward No.",
    "hi": "वार्ड संख्या",
    "bi": "Ward No. (वार्ड संख्या)"
  },
  "वार्ड संख्या": {
    "en": "Ward No.",
    "hi": "वार्ड संख्या",
    "bi": "Ward No. (वार्ड संख्या)"
  },
  "ward no. (वार्ड संख्या)": {
    "en": "Ward No.",
    "hi": "वार्ड संख्या",
    "bi": "Ward No. (वार्ड संख्या)"
  },
  "work activity": {
    "en": "Work Activity",
    "hi": "कार्य विवरण",
    "bi": "Work Activity (कार्य विवरण)"
  },
  "कार्य विवरण": {
    "en": "Work Activity",
    "hi": "कार्य विवरण",
    "bi": "Work Activity (कार्य विवरण)"
  },
  "work activity (कार्य विवरण)": {
    "en": "Work Activity",
    "hi": "कार्य विवरण",
    "bi": "Work Activity (कार्य विवरण)"
  },
  "new connection": {
    "en": "New Connection",
    "hi": "नया कनेक्शन",
    "bi": "New Connection (नया कनेक्शन)"
  },
  "नया कनेक्शन": {
    "en": "New Connection",
    "hi": "नया कनेक्शन",
    "bi": "New Connection (नया कनेक्शन)"
  },
  "new connection (नया कनेक्शन)": {
    "en": "New Connection",
    "hi": "नया कनेक्शन",
    "bi": "New Connection (नया कनेक्शन)"
  },
  "connection repairing": {
    "en": "Connection Repairing",
    "hi": "कनेक्शन मरम्मत",
    "bi": "Connection Repairing (कनेक्शन मरम्मत)"
  },
  "कनेक्शन मरम्मत": {
    "en": "Connection Repairing",
    "hi": "कनेक्शन मरम्मत",
    "bi": "Connection Repairing (कनेक्शन मरम्मत)"
  },
  "connection repairing (कनेक्शन मरम्मत)": {
    "en": "Connection Repairing",
    "hi": "कनेक्शन मरम्मत",
    "bi": "Connection Repairing (कनेक्शन मरम्मत)"
  },
  "motor/starter repair": {
    "en": "Motor/Starter Repair",
    "hi": "मोटर/स्टार्टर मरम्मत",
    "bi": "Motor/Starter Repair (मोटर/स्टार्टर मरम्मत)"
  },
  "मोटर/स्टार्टर मरम्मत": {
    "en": "Motor/Starter Repair",
    "hi": "मोटर/स्टार्टर मरम्मत",
    "bi": "Motor/Starter Repair (मोटर/स्टार्टर मरम्मत)"
  },
  "motor/starter repair (मोटर/स्टार्टर मरम्मत)": {
    "en": "Motor/Starter Repair",
    "hi": "मोटर/स्टार्टर मरम्मत",
    "bi": "Motor/Starter Repair (मोटर/स्टार्टर मरम्मत)"
  },
  "main pipe repairing": {
    "en": "Main Pipe Repairing",
    "hi": "मेन पाइपलाइन मरम्मत",
    "bi": "Main Pipe Repairing (मेन पाइपलाइन मरम्मत)"
  },
  "मेन पाइपलाइन मरम्मत": {
    "en": "Main Pipe Repairing",
    "hi": "मेन पाइपलाइन मरम्मत",
    "bi": "Main Pipe Repairing (मेन पाइपलाइन मरम्मत)"
  },
  "main pipe repairing (मेन पाइपलाइन मरम्मत)": {
    "en": "Main Pipe Repairing",
    "hi": "मेन पाइपलाइन मरम्मत",
    "bi": "Main Pipe Repairing (मेन पाइपलाइन मरम्मत)"
  },
  "new motor & starter": {
    "en": "New Motor & Starter",
    "hi": "नया मोटर व स्टार्टर",
    "bi": "New Motor & Starter (नया मोटर व स्टार्टर)"
  },
  "नया मोटर व स्टार्टर": {
    "en": "New Motor & Starter",
    "hi": "नया मोटर व स्टार्टर",
    "bi": "New Motor & Starter (नया मोटर व स्टार्टर)"
  },
  "new motor & starter (नया मोटर व स्टार्टर)": {
    "en": "New Motor & Starter",
    "hi": "नया मोटर व स्टार्टर",
    "bi": "New Motor & Starter (नया मोटर व स्टार्टर)"
  },
  "other work": {
    "en": "Other Work",
    "hi": "अन्य कार्य",
    "bi": "Other Work (अन्य कार्य)"
  },
  "अन्य कार्य": {
    "en": "Other Work",
    "hi": "अन्य कार्य",
    "bi": "Other Work (अन्य कार्य)"
  },
  "other work (अन्य कार्य)": {
    "en": "Other Work",
    "hi": "अन्य कार्य",
    "bi": "Other Work (अन्य कार्य)"
  },
  "save dpr": {
    "en": "Save DPR",
    "hi": "DPR सुरक्षित करें",
    "bi": "Save DPR (DPR सुरक्षित करें)"
  },
  "dpr सुरक्षित करें": {
    "en": "Save DPR",
    "hi": "DPR सुरक्षित करें",
    "bi": "Save DPR (DPR सुरक्षित करें)"
  },
  "save dpr (dpr सुरक्षित करें)": {
    "en": "Save DPR",
    "hi": "DPR सुरक्षित करें",
    "bi": "Save DPR (DPR सुरक्षित करें)"
  },
  "print dpr (a4)": {
    "en": "Print DPR (A4)",
    "hi": "A4 प्रिंट निकालें",
    "bi": "Print DPR (A4 प्रिंट)"
  },
  "a4 प्रिंट निकालें": {
    "en": "Print DPR (A4)",
    "hi": "A4 प्रिंट निकालें",
    "bi": "Print DPR (A4 प्रिंट)"
  },
  "print dpr (a4 प्रिंट)": {
    "en": "Print DPR (A4)",
    "hi": "A4 प्रिंट निकालें",
    "bi": "Print DPR (A4 प्रिंट)"
  },
  "letters": {
    "en": "Letters",
    "hi": "पत्र",
    "bi": "Letters (पत्र)"
  },
  "पत्र": {
    "en": "Letters",
    "hi": "पत्र",
    "bi": "Letters (पत्र)"
  },
  "letters (पत्र)": {
    "en": "Letters",
    "hi": "पत्र",
    "bi": "Letters (पत्र)"
  },
  "outgoing letters register": {
    "en": "Outgoing Letters Register",
    "hi": "जावक पत्र रजिस्टर",
    "bi": "Outgoing Letters Register (जावक पत्र रजिस्टर)"
  },
  "जावक पत्र रजिस्टर": {
    "en": "Outgoing Letters Register",
    "hi": "जावक पत्र रजिस्टर",
    "bi": "Outgoing Letters Register (जावक पत्र रजिस्टर)"
  },
  "outgoing letters register (जावक पत्र रजिस्टर)": {
    "en": "Outgoing Letters Register",
    "hi": "जावक पत्र रजिस्टर",
    "bi": "Outgoing Letters Register (जावक पत्र रजिस्टर)"
  },
  "dispatch register": {
    "en": "Dispatch Register",
    "hi": "प्रेषण पंजी",
    "bi": "Dispatch Register (प्रेषण पंजी)"
  },
  "प्रेषण पंजी": {
    "en": "Dispatch Register",
    "hi": "प्रेषण पंजी",
    "bi": "Dispatch Register (प्रेषण पंजी)"
  },
  "dispatch register (प्रेषण पंजी)": {
    "en": "Dispatch Register",
    "hi": "प्रेषण पंजी",
    "bi": "Dispatch Register (प्रेषण पंजी)"
  },
  "+ new letter reference": {
    "en": "+ New Letter Reference",
    "hi": "+ नया पत्रांक दर्ज करें",
    "bi": "+ New Letter Reference (नया पत्रांक दर्ज करें)"
  },
  "+ नया पत्रांक दर्ज करें": {
    "en": "+ New Letter Reference",
    "hi": "+ नया पत्रांक दर्ज करें",
    "bi": "+ New Letter Reference (नया पत्रांक दर्ज करें)"
  },
  "+ new letter reference (नया पत्रांक दर्ज करें)": {
    "en": "+ New Letter Reference",
    "hi": "+ नया पत्रांक दर्ज करें",
    "bi": "+ New Letter Reference (नया पत्रांक दर्ज करें)"
  },
  "reference no.": {
    "en": "Reference No.",
    "hi": "पत्रांक संख्या",
    "bi": "Reference No. (पत्रांक संख्या)"
  },
  "पत्रांक संख्या": {
    "en": "Reference No.",
    "hi": "पत्रांक संख्या",
    "bi": "Reference No. (पत्रांक संख्या)"
  },
  "reference no. (पत्रांक संख्या)": {
    "en": "Reference No.",
    "hi": "पत्रांक संख्या",
    "bi": "Reference No. (पत्रांक संख्या)"
  },
  "department": {
    "en": "Department",
    "hi": "विभाग",
    "bi": "Department (विभाग)"
  },
  "विभाग": {
    "en": "Department",
    "hi": "विभाग",
    "bi": "Department (विभाग)"
  },
  "department (विभाग)": {
    "en": "Department",
    "hi": "विभाग",
    "bi": "Department (विभाग)"
  },
  "subject": {
    "en": "Subject",
    "hi": "विषय",
    "bi": "Subject (विषय)"
  },
  "विषय": {
    "en": "Subject",
    "hi": "विषय",
    "bi": "Subject (विषय)"
  },
  "subject (विषय)": {
    "en": "Subject",
    "hi": "विषय",
    "bi": "Subject (विषय)"
  },
  "recipient": {
    "en": "Recipient",
    "hi": "पाने वाले का नाम / पद",
    "bi": "Recipient (प्राप्तकर्ता)"
  },
  "पाने वाले का नाम / पद": {
    "en": "Recipient",
    "hi": "पाने वाले का नाम / पद",
    "bi": "Recipient (प्राप्तकर्ता)"
  },
  "recipient (प्राप्तकर्ता)": {
    "en": "Recipient",
    "hi": "पाने वाले का नाम / पद",
    "bi": "Recipient (प्राप्तकर्ता)"
  },
  "dispatch mode": {
    "en": "Dispatch Mode",
    "hi": "प्रेषण माध्यम",
    "bi": "Dispatch Mode (प्रेषण माध्यम)"
  },
  "प्रेषण माध्यम": {
    "en": "Dispatch Mode",
    "hi": "प्रेषण माध्यम",
    "bi": "Dispatch Mode (प्रेषण माध्यम)"
  },
  "dispatch mode (प्रेषण माध्यम)": {
    "en": "Dispatch Mode",
    "hi": "प्रेषण माध्यम",
    "bi": "Dispatch Mode (प्रेषण माध्यम)"
  },
  "speed post / hand delivery": {
    "en": "Speed Post / Hand Delivery",
    "hi": "स्पीड पोस्ट / हस्तगत",
    "bi": "Speed Post / Hand Delivery (स्पीड पोस्ट / हस्तगत)"
  },
  "स्पीड पोस्ट / हस्तगत": {
    "en": "Speed Post / Hand Delivery",
    "hi": "स्पीड पोस्ट / हस्तगत",
    "bi": "Speed Post / Hand Delivery (स्पीड पोस्ट / हस्तगत)"
  },
  "speed post / hand delivery (स्पीड पोस्ट / हस्तगत)": {
    "en": "Speed Post / Hand Delivery",
    "hi": "स्पीड पोस्ट / हस्तगत",
    "bi": "Speed Post / Hand Delivery (स्पीड पोस्ट / हस्तगत)"
  },
  "reports": {
    "en": "Reports",
    "hi": "रिपोर्ट्स",
    "bi": "Reports (रिपोर्ट्स)"
  },
  "रिपोर्ट्स": {
    "en": "Reports",
    "hi": "रिपोर्ट्स",
    "bi": "Reports (रिपोर्ट्स)"
  },
  "reports (रिपोर्ट्स)": {
    "en": "Reports",
    "hi": "रिपोर्ट्स",
    "bi": "Reports (रिपोर्ट्स)"
  },
  "daily ledger": {
    "en": "Daily Ledger",
    "hi": "दैनिक लेजर",
    "bi": "Daily Ledger (दैनिक लेजर)"
  },
  "दैनिक लेजर": {
    "en": "Daily Ledger",
    "hi": "दैनिक लेजर",
    "bi": "Daily Ledger (दैनिक लेजर)"
  },
  "daily ledger (दैनिक लेजर)": {
    "en": "Daily Ledger",
    "hi": "दैनिक लेजर",
    "bi": "Daily Ledger (दैनिक लेजर)"
  },
  "monthly ledger": {
    "en": "Monthly Ledger",
    "hi": "मासिक लेजर",
    "bi": "Monthly Ledger (मासिक लेजर)"
  },
  "मासिक लेजर": {
    "en": "Monthly Ledger",
    "hi": "मासिक लेजर",
    "bi": "Monthly Ledger (मासिक लेजर)"
  },
  "monthly ledger (मासिक लेजर)": {
    "en": "Monthly Ledger",
    "hi": "मासिक लेजर",
    "bi": "Monthly Ledger (मासिक लेजर)"
  },
  "cost matrix": {
    "en": "Cost Matrix",
    "hi": "लागत मैट्रिक्स",
    "bi": "Cost Matrix (लागत मैट्रिक्स)"
  },
  "लागत मैट्रिक्स": {
    "en": "Cost Matrix",
    "hi": "लागत मैट्रिक्स",
    "bi": "Cost Matrix (लागत मैट्रिक्स)"
  },
  "cost matrix (लागत मैट्रिक्स)": {
    "en": "Cost Matrix",
    "hi": "लागत मैट्रिक्स",
    "bi": "Cost Matrix (लागत मैट्रिक्स)"
  },
  "total material cost": {
    "en": "Total Material Cost",
    "hi": "कुल सामग्री लागत",
    "bi": "Total Material Cost (कुल सामग्री लागत)"
  },
  "कुल सामग्री लागत": {
    "en": "Total Material Cost",
    "hi": "कुल सामग्री लागत",
    "bi": "Total Material Cost (कुल सामग्री लागत)"
  },
  "total material cost (कुल सामग्री लागत)": {
    "en": "Total Material Cost",
    "hi": "कुल सामग्री लागत",
    "bi": "Total Material Cost (कुल सामग्री लागत)"
  },
  "date range": {
    "en": "Date Range",
    "hi": "तारीख सीमा",
    "bi": "Date Range (तारीख सीमा)"
  },
  "तारीख सीमा": {
    "en": "Date Range",
    "hi": "तारीख सीमा",
    "bi": "Date Range (तारीख सीमा)"
  },
  "date range (तारीख सीमा)": {
    "en": "Date Range",
    "hi": "तारीख सीमा",
    "bi": "Date Range (तारीख सीमा)"
  },
  "from date": {
    "en": "From Date",
    "hi": "प्रारंभ तिथि",
    "bi": "From Date (प्रारंभ तिथि)"
  },
  "प्रारंभ तिथि": {
    "en": "From Date",
    "hi": "प्रारंभ तिथि",
    "bi": "From Date (प्रारंभ तिथि)"
  },
  "from date (प्रारंभ तिथि)": {
    "en": "From Date",
    "hi": "प्रारंभ तिथि",
    "bi": "From Date (प्रारंभ तिथि)"
  },
  "to date": {
    "en": "To Date",
    "hi": "अंतिम तिथि",
    "bi": "To Date (अंतिम तिथि)"
  },
  "अंतिम तिथि": {
    "en": "To Date",
    "hi": "अंतिम तिथि",
    "bi": "To Date (अंतिम तिथि)"
  },
  "to date (अंतिम तिथि)": {
    "en": "To Date",
    "hi": "अंतिम तिथि",
    "bi": "To Date (अंतिम तिथि)"
  },
  "generate report": {
    "en": "Generate Report",
    "hi": "रिपोर्ट तैयार करें",
    "bi": "Generate Report (रिपोर्ट तैयार करें)"
  },
  "रिपोर्ट तैयार करें": {
    "en": "Generate Report",
    "hi": "रिपोर्ट तैयार करें",
    "bi": "Generate Report (रिपोर्ट तैयार करें)"
  },
  "generate report (रिपोर्ट तैयार करें)": {
    "en": "Generate Report",
    "hi": "रिपोर्ट तैयार करें",
    "bi": "Generate Report (रिपोर्ट तैयार करें)"
  },
  "master": {
    "en": "Master",
    "hi": "मास्टर",
    "bi": "Master (मास्टर डेटा)"
  },
  "मास्टर": {
    "en": "Master",
    "hi": "मास्टर",
    "bi": "Master (मास्टर डेटा)"
  },
  "master (मास्टर डेटा)": {
    "en": "Master",
    "hi": "मास्टर",
    "bi": "Master (मास्टर डेटा)"
  },
  "sites management": {
    "en": "Sites Management",
    "hi": "साइट्स प्रबंधन",
    "bi": "Sites Management (साइट्स प्रबंधन)"
  },
  "साइट्स प्रबंधन": {
    "en": "Sites Management",
    "hi": "साइट्स प्रबंधन",
    "bi": "Sites Management (साइट्स प्रबंधन)"
  },
  "sites management (साइट्स प्रबंधन)": {
    "en": "Sites Management",
    "hi": "साइट्स प्रबंधन",
    "bi": "Sites Management (साइट्स प्रबंधन)"
  },
  "rates master": {
    "en": "Rates Master",
    "hi": "दर सूची",
    "bi": "Rates Master (दर सूची)"
  },
  "दर सूची": {
    "en": "Rates Master",
    "hi": "दर सूची",
    "bi": "Rates Master (दर सूची)"
  },
  "rates master (दर सूची)": {
    "en": "Rates Master",
    "hi": "दर सूची",
    "bi": "Rates Master (दर सूची)"
  },
  "gps setup": {
    "en": "GPS Setup",
    "hi": "जीपीएस सेटअप",
    "bi": "GPS Setup (जीपीएस सेटअप)"
  },
  "जीपीएस सेटअप": {
    "en": "GPS Setup",
    "hi": "जीपीएस सेटअप",
    "bi": "GPS Setup (जीपीएस सेटअप)"
  },
  "gps setup (जीपीएस सेटअप)": {
    "en": "GPS Setup",
    "hi": "जीपीएस सेटअप",
    "bi": "GPS Setup (जीपीएस सेटअप)"
  },
  "app download": {
    "en": "App Download",
    "hi": "ऐप डाउनलोड",
    "bi": "App Download (ऐप डाउनलोड)"
  },
  "ऐप डाउनलोड": {
    "en": "App Download",
    "hi": "ऐप डाउनलोड",
    "bi": "App Download (ऐप डाउनलोड)"
  },
  "app download (ऐप डाउनलोड)": {
    "en": "App Download",
    "hi": "ऐप डाउनलोड",
    "bi": "App Download (ऐप डाउनलोड)"
  },
  "backup & restore": {
    "en": "Backup & Restore",
    "hi": "बैकअप एवं रिस्टोर",
    "bi": "Backup & Restore (बैकअप व रिस्टोर)"
  },
  "बैकअप एवं रिस्टोर": {
    "en": "Backup & Restore",
    "hi": "बैकअप एवं रिस्टोर",
    "bi": "Backup & Restore (बैकअप व रिस्टोर)"
  },
  "backup & restore (बैकअप व रिस्टोर)": {
    "en": "Backup & Restore",
    "hi": "बैकअप एवं रिस्टोर",
    "bi": "Backup & Restore (बैकअप व रिस्टोर)"
  },
  "track daily material usage (pipes, motors, cables, fittings) and generate reports across all 19 sites including mairwa, siwan, chhapra, madhubani, darbhanga.": {
    "en": "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga.",
    "hi": "मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।",
    "bi": "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga. (मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।)"
  },
  "मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।": {
    "en": "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga.",
    "hi": "मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।",
    "bi": "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga. (मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।)"
  },
  "track daily material usage (pipes, motors, cables, fittings) and generate reports across all 19 sites including mairwa, siwan, chhapra, madhubani, darbhanga. (मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।)": {
    "en": "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga.",
    "hi": "मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।",
    "bi": "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga. (मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।)"
  },
  "daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including siwan, mairwa, chapra, madhubani, darbhanga.": {
    "en": "Daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including Siwan, Mairwa, Chapra, Madhubani, Darbhanga.",
    "hi": "सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।",
    "bi": "Daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including Siwan, Mairwa, Chapra, Madhubani, Darbhanga. (सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।)"
  },
  "सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।": {
    "en": "Daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including Siwan, Mairwa, Chapra, Madhubani, Darbhanga.",
    "hi": "सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।",
    "bi": "Daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including Siwan, Mairwa, Chapra, Madhubani, Darbhanga. (सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।)"
  },
  "daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including siwan, mairwa, chapra, madhubani, darbhanga. (सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।)": {
    "en": "Daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including Siwan, Mairwa, Chapra, Madhubani, Darbhanga.",
    "hi": "सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।",
    "bi": "Daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including Siwan, Mairwa, Chapra, Madhubani, Darbhanga. (सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।)"
  },
  "sequential reference numbers (sk/yyyy-yy/0001) and dispatch records of letters sent to phed, rwd, dwsm, banks, and other departments.": {
    "en": "Sequential reference numbers (SK/YYYY-YY/0001) and dispatch records of letters sent to PHED, RWD, DWSM, Banks, and other departments.",
    "hi": "PHED, RWD, DWSM, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।",
    "bi": "Sequential reference numbers (SK/YYYY-YY/0001) and dispatch records of letters sent to PHED, RWD, DWSM, Banks, and other departments. (PHED, RWD, DWSM, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।)"
  },
  "phed, rwd, dwsm, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।": {
    "en": "Sequential reference numbers (SK/YYYY-YY/0001) and dispatch records of letters sent to PHED, RWD, DWSM, Banks, and other departments.",
    "hi": "PHED, RWD, DWSM, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।",
    "bi": "Sequential reference numbers (SK/YYYY-YY/0001) and dispatch records of letters sent to PHED, RWD, DWSM, Banks, and other departments. (PHED, RWD, DWSM, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।)"
  },
  "sequential reference numbers (sk/yyyy-yy/0001) and dispatch records of letters sent to phed, rwd, dwsm, banks, and other departments. (phed, rwd, dwsm, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।)": {
    "en": "Sequential reference numbers (SK/YYYY-YY/0001) and dispatch records of letters sent to PHED, RWD, DWSM, Banks, and other departments.",
    "hi": "PHED, RWD, DWSM, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।",
    "bi": "Sequential reference numbers (SK/YYYY-YY/0001) and dispatch records of letters sent to PHED, RWD, DWSM, Banks, and other departments. (PHED, RWD, DWSM, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या एवं प्रेषण विवरण।)"
  },
  "e.g. submission of pipeline work and fhtc connection progress report under har ghar nal ka jal scheme.": {
    "en": "e.g. Submission of pipeline work and FHTC connection progress report under Har Ghar Nal Ka Jal Scheme.",
    "hi": "जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं FHTC कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।",
    "bi": "e.g. Submission of pipeline work and FHTC connection progress report under Har Ghar Nal Ka Jal Scheme. (जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं FHTC कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।)"
  },
  "जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं fhtc कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।": {
    "en": "e.g. Submission of pipeline work and FHTC connection progress report under Har Ghar Nal Ka Jal Scheme.",
    "hi": "जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं FHTC कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।",
    "bi": "e.g. Submission of pipeline work and FHTC connection progress report under Har Ghar Nal Ka Jal Scheme. (जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं FHTC कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।)"
  },
  "e.g. submission of pipeline work and fhtc connection progress report under har ghar nal ka jal scheme. (जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं fhtc कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।)": {
    "en": "e.g. Submission of pipeline work and FHTC connection progress report under Har Ghar Nal Ka Jal Scheme.",
    "hi": "जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं FHTC कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।",
    "bi": "e.g. Submission of pipeline work and FHTC connection progress report under Har Ghar Nal Ka Jal Scheme. (जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं FHTC कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।)"
  },
  "e.g. hand delivered / speed post ed123456789in / acknowledgment attached": {
    "en": "e.g. Hand delivered / Speed Post ED123456789IN / Acknowledgment attached",
    "hi": "जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ED123456789IN / पावती संलग्न",
    "bi": "e.g. Hand delivered / Speed Post ED123456789IN / Acknowledgment attached (जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ED123456789IN / पावती संलग्न)"
  },
  "जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ed123456789in / पावती संलग्न": {
    "en": "e.g. Hand delivered / Speed Post ED123456789IN / Acknowledgment attached",
    "hi": "जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ED123456789IN / पावती संलग्न",
    "bi": "e.g. Hand delivered / Speed Post ED123456789IN / Acknowledgment attached (जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ED123456789IN / पावती संलग्न)"
  },
  "e.g. hand delivered / speed post ed123456789in / acknowledgment attached (जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ed123456789in / पावती संलग्न)": {
    "en": "e.g. Hand delivered / Speed Post ED123456789IN / Acknowledgment attached",
    "hi": "जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ED123456789IN / पावती संलग्न",
    "bi": "e.g. Hand delivered / Speed Post ED123456789IN / Acknowledgment attached (जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ED123456789IN / पावती संलग्न)"
  },
  "record materials used at site today with date and details": {
    "en": "Record materials used at site today with date and details",
    "hi": "साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें",
    "bi": "Record materials used at site today with date and details (साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें)"
  },
  "साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें": {
    "en": "Record materials used at site today with date and details",
    "hi": "साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें",
    "bi": "Record materials used at site today with date and details (साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें)"
  },
  "record materials used at site today with date and details (साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें)": {
    "en": "Record materials used at site today with date and details",
    "hi": "साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें",
    "bi": "Record materials used at site today with date and details (साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें)"
  },
  "📑 outgoing letters reference register": {
    "en": "📑 Outgoing Letters Reference Register",
    "hi": "📑 विभिन्न विभागों को जावक पत्र",
    "bi": "📑 Outgoing Letters Reference Register (📑 विभिन्न विभागों को जावक पत्र)"
  },
  "📑 विभिन्न विभागों को जावक पत्र": {
    "en": "📑 Outgoing Letters Reference Register",
    "hi": "📑 विभिन्न विभागों को जावक पत्र",
    "bi": "📑 Outgoing Letters Reference Register (📑 विभिन्न विभागों को जावक पत्र)"
  },
  "📑 outgoing letters reference register (📑 विभिन्न विभागों को जावक पत्र)": {
    "en": "📑 Outgoing Letters Reference Register",
    "hi": "📑 विभिन्न विभागों को जावक पत्र",
    "bi": "📑 Outgoing Letters Reference Register (📑 विभिन्न विभागों को जावक पत्र)"
  },
  "click any site to view its complete material ledger:": {
    "en": "Click any site to view its complete material ledger:",
    "hi": "किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:",
    "bi": "Click any site to view its complete material ledger: (किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:)"
  },
  "किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:": {
    "en": "Click any site to view its complete material ledger:",
    "hi": "किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:",
    "bi": "Click any site to view its complete material ledger: (किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:)"
  },
  "click any site to view its complete material ledger: (किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:)": {
    "en": "Click any site to view its complete material ledger:",
    "hi": "किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:",
    "bi": "Click any site to view its complete material ledger: (किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:)"
  },
  "1-page attendance register for masons, plumbers, helpers, and staff": {
    "en": "1-Page attendance register for masons, plumbers, helpers, and staff",
    "hi": "मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर",
    "bi": "1-Page attendance register for masons, plumbers, helpers, and staff (मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर)"
  },
  "मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर": {
    "en": "1-Page attendance register for masons, plumbers, helpers, and staff",
    "hi": "मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर",
    "bi": "1-Page attendance register for masons, plumbers, helpers, and staff (मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर)"
  },
  "1-page attendance register for masons, plumbers, helpers, and staff (मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर)": {
    "en": "1-Page attendance register for masons, plumbers, helpers, and staff",
    "hi": "मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर",
    "bi": "1-Page attendance register for masons, plumbers, helpers, and staff (मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर)"
  },
  "e.g. executive engineer, phed siwan": {
    "en": "e.g. Executive Engineer, PHED Siwan",
    "hi": "जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान",
    "bi": "e.g. Executive Engineer, PHED Siwan (जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान)"
  },
  "जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान": {
    "en": "e.g. Executive Engineer, PHED Siwan",
    "hi": "जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान",
    "bi": "e.g. Executive Engineer, PHED Siwan (जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान)"
  },
  "e.g. executive engineer, phed siwan (जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान)": {
    "en": "e.g. Executive Engineer, PHED Siwan",
    "hi": "जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान",
    "bi": "e.g. Executive Engineer, PHED Siwan (जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान)"
  },
  "m/s sandip kumar • 21 sites live project tracker": {
    "en": "M/S SANDIP KUMAR • 21 Sites Live Project Tracker",
    "hi": "M/S SANDIP KUMAR • 21 Sites Live Project Tracker",
    "bi": "M/S SANDIP KUMAR • 21 Sites Live Project Tracker"
  },
  "m/s sandip kumar • 19 sites live project tracker": {
    "en": "M/S SANDIP KUMAR • 19 Sites Live Project Tracker",
    "hi": "M/S SANDIP KUMAR • 19 Sites Live Project Tracker",
    "bi": "M/S SANDIP KUMAR • 19 Sites Live Project Tracker"
  },
  "latest material usage entries recorded across 21 sites": {
    "en": "Latest material usage entries recorded across 21 sites",
    "hi": "21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ",
    "bi": "Latest material usage entries recorded across 21 sites (21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ)"
  },
  "21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ": {
    "en": "Latest material usage entries recorded across 21 sites",
    "hi": "21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ",
    "bi": "Latest material usage entries recorded across 21 sites (21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ)"
  },
  "latest material usage entries recorded across 21 sites (21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ)": {
    "en": "Latest material usage entries recorded across 21 sites",
    "hi": "21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ",
    "bi": "Latest material usage entries recorded across 21 sites (21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ)"
  },
  "no entries found. record new daily entry.": {
    "en": "No entries found. Record new daily entry.",
    "hi": "कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।",
    "bi": "No entries found. Record new daily entry. (कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।)"
  },
  "कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।": {
    "en": "No entries found. Record new daily entry.",
    "hi": "कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।",
    "bi": "No entries found. Record new daily entry. (कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।)"
  },
  "no entries found. record new daily entry. (कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।)": {
    "en": "No entries found. Record new daily entry.",
    "hi": "कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।",
    "bi": "No entries found. Record new daily entry. (कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।)"
  },
  "search by department, place, ref number, or subject...": {
    "en": "Search by department, place, ref number, or subject...",
    "hi": "विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...",
    "bi": "Search by department, place, ref number, or subject... (विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...)"
  },
  "विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...": {
    "en": "Search by department, place, ref number, or subject...",
    "hi": "विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...",
    "bi": "Search by department, place, ref number, or subject... (विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...)"
  },
  "search by department, place, ref number, or subject... (विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...)": {
    "en": "Search by department, place, ref number, or subject...",
    "hi": "विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...",
    "bi": "Search by department, place, ref number, or subject... (विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...)"
  },
  "download 4-photo official a4 sheet (with gps & date)": {
    "en": "Download 4-photo official A4 sheet (with GPS & date)",
    "hi": "4-फोटो सरकारी A4 शीट डाउनलोड (GPS व तारीख सहित)",
    "bi": "Download 4-photo official A4 sheet (with GPS & date) (4-फोटो सरकारी A4 शीट डाउनलोड (GPS व तारीख सहित))"
  },
  "4-फोटो सरकारी a4 शीट डाउनलोड (gps व तारीख सहित)": {
    "en": "Download 4-photo official A4 sheet (with GPS & date)",
    "hi": "4-फोटो सरकारी A4 शीट डाउनलोड (GPS व तारीख सहित)",
    "bi": "Download 4-photo official A4 sheet (with GPS & date) (4-फोटो सरकारी A4 शीट डाउनलोड (GPS व तारीख सहित))"
  },
  "download 4-photo official a4 sheet (with gps & date) (4-फोटो सरकारी a4 शीट डाउनलोड (gps व तारीख सहित))": {
    "en": "Download 4-photo official A4 sheet (with GPS & date)",
    "hi": "4-फोटो सरकारी A4 शीट डाउनलोड (GPS व तारीख सहित)",
    "bi": "Download 4-photo official A4 sheet (with GPS & date) (4-फोटो सरकारी A4 शीट डाउनलोड (GPS व तारीख सहित))"
  },
  "purpose of the letter / subject": {
    "en": "Purpose of the Letter / Subject",
    "hi": "पत्र का उद्देश्य / विषय",
    "bi": "Purpose of the Letter / Subject (पत्र का उद्देश्य / विषय)"
  },
  "पत्र का उद्देश्य / विषय": {
    "en": "Purpose of the Letter / Subject",
    "hi": "पत्र का उद्देश्य / विषय",
    "bi": "Purpose of the Letter / Subject (पत्र का उद्देश्य / विषय)"
  },
  "purpose of the letter / subject (पत्र का उद्देश्य / विषय)": {
    "en": "Purpose of the Letter / Subject",
    "hi": "पत्र का उद्देश्य / विषय",
    "bi": "Purpose of the Letter / Subject (पत्र का उद्देश्य / विषय)"
  },
  "no material consumption recorded yet.": {
    "en": "No material consumption recorded yet.",
    "hi": "अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।",
    "bi": "No material consumption recorded yet. (अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।)"
  },
  "अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।": {
    "en": "No material consumption recorded yet.",
    "hi": "अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।",
    "bi": "No material consumption recorded yet. (अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।)"
  },
  "no material consumption recorded yet. (अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।)": {
    "en": "No material consumption recorded yet.",
    "hi": "अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।",
    "bi": "No material consumption recorded yet. (अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।)"
  },
  "21 sites manual attendance sheet (main register)": {
    "en": "21 Sites Manual Attendance Sheet (Main Register)",
    "hi": "21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर)",
    "bi": "21 Sites Manual Attendance Sheet (Main Register) (21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर))"
  },
  "21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर)": {
    "en": "21 Sites Manual Attendance Sheet (Main Register)",
    "hi": "21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर)",
    "bi": "21 Sites Manual Attendance Sheet (Main Register) (21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर))"
  },
  "21 sites manual attendance sheet (main register) (21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर))": {
    "en": "21 Sites Manual Attendance Sheet (Main Register)",
    "hi": "21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर)",
    "bi": "21 Sites Manual Attendance Sheet (Main Register) (21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर))"
  },
  "gps automatic attendance & work hours (500m radius)": {
    "en": "GPS Automatic Attendance & Work Hours (500m Radius)",
    "hi": "GPS ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा)",
    "bi": "GPS Automatic Attendance & Work Hours (500m Radius) (GPS ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा))"
  },
  "gps ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा)": {
    "en": "GPS Automatic Attendance & Work Hours (500m Radius)",
    "hi": "GPS ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा)",
    "bi": "GPS Automatic Attendance & Work Hours (500m Radius) (GPS ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा))"
  },
  "gps automatic attendance & work hours (500m radius) (gps ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा))": {
    "en": "GPS Automatic Attendance & Work Hours (500m Radius)",
    "hi": "GPS ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा)",
    "bi": "GPS Automatic Attendance & Work Hours (500m Radius) (GPS ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा))"
  },
  "daily material usage entry": {
    "en": "Daily Material Usage Entry",
    "hi": "दैनिक सामग्री इस्तेमाल एंट्री",
    "bi": "Daily Material Usage Entry (दैनिक सामग्री इस्तेमाल एंट्री)"
  },
  "दैनिक सामग्री इस्तेमाल एंट्री": {
    "en": "Daily Material Usage Entry",
    "hi": "दैनिक सामग्री इस्तेमाल एंट्री",
    "bi": "Daily Material Usage Entry (दैनिक सामग्री इस्तेमाल एंट्री)"
  },
  "daily material usage entry (दैनिक सामग्री इस्तेमाल एंट्री)": {
    "en": "Daily Material Usage Entry",
    "hi": "दैनिक सामग्री इस्तेमाल एंट्री",
    "bi": "Daily Material Usage Entry (दैनिक सामग्री इस्तेमाल एंट्री)"
  },
  "comprehensive daily, monthly, and site-wise ledger accounting": {
    "en": "Comprehensive daily, monthly, and site-wise ledger accounting",
    "hi": "दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब",
    "bi": "Comprehensive daily, monthly, and site-wise ledger accounting (दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब)"
  },
  "दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब": {
    "en": "Comprehensive daily, monthly, and site-wise ledger accounting",
    "hi": "दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब",
    "bi": "Comprehensive daily, monthly, and site-wise ledger accounting (दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब)"
  },
  "comprehensive daily, monthly, and site-wise ledger accounting (दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब)": {
    "en": "Comprehensive daily, monthly, and site-wise ledger accounting",
    "hi": "दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब",
    "bi": "Comprehensive daily, monthly, and site-wise ledger accounting (दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब)"
  },
  "purpose of letter / subject": {
    "en": "Purpose of Letter / Subject",
    "hi": "पत्र का उद्देश्य / विषय",
    "bi": "Purpose of Letter / Subject (पत्र का उद्देश्य / विषय)"
  },
  "purpose of letter / subject (पत्र का उद्देश्य / विषय)": {
    "en": "Purpose of Letter / Subject",
    "hi": "पत्र का उद्देश्य / विषय",
    "bi": "Purpose of Letter / Subject (पत्र का उद्देश्य / विषय)"
  },
  "remarks / dispatch details": {
    "en": "Remarks / Dispatch Details",
    "hi": "टिप्पणी / प्रेषण विवरण",
    "bi": "Remarks / Dispatch Details (टिप्पणी / प्रेषण विवरण)"
  },
  "टिप्पणी / प्रेषण विवरण": {
    "en": "Remarks / Dispatch Details",
    "hi": "टिप्पणी / प्रेषण विवरण",
    "bi": "Remarks / Dispatch Details (टिप्पणी / प्रेषण विवरण)"
  },
  "remarks / dispatch details (टिप्पणी / प्रेषण विवरण)": {
    "en": "Remarks / Dispatch Details",
    "hi": "टिप्पणी / प्रेषण विवरण",
    "bi": "Remarks / Dispatch Details (टिप्पणी / प्रेषण विवरण)"
  },
  "recent usage logs": {
    "en": "Recent Usage Logs",
    "hi": "हाल ही की प्रविष्टियाँ",
    "bi": "Recent Usage Logs (हाल ही की प्रविष्टियाँ)"
  },
  "हाल ही की प्रविष्टियाँ": {
    "en": "Recent Usage Logs",
    "hi": "हाल ही की प्रविष्टियाँ",
    "bi": "Recent Usage Logs (हाल ही की प्रविष्टियाँ)"
  },
  "recent usage logs (हाल ही की प्रविष्टियाँ)": {
    "en": "Recent Usage Logs",
    "hi": "हाल ही की प्रविष्टियाँ",
    "bi": "Recent Usage Logs (हाल ही की प्रविष्टियाँ)"
  },
  "dispatched goods, daily consumption, and remaining balance": {
    "en": "Dispatched goods, daily consumption, and remaining balance",
    "hi": "भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस",
    "bi": "Dispatched goods, daily consumption, and remaining balance (भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस)"
  },
  "भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस": {
    "en": "Dispatched goods, daily consumption, and remaining balance",
    "hi": "भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस",
    "bi": "Dispatched goods, daily consumption, and remaining balance (भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस)"
  },
  "dispatched goods, daily consumption, and remaining balance (भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस)": {
    "en": "Dispatched goods, daily consumption, and remaining balance",
    "hi": "भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस",
    "bi": "Dispatched goods, daily consumption, and remaining balance (भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस)"
  },
  "enter place name (e.g., siwan / patna)": {
    "en": "Enter place name (e.g., Siwan / Patna)",
    "hi": "स्थान का नाम लिखें (जैसे: सीवान / पटना)",
    "bi": "Enter place name (e.g., Siwan / Patna) (स्थान का नाम लिखें (जैसे: सीवान / पटना))"
  },
  "स्थान का नाम लिखें (जैसे: सीवान / पटना)": {
    "en": "Enter place name (e.g., Siwan / Patna)",
    "hi": "स्थान का नाम लिखें (जैसे: सीवान / पटना)",
    "bi": "Enter place name (e.g., Siwan / Patna) (स्थान का नाम लिखें (जैसे: सीवान / पटना))"
  },
  "enter place name (e.g., siwan / patna) (स्थान का नाम लिखें (जैसे: सीवान / पटना))": {
    "en": "Enter place name (e.g., Siwan / Patna)",
    "hi": "स्थान का नाम लिखें (जैसे: सीवान / पटना)",
    "bi": "Enter place name (e.g., Siwan / Patna) (स्थान का नाम लिखें (जैसे: सीवान / पटना))"
  },
  "no outgoing letters recorded yet.": {
    "en": "No outgoing letters recorded yet.",
    "hi": "अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।",
    "bi": "No outgoing letters recorded yet. (अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।)"
  },
  "अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।": {
    "en": "No outgoing letters recorded yet.",
    "hi": "अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।",
    "bi": "No outgoing letters recorded yet. (अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।)"
  },
  "no outgoing letters recorded yet. (अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।)": {
    "en": "No outgoing letters recorded yet.",
    "hi": "अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।",
    "bi": "No outgoing letters recorded yet. (अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।)"
  },
  "daily work progress (pipeline, fhtc tap)": {
    "en": "Daily Work Progress (Pipeline, FHTC Tap)",
    "hi": "दैनिक कार्य प्रगति (पाइपलाइन, FHTC नल)",
    "bi": "Daily Work Progress (Pipeline, FHTC Tap) (दैनिक कार्य प्रगति (पाइपलाइन, FHTC नल))"
  },
  "दैनिक कार्य प्रगति (पाइपलाइन, fhtc नल)": {
    "en": "Daily Work Progress (Pipeline, FHTC Tap)",
    "hi": "दैनिक कार्य प्रगति (पाइपलाइन, FHTC नल)",
    "bi": "Daily Work Progress (Pipeline, FHTC Tap) (दैनिक कार्य प्रगति (पाइपलाइन, FHTC नल))"
  },
  "daily work progress (pipeline, fhtc tap) (दैनिक कार्य प्रगति (पाइपलाइन, fhtc नल))": {
    "en": "Daily Work Progress (Pipeline, FHTC Tap)",
    "hi": "दैनिक कार्य प्रगति (पाइपलाइन, FHTC नल)",
    "bi": "Daily Work Progress (Pipeline, FHTC Tap) (दैनिक कार्य प्रगति (पाइपलाइन, FHTC नल))"
  },
  "letters register (outgoing)": {
    "en": "Letters Register (Outgoing)",
    "hi": "जावक पत्रांक पंजी",
    "bi": "Letters Register (Outgoing) (जावक पत्रांक पंजी)"
  },
  "जावक पत्रांक पंजी": {
    "en": "Letters Register (Outgoing)",
    "hi": "जावक पत्रांक पंजी",
    "bi": "Letters Register (Outgoing) (जावक पत्रांक पंजी)"
  },
  "letters register (outgoing) (जावक पत्रांक पंजी)": {
    "en": "Letters Register (Outgoing)",
    "hi": "जावक पत्रांक पंजी",
    "bi": "Letters Register (Outgoing) (जावक पत्रांक पंजी)"
  },
  "remarks / dispatch details (टिप्पणी)": {
    "en": "Remarks / Dispatch Details",
    "hi": "टिप्पणी",
    "bi": "Remarks / Dispatch Details (टिप्पणी)"
  },
  "📝 1. manual attendance (21 sites sheet)": {
    "en": "📝 1. Manual Attendance (21 Sites Sheet)",
    "hi": "📝 1. मैन्युअल हाजिरी (21 साइट्स शीट)",
    "bi": "📝 1. Manual Attendance (21 Sites Sheet) (📝 1. मैन्युअल हाजिरी (21 साइट्स शीट))"
  },
  "📝 1. मैन्युअल हाजिरी (21 साइट्स शीट)": {
    "en": "📝 1. Manual Attendance (21 Sites Sheet)",
    "hi": "📝 1. मैन्युअल हाजिरी (21 साइट्स शीट)",
    "bi": "📝 1. Manual Attendance (21 Sites Sheet) (📝 1. मैन्युअल हाजिरी (21 साइट्स शीट))"
  },
  "📝 1. manual attendance (21 sites sheet) (📝 1. मैन्युअल हाजिरी (21 साइट्स शीट))": {
    "en": "📝 1. Manual Attendance (21 Sites Sheet)",
    "hi": "📝 1. मैन्युअल हाजिरी (21 साइट्स शीट)",
    "bi": "📝 1. Manual Attendance (21 Sites Sheet) (📝 1. मैन्युअल हाजिरी (21 साइट्स शीट))"
  },
  "dispatch & reference register": {
    "en": "Dispatch & Reference Register",
    "hi": "पत्रांक रजिस्टर",
    "bi": "Dispatch & Reference Register (पत्रांक रजिस्टर)"
  },
  "पत्रांक रजिस्टर": {
    "en": "Dispatch & Reference Register",
    "hi": "पत्रांक रजिस्टर",
    "bi": "Dispatch & Reference Register (पत्रांक रजिस्टर)"
  },
  "dispatch & reference register (पत्रांक रजिस्टर)": {
    "en": "Dispatch & Reference Register",
    "hi": "पत्रांक रजिस्टर",
    "bi": "Dispatch & Reference Register (पत्रांक रजिस्टर)"
  },
  "tap the faucet icon anytime to switch language": {
    "en": "Tap the faucet icon anytime to switch language",
    "hi": "नल आइकन पर दबाकर कभी भी बदलें",
    "bi": "Tap the faucet icon anytime to switch language (नल आइकन पर दबाकर कभी भी बदलें)"
  },
  "नल आइकन पर दबाकर कभी भी बदलें": {
    "en": "Tap the faucet icon anytime to switch language",
    "hi": "नल आइकन पर दबाकर कभी भी बदलें",
    "bi": "Tap the faucet icon anytime to switch language (नल आइकन पर दबाकर कभी भी बदलें)"
  },
  "tap the faucet icon anytime to switch language (नल आइकन पर दबाकर कभी भी बदलें)": {
    "en": "Tap the faucet icon anytime to switch language",
    "hi": "नल आइकन पर दबाकर कभी भी बदलें",
    "bi": "Tap the faucet icon anytime to switch language (नल आइकन पर दबाकर कभी भी बदलें)"
  },
  "reports hub (daily & monthly)": {
    "en": "Reports Hub (Daily & Monthly)",
    "hi": "रिपोर्ट्स केंद्र",
    "bi": "Reports Hub (Daily & Monthly) (रिपोर्ट्स केंद्र)"
  },
  "रिपोर्ट्स केंद्र": {
    "en": "Reports Hub (Daily & Monthly)",
    "hi": "रिपोर्ट्स केंद्र",
    "bi": "Reports Hub (Daily & Monthly) (रिपोर्ट्स केंद्र)"
  },
  "reports hub (daily & monthly) (रिपोर्ट्स केंद्र)": {
    "en": "Reports Hub (Daily & Monthly)",
    "hi": "रिपोर्ट्स केंद्र",
    "bi": "Reports Hub (Daily & Monthly) (रिपोर्ट्स केंद्र)"
  },
  "site photos & a4 album": {
    "en": "Site Photos & A4 Album",
    "hi": "साइट फोटो व A4 एल्बम",
    "bi": "Site Photos & A4 Album (साइट फोटो व A4 एल्बम)"
  },
  "साइट फोटो व a4 एल्बम": {
    "en": "Site Photos & A4 Album",
    "hi": "साइट फोटो व A4 एल्बम",
    "bi": "Site Photos & A4 Album (साइट फोटो व A4 एल्बम)"
  },
  "site photos & a4 album (साइट फोटो व a4 एल्बम)": {
    "en": "Site Photos & A4 Album",
    "hi": "साइट फोटो व A4 एल्बम",
    "bi": "Site Photos & A4 Album (साइट फोटो व A4 एल्बम)"
  },
  "site photos & official 4-photo a4 album": {
    "en": "Site Photos & Official 4-Photo A4 Album",
    "hi": "साइट फोटो व सरकारी 4-फोटो A4 एल्बम",
    "bi": "Site Photos & Official 4-Photo A4 Album (साइट फोटो व सरकारी 4-फोटो A4 एल्बम)"
  },
  "साइट फोटो व सरकारी 4-फोटो a4 एल्बम": {
    "en": "Site Photos & Official 4-Photo A4 Album",
    "hi": "साइट फोटो व सरकारी 4-फोटो A4 एल्बम",
    "bi": "Site Photos & Official 4-Photo A4 Album (साइट फोटो व सरकारी 4-फोटो A4 एल्बम)"
  },
  "site photos & official 4-photo a4 album (साइट फोटो व सरकारी 4-फोटो a4 एल्बम)": {
    "en": "Site Photos & Official 4-Photo A4 Album",
    "hi": "साइट फोटो व सरकारी 4-फोटो A4 एल्बम",
    "bi": "Site Photos & Official 4-Photo A4 Album (साइट फोटो व सरकारी 4-फोटो A4 एल्बम)"
  },
  "name of department": {
    "en": "Name of Department",
    "hi": "विभाग का नाम",
    "bi": "Name of Department (विभाग का नाम)"
  },
  "विभाग का नाम": {
    "en": "Name of Department",
    "hi": "विभाग का नाम",
    "bi": "Name of Department (विभाग का नाम)"
  },
  "name of department (विभाग का नाम)": {
    "en": "Name of Department",
    "hi": "विभाग का नाम",
    "bi": "Name of Department (विभाग का नाम)"
  },
  "date-wise stock ledger": {
    "en": "Date-wise Stock Ledger",
    "hi": "तारीख-वार लेजर",
    "bi": "Date-wise Stock Ledger (तारीख-वार लेजर)"
  },
  "तारीख-वार लेजर": {
    "en": "Date-wise Stock Ledger",
    "hi": "तारीख-वार लेजर",
    "bi": "Date-wise Stock Ledger (तारीख-वार लेजर)"
  },
  "date-wise stock ledger (तारीख-वार लेजर)": {
    "en": "Date-wise Stock Ledger",
    "hi": "तारीख-वार लेजर",
    "bi": "Date-wise Stock Ledger (तारीख-वार लेजर)"
  },
  "work purpose / remarks:": {
    "en": "Work Purpose / Remarks:",
    "hi": "विवरण / कहाँ लगाया गया:",
    "bi": "Work Purpose / Remarks: (विवरण / कहाँ लगाया गया:)"
  },
  "विवरण / कहाँ लगाया गया:": {
    "en": "Work Purpose / Remarks:",
    "hi": "विवरण / कहाँ लगाया गया:",
    "bi": "Work Purpose / Remarks: (विवरण / कहाँ लगाया गया:)"
  },
  "work purpose / remarks: (विवरण / कहाँ लगाया गया:)": {
    "en": "Work Purpose / Remarks:",
    "hi": "विवरण / कहाँ लगाया गया:",
    "bi": "Work Purpose / Remarks: (विवरण / कहाँ लगाया गया:)"
  },
  "+ type custom place": {
    "en": "+ Type Custom Place",
    "hi": "+ अन्य स्थान",
    "bi": "+ Type Custom Place (+ अन्य स्थान)"
  },
  "+ अन्य स्थान": {
    "en": "+ Type Custom Place",
    "hi": "+ अन्य स्थान",
    "bi": "+ Type Custom Place (+ अन्य स्थान)"
  },
  "+ type custom place (+ अन्य स्थान)": {
    "en": "+ Type Custom Place",
    "hi": "+ अन्य स्थान",
    "bi": "+ Type Custom Place (+ अन्य स्थान)"
  },
  "site stock & balance": {
    "en": "Site Stock & Balance",
    "hi": "साइट स्टॉक व बैलेंस",
    "bi": "Site Stock & Balance (साइट स्टॉक व बैलेंस)"
  },
  "साइट स्टॉक व बैलेंस": {
    "en": "Site Stock & Balance",
    "hi": "साइट स्टॉक व बैलेंस",
    "bi": "Site Stock & Balance (साइट स्टॉक व बैलेंस)"
  },
  "site stock & balance (साइट स्टॉक व बैलेंस)": {
    "en": "Site Stock & Balance",
    "hi": "साइट स्टॉक व बैलेंस",
    "bi": "Site Stock & Balance (साइट स्टॉक व बैलेंस)"
  },
  "letters register": {
    "en": "Letters Register",
    "hi": "पत्रांक पंजी",
    "bi": "Letters Register (पत्रांक पंजी)"
  },
  "पत्रांक पंजी": {
    "en": "Letters Register",
    "hi": "पत्रांक पंजी",
    "bi": "Letters Register (पत्रांक पंजी)"
  },
  "letters register (पत्रांक पंजी)": {
    "en": "Letters Register",
    "hi": "पत्रांक पंजी",
    "bi": "Letters Register (पत्रांक पंजी)"
  },
  "place / location": {
    "en": "Place / Location",
    "hi": "स्थान / साइट",
    "bi": "Place / Location (स्थान / साइट)"
  },
  "स्थान / साइट": {
    "en": "Place / Location",
    "hi": "स्थान / साइट",
    "bi": "Place / Location (स्थान / साइट)"
  },
  "place / location (स्थान / साइट)": {
    "en": "Place / Location",
    "hi": "स्थान / साइट",
    "bi": "Place / Location (स्थान / साइट)"
  },
  "dpr work progress (pipeline, fhtc)": {
    "en": "DPR Work Progress (Pipeline, FHTC)",
    "hi": "DPR कार्य प्रगति (पाइपलाइन, नल)",
    "bi": "DPR Work Progress (Pipeline, FHTC) (DPR कार्य प्रगति (पाइपलाइन, नल))"
  },
  "dpr कार्य प्रगति (पाइपलाइन, नल)": {
    "en": "DPR Work Progress (Pipeline, FHTC)",
    "hi": "DPR कार्य प्रगति (पाइपलाइन, नल)",
    "bi": "DPR Work Progress (Pipeline, FHTC) (DPR कार्य प्रगति (पाइपलाइन, नल))"
  },
  "dpr work progress (pipeline, fhtc) (dpr कार्य प्रगति (पाइपलाइन, नल))": {
    "en": "DPR Work Progress (Pipeline, FHTC)",
    "hi": "DPR कार्य प्रगति (पाइपलाइन, नल)",
    "bi": "DPR Work Progress (Pipeline, FHTC) (DPR कार्य प्रगति (पाइपलाइन, नल))"
  },
  "21 construction sites overview": {
    "en": "21 Construction Sites Overview",
    "hi": "21 Construction Sites Overview",
    "bi": "21 Construction Sites Overview"
  },
  "add daily consumption entry": {
    "en": "Add Daily Consumption Entry",
    "hi": "Daily Consumption Entry Dalein",
    "bi": "Add Daily Consumption Entry (Daily Consumption Entry Dalein)"
  },
  "daily consumption entry dalein": {
    "en": "Add Daily Consumption Entry",
    "hi": "Daily Consumption Entry Dalein",
    "bi": "Add Daily Consumption Entry (Daily Consumption Entry Dalein)"
  },
  "add daily consumption entry (daily consumption entry dalein)": {
    "en": "Add Daily Consumption Entry",
    "hi": "Daily Consumption Entry Dalein",
    "bi": "Add Daily Consumption Entry (Daily Consumption Entry Dalein)"
  },
  "financial year:": {
    "en": "Financial Year:",
    "hi": "वित्तीय वर्ष:",
    "bi": "Financial Year: (वित्तीय वर्ष:)"
  },
  "वित्तीय वर्ष:": {
    "en": "Financial Year:",
    "hi": "वित्तीय वर्ष:",
    "bi": "Financial Year: (वित्तीय वर्ष:)"
  },
  "financial year: (वित्तीय वर्ष:)": {
    "en": "Financial Year:",
    "hi": "वित्तीय वर्ष:",
    "bi": "Financial Year: (वित्तीय वर्ष:)"
  },
  "reference number": {
    "en": "Reference Number",
    "hi": "पत्रांक संख्या",
    "bi": "Reference Number (पत्रांक संख्या)"
  },
  "reference number (पत्रांक संख्या)": {
    "en": "Reference Number",
    "hi": "पत्रांक संख्या",
    "bi": "Reference Number (पत्रांक संख्या)"
  },
  "material consumption & site tracking": {
    "en": "Material Consumption & Site Tracking",
    "hi": "सामग्री खपत एवं साइट ट्रैकिंग",
    "bi": "Material Consumption & Site Tracking (सामग्री खपत एवं साइट ट्रैकिंग)"
  },
  "सामग्री खपत एवं साइट ट्रैकिंग": {
    "en": "Material Consumption & Site Tracking",
    "hi": "सामग्री खपत एवं साइट ट्रैकिंग",
    "bi": "Material Consumption & Site Tracking (सामग्री खपत एवं साइट ट्रैकिंग)"
  },
  "material consumption & site tracking (सामग्री खपत एवं साइट ट्रैकिंग)": {
    "en": "Material Consumption & Site Tracking",
    "hi": "सामग्री खपत एवं साइट ट्रैकिंग",
    "bi": "Material Consumption & Site Tracking (सामग्री खपत एवं साइट ट्रैकिंग)"
  },
  "letter reference entry": {
    "en": "Letter Reference Entry",
    "hi": "पत्रांक पंजी",
    "bi": "Letter Reference Entry (पत्रांक पंजी)"
  },
  "letter reference entry (पत्रांक पंजी)": {
    "en": "Letter Reference Entry",
    "hi": "पत्रांक पंजी",
    "bi": "Letter Reference Entry (पत्रांक पंजी)"
  },
  "download android app (apk)": {
    "en": "Download Android App (APK)",
    "hi": "Android ऐप डाउनलोड करें",
    "bi": "Download Android App (APK) (Android ऐप डाउनलोड करें)"
  },
  "android ऐप डाउनलोड करें": {
    "en": "Download Android App (APK)",
    "hi": "Android ऐप डाउनलोड करें",
    "bi": "Download Android App (APK) (Android ऐप डाउनलोड करें)"
  },
  "download android app (apk) (android ऐप डाउनलोड करें)": {
    "en": "Download Android App (APK)",
    "hi": "Android ऐप डाउनलोड करें",
    "bi": "Download Android App (APK) (Android ऐप डाउनलोड करें)"
  },
  "📍 2. gps attendance (geo-location)": {
    "en": "📍 2. GPS Attendance (Geo-Location)",
    "hi": "📍 2. GPS हाजिरी (जियो-लोकेशन)",
    "bi": "📍 2. GPS Attendance (Geo-Location) (📍 2. GPS हाजिरी (जियो-लोकेशन))"
  },
  "📍 2. gps हाजिरी (जियो-लोकेशन)": {
    "en": "📍 2. GPS Attendance (Geo-Location)",
    "hi": "📍 2. GPS हाजिरी (जियो-लोकेशन)",
    "bi": "📍 2. GPS Attendance (Geo-Location) (📍 2. GPS हाजिरी (जियो-लोकेशन))"
  },
  "📍 2. gps attendance (geo-location) (📍 2. gps हाजिरी (जियो-लोकेशन))": {
    "en": "📍 2. GPS Attendance (Geo-Location)",
    "hi": "📍 2. GPS हाजिरी (जियो-लोकेशन)",
    "bi": "📍 2. GPS Attendance (Geo-Location) (📍 2. GPS हाजिरी (जियो-लोकेशन))"
  },
  "daily material consumption entry": {
    "en": "Daily Material Consumption Entry",
    "hi": "दैनिक सामग्री इस्तेमाल एंट्री",
    "bi": "Daily Material Consumption Entry (दैनिक सामग्री इस्तेमाल एंट्री)"
  },
  "daily material consumption entry (दैनिक सामग्री इस्तेमाल एंट्री)": {
    "en": "Daily Material Consumption Entry",
    "hi": "दैनिक सामग्री इस्तेमाल एंट्री",
    "bi": "Daily Material Consumption Entry (दैनिक सामग्री इस्तेमाल एंट्री)"
  },
  "outgoing letters reference register": {
    "en": "Outgoing Letters Reference Register",
    "hi": "विभिन्न विभागों को जावक पत्र",
    "bi": "Outgoing Letters Reference Register (विभिन्न विभागों को जावक पत्र)"
  },
  "विभिन्न विभागों को जावक पत्र": {
    "en": "Outgoing Letters Reference Register",
    "hi": "विभिन्न विभागों को जावक पत्र",
    "bi": "Outgoing Letters Reference Register (विभिन्न विभागों को जावक पत्र)"
  },
  "outgoing letters reference register (विभिन्न विभागों को जावक पत्र)": {
    "en": "Outgoing Letters Reference Register",
    "hi": "विभिन्न विभागों को जावक पत्र",
    "bi": "Outgoing Letters Reference Register (विभिन्न विभागों को जावक पत्र)"
  },
  "supervisor & worker mobile app": {
    "en": "Supervisor & Worker Mobile App",
    "hi": "सुपरवाइज़र व वर्कर मोबाइल ऐप",
    "bi": "Supervisor & Worker Mobile App (सुपरवाइज़र व वर्कर मोबाइल ऐप)"
  },
  "सुपरवाइज़र व वर्कर मोबाइल ऐप": {
    "en": "Supervisor & Worker Mobile App",
    "hi": "सुपरवाइज़र व वर्कर मोबाइल ऐप",
    "bi": "Supervisor & Worker Mobile App (सुपरवाइज़र व वर्कर मोबाइल ऐप)"
  },
  "supervisor & worker mobile app (सुपरवाइज़र व वर्कर मोबाइल ऐप)": {
    "en": "Supervisor & Worker Mobile App",
    "hi": "सुपरवाइज़र व वर्कर मोबाइल ऐप",
    "bi": "Supervisor & Worker Mobile App (सुपरवाइज़र व वर्कर मोबाइल ऐप)"
  },
  "select language / भाषा चुनें": {
    "en": "Select Language / भाषा चुनें",
    "hi": "भाषा चुनें / Select Language",
    "bi": "Select Language / भाषा चुनें (भाषा चुनें / Select Language)"
  },
  "भाषा चुनें / select language": {
    "en": "Select Language / भाषा चुनें",
    "hi": "भाषा चुनें / Select Language",
    "bi": "Select Language / भाषा चुनें (भाषा चुनें / Select Language)"
  },
  "select language / भाषा चुनें (भाषा चुनें / select language)": {
    "en": "Select Language / भाषा चुनें",
    "hi": "भाषा चुनें / Select Language",
    "bi": "Select Language / भाषा चुनें (भाषा चुनें / Select Language)"
  },
  "site stock & balance register": {
    "en": "Site Stock & Balance Register",
    "hi": "साइट स्टॉक और बैलेंस रजिस्टर",
    "bi": "Site Stock & Balance Register (साइट स्टॉक और बैलेंस रजिस्टर)"
  },
  "साइट स्टॉक और बैलेंस रजिस्टर": {
    "en": "Site Stock & Balance Register",
    "hi": "साइट स्टॉक और बैलेंस रजिस्टर",
    "bi": "Site Stock & Balance Register (साइट स्टॉक और बैलेंस रजिस्टर)"
  },
  "site stock & balance register (साइट स्टॉक और बैलेंस रजिस्टर)": {
    "en": "Site Stock & Balance Register",
    "hi": "साइट स्टॉक और बैलेंस रजिस्टर",
    "bi": "Site Stock & Balance Register (साइट स्टॉक और बैलेंस रजिस्टर)"
  },
  "🚰 dpr progress (pipeline, fhtc)": {
    "en": "🚰 DPR Progress (Pipeline, FHTC)",
    "hi": "🚰 DPR प्रगति (पाइपलाइन, नल)",
    "bi": "🚰 DPR Progress (Pipeline, FHTC) (🚰 DPR प्रगति (पाइपलाइन, नल))"
  },
  "🚰 dpr प्रगति (पाइपलाइन, नल)": {
    "en": "🚰 DPR Progress (Pipeline, FHTC)",
    "hi": "🚰 DPR प्रगति (पाइपलाइन, नल)",
    "bi": "🚰 DPR Progress (Pipeline, FHTC) (🚰 DPR प्रगति (पाइपलाइन, नल))"
  },
  "🚰 dpr progress (pipeline, fhtc) (🚰 dpr प्रगति (पाइपलाइन, नल))": {
    "en": "🚰 DPR Progress (Pipeline, FHTC)",
    "hi": "🚰 DPR प्रगति (पाइपलाइन, नल)",
    "bi": "🚰 DPR Progress (Pipeline, FHTC) (🚰 DPR प्रगति (पाइपलाइन, नल))"
  },
  "साइट स्टॉक व बैलेंस रजिस्टर": {
    "en": "Site Stock & Balance Register",
    "hi": "साइट स्टॉक व बैलेंस रजिस्टर",
    "bi": "Site Stock & Balance Register (साइट स्टॉक व बैलेंस रजिस्टर)"
  },
  "site stock & balance register (साइट स्टॉक व बैलेंस रजिस्टर)": {
    "en": "Site Stock & Balance Register",
    "hi": "साइट स्टॉक व बैलेंस रजिस्टर",
    "bi": "Site Stock & Balance Register (साइट स्टॉक व बैलेंस रजिस्टर)"
  },
  "record new outgoing letter reference": {
    "en": "Record New Outgoing Letter Reference",
    "hi": "नया जावक पत्रांक दर्ज करें",
    "bi": "Record New Outgoing Letter Reference (नया जावक पत्रांक दर्ज करें)"
  },
  "नया जावक पत्रांक दर्ज करें": {
    "en": "Record New Outgoing Letter Reference",
    "hi": "नया जावक पत्रांक दर्ज करें",
    "bi": "Record New Outgoing Letter Reference (नया जावक पत्रांक दर्ज करें)"
  },
  "record new outgoing letter reference (नया जावक पत्रांक दर्ज करें)": {
    "en": "Record New Outgoing Letter Reference",
    "hi": "नया जावक पत्रांक दर्ज करें",
    "bi": "Record New Outgoing Letter Reference (नया जावक पत्रांक दर्ज करें)"
  },
  "edit letter reference details": {
    "en": "Edit Letter Reference Details",
    "hi": "पत्रांक विवरण संपादित करें",
    "bi": "Edit Letter Reference Details (पत्रांक विवरण संपादित करें)"
  },
  "पत्रांक विवरण संपादित करें": {
    "en": "Edit Letter Reference Details",
    "hi": "पत्रांक विवरण संपादित करें",
    "bi": "Edit Letter Reference Details (पत्रांक विवरण संपादित करें)"
  },
  "edit letter reference details (पत्रांक विवरण संपादित करें)": {
    "en": "Edit Letter Reference Details",
    "hi": "पत्रांक विवरण संपादित करें",
    "bi": "Edit Letter Reference Details (पत्रांक विवरण संपादित करें)"
  },
  "main actions": {
    "en": "Main Actions",
    "hi": "मुख्य कार्य",
    "bi": "Main Actions (मुख्य कार्य)"
  },
  "मुख्य कार्य": {
    "en": "Main Actions",
    "hi": "मुख्य कार्य",
    "bi": "Main Actions (मुख्य कार्य)"
  },
  "main actions (मुख्य कार्य)": {
    "en": "Main Actions",
    "hi": "मुख्य कार्य",
    "bi": "Main Actions (मुख्य कार्य)"
  },
  "दैनिक एंट्री": {
    "en": "Daily Entry",
    "hi": "दैनिक एंट्री",
    "bi": "Daily Entry (दैनिक एंट्री)"
  },
  "daily entry (दैनिक एंट्री)": {
    "en": "Daily Entry",
    "hi": "दैनिक एंट्री",
    "bi": "Daily Entry (दैनिक एंट्री)"
  },
  "record materials used at site today": {
    "en": "Record materials used at site today",
    "hi": "साइट पर आज कितना सामान लगा",
    "bi": "Record materials used at site today (साइट पर आज कितना सामान लगा)"
  },
  "साइट पर आज कितना सामान लगा": {
    "en": "Record materials used at site today",
    "hi": "साइट पर आज कितना सामान लगा",
    "bi": "Record materials used at site today (साइट पर आज कितना सामान लगा)"
  },
  "record materials used at site today (साइट पर आज कितना सामान लगा)": {
    "en": "Record materials used at site today",
    "hi": "साइट पर आज कितना सामान लगा",
    "bi": "Record materials used at site today (साइट पर आज कितना सामान लगा)"
  },
  "👥 daily manpower attendance": {
    "en": "👥 Daily Manpower Attendance",
    "hi": "👥 दैनिक हाजिरी",
    "bi": "👥 Daily Manpower Attendance (👥 दैनिक हाजिरी)"
  },
  "👥 दैनिक हाजिरी": {
    "en": "👥 Daily Manpower Attendance",
    "hi": "👥 दैनिक हाजिरी",
    "bi": "👥 Daily Manpower Attendance (👥 दैनिक हाजिरी)"
  },
  "👥 daily manpower attendance (👥 दैनिक हाजिरी)": {
    "en": "👥 Daily Manpower Attendance",
    "hi": "👥 दैनिक हाजिरी",
    "bi": "👥 Daily Manpower Attendance (👥 दैनिक हाजिरी)"
  },
  "📸 site work photos & album": {
    "en": "📸 Site Work Photos & Album",
    "hi": "📸 साइट कार्य फोटो व एल्बम",
    "bi": "📸 Site Work Photos & Album (📸 साइट कार्य फोटो व एल्बम)"
  },
  "📸 साइट कार्य फोटो व एल्बम": {
    "en": "📸 Site Work Photos & Album",
    "hi": "📸 साइट कार्य फोटो व एल्बम",
    "bi": "📸 Site Work Photos & Album (📸 साइट कार्य फोटो व एल्बम)"
  },
  "📸 site work photos & album (📸 साइट कार्य फोटो व एल्बम)": {
    "en": "📸 Site Work Photos & Album",
    "hi": "📸 साइट कार्य फोटो व एल्बम",
    "bi": "📸 Site Work Photos & Album (📸 साइट कार्य फोटो व एल्बम)"
  },
  "📊 reports & ledger hub": {
    "en": "📊 Reports & Ledger Hub",
    "hi": "📊 रिपोर्ट्स व लेजर केंद्र",
    "bi": "📊 Reports & Ledger Hub (📊 रिपोर्ट्स व लेजर केंद्र)"
  },
  "📊 रिपोर्ट्स व लेजर केंद्र": {
    "en": "📊 Reports & Ledger Hub",
    "hi": "📊 रिपोर्ट्स व लेजर केंद्र",
    "bi": "📊 Reports & Ledger Hub (📊 रिपोर्ट्स व लेजर केंद्र)"
  },
  "📊 reports & ledger hub (📊 रिपोर्ट्स व लेजर केंद्र)": {
    "en": "📊 Reports & Ledger Hub",
    "hi": "📊 रिपोर्ट्स व लेजर केंद्र",
    "bi": "📊 Reports & Ledger Hub (📊 रिपोर्ट्स व लेजर केंद्र)"
  },
  "जावक पत्र पत्रांक रजिस्टर": {
    "en": "Outgoing Letters Reference Register",
    "hi": "जावक पत्र पत्रांक रजिस्टर",
    "bi": "Outgoing Letters Reference Register (जावक पत्र पत्रांक रजिस्टर)"
  },
  "outgoing letters reference register (जावक पत्र पत्रांक रजिस्टर)": {
    "en": "Outgoing Letters Reference Register",
    "hi": "जावक पत्र पत्रांक रजिस्टर",
    "bi": "Outgoing Letters Reference Register (जावक पत्र पत्रांक रजिस्टर)"
  },
  "department name": {
    "en": "Department Name",
    "hi": "विभाग का नाम",
    "bi": "Department Name (विभाग का नाम)"
  },
  "department name (विभाग का नाम)": {
    "en": "Department Name",
    "hi": "विभाग का नाम",
    "bi": "Department Name (विभाग का नाम)"
  },
  "quick links": {
    "en": "Quick Links",
    "hi": "अन्य लिंक्स",
    "bi": "Quick Links (अन्य लिंक्स)"
  },
  "अन्य लिंक्स": {
    "en": "Quick Links",
    "hi": "अन्य लिंक्स",
    "bi": "Quick Links (अन्य लिंक्स)"
  },
  "quick links (अन्य लिंक्स)": {
    "en": "Quick Links",
    "hi": "अन्य लिंक्स",
    "bi": "Quick Links (अन्य लिंक्स)"
  },
  "daily manual attendance sheet": {
    "en": "Daily Manual Attendance Sheet",
    "hi": "दैनिक मैन्युअल हाजिरी शीट",
    "bi": "Daily Manual Attendance Sheet (दैनिक मैन्युअल हाजिरी शीट)"
  },
  "दैनिक मैन्युअल हाजिरी शीट": {
    "en": "Daily Manual Attendance Sheet",
    "hi": "दैनिक मैन्युअल हाजिरी शीट",
    "bi": "Daily Manual Attendance Sheet (दैनिक मैन्युअल हाजिरी शीट)"
  },
  "daily manual attendance sheet (दैनिक मैन्युअल हाजिरी शीट)": {
    "en": "Daily Manual Attendance Sheet",
    "hi": "दैनिक मैन्युअल हाजिरी शीट",
    "bi": "Daily Manual Attendance Sheet (दैनिक मैन्युअल हाजिरी शीट)"
  },
  "dispatch inward stock": {
    "en": "Dispatch Inward Stock",
    "hi": "नया माल भेजें (स्टॉक आवक)",
    "bi": "Dispatch Inward Stock (नया माल भेजें (स्टॉक आवक))"
  },
  "नया माल भेजें (स्टॉक आवक)": {
    "en": "Dispatch Inward Stock",
    "hi": "नया माल भेजें (स्टॉक आवक)",
    "bi": "Dispatch Inward Stock (नया माल भेजें (स्टॉक आवक))"
  },
  "dispatch inward stock (नया माल भेजें (स्टॉक आवक))": {
    "en": "Dispatch Inward Stock",
    "hi": "नया माल भेजें (स्टॉक आवक)",
    "bi": "Dispatch Inward Stock (नया माल भेजें (स्टॉक आवक))"
  },
  "offline (saved locally)": {
    "en": "Offline (Saved locally)",
    "hi": "ऑफलाइन (स्थानीय सुरक्षित)",
    "bi": "Offline (Saved locally) (ऑफलाइन (स्थानीय सुरक्षित))"
  },
  "ऑफलाइन (स्थानीय सुरक्षित)": {
    "en": "Offline (Saved locally)",
    "hi": "ऑफलाइन (स्थानीय सुरक्षित)",
    "bi": "Offline (Saved locally) (ऑफलाइन (स्थानीय सुरक्षित))"
  },
  "offline (saved locally) (ऑफलाइन (स्थानीय सुरक्षित))": {
    "en": "Offline (Saved locally)",
    "hi": "ऑफलाइन (स्थानीय सुरक्षित)",
    "bi": "Offline (Saved locally) (ऑफलाइन (स्थानीय सुरक्षित))"
  },
  "-- select site / place --": {
    "en": "-- Select Site / Place --",
    "hi": "-- साइट / स्थान चुनें --",
    "bi": "-- Select Site / Place -- (-- साइट / स्थान चुनें --)"
  },
  "-- साइट / स्थान चुनें --": {
    "en": "-- Select Site / Place --",
    "hi": "-- साइट / स्थान चुनें --",
    "bi": "-- Select Site / Place -- (-- साइट / स्थान चुनें --)"
  },
  "-- select site / place -- (-- साइट / स्थान चुनें --)": {
    "en": "-- Select Site / Place --",
    "hi": "-- साइट / स्थान चुनें --",
    "bi": "-- Select Site / Place -- (-- साइट / स्थान चुनें --)"
  },
  "+ new letter reference (+ नया पत्रांक दर्ज करें)": {
    "en": "+ New Letter Reference",
    "hi": "+ नया पत्रांक दर्ज करें",
    "bi": "+ New Letter Reference (+ नया पत्रांक दर्ज करें)"
  },
  "purpose / subject of letter": {
    "en": "Purpose / Subject of Letter",
    "hi": "पत्र का उद्देश्य / विषय",
    "bi": "Purpose / Subject of Letter (पत्र का उद्देश्य / विषय)"
  },
  "purpose / subject of letter (पत्र का उद्देश्य / विषय)": {
    "en": "Purpose / Subject of Letter",
    "hi": "पत्र का उद्देश्य / विषय",
    "bi": "Purpose / Subject of Letter (पत्र का उद्देश्य / विषय)"
  },
  "subject / purpose of letter": {
    "en": "Subject / Purpose of Letter",
    "hi": "पत्र का विषय / उद्देश्य",
    "bi": "Subject / Purpose of Letter (पत्र का विषय / उद्देश्य)"
  },
  "पत्र का विषय / उद्देश्य": {
    "en": "Subject / Purpose of Letter",
    "hi": "पत्र का विषय / उद्देश्य",
    "bi": "Subject / Purpose of Letter (पत्र का विषय / उद्देश्य)"
  },
  "subject / purpose of letter (पत्र का विषय / उद्देश्य)": {
    "en": "Subject / Purpose of Letter",
    "hi": "पत्र का विषय / उद्देश्य",
    "bi": "Subject / Purpose of Letter (पत्र का विषय / उद्देश्य)"
  },
  "total daily entries": {
    "en": "Total Daily Entries",
    "hi": "कुल दैनिक प्रविष्टियाँ",
    "bi": "Total Daily Entries (कुल दैनिक प्रविष्टियाँ)"
  },
  "कुल दैनिक प्रविष्टियाँ": {
    "en": "Total Daily Entries",
    "hi": "कुल दैनिक प्रविष्टियाँ",
    "bi": "Total Daily Entries (कुल दैनिक प्रविष्टियाँ)"
  },
  "total daily entries (कुल दैनिक प्रविष्टियाँ)": {
    "en": "Total Daily Entries",
    "hi": "कुल दैनिक प्रविष्टियाँ",
    "bi": "Total Daily Entries (कुल दैनिक प्रविष्टियाँ)"
  },
  "top consumed materials": {
    "en": "Top Consumed Materials",
    "hi": "Top Consumed Materials",
    "bi": "Top Consumed Materials"
  },
  "record first letter reference": {
    "en": "Record First Letter Reference",
    "hi": "पहला पत्रांक दर्ज करें",
    "bi": "Record First Letter Reference (पहला पत्रांक दर्ज करें)"
  },
  "पहला पत्रांक दर्ज करें": {
    "en": "Record First Letter Reference",
    "hi": "पहला पत्रांक दर्ज करें",
    "bi": "Record First Letter Reference (पहला पत्रांक दर्ज करें)"
  },
  "record first letter reference (पहला पत्रांक दर्ज करें)": {
    "en": "Record First Letter Reference",
    "hi": "पहला पत्रांक दर्ज करें",
    "bi": "Record First Letter Reference (पहला पत्रांक दर्ज करें)"
  },
  "outgoing letters dispatch & reference register": {
    "en": "Outgoing Letters Dispatch & Reference Register",
    "hi": "जावक पत्र पत्रांक पंजी",
    "bi": "Outgoing Letters Dispatch & Reference Register (जावक पत्र पत्रांक पंजी)"
  },
  "जावक पत्र पत्रांक पंजी": {
    "en": "Outgoing Letters Dispatch & Reference Register",
    "hi": "जावक पत्र पत्रांक पंजी",
    "bi": "Outgoing Letters Dispatch & Reference Register (जावक पत्र पत्रांक पंजी)"
  },
  "outgoing letters dispatch & reference register (जावक पत्र पत्रांक पंजी)": {
    "en": "Outgoing Letters Dispatch & Reference Register",
    "hi": "जावक पत्र पत्रांक पंजी",
    "bi": "Outgoing Letters Dispatch & Reference Register (जावक पत्र पत्रांक पंजी)"
  },
  "all financial years": {
    "en": "All Financial Years",
    "hi": "सभी वित्तीय वर्ष",
    "bi": "All Financial Years (सभी वित्तीय वर्ष)"
  },
  "सभी वित्तीय वर्ष": {
    "en": "All Financial Years",
    "hi": "सभी वित्तीय वर्ष",
    "bi": "All Financial Years (सभी वित्तीय वर्ष)"
  },
  "all financial years (सभी वित्तीय वर्ष)": {
    "en": "All Financial Years",
    "hi": "सभी वित्तीय वर्ष",
    "bi": "All Financial Years (सभी वित्तीय वर्ष)"
  },
  "all options (more menu)": {
    "en": "All Options (More Menu)",
    "hi": "सभी विकल्प",
    "bi": "All Options (More Menu) (सभी विकल्प)"
  },
  "सभी विकल्प": {
    "en": "All Options (More Menu)",
    "hi": "सभी विकल्प",
    "bi": "All Options (More Menu) (सभी विकल्प)"
  },
  "all options (more menu) (सभी विकल्प)": {
    "en": "All Options (More Menu)",
    "hi": "सभी विकल्प",
    "bi": "All Options (More Menu) (सभी विकल्प)"
  },
  "balance stock": {
    "en": "Balance Stock",
    "hi": "बचा हुआ स्टॉक (बैलेंस)",
    "bi": "Balance Stock (बचा हुआ स्टॉक (बैलेंस))"
  },
  "बचा हुआ स्टॉक (बैलेंस)": {
    "en": "Balance Stock",
    "hi": "बचा हुआ स्टॉक (बैलेंस)",
    "bi": "Balance Stock (बचा हुआ स्टॉक (बैलेंस))"
  },
  "balance stock (बचा हुआ स्टॉक (बैलेंस))": {
    "en": "Balance Stock",
    "hi": "बचा हुआ स्टॉक (बैलेंस)",
    "bi": "Balance Stock (बचा हुआ स्टॉक (बैलेंस))"
  },
  "record new entry": {
    "en": "Record New Entry",
    "hi": "नई प्रविष्टि दर्ज करें",
    "bi": "Record New Entry (नई प्रविष्टि दर्ज करें)"
  },
  "नई प्रविष्टि दर्ज करें": {
    "en": "Record New Entry",
    "hi": "नई प्रविष्टि दर्ज करें",
    "bi": "Record New Entry (नई प्रविष्टि दर्ज करें)"
  },
  "record new entry (नई प्रविष्टि दर्ज करें)": {
    "en": "Record New Entry",
    "hi": "नई प्रविष्टि दर्ज करें",
    "bi": "Record New Entry (नई प्रविष्टि दर्ज करें)"
  },
  "save reference number": {
    "en": "Save Reference Number",
    "hi": "पत्रांक सुरक्षित करें",
    "bi": "Save Reference Number (पत्रांक सुरक्षित करें)"
  },
  "पत्रांक सुरक्षित करें": {
    "en": "Save Reference Number",
    "hi": "पत्रांक सुरक्षित करें",
    "bi": "Save Reference Number (पत्रांक सुरक्षित करें)"
  },
  "save reference number (पत्रांक सुरक्षित करें)": {
    "en": "Save Reference Number",
    "hi": "पत्रांक सुरक्षित करें",
    "bi": "Save Reference Number (पत्रांक सुरक्षित करें)"
  },
  "gps attendance (500m auto)": {
    "en": "GPS Attendance (500m Auto)",
    "hi": "GPS हाजिरी (500M ऑटो)",
    "bi": "GPS Attendance (500m Auto) (GPS हाजिरी (500M ऑटो))"
  },
  "gps हाजिरी (500m ऑटो)": {
    "en": "GPS Attendance (500m Auto)",
    "hi": "GPS हाजिरी (500M ऑटो)",
    "bi": "GPS Attendance (500m Auto) (GPS हाजिरी (500M ऑटो))"
  },
  "gps attendance (500m auto) (gps हाजिरी (500m ऑटो))": {
    "en": "GPS Attendance (500m Auto)",
    "hi": "GPS हाजिरी (500M ऑटो)",
    "bi": "GPS Attendance (500m Auto) (GPS हाजिरी (500M ऑटो))"
  },
  "complete system in hindi": {
    "en": "Complete system in Hindi",
    "hi": "पूरा सिस्टम हिंदी में",
    "bi": "Complete system in Hindi (पूरा सिस्टम हिंदी में)"
  },
  "पूरा सिस्टम हिंदी में": {
    "en": "Complete system in Hindi",
    "hi": "पूरा सिस्टम हिंदी में",
    "bi": "Complete system in Hindi (पूरा सिस्टम हिंदी में)"
  },
  "complete system in hindi (पूरा सिस्टम हिंदी में)": {
    "en": "Complete system in Hindi",
    "hi": "पूरा सिस्टम हिंदी में",
    "bi": "Complete system in Hindi (पूरा सिस्टम हिंदी में)"
  },
  "कुल भेजा गया": {
    "en": "Total Inward",
    "hi": "कुल भेजा गया",
    "bi": "Total Inward (कुल भेजा गया)"
  },
  "total inward (कुल भेजा गया)": {
    "en": "Total Inward",
    "hi": "कुल भेजा गया",
    "bi": "Total Inward (कुल भेजा गया)"
  },
  "balance on site": {
    "en": "Balance on Site",
    "hi": "साइट पर शेष",
    "bi": "Balance on Site (साइट पर शेष)"
  },
  "साइट पर शेष": {
    "en": "Balance on Site",
    "hi": "साइट पर शेष",
    "bi": "Balance on Site (साइट पर शेष)"
  },
  "balance on site (साइट पर शेष)": {
    "en": "Balance on Site",
    "hi": "साइट पर शेष",
    "bi": "Balance on Site (साइट पर शेष)"
  },
  "📦 site stock & store": {
    "en": "📦 Site Stock & Store",
    "hi": "📦 साइट स्टॉक व स्टोर",
    "bi": "📦 Site Stock & Store (📦 साइट स्टॉक व स्टोर)"
  },
  "📦 साइट स्टॉक व स्टोर": {
    "en": "📦 Site Stock & Store",
    "hi": "📦 साइट स्टॉक व स्टोर",
    "bi": "📦 Site Stock & Store (📦 साइट स्टॉक व स्टोर)"
  },
  "📦 site stock & store (📦 साइट स्टॉक व स्टोर)": {
    "en": "📦 Site Stock & Store",
    "hi": "📦 साइट स्टॉक व स्टोर",
    "bi": "📦 Site Stock & Store (📦 साइट स्टॉक व स्टोर)"
  },
  "letter date": {
    "en": "Letter Date",
    "hi": "दिनांक",
    "bi": "Letter Date (दिनांक)"
  },
  "दिनांक": {
    "en": "Letter Date",
    "hi": "दिनांक",
    "bi": "Letter Date (दिनांक)"
  },
  "letter date (दिनांक)": {
    "en": "Letter Date",
    "hi": "दिनांक",
    "bi": "Letter Date (दिनांक)"
  },
  "place / site": {
    "en": "Place / Site",
    "hi": "स्थान / साइट",
    "bi": "Place / Site (स्थान / साइट)"
  },
  "place / site (स्थान / साइट)": {
    "en": "Place / Site",
    "hi": "स्थान / साइट",
    "bi": "Place / Site (स्थान / साइट)"
  },
  "new daily entry": {
    "en": "New Daily Entry",
    "hi": "नई दैनिक एंट्री करें",
    "bi": "New Daily Entry (नई दैनिक एंट्री करें)"
  },
  "नई दैनिक एंट्री करें": {
    "en": "New Daily Entry",
    "hi": "नई दैनिक एंट्री करें",
    "bi": "New Daily Entry (नई दैनिक एंट्री करें)"
  },
  "new daily entry (नई दैनिक एंट्री करें)": {
    "en": "New Daily Entry",
    "hi": "नई दैनिक एंट्री करें",
    "bi": "New Daily Entry (नई दैनिक एंट्री करें)"
  },
  "21 sites directory": {
    "en": "21 Sites Directory",
    "hi": "21 साइट्स डायरेक्टरी",
    "bi": "21 Sites Directory (21 साइट्स डायरेक्टरी)"
  },
  "21 साइट्स डायरेक्टरी": {
    "en": "21 Sites Directory",
    "hi": "21 साइट्स डायरेक्टरी",
    "bi": "21 Sites Directory (21 साइट्स डायरेक्टरी)"
  },
  "21 sites directory (21 साइट्स डायरेक्टरी)": {
    "en": "21 Sites Directory",
    "hi": "21 साइट्स डायरेक्टरी",
    "bi": "21 Sites Directory (21 साइट्स डायरेक्टरी)"
  },
  "dashboard": {
    "en": "Dashboard",
    "hi": "डैशबोर्ड",
    "bi": "Dashboard (डैशबोर्ड)"
  },
  "डैशबोर्ड": {
    "en": "Dashboard",
    "hi": "डैशबोर्ड",
    "bi": "Dashboard (डैशबोर्ड)"
  },
  "dashboard (डैशबोर्ड)": {
    "en": "Dashboard",
    "hi": "डैशबोर्ड",
    "bi": "Dashboard (डैशबोर्ड)"
  },
  "reset stock to 0": {
    "en": "Reset Stock to 0",
    "hi": "स्टॉक 0 करें",
    "bi": "Reset Stock to 0 (स्टॉक 0 करें)"
  },
  "स्टॉक 0 करें": {
    "en": "Reset Stock to 0",
    "hi": "स्टॉक 0 करें",
    "bi": "Reset Stock to 0 (स्टॉक 0 करें)"
  },
  "reset stock to 0 (स्टॉक 0 करें)": {
    "en": "Reset Stock to 0",
    "hi": "स्टॉक 0 करें",
    "bi": "Reset Stock to 0 (स्टॉक 0 करें)"
  },
  "view date-wise ledger": {
    "en": "View Date-wise Ledger",
    "hi": "तारीख-वार लेजर देखें",
    "bi": "View Date-wise Ledger (तारीख-वार लेजर देखें)"
  },
  "तारीख-वार लेजर देखें": {
    "en": "View Date-wise Ledger",
    "hi": "तारीख-वार लेजर देखें",
    "bi": "View Date-wise Ledger (तारीख-वार लेजर देखें)"
  },
  "view date-wise ledger (तारीख-वार लेजर देखें)": {
    "en": "View Date-wise Ledger",
    "hi": "तारीख-वार लेजर देखें",
    "bi": "View Date-wise Ledger (तारीख-वार लेजर देखें)"
  },
  "total consumed": {
    "en": "Total Consumed",
    "hi": "कुल खर्च (दैनिक खपत)",
    "bi": "Total Consumed (कुल खर्च (दैनिक खपत))"
  },
  "कुल खर्च (दैनिक खपत)": {
    "en": "Total Consumed",
    "hi": "कुल खर्च (दैनिक खपत)",
    "bi": "Total Consumed (कुल खर्च (दैनिक खपत))"
  },
  "total consumed (कुल खर्च (दैनिक खपत))": {
    "en": "Total Consumed",
    "hi": "कुल खर्च (दैनिक खपत)",
    "bi": "Total Consumed (कुल खर्च (दैनिक खपत))"
  },
  "quantity used today:": {
    "en": "Quantity Used Today:",
    "hi": "आज कितनी मात्रा लगी:",
    "bi": "Quantity Used Today: (आज कितनी मात्रा लगी:)"
  },
  "आज कितनी मात्रा लगी:": {
    "en": "Quantity Used Today:",
    "hi": "आज कितनी मात्रा लगी:",
    "bi": "Quantity Used Today: (आज कितनी मात्रा लगी:)"
  },
  "quantity used today: (आज कितनी मात्रा लगी:)": {
    "en": "Quantity Used Today:",
    "hi": "आज कितनी मात्रा लगी:",
    "bi": "Quantity Used Today: (आज कितनी मात्रा लगी:)"
  },
  "save entry": {
    "en": "Save Entry",
    "hi": "एंट्री सुरक्षित करें",
    "bi": "Save Entry (एंट्री सुरक्षित करें)"
  },
  "एंट्री सुरक्षित करें": {
    "en": "Save Entry",
    "hi": "एंट्री सुरक्षित करें",
    "bi": "Save Entry (एंट्री सुरक्षित करें)"
  },
  "save entry (एंट्री सुरक्षित करें)": {
    "en": "Save Entry",
    "hi": "एंट्री सुरक्षित करें",
    "bi": "Save Entry (एंट्री सुरक्षित करें)"
  },
  "view daily report": {
    "en": "View Daily Report",
    "hi": "दैनिक रिपोर्ट देखें",
    "bi": "View Daily Report (दैनिक रिपोर्ट देखें)"
  },
  "दैनिक रिपोर्ट देखें": {
    "en": "View Daily Report",
    "hi": "दैनिक रिपोर्ट देखें",
    "bi": "View Daily Report (दैनिक रिपोर्ट देखें)"
  },
  "view daily report (दैनिक रिपोर्ट देखें)": {
    "en": "View Daily Report",
    "hi": "दैनिक रिपोर्ट देखें",
    "bi": "View Daily Report (दैनिक रिपोर्ट देखें)"
  },
  "material store (+add)": {
    "en": "Material Store (+Add)",
    "hi": "मटेरियल स्टोर (+ऐड)",
    "bi": "Material Store (+Add) (मटेरियल स्टोर (+ऐड))"
  },
  "मटेरियल स्टोर (+ऐड)": {
    "en": "Material Store (+Add)",
    "hi": "मटेरियल स्टोर (+ऐड)",
    "bi": "Material Store (+Add) (मटेरियल स्टोर (+ऐड))"
  },
  "material store (+add) (मटेरियल स्टोर (+ऐड))": {
    "en": "Material Store (+Add)",
    "hi": "मटेरियल स्टोर (+ऐड)",
    "bi": "Material Store (+Add) (मटेरियल स्टोर (+ऐड))"
  },
  "📑 letters register": {
    "en": "📑 Letters Register",
    "hi": "📑 जावक पत्रांक पंजी",
    "bi": "📑 Letters Register (📑 जावक पत्रांक पंजी)"
  },
  "📑 जावक पत्रांक पंजी": {
    "en": "📑 Letters Register",
    "hi": "📑 जावक पत्रांक पंजी",
    "bi": "📑 Letters Register (📑 जावक पत्रांक पंजी)"
  },
  "📑 letters register (📑 जावक पत्रांक पंजी)": {
    "en": "📑 Letters Register",
    "hi": "📑 जावक पत्रांक पंजी",
    "bi": "📑 Letters Register (📑 जावक पत्रांक पंजी)"
  },
  "save changes": {
    "en": "Save Changes",
    "hi": "बदलाव सुरक्षित करें",
    "bi": "Save Changes (बदलाव सुरक्षित करें)"
  },
  "बदलाव सुरक्षित करें": {
    "en": "Save Changes",
    "hi": "बदलाव सुरक्षित करें",
    "bi": "Save Changes (बदलाव सुरक्षित करें)"
  },
  "save changes (बदलाव सुरक्षित करें)": {
    "en": "Save Changes",
    "hi": "बदलाव सुरक्षित करें",
    "bi": "Save Changes (बदलाव सुरक्षित करें)"
  },
  "edit (संपादित करें)": {
    "en": "Edit",
    "hi": "संपादित करें",
    "bi": "Edit (संपादित करें)"
  },
  "📍 set site gps": {
    "en": "📍 Set Site GPS",
    "hi": "📍 साइट GPS सेट करें",
    "bi": "📍 Set Site GPS (📍 साइट GPS सेट करें)"
  },
  "📍 साइट gps सेट करें": {
    "en": "📍 Set Site GPS",
    "hi": "📍 साइट GPS सेट करें",
    "bi": "📍 Set Site GPS (📍 साइट GPS सेट करें)"
  },
  "📍 set site gps (📍 साइट gps सेट करें)": {
    "en": "📍 Set Site GPS",
    "hi": "📍 साइट GPS सेट करें",
    "bi": "📍 Set Site GPS (📍 साइट GPS सेट करें)"
  },
  "material catalog & rates": {
    "en": "Material Catalog & Rates",
    "hi": "सामग्री कैटलॉग व दर",
    "bi": "Material Catalog & Rates (सामग्री कैटलॉग व दर)"
  },
  "सामग्री कैटलॉग व दर": {
    "en": "Material Catalog & Rates",
    "hi": "सामग्री कैटलॉग व दर",
    "bi": "Material Catalog & Rates (सामग्री कैटलॉग व दर)"
  },
  "material catalog & rates (सामग्री कैटलॉग व दर)": {
    "en": "Material Catalog & Rates",
    "hi": "सामग्री कैटलॉग व दर",
    "bi": "Material Catalog & Rates (सामग्री कैटलॉग व दर)"
  },
  "login (unlock)": {
    "en": "Login (Unlock)",
    "hi": "लॉगिन करें",
    "bi": "Login (Unlock) (लॉगिन करें)"
  },
  "लॉगिन करें": {
    "en": "Login (Unlock)",
    "hi": "लॉगिन करें",
    "bi": "Login (Unlock) (लॉगिन करें)"
  },
  "login (unlock) (लॉगिन करें)": {
    "en": "Login (Unlock)",
    "hi": "लॉगिन करें",
    "bi": "Login (Unlock) (लॉगिन करें)"
  },
  "sl. no.": {
    "en": "Sl. No.",
    "hi": "क्र. सं.",
    "bi": "Sl. No. (क्र. सं.)"
  },
  "क्र. सं.": {
    "en": "Sl. No.",
    "hi": "क्र. सं.",
    "bi": "Sl. No. (क्र. सं.)"
  },
  "sl. no. (क्र. सं.)": {
    "en": "Sl. No.",
    "hi": "क्र. सं.",
    "bi": "Sl. No. (क्र. सं.)"
  },
  "download full backup": {
    "en": "Download Full Backup",
    "hi": "पूरा बैकअप डाउनलोड",
    "bi": "Download Full Backup (पूरा बैकअप डाउनलोड)"
  },
  "पूरा बैकअप डाउनलोड": {
    "en": "Download Full Backup",
    "hi": "पूरा बैकअप डाउनलोड",
    "bi": "Download Full Backup (पूरा बैकअप डाउनलोड)"
  },
  "download full backup (पूरा बैकअप डाउनलोड)": {
    "en": "Download Full Backup",
    "hi": "पूरा बैकअप डाउनलोड",
    "bi": "Download Full Backup (पूरा बैकअप डाउनलोड)"
  },
  "कुल भेजा गया (आवक)": {
    "en": "Total Inward",
    "hi": "कुल भेजा गया (आवक)",
    "bi": "Total Inward (कुल भेजा गया (आवक))"
  },
  "total inward (कुल भेजा गया (आवक))": {
    "en": "Total Inward",
    "hi": "कुल भेजा गया (आवक)",
    "bi": "Total Inward (कुल भेजा गया (आवक))"
  },
  "daily work progress": {
    "en": "Daily Work Progress",
    "hi": "दैनिक कार्य प्रगति",
    "bi": "Daily Work Progress (दैनिक कार्य प्रगति)"
  },
  "दैनिक कार्य प्रगति": {
    "en": "Daily Work Progress",
    "hi": "दैनिक कार्य प्रगति",
    "bi": "Daily Work Progress (दैनिक कार्य प्रगति)"
  },
  "daily work progress (दैनिक कार्य प्रगति)": {
    "en": "Daily Work Progress",
    "hi": "दैनिक कार्य प्रगति",
    "bi": "Daily Work Progress (दैनिक कार्य प्रगति)"
  },
  "online (live sync)": {
    "en": "Online (Live Sync)",
    "hi": "ऑनलाइन (लाइव सिंक)",
    "bi": "Online (Live Sync) (ऑनलाइन (लाइव सिंक))"
  },
  "ऑनलाइन (लाइव सिंक)": {
    "en": "Online (Live Sync)",
    "hi": "ऑनलाइन (लाइव सिंक)",
    "bi": "Online (Live Sync) (ऑनलाइन (लाइव सिंक))"
  },
  "online (live sync) (ऑनलाइन (लाइव सिंक))": {
    "en": "Online (Live Sync)",
    "hi": "ऑनलाइन (लाइव सिंक)",
    "bi": "Online (Live Sync) (ऑनलाइन (लाइव सिंक))"
  },
  "outgoing letters register (जावक पत्रांक पंजी)": {
    "en": "Outgoing Letters Register",
    "hi": "जावक पत्रांक पंजी",
    "bi": "Outgoing Letters Register (जावक पत्रांक पंजी)"
  },
  "copy reference number": {
    "en": "Copy Reference Number",
    "hi": "पत्रांक कॉपी करें",
    "bi": "Copy Reference Number (पत्रांक कॉपी करें)"
  },
  "पत्रांक कॉपी करें": {
    "en": "Copy Reference Number",
    "hi": "पत्रांक कॉपी करें",
    "bi": "Copy Reference Number (पत्रांक कॉपी करें)"
  },
  "copy reference number (पत्रांक कॉपी करें)": {
    "en": "Copy Reference Number",
    "hi": "पत्रांक कॉपी करें",
    "bi": "Copy Reference Number (पत्रांक कॉपी करें)"
  },
  "📍 set location": {
    "en": "📍 Set Location",
    "hi": "📍 लोकेशन सेट करें",
    "bi": "📍 Set Location (📍 लोकेशन सेट करें)"
  },
  "📍 लोकेशन सेट करें": {
    "en": "📍 Set Location",
    "hi": "📍 लोकेशन सेट करें",
    "bi": "📍 Set Location (📍 लोकेशन सेट करें)"
  },
  "📍 set location (📍 लोकेशन सेट करें)": {
    "en": "📍 Set Location",
    "hi": "📍 लोकेशन सेट करें",
    "bi": "📍 Set Location (📍 लोकेशन सेट करें)"
  },
  "gps attendance monitor": {
    "en": "GPS Attendance Monitor",
    "hi": "GPS हाजिरी मॉनिटर",
    "bi": "GPS Attendance Monitor (GPS हाजिरी मॉनिटर)"
  },
  "gps हाजिरी मॉनिटर": {
    "en": "GPS Attendance Monitor",
    "hi": "GPS हाजिरी मॉनिटर",
    "bi": "GPS Attendance Monitor (GPS हाजिरी मॉनिटर)"
  },
  "gps attendance monitor (gps हाजिरी मॉनिटर)": {
    "en": "GPS Attendance Monitor",
    "hi": "GPS हाजिरी मॉनिटर",
    "bi": "GPS Attendance Monitor (GPS हाजिरी मॉनिटर)"
  },
  "📸 upload photos": {
    "en": "📸 Upload Photos",
    "hi": "📸 फोटो अपलोड करें",
    "bi": "📸 Upload Photos (📸 फोटो अपलोड करें)"
  },
  "📸 फोटो अपलोड करें": {
    "en": "📸 Upload Photos",
    "hi": "📸 फोटो अपलोड करें",
    "bi": "📸 Upload Photos (📸 फोटो अपलोड करें)"
  },
  "📸 upload photos (📸 फोटो अपलोड करें)": {
    "en": "📸 Upload Photos",
    "hi": "📸 फोटो अपलोड करें",
    "bi": "📸 Upload Photos (📸 फोटो अपलोड करें)"
  },
  "📝 manual attendance": {
    "en": "📝 Manual Attendance",
    "hi": "📝 मैन्युअल हाजिरी",
    "bi": "📝 Manual Attendance (📝 मैन्युअल हाजिरी)"
  },
  "📝 मैन्युअल हाजिरी": {
    "en": "📝 Manual Attendance",
    "hi": "📝 मैन्युअल हाजिरी",
    "bi": "📝 Manual Attendance (📝 मैन्युअल हाजिरी)"
  },
  "📝 manual attendance (📝 मैन्युअल हाजिरी)": {
    "en": "📝 Manual Attendance",
    "hi": "📝 मैन्युअल हाजिरी",
    "bi": "📝 Manual Attendance (📝 मैन्युअल हाजिरी)"
  },
  "last location ping": {
    "en": "Last Location Ping",
    "hi": "अंतिम लोकेशन पिंग",
    "bi": "Last Location Ping (अंतिम लोकेशन पिंग)"
  },
  "अंतिम लोकेशन पिंग": {
    "en": "Last Location Ping",
    "hi": "अंतिम लोकेशन पिंग",
    "bi": "Last Location Ping (अंतिम लोकेशन पिंग)"
  },
  "last location ping (अंतिम लोकेशन पिंग)": {
    "en": "Last Location Ping",
    "hi": "अंतिम लोकेशन पिंग",
    "bi": "Last Location Ping (अंतिम लोकेशन पिंग)"
  },
  "daily material usage": {
    "en": "Daily Material Usage",
    "hi": "दैनिक सामग्री खपत",
    "bi": "Daily Material Usage (दैनिक सामग्री खपत)"
  },
  "दैनिक सामग्री खपत": {
    "en": "Daily Material Usage",
    "hi": "दैनिक सामग्री खपत",
    "bi": "Daily Material Usage (दैनिक सामग्री खपत)"
  },
  "daily material usage (दैनिक सामग्री खपत)": {
    "en": "Daily Material Usage",
    "hi": "दैनिक सामग्री खपत",
    "bi": "Daily Material Usage (दैनिक सामग्री खपत)"
  },
  "purpose of letter": {
    "en": "Purpose of Letter",
    "hi": "पत्र का उद्देश्य",
    "bi": "Purpose of Letter (पत्र का उद्देश्य)"
  },
  "पत्र का उद्देश्य": {
    "en": "Purpose of Letter",
    "hi": "पत्र का उद्देश्य",
    "bi": "Purpose of Letter (पत्र का उद्देश्य)"
  },
  "purpose of letter (पत्र का उद्देश्य)": {
    "en": "Purpose of Letter",
    "hi": "पत्र का उद्देश्य",
    "bi": "Purpose of Letter (पत्र का उद्देश्य)"
  },
  "total letters:": {
    "en": "Total Letters:",
    "hi": "कुल पत्र संख्या:",
    "bi": "Total Letters: (कुल पत्र संख्या:)"
  },
  "कुल पत्र संख्या:": {
    "en": "Total Letters:",
    "hi": "कुल पत्र संख्या:",
    "bi": "Total Letters: (कुल पत्र संख्या:)"
  },
  "total letters: (कुल पत्र संख्या:)": {
    "en": "Total Letters:",
    "hi": "कुल पत्र संख्या:",
    "bi": "Total Letters: (कुल पत्र संख्या:)"
  },
  "refresh page": {
    "en": "Refresh Page",
    "hi": "पेज रिफ्रेश करें",
    "bi": "Refresh Page (पेज रिफ्रेश करें)"
  },
  "पेज रिफ्रेश करें": {
    "en": "Refresh Page",
    "hi": "पेज रिफ्रेश करें",
    "bi": "Refresh Page (पेज रिफ्रेश करें)"
  },
  "refresh page (पेज रिफ्रेश करें)": {
    "en": "Refresh Page (Try Again)",
    "hi": "पेज रिफ्रेश करें (Try Again)",
    "bi": "Refresh Page (पेज रिफ्रेश करें)"
  },
  "your authorized site": {
    "en": "Your Authorized Site",
    "hi": "आपकी अधिकृत साइट",
    "bi": "Your Authorized Site (आपकी अधिकृत साइट)"
  },
  "आपकी अधिकृत साइट": {
    "en": "Your Authorized Site",
    "hi": "आपकी अधिकृत साइट",
    "bi": "Your Authorized Site (आपकी अधिकृत साइट)"
  },
  "your authorized site (आपकी अधिकृत साइट)": {
    "en": "Your Authorized Site",
    "hi": "आपकी अधिकृत साइट",
    "bi": "Your Authorized Site (आपकी अधिकृत साइट)"
  },
  "add new entry": {
    "en": "Add New Entry",
    "hi": "नई एंट्री जोड़ें",
    "bi": "Add New Entry (नई एंट्री जोड़ें)"
  },
  "नई एंट्री जोड़ें": {
    "en": "Add New Entry",
    "hi": "नई एंट्री जोड़ें",
    "bi": "Add New Entry (नई एंट्री जोड़ें)"
  },
  "add new entry (नई एंट्री जोड़ें)": {
    "en": "Add New Entry",
    "hi": "नई एंट्री जोड़ें",
    "bi": "Add New Entry (नई एंट्री जोड़ें)"
  },
  "dpr work progress": {
    "en": "DPR Work Progress",
    "hi": "DPR कार्य प्रगति",
    "bi": "DPR Work Progress (DPR कार्य प्रगति)"
  },
  "dpr कार्य प्रगति": {
    "en": "DPR Work Progress",
    "hi": "DPR कार्य प्रगति",
    "bi": "DPR Work Progress (DPR कार्य प्रगति)"
  },
  "dpr work progress (dpr कार्य प्रगति)": {
    "en": "DPR Work Progress",
    "hi": "DPR कार्य प्रगति",
    "bi": "DPR Work Progress (DPR कार्य प्रगति)"
  },
  "total cumulative progress": {
    "en": "Total Cumulative Progress",
    "hi": "कुल संचयी प्रगति",
    "bi": "Total Cumulative Progress (कुल संचयी प्रगति)"
  },
  "कुल संचयी प्रगति": {
    "en": "Total Cumulative Progress",
    "hi": "कुल संचयी प्रगति",
    "bi": "Total Cumulative Progress (कुल संचयी प्रगति)"
  },
  "total cumulative progress (कुल संचयी प्रगति)": {
    "en": "Total Cumulative Progress",
    "hi": "कुल संचयी प्रगति",
    "bi": "Total Cumulative Progress (कुल संचयी प्रगति)"
  },
  "fixed rate list": {
    "en": "Fixed Rate List",
    "hi": "Fixed Rate List",
    "bi": "Fixed Rate List"
  },
  "estimated usage": {
    "en": "Estimated Usage",
    "hi": "Estimated Usage",
    "bi": "Estimated Usage"
  },
  "open reports": {
    "en": "Open Reports",
    "hi": "रिपोर्ट्स खोलें",
    "bi": "Open Reports (रिपोर्ट्स खोलें)"
  },
  "रिपोर्ट्स खोलें": {
    "en": "Open Reports",
    "hi": "रिपोर्ट्स खोलें",
    "bi": "Open Reports (रिपोर्ट्स खोलें)"
  },
  "open reports (रिपोर्ट्स खोलें)": {
    "en": "Open Reports",
    "hi": "रिपोर्ट्स खोलें",
    "bi": "Open Reports (रिपोर्ट्स खोलें)"
  },
  "reference register": {
    "en": "Reference Register",
    "hi": "पत्रांक रजिस्टर",
    "bi": "Reference Register (पत्रांक रजिस्टर)"
  },
  "reference register (पत्रांक रजिस्टर)": {
    "en": "Reference Register",
    "hi": "पत्रांक रजिस्टर",
    "bi": "Reference Register (पत्रांक रजिस्टर)"
  },
  "complete data backup": {
    "en": "Complete Data Backup",
    "hi": "पूरा डेटा बैकअप",
    "bi": "Complete Data Backup (पूरा डेटा बैकअप)"
  },
  "पूरा डेटा बैकअप": {
    "en": "Complete Data Backup",
    "hi": "पूरा डेटा बैकअप",
    "bi": "Complete Data Backup (पूरा डेटा बैकअप)"
  },
  "complete data backup (पूरा डेटा बैकअप)": {
    "en": "Complete Data Backup",
    "hi": "पूरा डेटा बैकअप",
    "bi": "Complete Data Backup (पूरा डेटा बैकअप)"
  },
  "हाजिरी सेव करें": {
    "en": "Save Attendance",
    "hi": "हाजिरी सेव करें",
    "bi": "Save Attendance (हाजिरी सेव करें)"
  },
  "save attendance (हाजिरी सेव करें)": {
    "en": "Save Attendance",
    "hi": "हाजिरी सेव करें",
    "bi": "Save Attendance (हाजिरी सेव करें)"
  },
  "कुल खर्च": {
    "en": "Total Consumed",
    "hi": "कुल खर्च",
    "bi": "Total Consumed (कुल खर्च)"
  },
  "total consumed (कुल खर्च)": {
    "en": "Total Consumed",
    "hi": "कुल खर्च",
    "bi": "Total Consumed (कुल खर्च)"
  },
  "fhtc tap connections": {
    "en": "FHTC Tap Connections",
    "hi": "FHTC नल कनेक्शन",
    "bi": "FHTC Tap Connections (FHTC नल कनेक्शन)"
  },
  "fhtc नल कनेक्शन": {
    "en": "FHTC Tap Connections",
    "hi": "FHTC नल कनेक्शन",
    "bi": "FHTC Tap Connections (FHTC नल कनेक्शन)"
  },
  "fhtc tap connections (fhtc नल कनेक्शन)": {
    "en": "FHTC Tap Connections",
    "hi": "FHTC नल कनेक्शन",
    "bi": "FHTC Tap Connections (FHTC नल कनेक्शन)"
  },
  "water tower construction": {
    "en": "Water Tower Construction",
    "hi": "जलमीनार निर्माण",
    "bi": "Water Tower Construction (जलमीनार निर्माण)"
  },
  "जलमीनार निर्माण": {
    "en": "Water Tower Construction",
    "hi": "जलमीनार निर्माण",
    "bi": "Water Tower Construction (जलमीनार निर्माण)"
  },
  "water tower construction (जलमीनार निर्माण)": {
    "en": "Water Tower Construction",
    "hi": "जलमीनार निर्माण",
    "bi": "Water Tower Construction (जलमीनार निर्माण)"
  },
  "category / type": {
    "en": "Category / Type",
    "hi": "श्रेणी / प्रकार",
    "bi": "Category / Type (श्रेणी / प्रकार)"
  },
  "श्रेणी / प्रकार": {
    "en": "Category / Type",
    "hi": "श्रेणी / प्रकार",
    "bi": "Category / Type (श्रेणी / प्रकार)"
  },
  "category / type (श्रेणी / प्रकार)": {
    "en": "Category / Type",
    "hi": "श्रेणी / प्रकार",
    "bi": "Category / Type (श्रेणी / प्रकार)"
  },
  "material catalog": {
    "en": "Material Catalog",
    "hi": "सामग्री कैटलॉग",
    "bi": "Material Catalog (सामग्री कैटलॉग)"
  },
  "सामग्री कैटलॉग": {
    "en": "Material Catalog",
    "hi": "सामग्री कैटलॉग",
    "bi": "Material Catalog (सामग्री कैटलॉग)"
  },
  "material catalog (सामग्री कैटलॉग)": {
    "en": "Material Catalog",
    "hi": "सामग्री कैटलॉग",
    "bi": "Material Catalog (सामग्री कैटलॉग)"
  },
  "total consumption value": {
    "en": "Total Consumption Value",
    "hi": "कुल खर्च मूल्य",
    "bi": "Total Consumption Value (कुल खर्च मूल्य)"
  },
  "कुल खर्च मूल्य": {
    "en": "Total Consumption Value",
    "hi": "कुल खर्च मूल्य",
    "bi": "Total Consumption Value (कुल खर्च मूल्य)"
  },
  "total consumption value (कुल खर्च मूल्य)": {
    "en": "Total Consumption Value",
    "hi": "कुल खर्च मूल्य",
    "bi": "Total Consumption Value (कुल खर्च मूल्य)"
  },
  "📑 पत्रांक पंजी": {
    "en": "📑 Letters Register",
    "hi": "📑 पत्रांक पंजी",
    "bi": "📑 Letters Register (📑 पत्रांक पंजी)"
  },
  "📑 letters register (📑 पत्रांक पंजी)": {
    "en": "📑 Letters Register",
    "hi": "📑 पत्रांक पंजी",
    "bi": "📑 Letters Register (📑 पत्रांक पंजी)"
  },
  "total outgoing letters:": {
    "en": "Total Outgoing Letters:",
    "hi": "कुल जावक पत्र:",
    "bi": "Total Outgoing Letters: (कुल जावक पत्र:)"
  },
  "कुल जावक पत्र:": {
    "en": "Total Outgoing Letters:",
    "hi": "कुल जावक पत्र:",
    "bi": "Total Outgoing Letters: (कुल जावक पत्र:)"
  },
  "total outgoing letters: (कुल जावक पत्र:)": {
    "en": "Total Outgoing Letters:",
    "hi": "कुल जावक पत्र:",
    "bi": "Total Outgoing Letters: (कुल जावक पत्र:)"
  },
  "total recorded letters:": {
    "en": "Total Recorded Letters:",
    "hi": "कुल दर्ज पत्र:",
    "bi": "Total Recorded Letters: (कुल दर्ज पत्र:)"
  },
  "कुल दर्ज पत्र:": {
    "en": "Total Recorded Letters:",
    "hi": "कुल दर्ज पत्र:",
    "bi": "Total Recorded Letters: (कुल दर्ज पत्र:)"
  },
  "total recorded letters: (कुल दर्ज पत्र:)": {
    "en": "Total Recorded Letters:",
    "hi": "कुल दर्ज पत्र:",
    "bi": "Total Recorded Letters: (कुल दर्ज पत्र:)"
  },
  "date-wise ledger": {
    "en": "Date-wise Ledger",
    "hi": "तारीख-वार लेजर",
    "bi": "Date-wise Ledger (तारीख-वार लेजर)"
  },
  "date-wise ledger (तारीख-वार लेजर)": {
    "en": "Date-wise Ledger",
    "hi": "तारीख-वार लेजर",
    "bi": "Date-wise Ledger (तारीख-वार लेजर)"
  },
  "healthy stock": {
    "en": "Healthy Stock",
    "hi": "पर्याप्त स्टॉक",
    "bi": "Healthy Stock (पर्याप्त स्टॉक)"
  },
  "पर्याप्त स्टॉक": {
    "en": "Healthy Stock",
    "hi": "पर्याप्त स्टॉक",
    "bi": "Healthy Stock (पर्याप्त स्टॉक)"
  },
  "healthy stock (पर्याप्त स्टॉक)": {
    "en": "Healthy Stock",
    "hi": "पर्याप्त स्टॉक",
    "bi": "Healthy Stock (पर्याप्त स्टॉक)"
  },
  "location / purpose of work": {
    "en": "Location / Purpose of Work",
    "hi": "कहाँ लगाया गया",
    "bi": "Location / Purpose of Work (कहाँ लगाया गया)"
  },
  "कहाँ लगाया गया": {
    "en": "Location / Purpose of Work",
    "hi": "कहाँ लगाया गया",
    "bi": "Location / Purpose of Work (कहाँ लगाया गया)"
  },
  "location / purpose of work (कहाँ लगाया गया)": {
    "en": "Location / Purpose of Work",
    "hi": "कहाँ लगाया गया",
    "bi": "Location / Purpose of Work (कहाँ लगाया गया)"
  },
  "pipeline trenching": {
    "en": "Pipeline Trenching",
    "hi": "पाइपलाइन खुदाई",
    "bi": "Pipeline Trenching (पाइपलाइन खुदाई)"
  },
  "पाइपलाइन खुदाई": {
    "en": "Pipeline Trenching",
    "hi": "पाइपलाइन खुदाई",
    "bi": "Pipeline Trenching (पाइपलाइन खुदाई)"
  },
  "pipeline trenching (पाइपलाइन खुदाई)": {
    "en": "Pipeline Trenching",
    "hi": "पाइपलाइन खुदाई",
    "bi": "Pipeline Trenching (पाइपलाइन खुदाई)"
  },
  "select material:": {
    "en": "Select Material:",
    "hi": "सामग्री चुनें:",
    "bi": "Select Material: (सामग्री चुनें:)"
  },
  "सामग्री चुनें:": {
    "en": "Select Material:",
    "hi": "सामग्री चुनें:",
    "bi": "Select Material: (सामग्री चुनें:)"
  },
  "select material: (सामग्री चुनें:)": {
    "en": "Select Material:",
    "hi": "सामग्री चुनें:",
    "bi": "Select Material: (सामग्री चुनें:)"
  },
  "download excel": {
    "en": "Download Excel",
    "hi": "एक्सेल डाउनलोड",
    "bi": "Download Excel (एक्सेल डाउनलोड)"
  },
  "एक्सेल डाउनलोड": {
    "en": "Download Excel",
    "hi": "एक्सेल डाउनलोड",
    "bi": "Download Excel (एक्सेल डाउनलोड)"
  },
  "download excel (एक्सेल डाउनलोड)": {
    "en": "Download Excel",
    "hi": "एक्सेल डाउनलोड",
    "bi": "Download Excel (एक्सेल डाउनलोड)"
  },
  "saved records": {
    "en": "Saved Records",
    "hi": "Saved Records",
    "bi": "Saved Records"
  },
  "all materials": {
    "en": "All Materials",
    "hi": "All Materials",
    "bi": "All Materials"
  },
  "material store": {
    "en": "Material Store",
    "hi": "मटेरियल स्टोर",
    "bi": "Material Store (मटेरियल स्टोर)"
  },
  "मटेरियल स्टोर": {
    "en": "Material Store",
    "hi": "मटेरियल स्टोर",
    "bi": "Material Store (मटेरियल स्टोर)"
  },
  "material store (मटेरियल स्टोर)": {
    "en": "Material Store",
    "hi": "मटेरियल स्टोर",
    "bi": "Material Store (मटेरियल स्टोर)"
  },
  "सामग्री स्टोर": {
    "en": "Material Store",
    "hi": "सामग्री स्टोर",
    "bi": "Material Store (सामग्री स्टोर)"
  },
  "material store (सामग्री स्टोर)": {
    "en": "Material Store",
    "hi": "सामग्री स्टोर",
    "bi": "Material Store (सामग्री स्टोर)"
  },
  "next ref no:": {
    "en": "Next Ref No:",
    "hi": "अगला पत्रांक:",
    "bi": "Next Ref No: (अगला पत्रांक:)"
  },
  "अगला पत्रांक:": {
    "en": "Next Ref No:",
    "hi": "अगला पत्रांक:",
    "bi": "Next Ref No: (अगला पत्रांक:)"
  },
  "next ref no: (अगला पत्रांक:)": {
    "en": "Next Ref No:",
    "hi": "अगला पत्रांक:",
    "bi": "Next Ref No: (अगला पत्रांक:)"
  },
  "date (दिनांक)": {
    "en": "Date",
    "hi": "दिनांक",
    "bi": "Date (दिनांक)"
  },
  "place": {
    "en": "Place",
    "hi": "स्थान",
    "bi": "Place (स्थान)"
  },
  "स्थान": {
    "en": "Place",
    "hi": "स्थान",
    "bi": "Place (स्थान)"
  },
  "place (स्थान)": {
    "en": "Place",
    "hi": "स्थान",
    "bi": "Place (स्थान)"
  },
  "download date:": {
    "en": "Download Date:",
    "hi": "डाउनलोड तिथि:",
    "bi": "Download Date: (डाउनलोड तिथि:)"
  },
  "डाउनलोड तिथि:": {
    "en": "Download Date:",
    "hi": "डाउनलोड तिथि:",
    "bi": "Download Date: (डाउनलोड तिथि:)"
  },
  "download date: (डाउनलोड तिथि:)": {
    "en": "Download Date:",
    "hi": "डाउनलोड तिथि:",
    "bi": "Download Date: (डाउनलोड तिथि:)"
  },
  "company website": {
    "en": "Company Website",
    "hi": "कंपनी वेबसाइट",
    "bi": "Company Website (कंपनी वेबसाइट)"
  },
  "कंपनी वेबसाइट": {
    "en": "Company Website",
    "hi": "कंपनी वेबसाइट",
    "bi": "Company Website (कंपनी वेबसाइट)"
  },
  "company website (कंपनी वेबसाइट)": {
    "en": "Company Website",
    "hi": "कंपनी वेबसाइट",
    "bi": "Company Website (कंपनी वेबसाइट)"
  },
  "material list": {
    "en": "Material List",
    "hi": "मटेरियल लिस्ट",
    "bi": "Material List (मटेरियल लिस्ट)"
  },
  "मटेरियल लिस्ट": {
    "en": "Material List",
    "hi": "मटेरियल लिस्ट",
    "bi": "Material List (मटेरियल लिस्ट)"
  },
  "material list (मटेरियल लिस्ट)": {
    "en": "Material List",
    "hi": "मटेरियल लिस्ट",
    "bi": "Material List (मटेरियल लिस्ट)"
  },
  "सामग्री लिस्ट": {
    "en": "Material List",
    "hi": "सामग्री लिस्ट",
    "bi": "Material List (सामग्री लिस्ट)"
  },
  "material list (सामग्री लिस्ट)": {
    "en": "Material List",
    "hi": "सामग्री लिस्ट",
    "bi": "Material List (सामग्री लिस्ट)"
  },
  "gi mistri": {
    "en": "GI Mistri",
    "hi": "जीआई मिस्त्री",
    "bi": "GI Mistri (जीआई मिस्त्री)"
  },
  "जीआई मिस्त्री": {
    "en": "GI Mistri",
    "hi": "जीआई मिस्त्री",
    "bi": "GI Mistri (जीआई मिस्त्री)"
  },
  "gi mistri (जीआई मिस्त्री)": {
    "en": "GI Mistri",
    "hi": "जीआई मिस्त्री",
    "bi": "GI Mistri (जीआई मिस्त्री)"
  },
  "selfie attendance": {
    "en": "Selfie Attendance",
    "hi": "सेल्फी हाजिरी",
    "bi": "Selfie Attendance (सेल्फी हाजिरी)"
  },
  "सेल्फी हाजिरी": {
    "en": "Selfie Attendance",
    "hi": "सेल्फी हाजिरी",
    "bi": "Selfie Attendance (सेल्फी हाजिरी)"
  },
  "selfie attendance (सेल्फी हाजिरी)": {
    "en": "Selfie Attendance",
    "hi": "सेल्फी हाजिरी",
    "bi": "Selfie Attendance (सेल्फी हाजिरी)"
  },
  "stock register": {
    "en": "Stock Register",
    "hi": "स्टॉक रजिस्टर",
    "bi": "Stock Register (स्टॉक रजिस्टर)"
  },
  "स्टॉक रजिस्टर": {
    "en": "Stock Register",
    "hi": "स्टॉक रजिस्टर",
    "bi": "Stock Register (स्टॉक रजिस्टर)"
  },
  "stock register (स्टॉक रजिस्टर)": {
    "en": "Stock Register",
    "hi": "स्टॉक रजिस्टर",
    "bi": "Stock Register (स्टॉक रजिस्टर)"
  },
  "नया माल भेजें": {
    "en": "Dispatch Inward Stock",
    "hi": "नया माल भेजें",
    "bi": "Dispatch Inward Stock (नया माल भेजें)"
  },
  "dispatch inward stock (नया माल भेजें)": {
    "en": "Dispatch Inward Stock",
    "hi": "नया माल भेजें",
    "bi": "Dispatch Inward Stock (नया माल भेजें)"
  },
  "बचा हुआ स्टॉक": {
    "en": "Balance Stock",
    "hi": "बचा हुआ स्टॉक",
    "bi": "Balance Stock (बचा हुआ स्टॉक)"
  },
  "balance stock (बचा हुआ स्टॉक)": {
    "en": "Balance Stock",
    "hi": "बचा हुआ स्टॉक",
    "bi": "Balance Stock (बचा हुआ स्टॉक)"
  },
  "date:": {
    "en": "Date:",
    "hi": "तारीख:",
    "bi": "Date (तारीख):"
  },
  "तारीख:": {
    "en": "Date:",
    "hi": "तारीख:",
    "bi": "Date (तारीख):"
  },
  "date: (तारीख:)": {
    "en": "Date:",
    "hi": "तारीख:",
    "bi": "Date: (तारीख:)"
  },
  "all categories": {
    "en": "All Categories",
    "hi": "सभी श्रेणियां",
    "bi": "All Categories (सभी श्रेणियां)"
  },
  "सभी श्रेणियां": {
    "en": "All Categories",
    "hi": "सभी श्रेणियां",
    "bi": "All Categories (सभी श्रेणियां)"
  },
  "all categories (सभी श्रेणियां)": {
    "en": "All Categories",
    "hi": "सभी श्रेणियां",
    "bi": "All Categories (सभी श्रेणियां)"
  },
  "select material": {
    "en": "Select Material",
    "hi": "सामग्री चुनें",
    "bi": "Select Material (सामग्री चुनें)"
  },
  "सामग्री चुनें": {
    "en": "Select Material",
    "hi": "सामग्री चुनें",
    "bi": "Select Material (सामग्री चुनें)"
  },
  "select material (सामग्री चुनें)": {
    "en": "Select Material",
    "hi": "सामग्री चुनें",
    "bi": "Select Material (सामग्री चुनें)"
  },
  "excel डाउनलोड": {
    "en": "Download Excel",
    "hi": "Excel डाउनलोड",
    "bi": "Download Excel (Excel डाउनलोड)"
  },
  "download excel (excel डाउनलोड)": {
    "en": "Download Excel",
    "hi": "Excel डाउनलोड",
    "bi": "Download Excel (Excel डाउनलोड)"
  },
  "total value:": {
    "en": "Total Value:",
    "hi": "Total Value:",
    "bi": "Total Value:"
  },
  "क्र.सं.": {
    "en": "Sl. No.",
    "hi": "क्र.सं.",
    "bi": "Sl. No. (क्र.सं.)"
  },
  "sl. no. (क्र.सं.)": {
    "en": "Sl. No.",
    "hi": "क्र.सं.",
    "bi": "Sl. No. (क्र.सं.)"
  },
  "📍 gps attendance": {
    "en": "📍 GPS Attendance",
    "hi": "📍 GPS हाजिरी",
    "bi": "📍 GPS Attendance (📍 GPS हाजिरी)"
  },
  "📍 gps हाजिरी": {
    "en": "📍 GPS Attendance",
    "hi": "📍 GPS हाजिरी",
    "bi": "📍 GPS Attendance (📍 GPS हाजिरी)"
  },
  "📍 gps attendance (📍 gps हाजिरी)": {
    "en": "📍 GPS Attendance",
    "hi": "📍 GPS हाजिरी",
    "bi": "📍 GPS Attendance (📍 GPS हाजिरी)"
  },
  "site incharge": {
    "en": "Site Incharge",
    "hi": "साइट इनचार्ज",
    "bi": "Site Incharge (साइट इनचार्ज)"
  },
  "साइट इनचार्ज": {
    "en": "Site Incharge",
    "hi": "साइट इनचार्ज",
    "bi": "Site Incharge (साइट इनचार्ज)"
  },
  "site incharge (साइट इनचार्ज)": {
    "en": "Site Incharge",
    "hi": "साइट इनचार्ज",
    "bi": "Site Incharge (साइट इनचार्ज)"
  },
  "distance from site": {
    "en": "Distance from Site",
    "hi": "साइट से दूरी",
    "bi": "Distance from Site (साइट से दूरी)"
  },
  "साइट से दूरी": {
    "en": "Distance from Site",
    "hi": "साइट से दूरी",
    "bi": "Distance from Site (साइट से दूरी)"
  },
  "distance from site (साइट से दूरी)": {
    "en": "Distance from Site",
    "hi": "साइट से दूरी",
    "bi": "Distance from Site (साइट से दूरी)"
  },
  "वर्कर का नाम": {
    "en": "Worker Name",
    "hi": "वर्कर का नाम",
    "bi": "Worker Name (वर्कर का नाम)"
  },
  "worker name (वर्कर का नाम)": {
    "en": "Worker Name",
    "hi": "वर्कर का नाम",
    "bi": "Worker Name (वर्कर का नाम)"
  },
  "बैलेंस स्टॉक": {
    "en": "Balance Stock",
    "hi": "बैलेंस स्टॉक",
    "bi": "Balance Stock (बैलेंस स्टॉक)"
  },
  "balance stock (बैलेंस स्टॉक)": {
    "en": "Balance Stock",
    "hi": "बैलेंस स्टॉक",
    "bi": "Balance Stock (बैलेंस स्टॉक)"
  },
  "boring work": {
    "en": "Boring Work",
    "hi": "बोरिंग कार्य",
    "bi": "Boring Work (बोरिंग कार्य)"
  },
  "बोरिंग कार्य": {
    "en": "Boring Work",
    "hi": "बोरिंग कार्य",
    "bi": "Boring Work (बोरिंग कार्य)"
  },
  "boring work (बोरिंग कार्य)": {
    "en": "Boring Work",
    "hi": "बोरिंग कार्य",
    "bi": "Boring Work (बोरिंग कार्य)"
  },
  "total amount (₹)": {
    "en": "Total Amount (₹)",
    "hi": "कुल राशि (₹)",
    "bi": "Total Amount (₹) (कुल राशि (₹))"
  },
  "कुल राशि (₹)": {
    "en": "Total Amount (₹)",
    "hi": "कुल राशि (₹)",
    "bi": "Total Amount (₹) (कुल राशि (₹))"
  },
  "total amount (₹) (कुल राशि (₹))": {
    "en": "Total Amount (₹)",
    "hi": "कुल राशि (₹)",
    "bi": "Total Amount (₹) (कुल राशि (₹))"
  },
  "select date:": {
    "en": "Select Date:",
    "hi": "तारीख चुनें:",
    "bi": "Select Date: (तारीख चुनें:)"
  },
  "तारीख चुनें:": {
    "en": "Select Date:",
    "hi": "तारीख चुनें:",
    "bi": "Select Date: (तारीख चुनें:)"
  },
  "select date: (तारीख चुनें:)": {
    "en": "Select Date:",
    "hi": "तारीख चुनें:",
    "bi": "Select Date: (तारीख चुनें:)"
  },
  "filter": {
    "en": "Filter",
    "hi": "फ़िल्टर करें",
    "bi": "Filter (फ़िल्टर करें)"
  },
  "फ़िल्टर करें": {
    "en": "Filter",
    "hi": "फ़िल्टर करें",
    "bi": "Filter (फ़िल्टर करें)"
  },
  "filter (फ़िल्टर करें)": {
    "en": "Filter",
    "hi": "फ़िल्टर करें",
    "bi": "Filter (फ़िल्टर करें)"
  },
  "open stock": {
    "en": "Open Stock",
    "hi": "स्टॉक खोलें",
    "bi": "Open Stock (स्टॉक खोलें)"
  },
  "स्टॉक खोलें": {
    "en": "Open Stock",
    "hi": "स्टॉक खोलें",
    "bi": "Open Stock (स्टॉक खोलें)"
  },
  "open stock (स्टॉक खोलें)": {
    "en": "Open Stock",
    "hi": "स्टॉक खोलें",
    "bi": "Open Stock (स्टॉक खोलें)"
  },
  "open gallery": {
    "en": "Open Gallery",
    "hi": "गैलरी खोलें",
    "bi": "Open Gallery (गैलरी खोलें)"
  },
  "गैलरी खोलें": {
    "en": "Open Gallery",
    "hi": "गैलरी खोलें",
    "bi": "Open Gallery (गैलरी खोलें)"
  },
  "open gallery (गैलरी खोलें)": {
    "en": "Open Gallery",
    "hi": "गैलरी खोलें",
    "bi": "Open Gallery (गैलरी खोलें)"
  },
  "quick select:": {
    "en": "Quick Select:",
    "hi": "त्वरित चयन:",
    "bi": "Quick Select: (त्वरित चयन:)"
  },
  "त्वरित चयन:": {
    "en": "Quick Select:",
    "hi": "त्वरित चयन:",
    "bi": "Quick Select: (त्वरित चयन:)"
  },
  "quick select: (त्वरित चयन:)": {
    "en": "Quick Select:",
    "hi": "त्वरित चयन:",
    "bi": "Quick Select: (त्वरित चयन:)"
  },
  "site portal": {
    "en": "Site Portal",
    "hi": "साइट पोर्टल",
    "bi": "Site Portal (साइट पोर्टल)"
  },
  "साइट पोर्टल": {
    "en": "Site Portal",
    "hi": "साइट पोर्टल",
    "bi": "Site Portal (साइट पोर्टल)"
  },
  "site portal (साइट पोर्टल)": {
    "en": "Site Portal",
    "hi": "साइट पोर्टल",
    "bi": "Site Portal (साइट पोर्टल)"
  },
  "office work (ऑफिस वर्क)": {
    "en": "Office Work",
    "hi": "ऑफिस वर्क",
    "bi": "Office Work (ऑफिस वर्क)"
  },
  "logout": {
    "en": "Logout",
    "hi": "लॉगआउट करें",
    "bi": "Logout (लॉगआउट करें)"
  },
  "लॉगआउट करें": {
    "en": "Logout",
    "hi": "लॉगआउट करें",
    "bi": "Logout (लॉगआउट करें)"
  },
  "logout (लॉगआउट करें)": {
    "en": "Logout",
    "hi": "लॉगआउट करें",
    "bi": "Logout (लॉगआउट करें)"
  },
  "data entry": {
    "en": "Data Entry",
    "hi": "डाटा एंट्री",
    "bi": "Data Entry (डाटा एंट्री)"
  },
  "डाटा एंट्री": {
    "en": "Data Entry",
    "hi": "डाटा एंट्री",
    "bi": "Data Entry (डाटा एंट्री)"
  },
  "data entry (डाटा एंट्री)": {
    "en": "Data Entry",
    "hi": "डाटा एंट्री",
    "bi": "Data Entry (डाटा एंट्री)"
  },
  "total manpower": {
    "en": "Total Manpower",
    "hi": "कुल मैनपावर",
    "bi": "Total Manpower (कुल मैनपावर)"
  },
  "कुल मैनपावर": {
    "en": "Total Manpower",
    "hi": "कुल मैनपावर",
    "bi": "Total Manpower (कुल मैनपावर)"
  },
  "total manpower (कुल मैनपावर)": {
    "en": "Total Manpower",
    "hi": "कुल मैनपावर",
    "bi": "Total Manpower (कुल मैनपावर)"
  },
  "mobile number": {
    "en": "Mobile Number",
    "hi": "मोबाइल नंबर",
    "bi": "Mobile Number (मोबाइल नंबर)"
  },
  "मोबाइल नंबर": {
    "en": "Mobile Number",
    "hi": "मोबाइल नंबर",
    "bi": "Mobile Number (मोबाइल नंबर)"
  },
  "mobile number (मोबाइल नंबर)": {
    "en": "Mobile Number",
    "hi": "मोबाइल नंबर",
    "bi": "Mobile Number (मोबाइल नंबर)"
  },
  "pipeline laying": {
    "en": "Pipeline Laying",
    "hi": "पाइप बिछाना",
    "bi": "Pipeline Laying (पाइप बिछाना)"
  },
  "पाइप बिछाना": {
    "en": "Pipeline Laying",
    "hi": "पाइप बिछाना",
    "bi": "Pipeline Laying (पाइप बिछाना)"
  },
  "pipeline laying (पाइप बिछाना)": {
    "en": "Pipeline Laying",
    "hi": "पाइप बिछाना",
    "bi": "Pipeline Laying (पाइप बिछाना)"
  },
  "today's work": {
    "en": "Today's Work",
    "hi": "आज का कार्य",
    "bi": "Today's Work (आज का कार्य)"
  },
  "आज का कार्य": {
    "en": "Today's Work",
    "hi": "आज का कार्य",
    "bi": "Today's Work (आज का कार्य)"
  },
  "today's work (आज का कार्य)": {
    "en": "Today's Work",
    "hi": "आज का कार्य",
    "bi": "Today's Work (आज का कार्य)"
  },
  "work description": {
    "en": "Work Description",
    "hi": "कार्य विवरण",
    "bi": "Work Description (कार्य विवरण)"
  },
  "work description (कार्य विवरण)": {
    "en": "Work Description",
    "hi": "कार्य विवरण",
    "bi": "Work Description (कार्य विवरण)"
  },
  "select site:": {
    "en": "Select Site:",
    "hi": "साइट चुनें:",
    "bi": "Select Site: (साइट चुनें:)"
  },
  "साइट चुनें:": {
    "en": "Select Site:",
    "hi": "साइट चुनें:",
    "bi": "Select Site: (साइट चुनें:)"
  },
  "select site: (साइट चुनें:)": {
    "en": "Select Site:",
    "hi": "साइट चुनें:",
    "bi": "Select Site: (साइट चुनें:)"
  },
  "select date": {
    "en": "Select Date",
    "hi": "तारीख चुनें",
    "bi": "Select Date (तारीख चुनें)"
  },
  "तारीख चुनें": {
    "en": "Select Date",
    "hi": "तारीख चुनें",
    "bi": "Select Date (तारीख चुनें)"
  },
  "select date (तारीख चुनें)": {
    "en": "Select Date",
    "hi": "तारीख चुनें",
    "bi": "Select Date (तारीख चुनें)"
  },
  "search material": {
    "en": "Search Material",
    "hi": "सामान खोजें",
    "bi": "Search Material (सामान खोजें)"
  },
  "सामान खोजें": {
    "en": "Search Material",
    "hi": "सामान खोजें",
    "bi": "Search Material (सामान खोजें)"
  },
  "search material (सामान खोजें)": {
    "en": "Search Material",
    "hi": "सामान खोजें",
    "bi": "Search Material (सामान खोजें)"
  },
  "pdf डाउनलोड": {
    "en": "Download PDF",
    "hi": "PDF डाउनलोड",
    "bi": "Download PDF (PDF डाउनलोड)"
  },
  "प्रिंट करें": {
    "en": "Print",
    "hi": "प्रिंट करें",
    "bi": "Print (प्रिंट करें)"
  },
  "print (प्रिंट करें)": {
    "en": "Print",
    "hi": "प्रिंट करें",
    "bi": "Print (प्रिंट करें)"
  },
  "attendance sheet": {
    "en": "Attendance Sheet",
    "hi": "हाजिरी शीट",
    "bi": "Attendance Sheet (हाजिरी शीट)"
  },
  "हाजिरी शीट": {
    "en": "Attendance Sheet",
    "hi": "हाजिरी शीट",
    "bi": "Attendance Sheet (हाजिरी शीट)"
  },
  "attendance sheet (हाजिरी शीट)": {
    "en": "Attendance Sheet",
    "hi": "हाजिरी शीट",
    "bi": "Attendance Sheet (हाजिरी शीट)"
  },
  "फोटो अपलोड": {
    "en": "Upload Photos",
    "hi": "फोटो अपलोड",
    "bi": "Upload Photos (फोटो अपलोड)"
  },
  "upload photos (फोटो अपलोड)": {
    "en": "Upload Photos",
    "hi": "फोटो अपलोड",
    "bi": "Upload Photos (फोटो अपलोड)"
  },
  "supervisor": {
    "en": "Supervisor",
    "hi": "सुपरवाइज़र",
    "bi": "Supervisor (सुपरवाइज़र)"
  },
  "सुपरवाइज़र": {
    "en": "Supervisor",
    "hi": "सुपरवाइज़र",
    "bi": "Supervisor (सुपरवाइज़र)"
  },
  "supervisor (सुपरवाइज़र)": {
    "en": "Supervisor",
    "hi": "सुपरवाइज़र",
    "bi": "Supervisor (सुपरवाइज़र)"
  },
  "site stock": {
    "en": "Site Stock",
    "hi": "साइट स्टॉक",
    "bi": "Site Stock (साइट स्टॉक)"
  },
  "साइट स्टॉक": {
    "en": "Site Stock",
    "hi": "साइट स्टॉक",
    "bi": "Site Stock (साइट स्टॉक)"
  },
  "site stock (साइट स्टॉक)": {
    "en": "Site Stock",
    "hi": "साइट स्टॉक",
    "bi": "Site Stock (साइट स्टॉक)"
  },
  "dpr progress": {
    "en": "DPR Progress",
    "hi": "DPR प्रगति",
    "bi": "DPR Progress (DPR प्रगति)"
  },
  "dpr प्रगति": {
    "en": "DPR Progress",
    "hi": "DPR प्रगति",
    "bi": "DPR Progress (DPR प्रगति)"
  },
  "dpr progress (dpr प्रगति)": {
    "en": "DPR Progress",
    "hi": "DPR प्रगति",
    "bi": "DPR Progress (DPR प्रगति)"
  },
  "photo album": {
    "en": "Photo Album",
    "hi": "फोटो एल्बम",
    "bi": "Photo Album (फोटो एल्बम)"
  },
  "फोटो एल्बम": {
    "en": "Photo Album",
    "hi": "फोटो एल्बम",
    "bi": "Photo Album (फोटो एल्बम)"
  },
  "photo album (फोटो एल्बम)": {
    "en": "Photo Album",
    "hi": "फोटो एल्बम",
    "bi": "Photo Album (फोटो एल्बम)"
  },
  "change language": {
    "en": "Change Language",
    "hi": "भाषा बदलें",
    "bi": "Change Language (भाषा बदलें)"
  },
  "भाषा बदलें": {
    "en": "Change Language",
    "hi": "भाषा बदलें",
    "bi": "Change Language (भाषा बदलें)"
  },
  "change language (भाषा बदलें)": {
    "en": "Change Language",
    "hi": "भाषा बदलें",
    "bi": "Change Language (भाषा बदलें)"
  },
  "total attendance": {
    "en": "Total Attendance",
    "hi": "कुल हाजिरी",
    "bi": "Total Attendance (कुल हाजिरी)"
  },
  "कुल हाजिरी": {
    "en": "Total Attendance",
    "hi": "कुल हाजिरी",
    "bi": "Total Attendance (कुल हाजिरी)"
  },
  "total attendance (कुल हाजिरी)": {
    "en": "Total Attendance",
    "hi": "कुल हाजिरी",
    "bi": "Total Attendance (कुल हाजिरी)"
  },
  "work hours": {
    "en": "Work Hours",
    "hi": "कार्य घंटे",
    "bi": "Work Hours (कार्य घंटे)"
  },
  "कार्य घंटे": {
    "en": "Work Hours",
    "hi": "कार्य घंटे",
    "bi": "Work Hours (कार्य घंटे)"
  },
  "work hours (कार्य घंटे)": {
    "en": "Work Hours",
    "hi": "कार्य घंटे",
    "bi": "Work Hours (कार्य घंटे)"
  },
  "view ledger": {
    "en": "View Ledger",
    "hi": "लेजर देखें",
    "bi": "View Ledger (लेजर देखें)"
  },
  "लेजर देखें": {
    "en": "View Ledger",
    "hi": "लेजर देखें",
    "bi": "View Ledger (लेजर देखें)"
  },
  "view ledger (लेजर देखें)": {
    "en": "View Ledger",
    "hi": "लेजर देखें",
    "bi": "View Ledger (लेजर देखें)"
  },
  "update": {
    "en": "Update",
    "hi": "अपडेट करें",
    "bi": "Update (अपडेट करें)"
  },
  "अपडेट करें": {
    "en": "Update",
    "hi": "अपडेट करें",
    "bi": "Update (अपडेट करें)"
  },
  "update (अपडेट करें)": {
    "en": "Update",
    "hi": "अपडेट करें",
    "bi": "Update (अपडेट करें)"
  },
  "login": {
    "en": "Login",
    "hi": "लॉगिन करें",
    "bi": "Login (लॉगिन करें)"
  },
  "login (लॉगिन करें)": {
    "en": "Login",
    "hi": "लॉगिन करें",
    "bi": "Login (लॉगिन करें)"
  },
  "सुपरवाइजर": {
    "en": "Supervisor",
    "hi": "सुपरवाइजर",
    "bi": "Supervisor (सुपरवाइजर)"
  },
  "supervisor (सुपरवाइजर)": {
    "en": "Supervisor",
    "hi": "सुपरवाइजर",
    "bi": "Supervisor (सुपरवाइजर)"
  },
  "stock inward": {
    "en": "Stock Inward",
    "hi": "स्टॉक आवक",
    "bi": "Stock Inward (स्टॉक आवक)"
  },
  "स्टॉक आवक": {
    "en": "Stock Inward",
    "hi": "स्टॉक आवक",
    "bi": "Stock Inward (स्टॉक आवक)"
  },
  "stock inward (स्टॉक आवक)": {
    "en": "Stock Inward",
    "hi": "स्टॉक आवक",
    "bi": "Stock Inward (स्टॉक आवक)"
  },
  "remaining stock": {
    "en": "Remaining Stock",
    "hi": "शेष स्टॉक",
    "bi": "Remaining Stock (शेष स्टॉक)"
  },
  "शेष स्टॉक": {
    "en": "Remaining Stock",
    "hi": "शेष स्टॉक",
    "bi": "Remaining Stock (शेष स्टॉक)"
  },
  "remaining stock (शेष स्टॉक)": {
    "en": "Remaining Stock",
    "hi": "शेष स्टॉक",
    "bi": "Remaining Stock (शेष स्टॉक)"
  },
  "दर्ज करें": {
    "en": "Submit",
    "hi": "दर्ज करें",
    "bi": "Submit (दर्ज करें)"
  },
  "submit (दर्ज करें)": {
    "en": "Submit",
    "hi": "दर्ज करें",
    "bi": "Submit (दर्ज करें)"
  },
  "auto-generated": {
    "en": "Auto-Generated",
    "hi": "ऑटोमैटिक",
    "bi": "Auto-Generated (ऑटोमैटिक)"
  },
  "ऑटोमैटिक": {
    "en": "Auto-Generated",
    "hi": "ऑटोमैटिक",
    "bi": "Auto-Generated (ऑटोमैटिक)"
  },
  "auto-generated (ऑटोमैटिक)": {
    "en": "Auto-Generated",
    "hi": "ऑटोमैटिक",
    "bi": "Auto-Generated (ऑटोमैटिक)"
  },
  "mason": {
    "en": "Mason",
    "hi": "मिस्त्री",
    "bi": "Mason (मिस्त्री)"
  },
  "available %": {
    "en": "Available %",
    "hi": "उपलब्ध %",
    "bi": "Available % (उपलब्ध %)"
  },
  "उपलब्ध %": {
    "en": "Available %",
    "hi": "उपलब्ध %",
    "bi": "Available % (उपलब्ध %)"
  },
  "available % (उपलब्ध %)": {
    "en": "Available %",
    "hi": "उपलब्ध %",
    "bi": "Available % (उपलब्ध %)"
  },
  "healthy": {
    "en": "Healthy",
    "hi": "पर्याप्त",
    "bi": "Healthy (पर्याप्त)"
  },
  "पर्याप्त": {
    "en": "Healthy",
    "hi": "पर्याप्त",
    "bi": "Healthy (पर्याप्त)"
  },
  "healthy (पर्याप्त)": {
    "en": "Healthy",
    "hi": "पर्याप्त",
    "bi": "Healthy (पर्याप्त)"
  },
  "low stock": {
    "en": "Low Stock",
    "hi": "कम स्टॉक",
    "bi": "Low Stock (कम स्टॉक)"
  },
  "कम स्टॉक": {
    "en": "Low Stock",
    "hi": "कम स्टॉक",
    "bi": "Low Stock (कम स्टॉक)"
  },
  "low stock (कम स्टॉक)": {
    "en": "Low Stock",
    "hi": "कम स्टॉक",
    "bi": "Low Stock (कम स्टॉक)"
  },
  "total amount": {
    "en": "Total Amount",
    "hi": "कुल राशि",
    "bi": "Total Amount (कुल राशि)"
  },
  "कुल राशि": {
    "en": "Total Amount",
    "hi": "कुल राशि",
    "bi": "Total Amount (कुल राशि)"
  },
  "total amount (कुल राशि)": {
    "en": "Total Amount",
    "hi": "कुल राशि",
    "bi": "Total Amount (कुल राशि)"
  },
  "search...": {
    "en": "Search...",
    "hi": "खोजें...",
    "bi": "Search... (खोजें...)"
  },
  "खोजें...": {
    "en": "Search...",
    "hi": "खोजें...",
    "bi": "Search... (खोजें...)"
  },
  "search... (खोजें...)": {
    "en": "Search...",
    "hi": "खोजें...",
    "bi": "Search... (खोजें...)"
  },
  "purpose": {
    "en": "Purpose",
    "hi": "उद्देश्य",
    "bi": "Purpose (उद्देश्य)"
  },
  "उद्देश्य": {
    "en": "Purpose",
    "hi": "उद्देश्य",
    "bi": "Purpose (उद्देश्य)"
  },
  "purpose (उद्देश्य)": {
    "en": "Purpose",
    "hi": "उद्देश्य",
    "bi": "Purpose (उद्देश्य)"
  },
  "saved": {
    "en": "Saved",
    "hi": "सुरक्षित",
    "bi": "Saved (सुरक्षित)"
  },
  "सुरक्षित": {
    "en": "Saved",
    "hi": "सुरक्षित",
    "bi": "Saved (सुरक्षित)"
  },
  "saved (सुरक्षित)": {
    "en": "Saved",
    "hi": "सुरक्षित",
    "bi": "Saved (सुरक्षित)"
  },
  "🏢 office work": {
    "en": "🏢 Office Work",
    "hi": "🏢 ऑफिस वर्क",
    "bi": "🏢 Office Work (🏢 ऑफिस वर्क)"
  },
  "🏢 ऑफिस वर्क": {
    "en": "🏢 Office Work",
    "hi": "🏢 ऑफिस वर्क",
    "bi": "🏢 Office Work (🏢 ऑफिस वर्क)"
  },
  "🏢 office work (🏢 ऑफिस वर्क)": {
    "en": "🏢 Office Work",
    "hi": "🏢 ऑफिस वर्क",
    "bi": "🏢 Office Work (🏢 ऑफिस वर्क)"
  },
  "on-site": {
    "en": "On-Site",
    "hi": "ऑन-साइट",
    "bi": "On-Site (ऑन-साइट)"
  },
  "ऑन-साइट": {
    "en": "On-Site",
    "hi": "ऑन-साइट",
    "bi": "On-Site (ऑन-साइट)"
  },
  "on-site (ऑन-साइट)": {
    "en": "On-Site",
    "hi": "ऑन-साइट",
    "bi": "On-Site (ऑन-साइट)"
  },
  "off-site": {
    "en": "Off-Site",
    "hi": "ऑफ-साइट",
    "bi": "Off-Site (ऑफ-साइट)"
  },
  "ऑफ-साइट": {
    "en": "Off-Site",
    "hi": "ऑफ-साइट",
    "bi": "Off-Site (ऑफ-साइट)"
  },
  "off-site (ऑफ-साइट)": {
    "en": "Off-Site",
    "hi": "ऑफ-साइट",
    "bi": "Off-Site (ऑफ-साइट)"
  },
  "check-out": {
    "en": "Check-Out",
    "hi": "चेक-आउट",
    "bi": "Check-Out (चेक-आउट)"
  },
  "चेक-आउट": {
    "en": "Check-Out",
    "hi": "चेक-आउट",
    "bi": "Check-Out (चेक-आउट)"
  },
  "check-out (चेक-आउट)": {
    "en": "Check-Out",
    "hi": "चेक-आउट",
    "bi": "Check-Out (चेक-आउट)"
  },
  "water tower": {
    "en": "Water Tower",
    "hi": "जलमीनार",
    "bi": "Water Tower (जलमीनार)"
  },
  "जलमीनार": {
    "en": "Water Tower",
    "hi": "जलमीनार",
    "bi": "Water Tower (जलमीनार)"
  },
  "water tower (जलमीनार)": {
    "en": "Water Tower",
    "hi": "जलमीनार",
    "bi": "Water Tower (जलमीनार)"
  },
  "hydro testing": {
    "en": "Hydro Testing",
    "hi": "परीक्षण",
    "bi": "Hydro Testing (परीक्षण)"
  },
  "परीक्षण": {
    "en": "Hydro Testing",
    "hi": "परीक्षण",
    "bi": "Hydro Testing (परीक्षण)"
  },
  "hydro testing (परीक्षण)": {
    "en": "Hydro Testing",
    "hi": "परीक्षण",
    "bi": "Hydro Testing (परीक्षण)"
  },
  "दिनांक:": {
    "en": "Date:",
    "hi": "दिनांक:",
    "bi": "Date: (दिनांक:)"
  },
  "date: (दिनांक:)": {
    "en": "Date:",
    "hi": "दिनांक:",
    "bi": "Date: (दिनांक:)"
  },
  "quantity:": {
    "en": "Quantity:",
    "hi": "मात्रा:",
    "bi": "Quantity: (मात्रा:)"
  },
  "मात्रा:": {
    "en": "Quantity:",
    "hi": "मात्रा:",
    "bi": "Quantity: (मात्रा:)"
  },
  "quantity: (मात्रा:)": {
    "en": "Quantity:",
    "hi": "मात्रा:",
    "bi": "Quantity: (मात्रा:)"
  },
  "total (₹)": {
    "en": "Total (₹)",
    "hi": "कुल (₹)",
    "bi": "Total (₹) (कुल (₹))"
  },
  "कुल (₹)": {
    "en": "Total (₹)",
    "hi": "कुल (₹)",
    "bi": "Total (₹) (कुल (₹))"
  },
  "total (₹) (कुल (₹))": {
    "en": "Total (₹)",
    "hi": "कुल (₹)",
    "bi": "Total (₹) (कुल (₹))"
  },
  "फ़िल्टर": {
    "en": "Filter",
    "hi": "फ़िल्टर",
    "bi": "Filter (फ़िल्टर)"
  },
  "filter (फ़िल्टर)": {
    "en": "Filter",
    "hi": "फ़िल्टर",
    "bi": "Filter (फ़िल्टर)"
  },
  "download": {
    "en": "Download",
    "hi": "डाउनलोड",
    "bi": "Download (डाउनलोड)"
  },
  "डाउनलोड": {
    "en": "Download",
    "hi": "डाउनलोड",
    "bi": "Download (डाउनलोड)"
  },
  "download (डाउनलोड)": {
    "en": "Download",
    "hi": "डाउनलोड",
    "bi": "Download (डाउनलोड)"
  },
  "मटेरियल": {
    "en": "Material",
    "hi": "मटेरियल",
    "bi": "Material (मटेरियल)"
  },
  "material (मटेरियल)": {
    "en": "Material",
    "hi": "मटेरियल",
    "bi": "Material (मटेरियल)"
  },
  "report": {
    "en": "Report",
    "hi": "रिपोर्ट",
    "bi": "Report (रिपोर्ट)"
  },
  "रिपोर्ट": {
    "en": "Report",
    "hi": "रिपोर्ट",
    "bi": "Report (रिपोर्ट)"
  },
  "report (रिपोर्ट)": {
    "en": "Report",
    "hi": "रिपोर्ट",
    "bi": "Report (रिपोर्ट)"
  },
  "register": {
    "en": "Register",
    "hi": "रजिस्टर",
    "bi": "Register (रजिस्टर)"
  },
  "रजिस्टर": {
    "en": "Register",
    "hi": "रजिस्टर",
    "bi": "Register (रजिस्टर)"
  },
  "register (रजिस्टर)": {
    "en": "Register",
    "hi": "रजिस्टर",
    "bi": "Register (रजिस्टर)"
  },
  "entries": {
    "en": "Entries",
    "hi": "एंट्रीज",
    "bi": "Entries (एंट्रीज)"
  },
  "एंट्रीज": {
    "en": "Entries",
    "hi": "एंट्रीज",
    "bi": "Entries (एंट्रीज)"
  },
  "entries (एंट्रीज)": {
    "en": "Entries",
    "hi": "एंट्रीज",
    "bi": "Entries (एंट्रीज)"
  },
  "संपादित": {
    "en": "Edit",
    "hi": "संपादित",
    "bi": "Edit (संपादित)"
  },
  "edit (संपादित)": {
    "en": "Edit",
    "hi": "संपादित",
    "bi": "Edit (संपादित)"
  },
  "incharge": {
    "en": "Incharge",
    "hi": "इनचार्ज",
    "bi": "Incharge (इनचार्ज)"
  },
  "इनचार्ज": {
    "en": "Incharge",
    "hi": "इनचार्ज",
    "bi": "Incharge (इनचार्ज)"
  },
  "incharge (इनचार्ज)": {
    "en": "Incharge",
    "hi": "इनचार्ज",
    "bi": "Incharge (इनचार्ज)"
  },
  "logout (लॉगआउट)": {
    "en": "Logout",
    "hi": "लॉगआउट",
    "bi": "Logout (लॉगआउट)"
  },
  "check-in": {
    "en": "Check-In",
    "hi": "चेक-इन",
    "bi": "Check-In (चेक-इन)"
  },
  "चेक-इन": {
    "en": "Check-In",
    "hi": "चेक-इन",
    "bi": "Check-In (चेक-इन)"
  },
  "check-in (चेक-इन)": {
    "en": "Check-In",
    "hi": "चेक-इन",
    "bi": "Check-In (चेक-इन)"
  },
  "balance": {
    "en": "Balance",
    "hi": "बैलेंस",
    "bi": "Balance (बैलेंस)"
  },
  "बैलेंस": {
    "en": "Balance",
    "hi": "बैलेंस",
    "bi": "Balance (बैलेंस)"
  },
  "balance (बैलेंस)": {
    "en": "Balance",
    "hi": "बैलेंस",
    "bi": "Balance (बैलेंस)"
  },
  "target": {
    "en": "Target",
    "hi": "लक्ष्य",
    "bi": "Target (लक्ष्य)"
  },
  "लक्ष्य": {
    "en": "Target",
    "hi": "लक्ष्य",
    "bi": "Target (लक्ष्य)"
  },
  "target (लक्ष्य)": {
    "en": "Target",
    "hi": "लक्ष्य",
    "bi": "Target (लक्ष्य)"
  },
  "category": {
    "en": "Category",
    "hi": "श्रेणी",
    "bi": "Category (श्रेणी)"
  },
  "श्रेणी": {
    "en": "Category",
    "hi": "श्रेणी",
    "bi": "Category (श्रेणी)"
  },
  "category (श्रेणी)": {
    "en": "Category",
    "hi": "श्रेणी",
    "bi": "Category (श्रेणी)"
  },
  "rate (₹)": {
    "en": "Rate (₹)",
    "hi": "दर (₹)",
    "bi": "Rate (₹) (दर (₹))"
  },
  "दर (₹)": {
    "en": "Rate (₹)",
    "hi": "दर (₹)",
    "bi": "Rate (₹) (दर (₹))"
  },
  "rate (₹) (दर (₹))": {
    "en": "Rate (₹)",
    "hi": "दर (₹)",
    "bi": "Rate (₹) (दर (₹))"
  },
  "sites": {
    "en": "Sites",
    "hi": "साइट्स",
    "bi": "Sites (साइट्स)"
  },
  "साइट्स": {
    "en": "Sites",
    "hi": "साइट्स",
    "bi": "Sites (साइट्स)"
  },
  "sites (साइट्स)": {
    "en": "Sites",
    "hi": "साइट्स",
    "bi": "Sites (साइट्स)"
  },
  "प्रिंट": {
    "en": "Print",
    "hi": "प्रिंट",
    "bi": "Print (प्रिंट)"
  },
  "print (प्रिंट)": {
    "en": "Print",
    "hi": "प्रिंट",
    "bi": "Print (प्रिंट)"
  },
  "online": {
    "en": "Online",
    "hi": "ऑनलाइन",
    "bi": "Online (ऑनलाइन)"
  },
  "ऑनलाइन": {
    "en": "Online",
    "hi": "ऑनलाइन",
    "bi": "Online (ऑनलाइन)"
  },
  "online (ऑनलाइन)": {
    "en": "Online",
    "hi": "ऑनलाइन",
    "bi": "Online (ऑनलाइन)"
  },
  "offline": {
    "en": "Offline",
    "hi": "ऑफलाइन",
    "bi": "Offline (ऑफलाइन)"
  },
  "ऑफलाइन": {
    "en": "Offline",
    "hi": "ऑफलाइन",
    "bi": "Offline (ऑफलाइन)"
  },
  "offline (ऑफलाइन)": {
    "en": "Offline",
    "hi": "ऑफलाइन",
    "bi": "Offline (ऑफलाइन)"
  },
  "monthly": {
    "en": "Monthly",
    "hi": "माहवार",
    "bi": "Monthly (माहवार)"
  },
  "माहवार": {
    "en": "Monthly",
    "hi": "माहवार",
    "bi": "Monthly (माहवार)"
  },
  "monthly (माहवार)": {
    "en": "Monthly",
    "hi": "माहवार",
    "bi": "Monthly (माहवार)"
  },
  "available": {
    "en": "Available",
    "hi": "उपलब्ध",
    "bi": "Available (उपलब्ध)"
  },
  "उपलब्ध": {
    "en": "Available",
    "hi": "उपलब्ध",
    "bi": "Available (उपलब्ध)"
  },
  "available (उपलब्ध)": {
    "en": "Available",
    "hi": "उपलब्ध",
    "bi": "Available (उपलब्ध)"
  },
  "entry": {
    "en": "Entry",
    "hi": "एंट्री",
    "bi": "Entry (एंट्री)"
  },
  "एंट्री": {
    "en": "Entry",
    "hi": "एंट्री",
    "bi": "Entry (एंट्री)"
  },
  "entry (एंट्री)": {
    "en": "Entry",
    "hi": "एंट्री",
    "bi": "Entry (एंट्री)"
  },
  "add": {
    "en": "Add",
    "hi": "जोड़ें",
    "bi": "Add (जोड़ें)"
  },
  "जोड़ें": {
    "en": "Add",
    "hi": "जोड़ें",
    "bi": "Add (जोड़ें)"
  },
  "add (जोड़ें)": {
    "en": "Add",
    "hi": "जोड़ें",
    "bi": "Add (जोड़ें)"
  },
  "owner": {
    "en": "Owner",
    "hi": "मालिक",
    "bi": "Owner (मालिक)"
  },
  "मालिक": {
    "en": "Owner",
    "hi": "मालिक",
    "bi": "Owner (मालिक)"
  },
  "owner (मालिक)": {
    "en": "Owner",
    "hi": "मालिक",
    "bi": "Owner (मालिक)"
  },
  "description": {
    "en": "Description",
    "hi": "विवरण",
    "bi": "Description (विवरण)"
  },
  "विवरण": {
    "en": "Description",
    "hi": "विवरण",
    "bi": "Description (विवरण)"
  },
  "description (विवरण)": {
    "en": "Description",
    "hi": "विवरण",
    "bi": "Description (विवरण)"
  },
  "एक्शन": {
    "en": "Actions",
    "hi": "एक्शन",
    "bi": "Actions (एक्शन)"
  },
  "actions (एक्शन)": {
    "en": "Actions",
    "hi": "एक्शन",
    "bi": "Actions (एक्शन)"
  },
  "search": {
    "en": "Search",
    "hi": "खोजें",
    "bi": "Search (खोजें)"
  },
  "खोजें": {
    "en": "Search",
    "hi": "खोजें",
    "bi": "Search (खोजें)"
  },
  "search (खोजें)": {
    "en": "Search",
    "hi": "खोजें",
    "bi": "Search (खोजें)"
  },
  "daily": {
    "en": "Daily",
    "hi": "दैनिक",
    "bi": "Daily (दैनिक)"
  },
  "दैनिक": {
    "en": "Daily",
    "hi": "दैनिक",
    "bi": "Daily (दैनिक)"
  },
  "daily (दैनिक)": {
    "en": "Daily",
    "hi": "दैनिक",
    "bi": "Daily (दैनिक)"
  },
  "मासिक": {
    "en": "Monthly",
    "hi": "मासिक",
    "bi": "Monthly (मासिक)"
  },
  "monthly (मासिक)": {
    "en": "Monthly",
    "hi": "मासिक",
    "bi": "Monthly (मासिक)"
  },
  "logs": {
    "en": "Logs",
    "hi": "लॉग्स",
    "bi": "Logs (लॉग्स)"
  },
  "लॉग्स": {
    "en": "Logs",
    "hi": "लॉग्स",
    "bi": "Logs (लॉग्स)"
  },
  "logs (लॉग्स)": {
    "en": "Logs",
    "hi": "लॉग्स",
    "bi": "Logs (लॉग्स)"
  },
  "secs": {
    "en": "Secs",
    "hi": "सेकंड",
    "bi": "Secs (सेकंड)"
  },
  "सेकंड": {
    "en": "Secs",
    "hi": "सेकंड",
    "bi": "Secs (सेकंड)"
  },
  "secs (सेकंड)": {
    "en": "Secs",
    "hi": "सेकंड",
    "bi": "Secs (सेकंड)"
  },
  "album": {
    "en": "Album",
    "hi": "एल्बम",
    "bi": "Album (एल्बम)"
  },
  "एल्बम": {
    "en": "Album",
    "hi": "एल्बम",
    "bi": "Album (एल्बम)"
  },
  "album (एल्बम)": {
    "en": "Album",
    "hi": "एल्बम",
    "bi": "Album (एल्बम)"
  },
  "open": {
    "en": "Open",
    "hi": "खोलें",
    "bi": "Open (खोलें)"
  },
  "खोलें": {
    "en": "Open",
    "hi": "खोलें",
    "bi": "Open (खोलें)"
  },
  "open (खोलें)": {
    "en": "Open",
    "hi": "खोलें",
    "bi": "Open (खोलें)"
  },
  "view": {
    "en": "View",
    "hi": "देखें",
    "bi": "View (देखें)"
  },
  "देखें": {
    "en": "View",
    "hi": "देखें",
    "bi": "View (देखें)"
  },
  "view (देखें)": {
    "en": "View",
    "hi": "देखें",
    "bi": "View (देखें)"
  },
  "worker": {
    "en": "Worker",
    "hi": "वर्कर",
    "bi": "Worker (वर्कर)"
  },
  "वर्कर": {
    "en": "Worker",
    "hi": "वर्कर",
    "bi": "Worker (वर्कर)"
  },
  "worker (वर्कर)": {
    "en": "Worker",
    "hi": "वर्कर",
    "bi": "Worker (वर्कर)"
  },
  "staff": {
    "en": "Staff",
    "hi": "स्टाफ",
    "bi": "Staff (स्टाफ)"
  },
  "स्टाफ": {
    "en": "Staff",
    "hi": "स्टाफ",
    "bi": "Staff (स्टाफ)"
  },
  "staff (स्टाफ)": {
    "en": "Staff",
    "hi": "स्टाफ",
    "bi": "Staff (स्टाफ)"
  },
  "photos": {
    "en": "Photos",
    "hi": "फोटो",
    "bi": "Photos (फोटो)"
  },
  "फोटो": {
    "en": "Photos",
    "hi": "फोटो",
    "bi": "Photos (फोटो)"
  },
  "photos (फोटो)": {
    "en": "Photos",
    "hi": "फोटो",
    "bi": "Photos (फोटो)"
  },
  "ledger": {
    "en": "Ledger",
    "hi": "लेजर",
    "bi": "Ledger (लेजर)"
  },
  "लेजर": {
    "en": "Ledger",
    "hi": "लेजर",
    "bi": "Ledger (लेजर)"
  },
  "ledger (लेजर)": {
    "en": "Ledger",
    "hi": "लेजर",
    "bi": "Ledger (लेजर)"
  },
  "total:": {
    "en": "Total:",
    "hi": "कुल:",
    "bi": "Total: (कुल:)"
  },
  "कुल:": {
    "en": "Total:",
    "hi": "कुल:",
    "bi": "Total: (कुल:)"
  },
  "total: (कुल:)": {
    "en": "Total:",
    "hi": "कुल:",
    "bi": "Total: (कुल:)"
  },
  "more": {
    "en": "More",
    "hi": "अधिक",
    "bi": "More (अधिक)"
  },
  "अधिक": {
    "en": "More",
    "hi": "अधिक",
    "bi": "More (अधिक)"
  },
  "more (अधिक)": {
    "en": "More",
    "hi": "अधिक",
    "bi": "More (अधिक)"
  },
  "deo": {
    "en": "DEO",
    "hi": "डीईओ",
    "bi": "DEO (डीईओ)"
  },
  "डीईओ": {
    "en": "DEO",
    "hi": "डीईओ",
    "bi": "DEO (डीईओ)"
  },
  "deo (डीईओ)": {
    "en": "DEO",
    "hi": "डीईओ",
    "bi": "DEO (डीईओ)"
  },
  "other": {
    "en": "Other",
    "hi": "अन्य",
    "bi": "Other (अन्य)"
  },
  "अन्य": {
    "en": "Other",
    "hi": "अन्य",
    "bi": "Other (अन्य)"
  },
  "other (अन्य)": {
    "en": "Other",
    "hi": "अन्य",
    "bi": "Other (अन्य)"
  },
  "out of stock": {
    "en": "Out of Stock",
    "hi": "खत्म",
    "bi": "Out of Stock (खत्म)"
  },
  "खत्म": {
    "en": "Out of Stock",
    "hi": "खत्म",
    "bi": "Out of Stock (खत्म)"
  },
  "out of stock (खत्म)": {
    "en": "Out of Stock",
    "hi": "खत्म",
    "bi": "Out of Stock (खत्म)"
  },
  "पंजी": {
    "en": "Register",
    "hi": "पंजी",
    "bi": "Register (पंजी)"
  },
  "register (पंजी)": {
    "en": "Register",
    "hi": "पंजी",
    "bi": "Register (पंजी)"
  },
  "directory": {
    "en": "Directory",
    "hi": "सूची",
    "bi": "Directory (सूची)"
  },
  "सूची": {
    "en": "Directory",
    "hi": "सूची",
    "bi": "Directory (सूची)"
  },
  "directory (सूची)": {
    "en": "Directory",
    "hi": "सूची",
    "bi": "Directory (सूची)"
  },
  "hours": {
    "en": "Hours",
    "hi": "घंटे",
    "bi": "Hours (घंटे)"
  },
  "घंटे": {
    "en": "Hours",
    "hi": "घंटे",
    "bi": "Hours (घंटे)"
  },
  "hours (घंटे)": {
    "en": "Hours",
    "hi": "घंटे",
    "bi": "Hours (घंटे)"
  },
  "mins": {
    "en": "Mins",
    "hi": "मिनट",
    "bi": "Mins (मिनट)"
  },
  "मिनट": {
    "en": "Mins",
    "hi": "मिनट",
    "bi": "Mins (मिनट)"
  },
  "mins (मिनट)": {
    "en": "Mins",
    "hi": "मिनट",
    "bi": "Mins (मिनट)"
  },
  "रद्द": {
    "en": "Cancel",
    "hi": "रद्द",
    "bi": "Cancel (रद्द)"
  },
  "cancel (रद्द)": {
    "en": "Cancel",
    "hi": "रद्द",
    "bi": "Cancel (रद्द)"
  },
  "एडिट": {
    "en": "Edit",
    "hi": "एडिट",
    "bi": "Edit (एडिट)"
  },
  "edit (एडिट)": {
    "en": "Edit",
    "hi": "एडिट",
    "bi": "Edit (एडिट)"
  },
  "inward": {
    "en": "Inward",
    "hi": "आवक",
    "bi": "Inward (आवक)"
  },
  "आवक": {
    "en": "Inward",
    "hi": "आवक",
    "bi": "Inward (आवक)"
  },
  "inward (आवक)": {
    "en": "Inward",
    "hi": "आवक",
    "bi": "Inward (आवक)"
  },
  "consumed": {
    "en": "Consumed",
    "hi": "खपत",
    "bi": "Consumed (खपत)"
  },
  "consumed (खपत)": {
    "en": "Consumed",
    "hi": "खपत",
    "bi": "Consumed (खपत)"
  },
  "rate:": {
    "en": "Rate:",
    "hi": "दर:",
    "bi": "Rate: (दर:)"
  },
  "दर:": {
    "en": "Rate:",
    "hi": "दर:",
    "bi": "Rate: (दर:)"
  },
  "rate: (दर:)": {
    "en": "Rate:",
    "hi": "दर:",
    "bi": "Rate: (दर:)"
  },
  "name": {
    "en": "Name",
    "hi": "नाम",
    "bi": "Name (नाम)"
  },
  "नाम": {
    "en": "Name",
    "hi": "नाम",
    "bi": "Name (नाम)"
  },
  "name (नाम)": {
    "en": "Name",
    "hi": "नाम",
    "bi": "Name (नाम)"
  },
  "code": {
    "en": "Code",
    "hi": "कोड",
    "bi": "Code (कोड)"
  },
  "कोड": {
    "en": "Code",
    "hi": "कोड",
    "bi": "Code (कोड)"
  },
  "code (कोड)": {
    "en": "Code",
    "hi": "कोड",
    "bi": "Code (कोड)"
  },
  "log": {
    "en": "Log",
    "hi": "लॉग",
    "bi": "Log (लॉग)"
  },
  "लॉग": {
    "en": "Log",
    "hi": "लॉग",
    "bi": "Log (लॉग)"
  },
  "log (लॉग)": {
    "en": "Log",
    "hi": "लॉग",
    "bi": "Log (लॉग)"
  },
  "सेव": {
    "en": "Save",
    "hi": "सेव",
    "bi": "Save (सेव)"
  },
  "save (सेव)": {
    "en": "Save",
    "hi": "सेव",
    "bi": "Save (सेव)"
  },
  "ओपन": {
    "en": "Open",
    "hi": "ओपन",
    "bi": "Open (ओपन)"
  },
  "open (ओपन)": {
    "en": "Open",
    "hi": "ओपन",
    "bi": "Open (ओपन)"
  },
  "new": {
    "en": "New",
    "hi": "नया",
    "bi": "New (नया)"
  },
  "नया": {
    "en": "New",
    "hi": "नया",
    "bi": "New (नया)"
  },
  "new (नया)": {
    "en": "New",
    "hi": "नया",
    "bi": "New (नया)"
  },
  "(कारीगरों के नाम)": {
    "en": "(Workers' Names)",
    "hi": "(कारीगरों के नाम)",
    "bi": "Workers' Names (कारीगरों के नाम)"
  },
  "(workers' names)": {
    "en": "(Workers' Names)",
    "hi": "(कारीगरों के नाम)",
    "bi": "Workers' Names (कारीगरों के नाम)"
  },
  "workers' names (कारीगरों के नाम)": {
    "en": "(Workers' Names)",
    "hi": "(कारीगरों के नाम)",
    "bi": "Workers' Names (कारीगरों के नाम)"
  },
  "(कार्य क्षेत्र)": {
    "en": "(Work Area)",
    "hi": "(कार्य क्षेत्र)",
    "bi": "Work Area (कार्य क्षेत्र)"
  },
  "(work area)": {
    "en": "(Work Area)",
    "hi": "(कार्य क्षेत्र)",
    "bi": "Work Area (कार्य क्षेत्र)"
  },
  "work area (कार्य क्षेत्र)": {
    "en": "(Work Area)",
    "hi": "(कार्य क्षेत्र)",
    "bi": "Work Area (कार्य क्षेत्र)"
  },
  "(कार्य गतिविधि)": {
    "en": "(Work Activity)",
    "hi": "(कार्य गतिविधि)",
    "bi": "Work Activity (कार्य गतिविधि)"
  },
  "(work activity)": {
    "en": "(Work Activity)",
    "hi": "(कार्य गतिविधि)",
    "bi": "Work Activity (कार्य गतिविधि)"
  },
  "work activity (कार्य गतिविधि)": {
    "en": "(Work Activity)",
    "hi": "(कार्य गतिविधि)",
    "bi": "Work Activity (कार्य गतिविधि)"
  },
  "(वार्ड नंबर)": {
    "en": "(Ward No.)",
    "hi": "(वार्ड नंबर)",
    "bi": "Ward No. (वार्ड नंबर)"
  },
  "(ward no.)": {
    "en": "(Ward No.)",
    "hi": "(वार्ड नंबर)",
    "bi": "Ward No. (वार्ड नंबर)"
  },
  "ward no. (वार्ड नंबर)": {
    "en": "(Ward No.)",
    "hi": "(वार्ड नंबर)",
    "bi": "Ward No. (वार्ड नंबर)"
  },
  "(टिप्पणी)": {
    "en": "(Remarks)",
    "hi": "(टिप्पणी)",
    "bi": "Remarks (टिप्पणी)"
  },
  "(remarks)": {
    "en": "(Remarks)",
    "hi": "(टिप्पणी)",
    "bi": "Remarks (टिप्पणी)"
  },
  "(मोबाइल नंबर)": {
    "en": "(Mobile No.)",
    "hi": "(मोबाइल नंबर)",
    "bi": "Mobile No. (मोबाइल नंबर)"
  },
  "(mobile no.)": {
    "en": "(Mobile No.)",
    "hi": "(मोबाइल नंबर)",
    "bi": "Mobile No. (मोबाइल नंबर)"
  },
  "mobile no. (मोबाइल नंबर)": {
    "en": "(Mobile No.)",
    "hi": "(मोबाइल नंबर)",
    "bi": "Mobile No. (मोबाइल नंबर)"
  },
  "कारीगर का नाम": {
    "en": "Worker Name",
    "hi": "कारीगर का नाम",
    "bi": "Worker Name (कारीगर का नाम)"
  },
  "worker name (कारीगर का नाम)": {
    "en": "Worker Name",
    "hi": "कारीगर का नाम",
    "bi": "Worker Name (कारीगर का नाम)"
  },
  "कार्य कि विवरणी": {
    "en": "Work Details",
    "hi": "कार्य कि विवरणी",
    "bi": "Work Details (कार्य विवरण)"
  },
  "work details": {
    "en": "Work Details",
    "hi": "कार्य कि विवरणी",
    "bi": "Work Details (कार्य विवरण)"
  },
  "work details (कार्य विवरण)": {
    "en": "Work Details",
    "hi": "कार्य कि विवरणी",
    "bi": "Work Details (कार्य विवरण)"
  },
  "कार्यस्थल एवं पता के साथ": {
    "en": "With Work Site & Location",
    "hi": "कार्यस्थल एवं पता के साथ",
    "bi": "Work Site & Location (कार्यस्थल एवं पता)"
  },
  "with work site & location": {
    "en": "With Work Site & Location",
    "hi": "कार्यस्थल एवं पता के साथ",
    "bi": "Work Site & Location (कार्यस्थल एवं पता)"
  },
  "work site & location (कार्यस्थल एवं पता)": {
    "en": "With Work Site & Location",
    "hi": "कार्यस्थल एवं पता के साथ",
    "bi": "Work Site & Location (कार्यस्थल एवं पता)"
  },
  "संख्या या विवरण लिखें": {
    "en": "Enter quantity or details",
    "hi": "संख्या या विवरण लिखें",
    "bi": "Enter quantity or details (संख्या या विवरण लिखें)"
  },
  "enter quantity or details": {
    "en": "Enter quantity or details",
    "hi": "संख्या या विवरण लिखें",
    "bi": "Enter quantity or details (संख्या या विवरण लिखें)"
  },
  "enter quantity or details (संख्या या विवरण लिखें)": {
    "en": "Enter quantity or details",
    "hi": "संख्या या विवरण लिखें",
    "bi": "Enter quantity or details (संख्या या विवरण लिखें)"
  },
  "यदि कोई हो तो लिखें": {
    "en": "Enter if any",
    "hi": "यदि कोई हो तो लिखें",
    "bi": "Enter if any (यदि कोई हो तो लिखें)"
  },
  "enter if any": {
    "en": "Enter if any",
    "hi": "यदि कोई हो तो लिखें",
    "bi": "Enter if any (यदि कोई हो तो लिखें)"
  },
  "enter if any (यदि कोई हो तो लिखें)": {
    "en": "Enter if any",
    "hi": "यदि कोई हो तो लिखें",
    "bi": "Enter if any (यदि कोई हो तो लिखें)"
  },
  "जैसे: 2": {
    "en": "e.g. 2",
    "hi": "जैसे: 2",
    "bi": "e.g. 2 (जैसे: 2)"
  },
  "e.g. 2": {
    "en": "e.g. 2",
    "hi": "जैसे: 2",
    "bi": "e.g. 2 (जैसे: 2)"
  },
  "e.g. 2 (जैसे: 2)": {
    "en": "e.g. 2",
    "hi": "जैसे: 2",
    "bi": "e.g. 2 (जैसे: 2)"
  },
  "जैसे: मोटर पंप खोला गया + रिपेयर": {
    "en": "e.g. Motor pump opened + repaired",
    "hi": "जैसे: मोटर पंप खोला गया + रिपेयर",
    "bi": "e.g. Motor pump opened + repaired (जैसे: मोटर पंप खोला गया + रिपेयर)"
  },
  "e.g. motor pump opened + repaired": {
    "en": "e.g. Motor pump opened + repaired",
    "hi": "जैसे: मोटर पंप खोला गया + रिपेयर",
    "bi": "e.g. Motor pump opened + repaired (जैसे: मोटर पंप खोला गया + रिपेयर)"
  },
  "e.g. motor pump opened + repaired (जैसे: मोटर पंप खोला गया + रिपेयर)": {
    "en": "e.g. Motor pump opened + repaired",
    "hi": "जैसे: मोटर पंप खोला गया + रिपेयर",
    "bi": "e.g. Motor pump opened + repaired (जैसे: मोटर पंप खोला गया + रिपेयर)"
  },
  "जैसे: रामटोल + महथी चौक": {
    "en": "e.g. Ramtol + Mahathi Chowk",
    "hi": "जैसे: रामटोल + महथी चौक",
    "bi": "e.g. Ramtol + Mahathi Chowk (जैसे: रामटोल + महथी चौक)"
  },
  "e.g. ramtol + mahathi chowk": {
    "en": "e.g. Ramtol + Mahathi Chowk",
    "hi": "जैसे: रामटोल + महथी चौक",
    "bi": "e.g. Ramtol + Mahathi Chowk (जैसे: रामटोल + महथी चौक)"
  },
  "e.g. ramtol + mahathi chowk (जैसे: रामटोल + महथी चौक)": {
    "en": "e.g. Ramtol + Mahathi Chowk",
    "hi": "जैसे: रामटोल + महथी चौक",
    "bi": "e.g. Ramtol + Mahathi Chowk (जैसे: रामटोल + महथी चौक)"
  },
  "जैसे: 05/10/08": {
    "en": "e.g. 05/10/08",
    "hi": "जैसे: 05/10/08",
    "bi": "e.g. 05/10/08 (जैसे: 05/10/08)"
  },
  "e.g. 05/10/08": {
    "en": "e.g. 05/10/08",
    "hi": "जैसे: 05/10/08",
    "bi": "e.g. 05/10/08 (जैसे: 05/10/08)"
  },
  "e.g. 05/10/08 (जैसे: 05/10/08)": {
    "en": "e.g. 05/10/08",
    "hi": "जैसे: 05/10/08",
    "bi": "e.g. 05/10/08 (जैसे: 05/10/08)"
  },
  "सुपरवाइजर:": {
    "en": "Supervisor:",
    "hi": "सुपरवाइजर:",
    "bi": "Supervisor (सुपरवाइजर):"
  },
  "supervisor:": {
    "en": "Supervisor:",
    "hi": "सुपरवाइजर:",
    "bi": "Supervisor (सुपरवाइजर):"
  },
  "supervisor (सुपरवाइजर):": {
    "en": "Supervisor:",
    "hi": "सुपरवाइजर:",
    "bi": "Supervisor (सुपरवाइजर):"
  },
  "सहायक का मोबाइल": {
    "en": "Assistant Mobile",
    "hi": "सहायक का मोबाइल",
    "bi": "Assistant Mobile (सहायक का मोबाइल)"
  },
  "assistant mobile": {
    "en": "Assistant Mobile",
    "hi": "सहायक का मोबाइल",
    "bi": "Assistant Mobile (सहायक का मोबाइल)"
  },
  "assistant mobile (सहायक का मोबाइल)": {
    "en": "Assistant Mobile",
    "hi": "सहायक का मोबाइल",
    "bi": "Assistant Mobile (सहायक का मोबाइल)"
  },
  "date (तारीख):": {
    "en": "Date:",
    "hi": "तारीख:",
    "bi": "Date (तारीख):"
  },
  "क्र.": {
    "en": "Sl.",
    "hi": "क्र.",
    "bi": "Sl. (क्र.)"
  },
  "sl.": {
    "en": "Sl.",
    "hi": "क्र.",
    "bi": "Sl. (क्र.)"
  },
  "sl. (क्र.)": {
    "en": "Sl.",
    "hi": "क्र.",
    "bi": "Sl. (क्र.)"
  },
  "जरूरी": {
    "en": "Urgent",
    "hi": "जरूरी",
    "bi": "Urgent (जरूरी)"
  },
  "urgent (जरूरी)": {
    "en": "Urgent",
    "hi": "जरूरी",
    "bi": "Urgent (जरूरी)"
  },
  "dpr भरें": {
    "en": "Fill DPR",
    "hi": "DPR भरें",
    "bi": "Fill DPR (DPR भरें)"
  },
  "fill dpr": {
    "en": "Fill DPR",
    "hi": "DPR भरें",
    "bi": "Fill DPR (DPR भरें)"
  },
  "fill dpr (dpr भरें)": {
    "en": "Fill DPR",
    "hi": "DPR भरें",
    "bi": "Fill DPR (DPR भरें)"
  },
  "जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी।": {
    "en": "All filled rows will be printed on the DPR sheet.",
    "hi": "जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी।",
    "bi": "All filled rows will be printed on sheet (जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी)।"
  },
  "all filled rows will be printed on the dpr sheet.": {
    "en": "All filled rows will be printed on the DPR sheet.",
    "hi": "जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी।",
    "bi": "All filled rows will be printed on sheet (जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी)।"
  },
  "all filled rows will be printed on sheet (जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी)।": {
    "en": "All filled rows will be printed on the DPR sheet.",
    "hi": "जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी।",
    "bi": "All filled rows will be printed on sheet (जितनी लाइनें भरेंगे, वे पर्चे पर प्रिंट होंगी)।"
  },
  "आज का dpr पर्चा अभी तक सबमिट नहीं हुआ है। कृपया नीचे कारीगरों और काम का विवरण लिखकर \"save dpr sheet\" दबाएं।": {
    "en": "Today's DPR sheet has not been submitted yet. Please fill worker and work details below and click \"Save DPR Sheet\".",
    "hi": "आज का DPR पर्चा अभी तक सबमिट नहीं हुआ है। कृपया नीचे कारीगरों और काम का विवरण लिखकर \"Save DPR Sheet\" दबाएं।",
    "bi": "Today's DPR sheet pending (आज का DPR पर्चा सबमिट करें - Save DPR Sheet दबाएं)"
  },
  "today's dpr sheet has not been submitted yet. please fill worker and work details below and click \"save dpr sheet\".": {
    "en": "Today's DPR sheet has not been submitted yet. Please fill worker and work details below and click \"Save DPR Sheet\".",
    "hi": "आज का DPR पर्चा अभी तक सबमिट नहीं हुआ है। कृपया नीचे कारीगरों और काम का विवरण लिखकर \"Save DPR Sheet\" दबाएं।",
    "bi": "Today's DPR sheet pending (आज का DPR पर्चा सबमिट करें - Save DPR Sheet दबाएं)"
  },
  "today's dpr sheet pending (आज का dpr पर्चा सबमिट करें - save dpr sheet दबाएं)": {
    "en": "Today's DPR sheet has not been submitted yet. Please fill worker and work details below and click \"Save DPR Sheet\".",
    "hi": "आज का DPR पर्चा अभी तक सबमिट नहीं हुआ है। कृपया नीचे कारीगरों और काम का विवरण लिखकर \"Save DPR Sheet\" दबाएं।",
    "bi": "Today's DPR sheet pending (आज का DPR पर्चा सबमिट करें - Save DPR Sheet दबाएं)"
  },
  "वार्ड अनुसार विशेष काम लिखें (जैसे: (1) (w-5) = मोटर खोला गया रिपेयर के लिए। (w-10) = स्टार्टर खोला गया रिपेयर के लिए।)": {
    "en": "Enter ward-wise specific work (e.g. (1) (W-5) = Motor opened for repair. (W-10) = Starter opened for repair.)",
    "hi": "वार्ड अनुसार विशेष काम लिखें (जैसे: (1) (W-5) = मोटर खोला गया रिपेयर के लिए। (W-10) = स्टार्टर खोला गया रिपेयर के लिए।)",
    "bi": "Enter ward-wise work (वार्ड अनुसार विशेष काम लिखें)"
  },
  "enter ward-wise specific work (e.g. (1) (w-5) = motor opened for repair. (w-10) = starter opened for repair.)": {
    "en": "Enter ward-wise specific work (e.g. (1) (W-5) = Motor opened for repair. (W-10) = Starter opened for repair.)",
    "hi": "वार्ड अनुसार विशेष काम लिखें (जैसे: (1) (W-5) = मोटर खोला गया रिपेयर के लिए। (W-10) = स्टार्टर खोला गया रिपेयर के लिए।)",
    "bi": "Enter ward-wise work (वार्ड अनुसार विशेष काम लिखें)"
  },
  "enter ward-wise work (वार्ड अनुसार विशेष काम लिखें)": {
    "en": "Enter ward-wise specific work (e.g. (1) (W-5) = Motor opened for repair. (W-10) = Starter opened for repair.)",
    "hi": "वार्ड अनुसार विशेष काम लिखें (जैसे: (1) (W-5) = मोटर खोला गया रिपेयर के लिए। (W-10) = स्टार्टर खोला गया रिपेयर के लिए।)",
    "bi": "Enter ward-wise work (वार्ड अनुसार विशेष काम लिखें)"
  },
  "⏰ शाम 7:30 - 8:00 pm dpr रिमाइंडर": {
    "en": "⏰ 7:30 - 8:00 PM DPR Reminder",
    "hi": "⏰ शाम 7:30 - 8:00 PM DPR रिमाइंडर",
    "bi": "⏰ 7:30 - 8:00 PM DPR Reminder (शाम DPR रिमाइंडर)"
  },
  "⏰ 7:30 - 8:00 pm dpr reminder": {
    "en": "⏰ 7:30 - 8:00 PM DPR Reminder",
    "hi": "⏰ शाम 7:30 - 8:00 PM DPR रिमाइंडर",
    "bi": "⏰ 7:30 - 8:00 PM DPR Reminder (शाम DPR रिमाइंडर)"
  },
  "⏰ 7:30 - 8:00 pm dpr reminder (शाम dpr रिमाइंडर)": {
    "en": "⏰ 7:30 - 8:00 PM DPR Reminder",
    "hi": "⏰ शाम 7:30 - 8:00 PM DPR रिमाइंडर",
    "bi": "⏰ 7:30 - 8:00 PM DPR Reminder (शाम DPR रिमाइंडर)"
  },
  "आज का दैनिक कार्य पर्चा (dpr sheet) अभी तक जमा नहीं हुआ है। कृपया तुरंत भरें।": {
    "en": "Today's Daily Progress Report (DPR Sheet) is not submitted yet. Please submit immediately.",
    "hi": "आज का दैनिक कार्य पर्चा (DPR Sheet) अभी तक जमा नहीं हुआ है। कृपया तुरंत भरें।",
    "bi": "Today's DPR Sheet pending (आज का दैनिक कार्य पर्चा जमा करें)"
  },
  "today's daily progress report (dpr sheet) is not submitted yet. please submit immediately.": {
    "en": "Today's Daily Progress Report (DPR Sheet) is not submitted yet. Please submit immediately.",
    "hi": "आज का दैनिक कार्य पर्चा (DPR Sheet) अभी तक जमा नहीं हुआ है। कृपया तुरंत भरें।",
    "bi": "Today's DPR Sheet pending (आज का दैनिक कार्य पर्चा जमा करें)"
  },
  "today's dpr sheet pending (आज का दैनिक कार्य पर्चा जमा करें)": {
    "en": "Today's Daily Progress Report (DPR Sheet) is not submitted yet. Please submit immediately.",
    "hi": "आज का दैनिक कार्य पर्चा (DPR Sheet) अभी तक जमा नहीं हुआ है। कृपया तुरंत भरें।",
    "bi": "Today's DPR Sheet pending (आज का दैनिक कार्य पर्चा जमा करें)"
  },
  "समस्या / help": {
    "en": "Help / Issues",
    "hi": "समस्या / Help",
    "bi": "Help / Issues (समस्या व सहायता)"
  },
  "help / issues": {
    "en": "Help / Issues",
    "hi": "समस्या / Help",
    "bi": "Help / Issues (समस्या व सहायता)"
  },
  "help / issues (समस्या व सहायता)": {
    "en": "Help / Issues",
    "hi": "समस्या / Help",
    "bi": "Help / Issues (समस्या व सहायता)"
  },
  "समस्या / complaint": {
    "en": "Complaints",
    "hi": "समस्या / Complaint",
    "bi": "Complaints (समस्या / शिकायत)"
  },
  "complaints": {
    "en": "Complaints",
    "hi": "समस्या / Complaint",
    "bi": "Complaints (समस्या / शिकायत)"
  },
  "complaints (समस्या / शिकायत)": {
    "en": "Complaints",
    "hi": "समस्या / Complaint",
    "bi": "Complaints (समस्या / शिकायत)"
  },
  "जहाँ काम रुका हुआ है": {
    "en": "Where work is halted",
    "hi": "जहाँ काम रुका हुआ है",
    "bi": "Where work is halted (जहाँ काम रुका हुआ है)"
  },
  "where work is halted": {
    "en": "Where work is halted",
    "hi": "जहाँ काम रुका हुआ है",
    "bi": "Where work is halted (जहाँ काम रुका हुआ है)"
  },
  "where work is halted (जहाँ काम रुका हुआ है)": {
    "en": "Where work is halted",
    "hi": "जहाँ काम रुका हुआ है",
    "bi": "Where work is halted (जहाँ काम रुका हुआ है)"
  },
  "क्या दिक्कत है? विस्तार से लिखें": {
    "en": "What is the problem? Describe in detail",
    "hi": "क्या दिक्कत है? विस्तार से लिखें",
    "bi": "Describe problem in detail (दिक्कत विस्तार से लिखें)"
  },
  "what is the problem? describe in detail": {
    "en": "What is the problem? Describe in detail",
    "hi": "क्या दिक्कत है? विस्तार से लिखें",
    "bi": "Describe problem in detail (दिक्कत विस्तार से लिखें)"
  },
  "describe problem in detail (दिक्कत विस्तार से लिखें)": {
    "en": "What is the problem? Describe in detail",
    "hi": "क्या दिक्कत है? विस्तार से लिखें",
    "bi": "Describe problem in detail (दिक्कत विस्तार से लिखें)"
  },
  "take live photo of defect or site": {
    "en": "Take live photo of defect or site",
    "hi": "खराबी या साइट का लाइव फोटो लें",
    "bi": "Take live site photo (साइट का लाइव फोटो लें)"
  },
  "take live site photo (साइट का लाइव फोटो लें)": {
    "en": "Take live photo of defect or site",
    "hi": "खराबी या साइट का लाइव फोटो लें",
    "bi": "Take live site photo (साइट का लाइव फोटो लें)"
  },
  "समस्या दर्ज हो गई है!": {
    "en": "Issue registered successfully!",
    "hi": "समस्या दर्ज हो गई है!",
    "bi": "Issue registered successfully! (समस्या दर्ज हो गई!)"
  },
  "issue registered successfully!": {
    "en": "Issue registered successfully!",
    "hi": "समस्या दर्ज हो गई है!",
    "bi": "Issue registered successfully! (समस्या दर्ज हो गई!)"
  },
  "issue registered successfully! (समस्या दर्ज हो गई!)": {
    "en": "Issue registered successfully!",
    "hi": "समस्या दर्ज हो गई है!",
    "bi": "Issue registered successfully! (समस्या दर्ज हो गई!)"
  },
  "समस्या का समाधान दर्ज करें": {
    "en": "Record Issue Resolution",
    "hi": "समस्या का समाधान दर्ज करें",
    "bi": "Record Issue Resolution (समस्या का समाधान दर्ज करें)"
  },
  "record issue resolution": {
    "en": "Record Issue Resolution",
    "hi": "समस्या का समाधान दर्ज करें",
    "bi": "Record Issue Resolution (समस्या का समाधान दर्ज करें)"
  },
  "record issue resolution (समस्या का समाधान दर्ज करें)": {
    "en": "Record Issue Resolution",
    "hi": "समस्या का समाधान दर्ज करें",
    "bi": "Record Issue Resolution (समस्या का समाधान दर्ज करें)"
  },
  "समाधान विवरण (resolution):": {
    "en": "Resolution Details:",
    "hi": "समाधान विवरण (Resolution):",
    "bi": "Resolution Details (समाधान विवरण):"
  },
  "resolution details:": {
    "en": "Resolution Details:",
    "hi": "समाधान विवरण (Resolution):",
    "bi": "Resolution Details (समाधान विवरण):"
  },
  "resolution details (समाधान विवरण):": {
    "en": "Resolution Details:",
    "hi": "समाधान विवरण (Resolution):",
    "bi": "Resolution Details (समाधान विवरण):"
  },
  "हल करें (resolve)": {
    "en": "Resolve",
    "hi": "हल करें (Resolve)",
    "bi": "Resolve (हल करें)"
  },
  "resolve": {
    "en": "Resolve",
    "hi": "हल करें (Resolve)",
    "bi": "Resolve (हल करें)"
  },
  "resolve (हल करें)": {
    "en": "Resolve",
    "hi": "हल करें (Resolve)",
    "bi": "Resolve (हल करें)"
  },
  "फोटो देखें (view photo)": {
    "en": "View Photo",
    "hi": "फोटो देखें (View Photo)",
    "bi": "View Photo (फोटो देखें)"
  },
  "view photo": {
    "en": "View Photo",
    "hi": "फोटो देखें (View Photo)",
    "bi": "View Photo (फोटो देखें)"
  },
  "view photo (फोटो देखें)": {
    "en": "View Photo",
    "hi": "फोटो देखें (View Photo)",
    "bi": "View Photo (फोटो देखें)"
  },
  "रद्द करें (cancel)": {
    "en": "Cancel",
    "hi": "रद्द करें (Cancel)",
    "bi": "Cancel (रद्द करें)"
  },
  "ठीक है (done)": {
    "en": "Done",
    "hi": "ठीक है (Done)",
    "bi": "Done (ठीक है)"
  },
  "done (ठीक है)": {
    "en": "Done",
    "hi": "ठीक है (Done)",
    "bi": "Done (ठीक है)"
  },
  "दर्ज हो रहा है...": {
    "en": "Submitting...",
    "hi": "दर्ज हो रहा है...",
    "bi": "Submitting (दर्ज हो रहा है)..."
  },
  "submitting...": {
    "en": "Submitting...",
    "hi": "दर्ज हो रहा है...",
    "bi": "Submitting (दर्ज हो रहा है)..."
  },
  "submitting (दर्ज हो रहा है)...": {
    "en": "Submitting...",
    "hi": "दर्ज हो रहा है...",
    "bi": "Submitting (दर्ज हो रहा है)..."
  },
  "इस समय कोई भी खुली (open) समस्या नहीं है। सब कुछ ठीक चल रहा है! अगर साइट पर कोई दिक्कत या सामान की कमी है तो नीचे बटन दबाकर शिकायत दर्ज करें।": {
    "en": "There are no open issues at this time. Everything is running smoothly! If there is any shortage or defect at site, click the button below to register a complaint.",
    "hi": "इस समय कोई भी खुली (Open) समस्या नहीं है। सब कुछ ठीक चल रहा है! अगर साइट पर कोई दिक्कत या सामान की कमी है तो नीचे बटन दबाकर शिकायत दर्ज करें।",
    "bi": "No open issues currently (इस समय कोई खुली समस्या नहीं है)"
  },
  "there are no open issues at this time. everything is running smoothly! if there is any shortage or defect at site, click the button below to register a complaint.": {
    "en": "There are no open issues at this time. Everything is running smoothly! If there is any shortage or defect at site, click the button below to register a complaint.",
    "hi": "इस समय कोई भी खुली (Open) समस्या नहीं है। सब कुछ ठीक चल रहा है! अगर साइट पर कोई दिक्कत या सामान की कमी है तो नीचे बटन दबाकर शिकायत दर्ज करें।",
    "bi": "No open issues currently (इस समय कोई खुली समस्या नहीं है)"
  },
  "no open issues currently (इस समय कोई खुली समस्या नहीं है)": {
    "en": "There are no open issues at this time. Everything is running smoothly! If there is any shortage or defect at site, click the button below to register a complaint.",
    "hi": "इस समय कोई भी खुली (Open) समस्या नहीं है। सब कुछ ठीक चल रहा है! अगर साइट पर कोई दिक्कत या सामान की कमी है तो नीचे बटन दबाकर शिकायत दर्ज करें।",
    "bi": "No open issues currently (इस समय कोई खुली समस्या नहीं है)"
  },
  "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें। हेड ऑफिस द्वारा तुरंत समाधान किया जाएगा।": {
    "en": "Report any site issues (material shortage, dispute, machine breakdown, labour) here. Head office will resolve immediately.",
    "hi": "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें। हेड ऑफिस द्वारा तुरंत समाधान किया जाएगा।",
    "bi": "Report site issues here (साइट की दिक्कत यहाँ दर्ज करें)"
  },
  "report any site issues (material shortage, dispute, machine breakdown, labour) here. head office will resolve immediately.": {
    "en": "Report any site issues (material shortage, dispute, machine breakdown, labour) here. Head office will resolve immediately.",
    "hi": "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें। हेड ऑफिस द्वारा तुरंत समाधान किया जाएगा।",
    "bi": "Report site issues here (साइट की दिक्कत यहाँ दर्ज करें)"
  },
  "report site issues here (साइट की दिक्कत यहाँ दर्ज करें)": {
    "en": "Report any site issues (material shortage, dispute, machine breakdown, labour) here. Head office will resolve immediately.",
    "hi": "साइट पर कोई भी दिक्कत (सामान की कमी, विवाद, मशीन खराबी, लेबर) हो तो यहाँ तुरंत दर्ज करें। हेड ऑफिस द्वारा तुरंत समाधान किया जाएगा।",
    "bi": "Report site issues here (साइट की दिक्कत यहाँ दर्ज करें)"
  },
  "उदाहरण: 63mm pvc पाइप खत्म हो गया है, 200 मीटर तुरंत चाहिए। या मशीन में खराबी आ गई है...": {
    "en": "e.g. 63mm PVC pipe shortage, need 200m immediately. Or machine breakdown...",
    "hi": "उदाहरण: 63mm PVC पाइप खत्म हो गया है, 200 मीटर तुरंत चाहिए। या मशीन में खराबी आ गई है...",
    "bi": "e.g. 63mm PVC pipe shortage (उदाहरण: 63mm PVC पाइप खत्म हो गया है...)"
  },
  "e.g. 63mm pvc pipe shortage, need 200m immediately. or machine breakdown...": {
    "en": "e.g. 63mm PVC pipe shortage, need 200m immediately. Or machine breakdown...",
    "hi": "उदाहरण: 63mm PVC पाइप खत्म हो गया है, 200 मीटर तुरंत चाहिए। या मशीन में खराबी आ गई है...",
    "bi": "e.g. 63mm PVC pipe shortage (उदाहरण: 63mm PVC पाइप खत्म हो गया है...)"
  },
  "e.g. 63mm pvc pipe shortage (उदाहरण: 63mm pvc पाइप खत्म हो गया है...)": {
    "en": "e.g. 63mm PVC pipe shortage, need 200m immediately. Or machine breakdown...",
    "hi": "उदाहरण: 63mm PVC पाइप खत्म हो गया है, 200 मीटर तुरंत चाहिए। या मशीन में खराबी आ गई है...",
    "bi": "e.g. 63mm PVC pipe shortage (उदाहरण: 63mm PVC पाइप खत्म हो गया है...)"
  },
  "आपकी शिकायत सिस्टम में सफलता-पूर्वक रिकॉर्ड हो गई है। हेड ऑफिस द्वारा इस पर तुरंत आवश्यक कार्रवाई की जाएगी।": {
    "en": "Your complaint has been successfully recorded in the system. Head office will take immediate action.",
    "hi": "आपकी शिकायत सिस्टम में सफलता-पूर्वक रिकॉर्ड हो गई है। हेड ऑफिस द्वारा इस पर तुरंत आवश्यक कार्रवाई की जाएगी।",
    "bi": "Complaint recorded successfully (शिकायत सफलता-पूर्वक रिकॉर्ड हो गई)"
  },
  "your complaint has been successfully recorded in the system. head office will take immediate action.": {
    "en": "Your complaint has been successfully recorded in the system. Head office will take immediate action.",
    "hi": "आपकी शिकायत सिस्टम में सफलता-पूर्वक रिकॉर्ड हो गई है। हेड ऑफिस द्वारा इस पर तुरंत आवश्यक कार्रवाई की जाएगी।",
    "bi": "Complaint recorded successfully (शिकायत सफलता-पूर्वक रिकॉर्ड हो गई)"
  },
  "complaint recorded successfully (शिकायत सफलता-पूर्वक रिकॉर्ड हो गई)": {
    "en": "Your complaint has been successfully recorded in the system. Head office will take immediate action.",
    "hi": "आपकी शिकायत सिस्टम में सफलता-पूर्वक रिकॉर्ड हो गई है। हेड ऑफिस द्वारा इस पर तुरंत आवश्यक कार्रवाई की जाएगी।",
    "bi": "Complaint recorded successfully (शिकायत सफलता-पूर्वक रिकॉर्ड हो गई)"
  },
  "acquired month क्या है?": {
    "en": "What is Acquired Month?",
    "hi": "Acquired Month क्या है?",
    "bi": "What is Acquired Month? (अधिग्रहण माह क्या है?)"
  },
  "what is acquired month?": {
    "en": "What is Acquired Month?",
    "hi": "Acquired Month क्या है?",
    "bi": "What is Acquired Month? (अधिग्रहण माह क्या है?)"
  },
  "what is acquired month? (अधिग्रहण माह क्या है?)": {
    "en": "What is Acquired Month?",
    "hi": "Acquired Month क्या है?",
    "bi": "What is Acquired Month? (अधिग्रहण माह क्या है?)"
  },
  "• जिस माह साइट शुरू या हैंडओवर हुई है, उसे सेट करें।": {
    "en": "• Set the month when site work started or was handed over.",
    "hi": "• जिस माह साइट शुरू या हैंडओवर हुई है, उसे सेट करें।",
    "bi": "• Set site takeover month (जिस माह साइट शुरू हुई उसे सेट करें)"
  },
  "• set the month when site work started or was handed over.": {
    "en": "• Set the month when site work started or was handed over.",
    "hi": "• जिस माह साइट शुरू या हैंडओवर हुई है, उसे सेट करें।",
    "bi": "• Set site takeover month (जिस माह साइट शुरू हुई उसे सेट करें)"
  },
  "• set site takeover month (जिस माह साइट शुरू हुई उसे सेट करें)": {
    "en": "• Set the month when site work started or was handed over.",
    "hi": "• जिस माह साइट शुरू या हैंडओवर हुई है, उसे सेट करें।",
    "bi": "• Set site takeover month (जिस माह साइट शुरू हुई उसे सेट करें)"
  },
  "• इस माह से पहले के महीनों पर \"pre-acquisition\" मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।": {
    "en": "• Months prior to this month will be marked \"Pre-Acquisition\" (no bill considered pending).",
    "hi": "• इस माह से पहले के महीनों पर \"Pre-Acquisition\" मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।",
    "bi": "• Prior months marked Pre-Acquisition (पहले के माह Pre-Acquisition रहेंगे)"
  },
  "• months prior to this month will be marked \"pre-acquisition\" (no bill considered pending).": {
    "en": "• Months prior to this month will be marked \"Pre-Acquisition\" (no bill considered pending).",
    "hi": "• इस माह से पहले के महीनों पर \"Pre-Acquisition\" मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।",
    "bi": "• Prior months marked Pre-Acquisition (पहले के माह Pre-Acquisition रहेंगे)"
  },
  "• prior months marked pre-acquisition (पहले के माह pre-acquisition रहेंगे)": {
    "en": "• Months prior to this month will be marked \"Pre-Acquisition\" (no bill considered pending).",
    "hi": "• इस माह से पहले के महीनों पर \"Pre-Acquisition\" मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।",
    "bi": "• Prior months marked Pre-Acquisition (पहले के माह Pre-Acquisition रहेंगे)"
  },
  "• इस माह और इसके बाद के महीनों में बिल ट्रैक होंगे। यदि पूरी साल साइट चालू रही है तो april 2026 चुनें।": {
    "en": "• Bills will be tracked for this month and subsequent months. If site was active all year, select April 2026.",
    "hi": "• इस माह और इसके बाद के महीनों में बिल ट्रैक होंगे। यदि पूरी साल साइट चालू रही है तो April 2026 चुनें।",
    "bi": "• Bills tracked from this month (इस माह से आगे बिल ट्रैक होंगे)"
  },
  "• bills will be tracked for this month and subsequent months. if site was active all year, select april 2026.": {
    "en": "• Bills will be tracked for this month and subsequent months. If site was active all year, select April 2026.",
    "hi": "• इस माह और इसके बाद के महीनों में बिल ट्रैक होंगे। यदि पूरी साल साइट चालू रही है तो April 2026 चुनें।",
    "bi": "• Bills tracked from this month (इस माह से आगे बिल ट्रैक होंगे)"
  },
  "• bills tracked from this month (इस माह से आगे बिल ट्रैक होंगे)": {
    "en": "• Bills will be tracked for this month and onwards. If site was active all year, select April 2026.",
    "hi": "• इस माह और इसके बाद के महीनों में बिल ट्रैक होंगे। यदि पूरी साल साइट चालू रही है तो",
    "bi": "• Bills tracked from this month (इस माह से आगे बिल ट्रैक होंगे)"
  },
  "पहले के महीनों": {
    "en": "Prior Months",
    "hi": "पहले के महीनों",
    "bi": "Prior Months (पहले के महीनों)"
  },
  "prior months": {
    "en": "Prior Months",
    "hi": "पहले के महीनों",
    "bi": "Prior Months (पहले के महीनों)"
  },
  "prior months (पहले के महीनों)": {
    "en": "Prior Months",
    "hi": "पहले के महीनों",
    "bi": "Prior Months (पहले के महीनों)"
  },
  "• इस माह से": {
    "en": "• From this month",
    "hi": "• इस माह से",
    "bi": "• From this month (इस माह से)"
  },
  "• from this month": {
    "en": "• From this month",
    "hi": "• इस माह से",
    "bi": "• From this month (इस माह से)"
  },
  "• from this month (इस माह से)": {
    "en": "• From this month",
    "hi": "• इस माह से",
    "bi": "• From this month (इस माह से)"
  },
  "मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।": {
    "en": "will be marked (where no bill is considered pending).",
    "hi": "मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।",
    "bi": "will be marked (no bill pending)"
  },
  "will be marked (where no bill is considered pending).": {
    "en": "will be marked (where no bill is considered pending).",
    "hi": "मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।",
    "bi": "will be marked (no bill pending)"
  },
  "will be marked (no bill pending)": {
    "en": "will be marked (where no bill is considered pending).",
    "hi": "मार्क होगा (जहां कोई बिल पेंडिंग नहीं माना जाएगा)।",
    "bi": "will be marked (no bill pending)"
  },
  "pdf, excel, word, इमेज या दस्तावेज़ अपलोड करें": {
    "en": "Upload PDF, Excel, Word, image or document",
    "hi": "PDF, Excel, Word, इमेज या दस्तावेज़ अपलोड करें",
    "bi": "Upload PDF, Excel, Word, image or document (दस्तावेज़ अपलोड करें)"
  },
  "upload pdf, excel, word, image or document": {
    "en": "Upload PDF, Excel, Word, image or document",
    "hi": "PDF, Excel, Word, इमेज या दस्तावेज़ अपलोड करें",
    "bi": "Upload PDF, Excel, Word, image or document (दस्तावेज़ अपलोड करें)"
  },
  "upload pdf, excel, word, image or document (दस्तावेज़ अपलोड करें)": {
    "en": "Upload PDF, Excel, Word, image or document",
    "hi": "PDF, Excel, Word, इमेज या दस्तावेज़ अपलोड करें",
    "bi": "Upload PDF, Excel, Word, image or document (दस्तावेज़ अपलोड करें)"
  },
  "सुपरवाइजर और स्टाफ के बीच pdf, excel, word, इमेज और महत्वपूर्ण दस्तावेजों का सुरक्षित आदान-प्रदान — प्रत्येक फ़ाइल पर शेयर करने वाले सुपरवाइजर का नाम व तारीख स्पष्ट रूप से दर्ज रहेगी।": {
    "en": "Secure exchange of PDF, Excel, Word, images and important documents between supervisors and staff — each file clearly records supervisor name and date.",
    "hi": "सुपरवाइजर और स्टाफ के बीच PDF, Excel, Word, इमेज और महत्वपूर्ण दस्तावेजों का सुरक्षित आदान-प्रदान — प्रत्येक फ़ाइल पर शेयर करने वाले सुपरवाइजर का नाम व तारीख स्पष्ट रूप से दर्ज रहेगी।",
    "bi": "Secure document sharing (सुपरवाइजर और स्टाफ के बीच सुरक्षित दस्तावेज़ आदान-प्रदान)"
  },
  "secure exchange of pdf, excel, word, images and important documents between supervisors and staff — each file clearly records supervisor name and date.": {
    "en": "Secure exchange of PDF, Excel, Word, images and important documents between supervisors and staff — each file clearly records supervisor name and date.",
    "hi": "सुपरवाइजर और स्टाफ के बीच PDF, Excel, Word, इमेज और महत्वपूर्ण दस्तावेजों का सुरक्षित आदान-प्रदान — प्रत्येक फ़ाइल पर शेयर करने वाले सुपरवाइजर का नाम व तारीख स्पष्ट रूप से दर्ज रहेगी।",
    "bi": "Secure document sharing (सुपरवाइजर और स्टाफ के बीच सुरक्षित दस्तावेज़ आदान-प्रदान)"
  },
  "secure document sharing (सुपरवाइजर और स्टाफ के बीच सुरक्षित दस्तावेज़ आदान-प्रदान)": {
    "en": "Secure exchange of PDF, Excel, Word, images and important documents between supervisors and staff — each file clearly records supervisor name and date.",
    "hi": "सुपरवाइजर और स्टाफ के बीच PDF, Excel, Word, इमेज और महत्वपूर्ण दस्तावेजों का सुरक्षित आदान-प्रदान — प्रत्येक फ़ाइल पर शेयर करने वाले सुपरवाइजर का नाम व तारीख स्पष्ट रूप से दर्ज रहेगी।",
    "bi": "Secure document sharing (सुपरवाइजर और स्टाफ के बीच सुरक्षित दस्तावेज़ आदान-प्रदान)"
  },
  "यह नाम प्रत्येक यूजर को फ़ाइल के साथ \"shared by\" के रूप में प्रदर्शित होगा।": {
    "en": "This name will be displayed to every user as \"Shared by\" with the file.",
    "hi": "यह नाम प्रत्येक यूजर को फ़ाइल के साथ \"Shared by\" के रूप में प्रदर्शित होगा।",
    "bi": "Name shown as Shared by (यह नाम फ़ाइल के साथ प्रदर्शित होगा)"
  },
  "this name will be displayed to every user as \"shared by\" with the file.": {
    "en": "This name will be displayed to every user as \"Shared by\" with the file.",
    "hi": "यह नाम प्रत्येक यूजर को फ़ाइल के साथ \"Shared by\" के रूप में प्रदर्शित होगा।",
    "bi": "Name shown as Shared by (यह नाम फ़ाइल के साथ प्रदर्शित होगा)"
  },
  "name shown as shared by (यह नाम फ़ाइल के साथ प्रदर्शित होगा)": {
    "en": "This name will be displayed to every user as \"Shared by\" with the file.",
    "hi": "यह नाम प्रत्येक यूजर को फ़ाइल के साथ \"Shared by\" के रूप में प्रदर्शित होगा।",
    "bi": "Name shown as Shared by (यह नाम फ़ाइल के साथ प्रदर्शित होगा)"
  },
  "फ़िल्टर या सर्च के अनुसार कोई दस्तावेज़ उपलब्ध नहीं है। कृपया फ़िल्टर रीसेट करें।": {
    "en": "No documents available matching filter or search. Please reset filters.",
    "hi": "फ़िल्टर या सर्च के अनुसार कोई दस्तावेज़ उपलब्ध नहीं है। कृपया फ़िल्टर रीसेट करें।",
    "bi": "No documents matching filter (कोई दस्तावेज़ उपलब्ध नहीं है)"
  },
  "no documents available matching filter or search. please reset filters.": {
    "en": "No documents available matching filter or search. Please reset filters.",
    "hi": "फ़िल्टर या सर्च के अनुसार कोई दस्तावेज़ उपलब्ध नहीं है। कृपया फ़िल्टर रीसेट करें।",
    "bi": "No documents matching filter (कोई दस्तावेज़ उपलब्ध नहीं है)"
  },
  "no documents matching filter (कोई दस्तावेज़ उपलब्ध नहीं है)": {
    "en": "No documents available matching filter or search. Please reset filters. No documents have been shared yet.",
    "hi": "फिल्टर या सर्च के अनुसार कोई दस्तावेज़ उपलब्ध नहीं है। कृपया फ़िल्टर रीसेट करें। अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।",
    "bi": "No documents matching filter (कोई दस्तावेज़ उपलब्ध नहीं है)"
  },
  "अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।": {
    "en": "No documents have been shared yet. Supervisors or staff can share the first file.",
    "hi": "अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।",
    "bi": "No documents shared yet (अभी तक कोई दस्तावेज़ शेयर नहीं किया गया)"
  },
  "no documents have been shared yet. supervisors or staff can share the first file.": {
    "en": "No documents have been shared yet. Supervisors or staff can share the first file.",
    "hi": "अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।",
    "bi": "No documents shared yet (अभी तक कोई दस्तावेज़ शेयर नहीं किया गया)"
  },
  "no documents shared yet (अभी तक कोई दस्तावेज़ शेयर नहीं किया गया)": {
    "en": "No documents have been shared yet. Supervisors or staff can share the first file.",
    "hi": "अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।",
    "bi": "No documents shared yet (अभी तक कोई दस्तावेज़ शेयर नहीं किया गया)"
  },
  "सर्वर पर एक अस्थाई समस्या उत्पन्न हुई है। आपकी सुरक्षित लॉगिन या कुकीज़ रीसेट करके दोबारा आसानी से पेज खोला जा सकता है।": {
    "en": "A temporary server issue occurred. Re-logging in or clearing cookies will restore access smoothly.",
    "hi": "सर्वर पर एक अस्थाई समस्या उत्पन्न हुई है। आपकी सुरक्षित लॉगिन या कुकीज़ रीसेट करके दोबारा आसानी से पेज खोला जा सकता है।",
    "bi": "Temporary server issue (सर्वर पर अस्थाई समस्या)"
  },
  "a temporary server issue occurred. re-logging in or clearing cookies will restore access smoothly.": {
    "en": "A temporary server issue occurred. Re-logging in or clearing cookies will restore access smoothly.",
    "hi": "सर्वर पर एक अस्थाई समस्या उत्पन्न हुई है। आपकी सुरक्षित लॉगिन या कुकीज़ रीसेट करके दोबारा आसानी से पेज खोला जा सकता है।",
    "bi": "Temporary server issue (सर्वर पर अस्थाई समस्या)"
  },
  "temporary server issue (सर्वर पर अस्थाई समस्या)": {
    "en": "A temporary server issue occurred. Re-logging in or clearing cookies will restore access smoothly.",
    "hi": "सर्वर पर एक अस्थाई समस्या उत्पन्न हुई है। आपकी सुरक्षित लॉगिन या कुकीज़ रीसेट करके दोबारा आसानी से पेज खोला जा सकता है।",
    "bi": "Temporary server issue (सर्वर पर अस्थाई समस्या)"
  },
  "सर्वर में तकनीकी समस्या (500)": {
    "en": "Server Technical Issue (500)",
    "hi": "सर्वर में तकनीकी समस्या (500)",
    "bi": "Server Technical Issue (सर्वर में तकनीकी समस्या - 500)"
  },
  "server technical issue (500)": {
    "en": "Server Technical Issue (500)",
    "hi": "सर्वर में तकनीकी समस्या (500)",
    "bi": "Server Technical Issue (सर्वर में तकनीकी समस्या - 500)"
  },
  "server technical issue (सर्वर में तकनीकी समस्या - 500)": {
    "en": "Server Technical Issue (500)",
    "hi": "सर्वर में तकनीकी समस्या (500)",
    "bi": "Server Technical Issue (सर्वर में तकनीकी समस्या - 500)"
  },
  "पेज रिफ्रेश करें (try again)": {
    "en": "Refresh Page (Try Again)",
    "hi": "पेज रिफ्रेश करें (Try Again)",
    "bi": "Refresh Page (पेज रिफ्रेश करें)"
  },
  "refresh page (try again)": {
    "en": "Refresh Page (Try Again)",
    "hi": "पेज रिफ्रेश करें (Try Again)",
    "bi": "Refresh Page (पेज रिफ्रेश करें)"
  },
  "मुख्य डैशबोर्ड (home)": {
    "en": "Main Dashboard (Home)",
    "hi": "मुख्य डैशबोर्ड (Home)",
    "bi": "Main Dashboard (मुख्य डैशबोर्ड)"
  },
  "main dashboard (home)": {
    "en": "Main Dashboard (Home)",
    "hi": "मुख्य डैशबोर्ड (Home)",
    "bi": "Main Dashboard (मुख्य डैशबोर्ड)"
  },
  "main dashboard (मुख्य डैशबोर्ड)": {
    "en": "Main Dashboard (Home)",
    "hi": "मुख्य डैशबोर्ड (Home)",
    "bi": "Main Dashboard (मुख्य डैशबोर्ड)"
  },
  "चुनें।": {
    "en": "Select.",
    "hi": "चुनें।",
    "bi": "Select (चुनें)।"
  },
  "select.": {
    "en": "Select.",
    "hi": "चुनें।",
    "bi": "Select (चुनें)।"
  },
  "select (चुनें)।": {
    "en": "Select.",
    "hi": "चुनें।",
    "bi": "Select (चुनें)।"
  },
  "पर": {
    "en": "on",
    "hi": "पर",
    "bi": "on (पर)"
  },
  "on": {
    "en": "on",
    "hi": "पर",
    "bi": "on (पर)"
  },
  "on (पर)": {
    "en": "on",
    "hi": "पर",
    "bi": "on (पर)"
  },
  "• इस माह और इसके बाद के महीनों में बिल ट्रैक होंगे। यदि पूरी साल साइट चालू रही है तो": {
    "en": "• Bills will be tracked for this month and onwards. If site was active all year, select April 2026.",
    "hi": "• इस माह और इसके बाद के महीनों में बिल ट्रैक होंगे। यदि पूरी साल साइट चालू रही है तो",
    "bi": "• Bills tracked from this month (इस माह से आगे बिल ट्रैक होंगे)"
  },
  "• bills will be tracked for this month and onwards. if site was active all year, select april 2026.": {
    "en": "• Bills will be tracked for this month and onwards. If site was active all year, select April 2026.",
    "hi": "• इस माह और इसके बाद के महीनों में बिल ट्रैक होंगे। यदि पूरी साल साइट चालू रही है तो",
    "bi": "• Bills tracked from this month (इस माह से आगे बिल ट्रैक होंगे)"
  },
  "उदाहरण: 200m पाइप आज गाड़ी से रवाना कर दिया गया है...": {
    "en": "e.g. 200m pipe dispatched today via vehicle...",
    "hi": "उदाहरण: 200m पाइप आज गाड़ी से रवाना कर दिया गया है...",
    "bi": "e.g. 200m pipe dispatched (उदाहरण: 200m पाइप रवाना किया गया...)"
  },
  "e.g. 200m pipe dispatched today via vehicle...": {
    "en": "e.g. 200m pipe dispatched today via vehicle...",
    "hi": "उदाहरण: 200m पाइप आज गाड़ी से रवाना कर दिया गया है...",
    "bi": "e.g. 200m pipe dispatched (उदाहरण: 200m पाइप रवाना किया गया...)"
  },
  "e.g. 200m pipe dispatched (उदाहरण: 200m पाइप रवाना किया गया...)": {
    "en": "e.g. 200m pipe dispatched today via vehicle...",
    "hi": "उदाहरण: 200m पाइप आज गाड़ी से रवाना कर दिया गया है...",
    "bi": "e.g. 200m pipe dispatched (उदाहरण: 200m पाइप रवाना किया गया...)"
  },
  "सेव करते ही पूरा पर्चा सुरक्षित हो जाएगा और ऑफिस में तुरंत दिखेगा।": {
    "en": "Once saved, entire DPR sheet is securely stored and visible to head office.",
    "hi": "सेव करते ही पूरा पर्चा सुरक्षित हो जाएगा और ऑफिस में तुरंत दिखेगा।",
    "bi": "Once saved, sheet is securely stored (सेव करते ही पूरा पर्चा सुरक्षित होगा)"
  },
  "once saved, entire dpr sheet is securely stored and visible to head office.": {
    "en": "Once saved, entire DPR sheet is securely stored and visible to head office.",
    "hi": "सेव करते ही पूरा पर्चा सुरक्षित हो जाएगा और ऑफिस में तुरंत दिखेगा।",
    "bi": "Once saved, sheet is securely stored (सेव करते ही पूरा पर्चा सुरक्षित होगा)"
  },
  "once saved, sheet is securely stored (सेव करते ही पूरा पर्चा सुरक्षित होगा)": {
    "en": "Once saved, entire DPR sheet is securely stored and visible to head office.",
    "hi": "सेव करते ही पूरा पर्चा सुरक्षित हो जाएगा और ऑफिस में तुरंत दिखेगा।",
    "bi": "Once saved, sheet is securely stored (सेव करते ही पूरा पर्चा सुरक्षित होगा)"
  },
  "🔴 अति आवश्यक (काम रुका है)": {
    "en": "🔴 Urgent (Work Halted)",
    "hi": "🔴 अति आवश्यक (काम रुका है)",
    "bi": "🔴 Urgent (अति आवश्यक - काम रुका है)"
  },
  "🔴 urgent (work halted)": {
    "en": "🔴 Urgent (Work Halted)",
    "hi": "🔴 अति आवश्यक (काम रुका है)",
    "bi": "🔴 Urgent (अति आवश्यक - काम रुका है)"
  },
  "🔴 urgent (अति आवश्यक - काम रुका है)": {
    "en": "🔴 Urgent (Work Halted)",
    "hi": "🔴 अति आवश्यक (काम रुका है)",
    "bi": "🔴 Urgent (अति आवश्यक - काम रुका है)"
  },
  "अति आवश्यक (काम रुका है)": {
    "en": "Urgent (Work Halted)",
    "hi": "अति आवश्यक (काम रुका है)",
    "bi": "Urgent (अति आवश्यक - काम रुका है)"
  },
  "urgent (work halted)": {
    "en": "Urgent (Work Halted)",
    "hi": "अति आवश्यक (काम रुका है)",
    "bi": "Urgent (अति आवश्यक - काम रुका है)"
  },
  "urgent (अति आवश्यक - काम रुका है)": {
    "en": "Urgent (Work Halted)",
    "hi": "अति आवश्यक (काम रुका है)",
    "bi": "Urgent (अति आवश्यक - काम रुका है)"
  },
  "साइट की दिक्कत लिखें, ऑफिस तक तुरंत पहुँचेगी": {
    "en": "Describe site problem, head office will resolve immediately",
    "hi": "साइट की दिक्कत लिखें, ऑफिस तक तुरंत पहुँचेगी",
    "bi": "Describe site problem (दिक्कत लिखें, तुरंत समाधान होगा)"
  },
  "describe site problem, head office will resolve immediately": {
    "en": "Describe site problem, head office will resolve immediately",
    "hi": "साइट की दिक्कत लिखें, ऑफिस तक तुरंत पहुँचेगी",
    "bi": "Describe site problem (दिक्कत लिखें, तुरंत समाधान होगा)"
  },
  "फिल्टर या सर्च के अनुसार कोई दस्तावेज़ उपलब्ध नहीं है। कृपया फ़िल्टर रीसेट करें। अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।": {
    "en": "No documents available matching filter or search. Please reset filters. No documents have been shared yet.",
    "hi": "फिल्टर या सर्च के अनुसार कोई दस्तावेज़ उपलब्ध नहीं है। कृपया फ़िल्टर रीसेट करें। अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।",
    "bi": "No documents matching filter (कोई दस्तावेज़ उपलब्ध नहीं है)"
  },
  "no documents available matching filter or search. please reset filters. no documents have been shared yet.": {
    "en": "No documents available matching filter or search. Please reset filters. No documents have been shared yet.",
    "hi": "फिल्टर या सर्च के अनुसार कोई दस्तावेज़ उपलब्ध नहीं है। कृपया फ़िल्टर रीसेट करें। अभी तक कोई दस्तावेज़ शेयर नहीं किया गया है। सुपरवाइजर या स्टाफ पहली फ़ाइल शेयर कर सकते हैं।",
    "bi": "No documents matching filter (कोई दस्तावेज़ उपलब्ध नहीं है)"
  },
  "(सुपरवाइजर कार्य क्षेत्र)": {
    "en": "(Supervisor Work Area)",
    "hi": "(सुपरवाइजर कार्य क्षेत्र)",
    "bi": "Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "(supervisor work area)": {
    "en": "(Supervisor Work Area)",
    "hi": "(सुपरवाइजर कार्य क्षेत्र)",
    "bi": "Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "&mdash; (सुपरवाइजर कार्य क्षेत्र)": {
    "en": "— (Supervisor Work Area)",
    "hi": "&mdash; (सुपरवाइजर कार्य क्षेत्र)",
    "bi": "— Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "— (supervisor work area)": {
    "en": "— (Supervisor Work Area)",
    "hi": "— (सुपरवाइजर कार्य क्षेत्र)",
    "bi": "— Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "— supervisor work area (सुपरवाइजर कार्य क्षेत्र)": {
    "en": "— (Supervisor Work Area)",
    "hi": "— (सुपरवाइजर कार्य क्षेत्र)",
    "bi": "— Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "— (सुपरवाइजर कार्य क्षेत्र)": {
    "en": "— (Supervisor Work Area)",
    "hi": "— (सुपरवाइजर कार्य क्षेत्र)",
    "bi": "— Supervisor Work Area (सुपरवाइजर कार्य क्षेत्र)"
  },
  "&bull; आज का दैनिक कार्य पर्चा (dpr) भरें। कारीगर, मोबाइल नंबर, कार्य क्षेत्र, वार्ड व कार्य विवरणी लिखकर सबमिट करें। कार्यालय dpr मॉनिटरिंग &bull; सभी 21 साइटों के दैनिक कार्य पर्चे (dpr sheets) का स्टेटस, 7:30 pm रिमाइंडर व 1-क्लिक प्रिंटआउट।": {
    "en": "• Fill today's DPR sheet with worker names, phone, work area, ward and activity. Office DPR Monitoring • Status of all 21 sites' daily DPR sheets, 7:30 PM WhatsApp reminder and 1-click A4 printout.",
    "hi": "&bull; आज का दैनिक कार्य पर्चा (DPR) भरें। कारीगर, मोबाइल नंबर, कार्य क्षेत्र, वार्ड व कार्य विवरणी लिखकर सबमिट करें। कार्यालय DPR मॉनिटरिंग &bull; सभी 21 साइटों के दैनिक कार्य पर्चे (DPR Sheets) का स्टेटस, 7:30 PM रिमाइंडर व 1-क्लिक प्रिंटआउट।",
    "bi": "Daily DPR Sheet Submission & Monitoring (दैनिक कार्य पर्चा व कार्यालय मॉनिटरिंग)"
  },
  "• fill today's dpr sheet with worker names, phone, work area, ward and activity. office dpr monitoring • status of all 21 sites' daily dpr sheets, 7:30 pm whatsapp reminder and 1-click a4 printout.": {
    "en": "• Fill today's DPR sheet with worker names, phone, work area, ward and activity. Office DPR Monitoring • Status of all 21 sites' daily DPR sheets, 7:30 PM WhatsApp reminder and 1-click A4 printout.",
    "hi": "• आज का दैनिक कार्य पर्चा (DPR) भरें। कारीगर, मोबाइल नंबर, कार्य क्षेत्र, वार्ड व कार्य विवरणी लिखकर सबमिट करें। कार्यालय DPR मॉनिटरिंग • सभी 21 साइटों के दैनिक कार्य पर्चे (DPR Sheets) का स्टेटस, 7:30 PM रिमाइंडर व 1-क्लिक प्रिंटआउट।",
    "bi": "Daily DPR Sheet Submission & Monitoring (दैनिक कार्य पर्चा व कार्यालय मॉनिटरिंग)"
  },
  "daily dpr sheet submission & monitoring (दैनिक कार्य पर्चा व कार्यालय मॉनिटरिंग)": {
    "en": "• Fill today's DPR sheet with worker names, phone, work area, ward and activity. Office DPR Monitoring • Status of all 21 sites' daily DPR sheets, 7:30 PM WhatsApp reminder and 1-click A4 printout.",
    "hi": "• आज का दैनिक कार्य पर्चा (DPR) भरें। कारीगर, मोबाइल नंबर, कार्य क्षेत्र, वार्ड व कार्य विवरणी लिखकर सबमिट करें। कार्यालय DPR मॉनिटरिंग • सभी 21 साइटों के दैनिक कार्य पर्चे (DPR Sheets) का स्टेटस, 7:30 PM रिमाइंडर व 1-क्लिक प्रिंटआउट।",
    "bi": "Daily DPR Sheet Submission & Monitoring (दैनिक कार्य पर्चा व कार्यालय मॉनिटरिंग)"
  },
  "• आज का दैनिक कार्य पर्चा (dpr) भरें। कारीगर, मोबाइल नंबर, कार्य क्षेत्र, वार्ड व कार्य विवरणी लिखकर सबमिट करें। कार्यालय dpr मॉनिटरिंग • सभी 21 साइटों के दैनिक कार्य पर्चे (dpr sheets) का स्टेटस, 7:30 pm रिमाइंडर व 1-क्लिक प्रिंटआउट।": {
    "en": "• Fill today's DPR sheet with worker names, phone, work area, ward and activity. Office DPR Monitoring • Status of all 21 sites' daily DPR sheets, 7:30 PM WhatsApp reminder and 1-click A4 printout.",
    "hi": "• आज का दैनिक कार्य पर्चा (DPR) भरें। कारीगर, मोबाइल नंबर, कार्य क्षेत्र, वार्ड व कार्य विवरणी लिखकर सबमिट करें। कार्यालय DPR मॉनिटरिंग • सभी 21 साइटों के दैनिक कार्य पर्चे (DPR Sheets) का स्टेटस, 7:30 PM रिमाइंडर व 1-क्लिक प्रिंटआउट।",
    "bi": "Daily DPR Sheet Submission & Monitoring (दैनिक कार्य पर्चा व कार्यालय मॉनिटरिंग)"
  },
  "आज () का dpr पर्चा सुरक्षित है। आप चाहें तो और लाइनें जोड़ या सुधार सकते हैं।": {
    "en": "Today's DPR sheet is securely saved. You can add or edit lines if needed.",
    "hi": "आज () का DPR पर्चा सुरक्षित है। आप चाहें तो और लाइनें जोड़ या सुधार सकते हैं।",
    "bi": "Today's DPR sheet is securely saved (आज का DPR पर्चा सुरक्षित है)"
  },
  "today's dpr sheet is securely saved. you can add or edit lines if needed.": {
    "en": "Today's DPR sheet is securely saved. You can add or edit lines if needed.",
    "hi": "आज () का DPR पर्चा सुरक्षित है। आप चाहें तो और लाइनें जोड़ या सुधार सकते हैं।",
    "bi": "Today's DPR sheet is securely saved (आज का DPR पर्चा सुरक्षित है)"
  },
  "today's dpr sheet is securely saved (आज का dpr पर्चा सुरक्षित है)": {
    "en": "Today's DPR sheet is securely saved. You can add or edit lines if needed.",
    "hi": "आज () का DPR पर्चा सुरक्षित है। आप चाहें तो और लाइनें जोड़ या सुधार सकते हैं।",
    "bi": "Today's DPR sheet is securely saved (आज का DPR पर्चा सुरक्षित है)"
  }
},

    /**
     * Resolves a string into the target language.
     * Guarantees 0 mixing in 'en' and 'hi', and clean dual output in 'bi'.
     * NEVER does partial substring replacement on words (eliminates 'Lowटी', 'टेक्निYesterday', etc.)
     */
    resolveString: function(str, targetLang) {
        if (!str || typeof str !== 'string') return str;
        let raw = str.trim();
        if (!raw) return str;

        // Clean common HTML entities
        raw = raw.replace(/&mdash;/g, '—').replace(/&bull;/g, '•').replace(/&amp;/g, '&');

        // Skip purely numeric, symbols, currency, dates
        if (/^[₹\$\d\s\-\/:\,\.\%\(\)\#\@\+]+$/.test(raw)) {
            return str;
        }

        // Extract leading emoji/icon/bullet
        const prefixMatch = raw.match(/^([^\w\s\u0900-\u097F]+[\s]*)/);
        const prefix = prefixMatch ? prefixMatch[1] : "";
        let body = raw.substring(prefix.length).trim();

        // Extract trailing punctuation (* or :)
        const suffixMatch = body.match(/([\s]*[\*\:]+)$/);
        const suffix = suffixMatch ? suffixMatch[1] : "";
        if (suffix) {
            body = body.substring(0, body.length - suffix.length).trim();
        }

        if (!body) return str;

        // 1. Direct O(1) Map Lookup by exact body (case-insensitive)
        const normKey = body.toLowerCase();
        if (this.dictMap[normKey]) {
            return prefix + this.dictMap[normKey][targetLang] + suffix;
        }

        // Also check raw directly
        const rawNorm = raw.toLowerCase();
        if (this.dictMap[rawNorm]) {
            return this.dictMap[rawNorm][targetLang];
        }

        const hasDev = /[\u0900-\u097F]/.test(body);
        const hasLat = /[A-Za-z]/.test(body);

        // 2. Intelligent Multi-Script Parser for mixed elements
        if (hasDev && hasLat) {
            // A. PARENTHESIS FIRST: "Part1 (Part2)" or "Part1 [Part2]"
            const parenMatch = body.match(/^(.*?)\s*[\(\[](.*?)[\)\]]$/);
            if (parenMatch) {
                const p1 = parenMatch[1].trim();
                const p2 = parenMatch[2].trim();
                const countMatch = p2.match(/(\d+)/);
                const countStr = countMatch ? (" (" + countMatch[1] + ")") : "";

                const p1HasDev = /[\u0900-\u097F]/.test(p1);
                const p2HasDev = /[\u0900-\u097F]/.test(p2);
                const p1HasLat = /[A-Za-z]/.test(p1);
                const p2HasLat = /[A-Za-z]/.test(p2);

                // Case: p1 has Latin (e.g. "Work Area", "Open", "Print DPR"), p2 has Devanagari
                if (p1HasLat && p2HasDev) {
                    let cleanLat = p1;
                    if (p1HasDev) {
                        cleanLat = p1.replace(/[\u0900-\u097F\s\/\-\:]+/g, '').trim();
                    }
                    if (cleanLat) {
                        if (targetLang === 'en') return prefix + cleanLat + countStr + suffix;
                        if (targetLang === 'hi') return prefix + p2 + suffix;
                        return prefix + cleanLat + " (" + p2 + ")" + suffix;
                    }
                }

                // Case: p1 has Devanagari, p2 has Latin (e.g. "सामान की कमी (Material Shortage)")
                if (p1HasDev && p2HasLat && !p2HasDev) {
                    if (targetLang === 'en') return prefix + p2 + suffix;
                    if (targetLang === 'hi') return prefix + p1 + suffix;
                    return prefix + p2 + " (" + p1 + ")" + suffix;
                }
            }

            // B. DASH SEPARATOR: "Part1 — Part2" or "Part1 - Part2"
            const dashMatch = body.match(/^(.*?)\s*[\—\–]\s*(.*?)$/);
            if (dashMatch) {
                const p1 = dashMatch[1].trim();
                const p2 = dashMatch[2].trim();
                const p1HasLat = /[A-Za-z]/.test(p1);
                const p2HasLat = /[A-Za-z]/.test(p2);

                if (p1HasLat && !p2HasLat) {
                    if (targetLang === 'en') return prefix + p1 + suffix;
                    if (targetLang === 'hi') return prefix + p2 + suffix;
                    return prefix + p1 + " (" + p2 + ")" + suffix;
                } else if (!p1HasLat && p2HasLat) {
                    if (targetLang === 'en') return prefix + p2 + suffix;
                    if (targetLang === 'hi') return prefix + p1 + suffix;
                    return prefix + p2 + " (" + p1 + ")" + suffix;
                }
            }

            // C. SLASH SEPARATOR: "Part1 / Part2" (only if no parentheses)
            const slashMatch = body.match(/^([^\(\)]*?)\s*[\/]\s*([^\(\)]*?)$/);
            if (slashMatch) {
                const p1 = slashMatch[1].trim();
                const p2 = slashMatch[2].trim();
                const p1HasLat = /[A-Za-z]/.test(p1);
                const p2HasLat = /[A-Za-z]/.test(p2);

                if (p1HasLat && !p2HasLat) {
                    if (targetLang === 'en') return prefix + p1 + suffix;
                    if (targetLang === 'hi') return prefix + p2 + suffix;
                    return prefix + p1 + " (" + p2 + ")" + suffix;
                } else if (!p1HasLat && p2HasLat) {
                    if (targetLang === 'en') return prefix + p2 + suffix;
                    if (targetLang === 'hi') return prefix + p1 + suffix;
                    return prefix + p2 + " (" + p1 + ")" + suffix;
                }
            }

            // D. UNIVERSAL STRIP: In 'en', strip any remaining bracketed or trailing Devanagari
            if (targetLang === 'en') {
                let stripped = body.replace(/\s*[\(\[][\u0900-\u097F\s\/\-\.\&\+\:]+[\)\]]/g, '').trim();
                stripped = stripped.replace(/\s*\/[\s\u0900-\u097F\s\/\-\.\&\+\:]+$/g, '').trim();
                if (stripped && /[A-Za-z]/.test(stripped) && !/[\u0900-\u097F]/.test(stripped)) {
                    return prefix + stripped + suffix;
                }
            } else if (targetLang === 'hi') {
                let stripped = body.replace(/\s*[\(\[][A-Za-z\s\/\-\.\&\+\:]+[\)\]]/g, '').trim();
                stripped = stripped.replace(/\s*\/[\sA-Za-z\s\/\-\.\&\+\:]+$/g, '').trim();
                if (stripped && /[\u0900-\u097F]/.test(stripped) && !/[A-Za-z]/.test(stripped)) {
                    return prefix + stripped + suffix;
                }
            }
        }

        // 3. Fallbacks: If pure language, keep as is
        if (targetLang === 'en' && !hasDev) return str;
        if (targetLang === 'hi' && !hasLat) return str;

        return str;
    },

    /**
     * Apply active language across the entire document
     */
    applyLanguage: function(lang) {
        if (!lang) lang = this.currentLang;
        if (lang !== 'en' && lang !== 'hi' && lang !== 'bi') lang = 'en';

        this.currentLang = lang;
        if (typeof localStorage !== 'undefined') {
            localStorage.setItem('sandip_app_lang', lang);
        }

        // 1. Direct data-i18n elements
        const dict = this.dictionary[lang] || this.dictionary['en'];
        if (typeof document !== 'undefined') {
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
        }

        // 5. Broadcast language change event
        if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('appLanguageChanged', { detail: { lang } }));
        }
    },

    /**
     * Update active button styles in Topbar and Sidebar
     */
    updateButtons: function(lang) {
        if (typeof document === 'undefined') return;

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
        if (typeof document === 'undefined') return;
        const root = rootNode || document.body;
        if (!root) return;

        // Translate SELECT options
        root.querySelectorAll('option').forEach(opt => {
            if (opt._origText === undefined) opt._origText = opt.textContent;
            const translated = this.resolveString(opt._origText, targetLang);
            if (translated && opt.textContent !== translated) {
                opt.textContent = translated;
            }
        });

        // TreeWalker for all text nodes
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    const tag = parent.tagName.toLowerCase();
                    if (tag === 'script' || tag === 'style' || tag === 'textarea' || tag === 'input' || tag === 'option') return NodeFilter.FILTER_REJECT;
                    if (parent.closest('#prominentLangSwitcher') || parent.closest('.sidebar-lang-pill-container') || parent.closest('#langSwitchToast')) return NodeFilter.FILTER_REJECT;
                    if (parent.hasAttribute('data-i18n')) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let node;
        while (node = walker.nextNode()) {
            let val = node.nodeValue;
            if (!val || val.trim().length === 0) continue;

            if (node._origValue === undefined) {
                node._origValue = val;
            }

            const translated = this.resolveString(node._origValue, targetLang);
            if (translated && node.nodeValue !== translated) {
                node.nodeValue = translated;
            }
        }
    },

    /**
     * Translate placeholders, titles, and alt text across all elements
     */
    translateAttributes: function(targetLang, rootNode) {
        if (typeof document === 'undefined') return;
        const root = rootNode || document;

        root.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
            if (el._origPlaceholder === undefined) el._origPlaceholder = el.getAttribute('placeholder');
            const translated = this.resolveString(el._origPlaceholder, targetLang);
            if (translated) el.setAttribute('placeholder', translated);
        });

        root.querySelectorAll('[title]').forEach(el => {
            if (el._origTitle === undefined) el._origTitle = el.getAttribute('title');
            const translated = this.resolveString(el._origTitle, targetLang);
            if (translated) el.setAttribute('title', translated);
        });
    },

    /**
     * Setup MutationObserver for dynamically added elements (like modals & supervisor rows)
     */
    setupObserver: function() {
        if (typeof MutationObserver === 'undefined' || typeof document === 'undefined') return;
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

        if (document.body) {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
    },

    /**
     * Show toast feedback
     */
    showToast: function(msg) {
        if (typeof document === 'undefined') return;
        let toast = document.getElementById('langSwitchToast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'langSwitchToast';
            toast.className = 'fixed top-20 left-1/2 transform -translate-x-1/2 bg-slate-900/95 border-2 border-emerald-400 text-white px-5 py-2.5 rounded-2xl shadow-2xl z-50 text-xs font-bold flex items-center gap-2 transition-all duration-300';
            document.body.appendChild(toast);
        }
        toast.innerHTML = `<i class="fa-solid fa-language text-emerald-300 text-base"></i> <span>${msg}</span>`;
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
