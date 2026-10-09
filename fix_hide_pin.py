# -*- coding: utf-8 -*-
"""
Remove any user-visible leak of the secret PIN 7808 from all messages, alerts, and buttons.
The PIN 7808 must remain 100% secret in validation only!
"""

def fix_app_py():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Hide PIN from delete error message
    old_del_msg = '❌ गलत पिन! केवल मालिक (PIN: 7808) ही एंट्री डिलीट कर सकते हैं।'
    new_del_msg = '❌ गलत पिन! केवल अधिकृत मालिक ही एंट्री डिलीट कर सकते हैं।'
    content = content.replace(old_del_msg, new_del_msg)

    # Hide PIN from login error message
    old_login_msg = '❌ गलत पिन! केवल मालिक (PIN: 7808) ही लॉगिन कर सकते हैं।'
    new_login_msg = '❌ गलत पिन! केवल अधिकृत मालिक ही लॉगिन कर सकते हैं।'
    content = content.replace(old_login_msg, new_login_msg)

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.py: Secret PIN removed from error messages!")

def fix_site_report():
    with open('templates/site_report.html', 'r', encoding='utf-8') as f:
        content = f.read()

    old_prompt = 'कृपया मालिक PIN (7808) डालें:'
    new_prompt = 'कृपया मालिक PIN डालें:'
    content = content.replace(old_prompt, new_prompt)

    with open('templates/site_report.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("site_report.html: Secret PIN removed from prompt!")

def fix_base_html():
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace any button text or comments
    content = content.replace('मालिक मोड (PIN: 7808)', 'मालिक लॉगिन')
    content = content.replace('(PIN: 7808)', '')

    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("base.html: Secret PIN removed from UI labels!")

def fix_standalone():
    with open('generate_standalone_package.py', 'r', encoding='utf-8') as f:
        content = f.read()

    old_prompt = 'कृपया मालिक PIN (7808) डालें:'
    new_prompt = 'कृपया मालिक PIN डालें:'
    content = content.replace(old_prompt, new_prompt)

    with open('generate_standalone_package.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("generate_standalone_package.py: Secret PIN removed from prompt!")

if __name__ == '__main__':
    fix_app_py()
    fix_site_report()
    fix_base_html()
    fix_standalone()
