/**
 * M/S SANDIP KUMAR - 21 Sites Material & Dispatch Tracker
 * Comprehensive Bilingual Translation Engine (Hindi <-> English)
 * 1-Tap Language Switcher controlled from the TAP ICON in UP LEFT
 */

const AppTranslations = {
    currentLang: localStorage.getItem('sandip_app_lang') || 'hi',

    // Full dictionary of phrase pairs (sorted by Hindi length descending)
    phrasePairs: [
    {
        "hi": "मैरवा, सीवान, छपरा, मधुबनी, दरभंगा सहित सभी 19 साइट्स पर रोज़ होने वाले सामग्री इस्तेमाल (पाइप, मोटर, केबल, फिटिंग) का हिसाब-किताब और दैनिक रिपोर्ट।",
        "en": "Track daily material usage (Pipes, Motors, Cables, Fittings) and generate reports across all 19 sites including Mairwa, Siwan, Chhapra, Madhubani, Darbhanga."
    },
    {
        "hi": "सीवान, मैरवा, छपरा, मधुबनी, दरभंगा सहित सभी 21 साइट्स पर रोज़ाना माल की खपत, साइट बैलेंस, हाजिरी और दैनिक व मासिक रिपोर्ट।",
        "en": "Daily material consumption, site balance, attendance, and daily & monthly reports across all 21 sites including Siwan, Mairwa, Chapra, Madhubani, Darbhanga."
    },
    {
        "hi": "PHED, RWD, DWSM, बैंक आदि विभागों को भेजे गए पत्रों की क्रमबद्ध पत्रांक संख्या (SK/YYYY-YY/0001) एवं प्रेषण विवरण।",
        "en": "Sequential reference numbers (SK/YYYY-YY/0001) and dispatch records of letters sent to PHED, RWD, DWSM, Banks, and other departments."
    },
    {
        "hi": "जैसे: हर घर नल का जल योजना के अंतर्गत पाइपलाइन कार्य एवं FHTC कनेक्शन की प्रगति रिपोर्ट समर्पित करने के संबंध में।",
        "en": "e.g. Submission of pipeline work and FHTC connection progress report under Har Ghar Nal Ka Jal Scheme."
    },
    {
        "hi": "जैसे: हस्तगत प्राप्त कराया / स्पीड पोस्ट संख्या: ED123456789IN / पावती संलग्न",
        "en": "e.g. Hand delivered / Speed Post ED123456789IN / Acknowledgment attached"
    },
    {
        "hi": "ऊपर दिए गए \"+ नया पत्रांक दर्ज करें\" बटन पर क्लिक करके पहला पत्र दर्ज करें।",
        "en": "Click \"+ New Letter Reference\" button above to record your first letter."
    },
    {
        "hi": "साइट पर आज कितना सामान लगा, तारीख और विवरण के साथ दर्ज करें",
        "en": "Record materials used at site today with date and details"
    },
    {
        "hi": "📑 विभिन्न विभागों को जावक पत्र (Outgoing Letters Register)",
        "en": "📑 Outgoing Letters Reference Register"
    },
    {
        "hi": "किसी भी साइट पर क्लिक करके उसका पूरा सामग्री लेजर देखें:",
        "en": "Click any site to view its complete material ledger:"
    },
    {
        "hi": "मिस्त्री, प्लंबर, हेल्पर व स्टाफ का 1-पेज हाजिरी रजिस्टर",
        "en": "1-Page attendance register for masons, plumbers, helpers, and staff"
    },
    {
        "hi": "जैसे: कार्यपालक अभियंता, लोक स्वास्थ्य प्रमंडल सीवान",
        "en": "e.g. Executive Engineer, PHED Siwan"
    },
    {
        "hi": "M/S SANDIP KUMAR • 21 Sites Live Project Tracker",
        "en": "M/S SANDIP KUMAR • 21 Sites Live Project Tracker"
    },
    {
        "hi": "M/S SANDIP KUMAR • 19 Sites Live Project Tracker",
        "en": "M/S SANDIP KUMAR • 19 Sites Live Project Tracker"
    },
    {
        "hi": "21 साइट्स पर दर्ज हुई अंतिम सामग्री प्रविष्टियाँ",
        "en": "Latest material usage entries recorded across 21 sites"
    },
    {
        "hi": "कोई प्रविष्टि नहीं मिली। नई प्रविष्टि दर्ज करें।",
        "en": "No entries found. Record new daily entry."
    },
    {
        "hi": "विभाग, स्थान, पत्रांक संख्या या विषय से खोजें...",
        "en": "Search by department, place, ref number, or subject..."
    },
    {
        "hi": "4-फोटो सरकारी A4 शीट डाउनलोड (GPS व तारीख सहित)",
        "en": "Download 4-photo official A4 sheet (with GPS & date)"
    },
    {
        "hi": "पत्र का उद्देश्य / विषय (Purpose of the Letter)",
        "en": "Purpose of the Letter / Subject"
    },
    {
        "hi": "अभी तक कोई मटेरियल इस्तेमाल दर्ज नहीं हुआ है।",
        "en": "No material consumption recorded yet."
    },
    {
        "hi": "21 साइट्स मैन्युअल हाजिरी शीट (मुख्य रजिस्टर)",
        "en": "21 Sites Manual Attendance Sheet (Main Register)"
    },
    {
        "hi": "GPS ऑटोमैटिक हाजिरी व कार्य घंटे (500m दायरा)",
        "en": "GPS Automatic Attendance & Work Hours (500m Radius)"
    },
    {
        "hi": "दैनिक सामग्री इस्तेमाल एंट्री (Roj Ka Kharch)",
        "en": "Daily Material Usage Entry"
    },
    {
        "hi": "दैनिक, मासिक और साइट-वार सम्पूर्ण लेजर हिसाब",
        "en": "Comprehensive daily, monthly, and site-wise ledger accounting"
    },
    {
        "hi": "पत्र का उद्देश्य / विषय (Purpose of Letter)",
        "en": "Purpose of Letter / Subject"
    },
    {
        "hi": "टिप्पणी / प्रेषण विवरण (Remarks / Dispatch)",
        "en": "Remarks / Dispatch Details"
    },
    {
        "hi": "हाल ही की प्रविष्टियाँ (Recent Usage Logs)",
        "en": "Recent Usage Logs"
    },
    {
        "hi": "भेजा गया माल, दैनिक खपत और बचा हुआ बैलेंस",
        "en": "Dispatched goods, daily consumption, and remaining balance"
    },
    {
        "hi": "स्थान का नाम लिखें (जैसे: सीवान / पटना)",
        "en": "Enter place name (e.g., Siwan / Patna)"
    },
    {
        "hi": "अभी तक कोई जावक पत्र दर्ज नहीं हुआ है।",
        "en": "No outgoing letters recorded yet."
    },
    {
        "hi": "दैनिक कार्य प्रगति (पाइपलाइन, FHTC नल)",
        "en": "Daily Work Progress (Pipeline, FHTC Tap)"
    },
    {
        "hi": "जावक पत्रांक पंजी (Letters Register)",
        "en": "Letters Register (Outgoing)"
    },
    {
        "hi": "टिप्पणी (Remarks / Dispatch Details)",
        "en": "Remarks / Dispatch Details"
    },
    {
        "hi": "📝 1. मैन्युअल हाजिरी (21 साइट्स शीट)",
        "en": "📝 1. Manual Attendance (21 Sites Sheet)"
    },
    {
        "hi": "पत्रांक रजिस्टर (Dispatch Register)",
        "en": "Dispatch & Reference Register"
    },
    {
        "hi": "नल आइकन (Tap) पर दबाकर कभी भी बदलें",
        "en": "Tap the faucet icon anytime to switch language"
    },
    {
        "hi": "रिपोर्ट्स केंद्र (Daily & Monthly)",
        "en": "Reports Hub (Daily & Monthly)"
    },
    {
        "hi": "साइट फोटो व A4 एल्बम (Site Photos)",
        "en": "Site Photos & A4 Album"
    },
    {
        "hi": "साइट फोटो व सरकारी 4-फोटो A4 एल्बम",
        "en": "Site Photos & Official 4-Photo A4 Album"
    },
    {
        "hi": "विभाग का नाम (Name of Department)",
        "en": "Name of Department"
    },
    {
        "hi": "तारीख-वार लेजर (Date-wise Ledger)",
        "en": "Date-wise Stock Ledger"
    },
    {
        "hi": "विवरण / कहाँ लगाया गया (Remarks):",
        "en": "Work Purpose / Remarks:"
    },
    {
        "hi": "+ अन्य स्थान (Type Custom Place)",
        "en": "+ Type Custom Place"
    },
    {
        "hi": "साइट स्टॉक व बैलेंस (Site Stock)",
        "en": "Site Stock & Balance"
    },
    {
        "hi": "पत्रांक पंजी (Letters Register)",
        "en": "Letters Register"
    },
    {
        "hi": "स्थान / साइट (Place / Location)",
        "en": "Place / Location"
    },
    {
        "hi": "DPR कार्य प्रगति (पाइपलाइन, नल)",
        "en": "DPR Work Progress (Pipeline, FHTC)"
    },
    {
        "hi": "21 Construction Sites Overview",
        "en": "21 Construction Sites Overview"
    },
    {
        "hi": "Daily Consumption Entry Dalein",
        "en": "Add Daily Consumption Entry"
    },
    {
        "hi": "वित्तीय वर्ष (Financial Year):",
        "en": "Financial Year:"
    },
    {
        "hi": "पत्रांक संख्या (Reference No.)",
        "en": "Reference Number"
    },
    {
        "hi": "सामग्री खपत एवं साइट ट्रैकिंग",
        "en": "Material Consumption & Site Tracking"
    },
    {
        "hi": "पत्रांक पंजी (Dispatch Entry)",
        "en": "Letter Reference Entry"
    },
    {
        "hi": "Android ऐप (APK) डाउनलोड करें",
        "en": "Download Android App (APK)"
    },
    {
        "hi": "📍 2. GPS हाजिरी (जियो-लोकेशन)",
        "en": "📍 2. GPS Attendance (Geo-Location)"
    },
    {
        "hi": "दैनिक सामग्री इस्तेमाल एंट्री",
        "en": "Daily Material Consumption Entry"
    },
    {
        "hi": "विभिन्न विभागों को जावक पत्र",
        "en": "Outgoing Letters Reference Register"
    },
    {
        "hi": "सुपरवाइज़र व वर्कर मोबाइल ऐप",
        "en": "Supervisor & Worker Mobile App"
    },
    {
        "hi": "भाषा चुनें / Select Language",
        "en": "Select Language / भाषा चुनें"
    },
    {
        "hi": "साइट स्टॉक और बैलेंस रजिस्टर",
        "en": "Site Stock & Balance Register"
    },
    {
        "hi": "🚰 DPR प्रगति (पाइपलाइन, नल)",
        "en": "🚰 DPR Progress (Pipeline, FHTC)"
    },
    {
        "hi": "साइट स्टॉक व बैलेंस रजिस्टर",
        "en": "Site Stock & Balance Register"
    },
    {
        "hi": "नया जावक पत्रांक दर्ज करें",
        "en": "Record New Outgoing Letter Reference"
    },
    {
        "hi": "पत्रांक विवरण संपादित करें",
        "en": "Edit Letter Reference Details"
    },
    {
        "hi": "मुख्य कार्य (Main Actions)",
        "en": "Main Actions"
    },
    {
        "hi": "दैनिक एंट्री (Daily Entry)",
        "en": "Daily Entry"
    },
    {
        "hi": "साइट पर आज कितना सामान लगा",
        "en": "Record materials used at site today"
    },
    {
        "hi": "👥 दैनिक हाजिरी (Manpower)",
        "en": "👥 Daily Manpower Attendance"
    },
    {
        "hi": "📸 साइट कार्य फोटो व एल्बम",
        "en": "📸 Site Work Photos & Album"
    },
    {
        "hi": "📊 रिपोर्ट्स व लेजर केंद्र",
        "en": "📊 Reports & Ledger Hub"
    },
    {
        "hi": "जावक पत्र पत्रांक रजिस्टर",
        "en": "Outgoing Letters Reference Register"
    },
    {
        "hi": "विभाग का नाम (Department)",
        "en": "Department Name"
    },
    {
        "hi": "अन्य लिंक्स (Quick Links)",
        "en": "Quick Links"
    },
    {
        "hi": "दैनिक मैन्युअल हाजिरी शीट",
        "en": "Daily Manual Attendance Sheet"
    },
    {
        "hi": "नया माल भेजें (स्टॉक आवक)",
        "en": "Dispatch Inward Stock"
    },
    {
        "hi": "ऑफलाइन (स्थानीय सुरक्षित)",
        "en": "Offline (Saved locally)"
    },
    {
        "hi": "पत्रांक संख्या (Ref No.)",
        "en": "Reference Number"
    },
    {
        "hi": "-- साइट / स्थान चुनें --",
        "en": "-- Select Site / Place --"
    },
    {
        "hi": "+ नया पत्रांक दर्ज करें",
        "en": "+ New Letter Reference"
    },
    {
        "hi": "पत्रांक संख्या (Ref No)",
        "en": "Reference Number"
    },
    {
        "hi": "पत्र का उद्देश्य / विषय",
        "en": "Purpose / Subject of Letter"
    },
    {
        "hi": "पत्र का विषय / उद्देश्य",
        "en": "Subject / Purpose of Letter"
    },
    {
        "hi": "कुल दैनिक प्रविष्टियाँ",
        "en": "Total Daily Entries"
    },
    {
        "hi": "Top Consumed Materials",
        "en": "Top Consumed Materials"
    },
    {
        "hi": "पहला पत्रांक दर्ज करें",
        "en": "Record First Letter Reference"
    },
    {
        "hi": "जावक पत्र पत्रांक पंजी",
        "en": "Outgoing Letters Dispatch & Reference Register"
    },
    {
        "hi": "सभी वित्तीय वर्ष (All)",
        "en": "All Financial Years"
    },
    {
        "hi": "टिप्पणी / प्रेषण विवरण",
        "en": "Remarks / Dispatch Details"
    },
    {
        "hi": "सभी विकल्प (More Menu)",
        "en": "All Options (More Menu)"
    },
    {
        "hi": "बचा हुआ स्टॉक (बैलेंस)",
        "en": "Balance Stock"
    },
    {
        "hi": "नई प्रविष्टि दर्ज करें",
        "en": "Record New Entry"
    },
    {
        "hi": "पत्रांक सुरक्षित करें",
        "en": "Save Reference Number"
    },
    {
        "hi": "GPS हाजिरी (500M ऑटो)",
        "en": "GPS Attendance (500m Auto)"
    },
    {
        "hi": "पूरा सिस्टम हिंदी में",
        "en": "Complete system in Hindi"
    },
    {
        "hi": "कुल भेजा गया (Inward)",
        "en": "Total Inward"
    },
    {
        "hi": "साइट पर शेष (Balance)",
        "en": "Balance on Site"
    },
    {
        "hi": "📦 साइट स्टॉक व स्टोर",
        "en": "📦 Site Stock & Store"
    },
    {
        "hi": "दिनांक (Letter Date)",
        "en": "Letter Date"
    },
    {
        "hi": "स्थान / साइट (Place)",
        "en": "Place / Site"
    },
    {
        "hi": "नई दैनिक एंट्री करें",
        "en": "New Daily Entry"
    },
    {
        "hi": "दैनिक हाजिरी (67-72)",
        "en": "Daily Attendance (67-72)"
    },
    {
        "hi": "21 साइट्स डायरेक्टरी",
        "en": "21 Sites Directory"
    },
    {
        "hi": "डैशबोर्ड (Dashboard)",
        "en": "Dashboard"
    },
    {
        "hi": "हाजिरी सुरक्षित करें",
        "en": "Save Attendance"
    },
    {
        "hi": "स्टॉक 0 करें (Reset)",
        "en": "Reset Stock to 0"
    },
    {
        "hi": "तारीख-वार लेजर देखें",
        "en": "View Date-wise Ledger"
    },
    {
        "hi": "कुल खर्च (दैनिक खपत)",
        "en": "Total Consumed"
    },
    {
        "hi": "आज कितनी मात्रा लगी:",
        "en": "Quantity Used Today:"
    },
    {
        "hi": "एंट्री सुरक्षित करें",
        "en": "Save Entry"
    },
    {
        "hi": "दैनिक रिपोर्ट देखें",
        "en": "View Daily Report"
    },
    {
        "hi": "मटेरियल स्टोर (+ऐड)",
        "en": "Material Store (+Add)"
    },
    {
        "hi": "📑 जावक पत्रांक पंजी",
        "en": "📑 Letters Register"
    },
    {
        "hi": "बदलाव सुरक्षित करें",
        "en": "Save Changes"
    },
    {
        "hi": "संपादित करें (Edit)",
        "en": "Edit"
    },
    {
        "hi": "📍 साइट GPS सेट करें",
        "en": "📍 Set Site GPS"
    },
    {
        "hi": "सामग्री कैटलॉग व दर",
        "en": "Material Catalog & Rates"
    },
    {
        "hi": "रिपोर्ट्स (Reports)",
        "en": "Reports"
    },
    {
        "hi": "साइट स्टॉक व बैलेंस",
        "en": "Site Stock & Balance"
    },
    {
        "hi": "लॉगिन करें (Unlock)",
        "en": "Login (Unlock)"
    },
    {
        "hi": "क्र. सं. (Sl. No.)",
        "en": "Sl. No."
    },
    {
        "hi": "रद्द करें (Cancel)",
        "en": "Cancel"
    },
    {
        "hi": "पूरा बैकअप डाउनलोड",
        "en": "Download Full Backup"
    },
    {
        "hi": "कुल भेजा गया (आवक)",
        "en": "Total Inward"
    },
    {
        "hi": "दैनिक कार्य प्रगति",
        "en": "Daily Work Progress"
    },
    {
        "hi": "ऑनलाइन (लाइव सिंक)",
        "en": "Online (Live Sync)"
    },
    {
        "hi": "जावक पत्रांक पंजी",
        "en": "Outgoing Letters Register"
    },
    {
        "hi": "टिप्पणी (Remarks)",
        "en": "Remarks"
    },
    {
        "hi": "पत्रांक कॉपी करें",
        "en": "Copy Reference Number"
    },
    {
        "hi": "📍 लोकेशन सेट करें",
        "en": "📍 Set Location"
    },
    {
        "hi": "GPS हाजिरी मॉनिटर",
        "en": "GPS Attendance Monitor"
    },
    {
        "hi": "📸 फोटो अपलोड करें",
        "en": "📸 Upload Photos"
    },
    {
        "hi": "📝 मैन्युअल हाजिरी",
        "en": "📝 Manual Attendance"
    },
    {
        "hi": "अंतिम लोकेशन पिंग",
        "en": "Last Location Ping"
    },
    {
        "hi": "दैनिक सामग्री खपत",
        "en": "Daily Material Usage"
    },
    {
        "hi": "सभी वित्तीय वर्ष",
        "en": "All Financial Years"
    },
    {
        "hi": "पत्र का उद्देश्य",
        "en": "Purpose of Letter"
    },
    {
        "hi": "कुल पत्र संख्या:",
        "en": "Total Letters:"
    },
    {
        "hi": "पेज रिफ्रेश करें",
        "en": "Refresh Page"
    },
    {
        "hi": "आपकी अधिकृत साइट",
        "en": "Your Authorized Site"
    },
    {
        "hi": "नई एंट्री जोड़ें",
        "en": "Add New Entry"
    },
    {
        "hi": "DPR कार्य प्रगति",
        "en": "DPR Work Progress"
    },
    {
        "hi": "कुल संचयी प्रगति",
        "en": "Total Cumulative Progress"
    },
    {
        "hi": "Fixed Rate List",
        "en": "Fixed Rate List"
    },
    {
        "hi": "Estimated Usage",
        "en": "Estimated Usage"
    },
    {
        "hi": "रिपोर्ट्स खोलें",
        "en": "Open Reports"
    },
    {
        "hi": "पत्रांक रजिस्टर",
        "en": "Reference Register"
    },
    {
        "hi": "पूरा डेटा बैकअप",
        "en": "Complete Data Backup"
    },
    {
        "hi": "मैन्युअल हाजिरी",
        "en": "Manual Attendance"
    },
    {
        "hi": "हाजिरी सेव करें",
        "en": "Save Attendance"
    },
    {
        "hi": "कुल खर्च (Used)",
        "en": "Total Consumed"
    },
    {
        "hi": "FHTC नल कनेक्शन",
        "en": "FHTC Tap Connections"
    },
    {
        "hi": "जलमीनार निर्माण",
        "en": "Water Tower Construction"
    },
    {
        "hi": "श्रेणी / प्रकार",
        "en": "Category / Type"
    },
    {
        "hi": "सामग्री कैटलॉग",
        "en": "Material Catalog"
    },
    {
        "hi": "कुल खर्च मूल्य",
        "en": "Total Consumption Value"
    },
    {
        "hi": "📑 पत्रांक पंजी",
        "en": "📑 Letters Register"
    },
    {
        "hi": "पत्रांक संख्या",
        "en": "Reference Number"
    },
    {
        "hi": "हटाएं (Delete)",
        "en": "Delete"
    },
    {
        "hi": "कुल जावक पत्र:",
        "en": "Total Outgoing Letters:"
    },
    {
        "hi": "कुल दर्ज पत्र:",
        "en": "Total Recorded Letters:"
    },
    {
        "hi": "हाजिरी रजिस्टर",
        "en": "Attendance Register"
    },
    {
        "hi": "तारीख-वार लेजर",
        "en": "Date-wise Ledger"
    },
    {
        "hi": "पर्याप्त स्टॉक",
        "en": "Healthy Stock"
    },
    {
        "hi": "कहाँ लगाया गया",
        "en": "Location / Purpose of Work"
    },
    {
        "hi": "पाइपलाइन खुदाई",
        "en": "Pipeline Trenching"
    },
    {
        "hi": "सामग्री का नाम",
        "en": "Material Name"
    },
    {
        "hi": "सामग्री चुनें:",
        "en": "Select Material:"
    },
    {
        "hi": "एक्सेल डाउनलोड",
        "en": "Download Excel"
    },
    {
        "hi": "Saved Records",
        "en": "Saved Records"
    },
    {
        "hi": "All Materials",
        "en": "All Materials"
    },
    {
        "hi": "मटेरियल स्टोर",
        "en": "Material Store"
    },
    {
        "hi": "सामग्री स्टोर",
        "en": "Material Store"
    },
    {
        "hi": "वित्तीय वर्ष:",
        "en": "Financial Year:"
    },
    {
        "hi": "अगला पत्रांक:",
        "en": "Next Ref No:"
    },
    {
        "hi": "दिनांक (Date)",
        "en": "Date"
    },
    {
        "hi": "स्थान (Place)",
        "en": "Place"
    },
    {
        "hi": "डाउनलोड तिथि:",
        "en": "Download Date:"
    },
    {
        "hi": "कंपनी वेबसाइट",
        "en": "Company Website"
    },
    {
        "hi": "मटेरियल लिस्ट",
        "en": "Material List"
    },
    {
        "hi": "सामग्री लिस्ट",
        "en": "Material List"
    },
    {
        "hi": "इलेक्ट्रीशियन",
        "en": "Electrician"
    },
    {
        "hi": "जीआई मिस्त्री",
        "en": "GI Mistri"
    },
    {
        "hi": "सेल्फी हाजिरी",
        "en": "Selfie Attendance"
    },
    {
        "hi": "स्टॉक रजिस्टर",
        "en": "Stock Register"
    },
    {
        "hi": "नया माल भेजें",
        "en": "Dispatch Inward Stock"
    },
    {
        "hi": "बचा हुआ स्टॉक",
        "en": "Balance Stock"
    },
    {
        "hi": "तारीख (Date):",
        "en": "Date:"
    },
    {
        "hi": "सभी 21 साइट्स",
        "en": "All 21 Sites"
    },
    {
        "hi": "सभी श्रेणियां",
        "en": "All Categories"
    },
    {
        "hi": "सामग्री चुनें",
        "en": "Select Material"
    },
    {
        "hi": "Excel डाउनलोड",
        "en": "Download Excel"
    },
    {
        "hi": "सुरक्षित करें",
        "en": "Save"
    },
    {
        "hi": "Total Value:",
        "en": "Total Value:"
    },
    {
        "hi": "पत्रांक पंजी",
        "en": "Letters Register"
    },
    {
        "hi": "क्र.सं. (Sl)",
        "en": "Sl. No."
    },
    {
        "hi": "विभाग का नाम",
        "en": "Department Name"
    },
    {
        "hi": "स्थान / साइट",
        "en": "Place / Location"
    },
    {
        "hi": "दैनिक एंट्री",
        "en": "Daily Entry"
    },
    {
        "hi": "📍 GPS हाजिरी",
        "en": "📍 GPS Attendance"
    },
    {
        "hi": "दैनिक हाजिरी",
        "en": "Daily Attendance"
    },
    {
        "hi": "साइट इनचार्ज",
        "en": "Site Incharge"
    },
    {
        "hi": "साइट से दूरी",
        "en": "Distance from Site"
    },
    {
        "hi": "वर्कर का नाम",
        "en": "Worker Name"
    },
    {
        "hi": "स्टॉक 0 करें",
        "en": "Reset Stock to 0"
    },
    {
        "hi": "कुल भेजा गया",
        "en": "Total Inward"
    },
    {
        "hi": "बैलेंस स्टॉक",
        "en": "Balance Stock"
    },
    {
        "hi": "बोरिंग कार्य",
        "en": "Boring Work"
    },
    {
        "hi": "तारीख (Date)",
        "en": "Date"
    },
    {
        "hi": "कुल राशि (₹)",
        "en": "Total Amount (₹)"
    },
    {
        "hi": "तारीख चुनें:",
        "en": "Select Date:"
    },
    {
        "hi": "फ़िल्टर करें",
        "en": "Filter"
    },
    {
        "hi": "संपादित करें",
        "en": "Edit"
    },
    {
        "hi": "स्टॉक खोलें",
        "en": "Open Stock"
    },
    {
        "hi": "गैलरी खोलें",
        "en": "Open Gallery"
    },
    {
        "hi": "त्वरित चयन:",
        "en": "Quick Select:"
    },
    {
        "hi": "साइट पोर्टल",
        "en": "Site Portal"
    },
    {
        "hi": "मालिक लॉगिन",
        "en": "Owner Login"
    },
    {
        "hi": "लॉगआउट करें",
        "en": "Logout"
    },
    {
        "hi": "डाटा एंट्री",
        "en": "Data Entry"
    },
    {
        "hi": "कुल मैनपावर",
        "en": "Total Manpower"
    },
    {
        "hi": "मोबाइल नंबर",
        "en": "Mobile Number"
    },
    {
        "hi": "पाइप बिछाना",
        "en": "Pipeline Laying"
    },
    {
        "hi": "आज का कार्य",
        "en": "Today's Work"
    },
    {
        "hi": "साइट का नाम",
        "en": "Site Name"
    },
    {
        "hi": "कार्य विवरण",
        "en": "Work Description"
    },
    {
        "hi": "साइट चुनें:",
        "en": "Select Site:"
    },
    {
        "hi": "तारीख चुनें",
        "en": "Select Date"
    },
    {
        "hi": "सामान खोजें",
        "en": "Search Material"
    },
    {
        "hi": "PDF डाउनलोड",
        "en": "Download PDF"
    },
    {
        "hi": "प्रिंट करें",
        "en": "Print"
    },
    {
        "hi": "हाजिरी शीट",
        "en": "Attendance Sheet"
    },
    {
        "hi": "फोटो अपलोड",
        "en": "Upload Photos"
    },
    {
        "hi": "सुपरवाइज़र",
        "en": "Supervisor"
    },
    {
        "hi": "साइट स्टॉक",
        "en": "Site Stock"
    },
    {
        "hi": "DPR प्रगति",
        "en": "DPR Progress"
    },
    {
        "hi": "फोटो एल्बम",
        "en": "Photo Album"
    },
    {
        "hi": "भाषा बदलें",
        "en": "Change Language"
    },
    {
        "hi": "कुल हाजिरी",
        "en": "Total Attendance"
    },
    {
        "hi": "कार्य घंटे",
        "en": "Work Hours"
    },
    {
        "hi": "लेजर देखें",
        "en": "View Ledger"
    },
    {
        "hi": "सभी साइट्स",
        "en": "All Sites"
    },
    {
        "hi": "साइट चुनें",
        "en": "Select Site"
    },
    {
        "hi": "अपडेट करें",
        "en": "Update"
    },
    {
        "hi": "लॉगिन करें",
        "en": "Login"
    },
    {
        "hi": "सुपरवाइजर",
        "en": "Supervisor"
    },
    {
        "hi": "रिपोर्ट्स",
        "en": "Reports"
    },
    {
        "hi": "21 साइट्स",
        "en": "21 Sites"
    },
    {
        "hi": "अनुपस्थित",
        "en": "Absent"
    },
    {
        "hi": "स्टॉक आवक",
        "en": "Stock Inward"
    },
    {
        "hi": "शेष स्टॉक",
        "en": "Remaining Stock"
    },
    {
        "hi": "दर्ज करें",
        "en": "Submit"
    },
    {
        "hi": "रद्द करें",
        "en": "Cancel"
    },
    {
        "hi": "क्र. सं.",
        "en": "Sl. No."
    },
    {
        "hi": "ऑटोमैटिक",
        "en": "Auto-Generated"
    },
    {
        "hi": "डैशबोर्ड",
        "en": "Dashboard"
    },
    {
        "hi": "मिस्त्री",
        "en": "Mason"
    },
    {
        "hi": "कुल खर्च",
        "en": "Total Consumed"
    },
    {
        "hi": "उपलब्ध %",
        "en": "Available %"
    },
    {
        "hi": "पर्याप्त",
        "en": "Healthy"
    },
    {
        "hi": "कम स्टॉक",
        "en": "Low Stock"
    },
    {
        "hi": "कुल राशि",
        "en": "Total Amount"
    },
    {
        "hi": "खोजें...",
        "en": "Search..."
    },
    {
        "hi": "बंद करें",
        "en": "Close"
    },
    {
        "hi": "उद्देश्य",
        "en": "Purpose"
    },
    {
        "hi": "सुरक्षित",
        "en": "Saved"
    },
    {
        "hi": "क्र.सं.",
        "en": "Sl. No."
    },
    {
        "hi": "👑 मालिक",
        "en": "👑 Owner"
    },
    {
        "hi": "उपस्थित",
        "en": "Present"
    },
    {
        "hi": "ऑन-साइट",
        "en": "On-Site"
    },
    {
        "hi": "ऑफ-साइट",
        "en": "Off-Site"
    },
    {
        "hi": "चेक-आउट",
        "en": "Check-Out"
    },
    {
        "hi": "जलमीनार",
        "en": "Water Tower"
    },
    {
        "hi": "परीक्षण",
        "en": "Hydro Testing"
    },
    {
        "hi": "सामग्री",
        "en": "Material"
    },
    {
        "hi": "दिनांक:",
        "en": "Date:"
    },
    {
        "hi": "मात्रा:",
        "en": "Quantity:"
    },
    {
        "hi": "कुल (₹)",
        "en": "Total (₹)"
    },
    {
        "hi": "टिप्पणी",
        "en": "Remarks"
    },
    {
        "hi": "फ़िल्टर",
        "en": "Filter"
    },
    {
        "hi": "डाउनलोड",
        "en": "Download"
    },
    {
        "hi": "मटेरियल",
        "en": "Material"
    },
    {
        "hi": "रिपोर्ट",
        "en": "Report"
    },
    {
        "hi": "रजिस्टर",
        "en": "Register"
    },
    {
        "hi": "एंट्रीज",
        "en": "Entries"
    },
    {
        "hi": "संपादित",
        "en": "Edit"
    },
    {
        "hi": "इनचार्ज",
        "en": "Incharge"
    },
    {
        "hi": "लॉगआउट",
        "en": "Logout"
    },
    {
        "hi": "प्लंबर",
        "en": "Plumber"
    },
    {
        "hi": "हेल्पर",
        "en": "Helper"
    },
    {
        "hi": "चेक-इन",
        "en": "Check-In"
    },
    {
        "hi": "बैलेंस",
        "en": "Balance"
    },
    {
        "hi": "लक्ष्य",
        "en": "Target"
    },
    {
        "hi": "श्रेणी",
        "en": "Category"
    },
    {
        "hi": "तारीख:",
        "en": "Date:"
    },
    {
        "hi": "दिनांक",
        "en": "Date"
    },
    {
        "hi": "मात्रा",
        "en": "Quantity"
    },
    {
        "hi": "दर (₹)",
        "en": "Rate (₹)"
    },
    {
        "hi": "स्थिति",
        "en": "Status"
    },
    {
        "hi": "साइट्स",
        "en": "Sites"
    },
    {
        "hi": "प्रिंट",
        "en": "Print"
    },
    {
        "hi": "ऑनलाइन",
        "en": "Online"
    },
    {
        "hi": "ऑफलाइन",
        "en": "Offline"
    },
    {
        "hi": "हाजिरी",
        "en": "Attendance"
    },
    {
        "hi": "प्रगति",
        "en": "Progress"
    },
    {
        "hi": "माहवार",
        "en": "Monthly"
    },
    {
        "hi": "सक्रिय",
        "en": "Active"
    },
    {
        "hi": "उपलब्ध",
        "en": "Available"
    },
    {
        "hi": "एंट्री",
        "en": "Entry"
    },
    {
        "hi": "जोड़ें",
        "en": "Add"
    },
    {
        "hi": "स्टोर",
        "en": "Store"
    },
    {
        "hi": "मालिक",
        "en": "Owner"
    },
    {
        "hi": "तारीख",
        "en": "Date"
    },
    {
        "hi": "विवरण",
        "en": "Description"
    },
    {
        "hi": "एक्शन",
        "en": "Actions"
    },
    {
        "hi": "खोजें",
        "en": "Search"
    },
    {
        "hi": "हटाएं",
        "en": "Delete"
    },
    {
        "hi": "स्टॉक",
        "en": "Stock"
    },
    {
        "hi": "दैनिक",
        "en": "Daily"
    },
    {
        "hi": "मासिक",
        "en": "Monthly"
    },
    {
        "hi": "लॉग्स",
        "en": "Logs"
    },
    {
        "hi": "सेकंड",
        "en": "Secs"
    },
    {
        "hi": "स्थान",
        "en": "Place"
    },
    {
        "hi": "विभाग",
        "en": "Department"
    },
    {
        "hi": "एल्बम",
        "en": "Album"
    },
    {
        "hi": "खोलें",
        "en": "Open"
    },
    {
        "hi": "देखें",
        "en": "View"
    },
    {
        "hi": "वर्कर",
        "en": "Worker"
    },
    {
        "hi": "स्टाफ",
        "en": "Staff"
    },
    {
        "hi": "फोटो",
        "en": "Photos"
    },
    {
        "hi": "लेजर",
        "en": "Ledger"
    },
    {
        "hi": "कुल:",
        "en": "Total:"
    },
    {
        "hi": "पत्र",
        "en": "Letters"
    },
    {
        "hi": "अधिक",
        "en": "More"
    },
    {
        "hi": "डीईओ",
        "en": "DEO"
    },
    {
        "hi": "अन्य",
        "en": "Other"
    },
    {
        "hi": "खत्म",
        "en": "Out of Stock"
    },
    {
        "hi": "इकाई",
        "en": "Unit"
    },
    {
        "hi": "साइट",
        "en": "Site"
    },
    {
        "hi": "पंजी",
        "en": "Register"
    },
    {
        "hi": "सूची",
        "en": "Directory"
    },
    {
        "hi": "घंटे",
        "en": "Hours"
    },
    {
        "hi": "मिनट",
        "en": "Mins"
    },
    {
        "hi": "विषय",
        "en": "Subject"
    },
    {
        "hi": "रद्द",
        "en": "Cancel"
    },
    {
        "hi": "एडिट",
        "en": "Edit"
    },
    {
        "hi": "आवक",
        "en": "Inward"
    },
    {
        "hi": "खपत",
        "en": "Consumed"
    },
    {
        "hi": "दर:",
        "en": "Rate:"
    },
    {
        "hi": "नाम",
        "en": "Name"
    },
    {
        "hi": "कोड",
        "en": "Code"
    },
    {
        "hi": "लॉग",
        "en": "Log"
    },
    {
        "hi": "कुल",
        "en": "Total"
    },
    {
        "hi": "सेव",
        "en": "Save"
    },
    {
        "hi": "ओपन",
        "en": "Open"
    },
    {
        "hi": "नया",
        "en": "New"
    },
    {
        "hi": "पद",
        "en": "Designation"
    },
    {
        "hi": "दर",
        "en": "Rate"
    },
    {
        "hi": "आज",
        "en": "Today"
    },
    {
        "hi": "कल",
        "en": "Yesterday"
    },
    {
        "hi": "कम",
        "en": "Low"
    },
    {
        "hi": "नई",
        "en": "New"
    }
],

    /**
     * Dictionary for direct data-i18n lookup
     */
        dictionary: {
        hi: {
            app_title: "M/S संदीप कुमार",
            app_subtitle: "२१ साइट्स",
            top_status: "२१ साइट्स चालू",
            top_user: "संदीप कुमार",
            top_role: "मालिक",
            sign_out: "लॉगआउट",

            // Sidebar Segments & Sub-items
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
            sub_sites: "साइट्स",
            sub_rates: "दरें",
            sub_gps_setup: "GPS सेटअप",
            sub_apk: "ऐप",
            sub_website: "वेबसाइट",
            sub_backup: "बैकअप",

            // Dashboard Header & Status
            dash_title: "डैशबोर्ड",
            dash_subtitle: "२१ साइट्स",
            dash_active_date: "दिनांक:",
            dash_status_title: "परियोजना स्थिति",
            dash_status_body: "२१ जलापूर्ति साइट्स चालू",
            dash_status_badge: "● सक्रिय",

            // Dashboard 6 Tiles
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

            // 4 Modules
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

            // Letters Section
            letters_heading: "जावक पत्र पंजी",
            letters_subheading: "विभिन्न विभागों को भेजे गए पत्रांक",
            btn_new_letter: "नया पत्र",
            col_sr: "क्र.",
            col_date: "दिनांक",
            col_ref: "पत्रांक संख्या",
            col_dept: "विभाग",
            col_place: "स्थान",
            col_purpose: "उद्देश्य",
            col_remarks: "रिमार्क्स",
            col_action: "कार्रवाई",

            // Recent Logs Section
            logs_heading: "हाल की खपत",
            logs_sub: "अंतिम सामग्री प्रविष्टियां",
            view_daily: "दैनिक रिपोर्ट",
            col_site: "साइट",
            col_item: "सामग्री",
            col_qty: "मात्रा",
            col_rate: "दर",
            col_val: "लागत (₹)",
            col_desc: "विवरण",

            // Dropdown & Language
            lang_selector_title: "भाषा चुनें / Select Language",
            lang_hi_title: "हिंदी (Hindi)",
            lang_hi_sub: "पूरा सिस्टम हिंदी में",
            lang_en_title: "English",
            lang_en_sub: "Complete system in English",
            lang_switch_toast_hi: "✅ भाषा बदलकर 'हिंदी' कर दी गई है।",
            lang_switch_toast_en: "✅ Language switched to 'English'."
        },
        en: {
            app_title: "M/S Sandip Kumar",
            app_subtitle: "21 Sites",
            top_status: "21 Sites Live",
            top_user: "Sandip Kumar",
            top_role: "Owner",
            sign_out: "Sign out",

            // Sidebar Segments & Sub-items
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
            sub_sites: "Sites",
            sub_rates: "Rates",
            sub_gps_setup: "GPS Setup",
            sub_apk: "App",
            sub_website: "Website",
            sub_backup: "Backup",

            // Dashboard Header & Status
            dash_title: "Dashboard",
            dash_subtitle: "21 Sites",
            dash_active_date: "Date:",
            dash_status_title: "Project Status",
            dash_status_body: "21 Water Supply Sites Live",
            dash_status_badge: "● Active",

            // Dashboard 6 Tiles
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

            // 4 Modules
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

            // Letters Section
            letters_heading: "Outgoing Letters",
            letters_subheading: "Letters dispatched to departments",
            btn_new_letter: "New Letter",
            col_sr: "Sr.",
            col_date: "Date",
            col_ref: "Ref No",
            col_dept: "Department",
            col_place: "Place",
            col_purpose: "Purpose",
            col_remarks: "Remarks",
            col_action: "Action",

            // Recent Logs Section
            logs_heading: "Recent Usage Logs",
            logs_sub: "Latest usage entries",
            view_daily: "Daily Report",
            col_site: "Site",
            col_item: "Material",
            col_qty: "Quantity",
            col_rate: "Rate",
            col_val: "Cost (₹)",
            col_desc: "Details",

            // Dropdown & Language
            lang_selector_title: "Select Language / भाषा चुनें",
            lang_hi_title: "हिंदी (Hindi)",
            lang_hi_sub: "Entire system in Hindi",
            lang_en_title: "English",
            lang_en_sub: "Complete system in English",
            lang_switch_toast_hi: "✅ भाषा बदलकर 'हिंदी' कर दी गई है।",
            lang_switch_toast_en: "✅ Language switched to 'English'."
        }
    },

    /**
     * Apply active language to the entire document
     */
    applyLanguage: function(lang) {
        if (!lang) lang = this.currentLang;
        if (lang !== 'hi' && lang !== 'en') lang = 'hi';

        this.currentLang = lang;
        localStorage.setItem('sandip_app_lang', lang);

        // 1. Direct data-i18n tags
        const dict = this.dictionary[lang] || {};
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

        // 2. Update visual display of TAP ICON in UP LEFT
        this.updateTapIconButton(lang);

        // 3. Walk all text nodes & translate untagged content
        this.walkAndTranslate(lang);

        // 4. Translate all attributes (placeholder, title, alt)
        this.translateAttributes(lang);

        // 5. Broadcast language change event
        window.dispatchEvent(new CustomEvent('appLanguageChanged', { detail: { lang } }));
    },

    /**
     * Update TAP ICON in UP LEFT
     */
    updateTapIconButton: function(lang) {
        // 1. Top Bar Prominent Direct Toggle
        const topHi = document.getElementById('topBtnLangHi');
        const topEn = document.getElementById('topBtnLangEn');
        if (topHi && topEn) {
            if (lang === 'hi') {
                topHi.className = 'px-2 sm:px-2.5 py-1 rounded-lg text-xs font-black transition flex items-center gap-1 bg-[#0A261F] text-amber-300 shadow-xs';
                topEn.className = 'px-2 sm:px-2.5 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1 text-slate-600 hover:text-slate-900';
            } else {
                topHi.className = 'px-2 sm:px-2.5 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1 text-slate-600 hover:text-slate-900';
                topEn.className = 'px-2 sm:px-2.5 py-1 rounded-lg text-xs font-black transition flex items-center gap-1 bg-[#0A261F] text-amber-300 shadow-xs';
            }
        }

        // 2. Sidebar Direct Toggle
        const sideHi = document.getElementById('sideBtnLangHi');
        const sideEn = document.getElementById('sideBtnLangEn');
        if (sideHi && sideEn) {
            if (lang === 'hi') {
                sideHi.className = 'px-2 py-0.5 rounded text-[10px] font-black transition bg-emerald-600 text-white';
                sideEn.className = 'px-2 py-0.5 rounded text-[10px] font-bold transition text-slate-400 hover:text-white';
            } else {
                sideHi.className = 'px-2 py-0.5 rounded text-[10px] font-bold transition text-slate-400 hover:text-white';
                sideEn.className = 'px-2 py-0.5 rounded text-[10px] font-black transition bg-emerald-600 text-white';
            }
        }
    },

    /**
     * Cache and return pairs sorted by search key length descending
     */
    getSortedPairs: function(targetLang) {
        if (!this._hiToEnPairs) {
            this._hiToEnPairs = [...this.phrasePairs].sort((a, b) => b.hi.length - a.hi.length);
            this._enToHiPairs = [...this.phrasePairs].sort((a, b) => b.en.length - a.en.length);
        }
        return targetLang === 'en' ? this._hiToEnPairs : this._enToHiPairs;
    },

    /**
     * Walk text nodes to translate content cleanly
     */
    walkAndTranslate: function(targetLang, rootNode) {
        const root = rootNode || document.body;
        if (!root) return;

        const pairs = this.getSortedPairs(targetLang);
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    const tag = parent.tagName.toLowerCase();
                    if (tag === 'script' || tag === 'style' || tag === 'textarea' || tag === 'input') return NodeFilter.FILTER_REJECT;
                    if (parent.closest('#tapLangContainer') || parent.closest('#tapLangDropdown')) return NodeFilter.FILTER_REJECT;
                    if (parent.closest('[data-i18n]')) return NodeFilter.FILTER_REJECT;
                    // Do not translate raw numbers or date patterns
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
                if (targetLang === 'en') {
                    if (val.includes(pair.hi)) {
                        val = val.replaceAll(pair.hi, pair.en);
                    }
                } else {
                    if (val.includes(pair.en)) {
                        val = val.replaceAll(pair.en, pair.hi);
                    }
                }
            }
            if (node.nodeValue !== val) {
                node.nodeValue = val;
            }
        }
    },

    /**
     * Translate placeholders, titles, and alt text across all elements
     */
    translateAttributes: function(targetLang, rootNode) {
        const root = rootNode || document;
        const pairs = this.getSortedPairs(targetLang);

        // Placeholders in inputs & textareas
        root.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
            let ph = el.getAttribute('placeholder');
            if (!ph) return;
            for (let i = 0; i < pairs.length; i++) {
                const pair = pairs[i];
                if (targetLang === 'en') {
                    if (ph.includes(pair.hi)) ph = ph.replaceAll(pair.hi, pair.en);
                } else {
                    if (ph.includes(pair.en)) ph = ph.replaceAll(pair.en, pair.hi);
                }
            }
            el.setAttribute('placeholder', ph);
        });

        // Tooltips / Titles
        root.querySelectorAll('[title]').forEach(el => {
            let title = el.getAttribute('title');
            if (!title) return;
            for (let i = 0; i < pairs.length; i++) {
                const pair = pairs[i];
                if (targetLang === 'en') {
                    if (title.includes(pair.hi)) title = title.replaceAll(pair.hi, pair.en);
                } else {
                    if (title.includes(pair.en)) title = title.replaceAll(pair.en, pair.hi);
                }
            }
            el.setAttribute('title', title);
        });

        // Option values in select elements
        root.querySelectorAll('select option').forEach(opt => {
            let txt = opt.textContent;
            if (!txt) return;
            for (let i = 0; i < pairs.length; i++) {
                const pair = pairs[i];
                if (targetLang === 'en') {
                    if (txt.includes(pair.hi)) txt = txt.replaceAll(pair.hi, pair.en);
                } else {
                    if (txt.includes(pair.en)) txt = txt.replaceAll(pair.en, pair.hi);
                }
            }
            opt.textContent = txt;
        });
    },

    /**
     * Setup MutationObserver to translate dynamically rendered elements (modals, AJAX)
     */
    setupObserver: function() {
        if (this._observer) return;
        const self = this;
        this._observer = new MutationObserver(mutations => {
            if (self.currentLang !== 'en') return;
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        self.walkAndTranslate('en', node);
                        self.translateAttributes('en', node);
                    }
                });
            });
        });

        this._observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    },

    /**
     * Show brief toast notification
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
    AppTranslations.setupObserver();
});

if (typeof window !== 'undefined') {
    window.AppTranslations = AppTranslations;
    window.setAppLanguage = setAppLanguage;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AppTranslations, setAppLanguage };
}
