# -*- coding: utf-8 -*-
with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to desktop nav
target_desktop = """                    <a href="{{ url_for('daily_entry') }}" class="px-3 py-2 rounded-md text-sm font-semibold bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm transition flex items-center gap-2">
                        <i class="fa-solid fa-plus-circle text-xs"></i> Roj Ka Entry
                    </a>"""

attendance_desktop_link = """                    <a href="{{ url_for('daily_entry') }}" class="px-3 py-2 rounded-md text-sm font-semibold bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm transition flex items-center gap-2">
                        <i class="fa-solid fa-plus-circle text-xs"></i> Roj Ka Entry
                    </a>
                    <a href="{{ url_for('attendance_view') }}" class="px-3 py-2 rounded-md text-sm font-bold bg-indigo-600 hover:bg-indigo-500 text-white shadow-sm transition flex items-center gap-1.5">
                        <i class="fa-solid fa-users-gear text-xs"></i> <span>हाजिरी (Manpower)</span>
                    </a>"""

# Add to mobile nav if exists
target_mobile = """            <a href="{{ url_for('daily_entry') }}" class="block px-3 py-2 rounded-md text-base font-medium text-white bg-emerald-600 hover:bg-emerald-500 transition">
                <i class="fa-solid fa-plus-circle mr-2"></i> Roj Ka Entry
            </a>"""

attendance_mobile_link = """            <a href="{{ url_for('daily_entry') }}" class="block px-3 py-2 rounded-md text-base font-medium text-white bg-emerald-600 hover:bg-emerald-500 transition">
                <i class="fa-solid fa-plus-circle mr-2"></i> Roj Ka Entry
            </a>
            <a href="{{ url_for('attendance_view') }}" class="block px-3 py-2 rounded-md text-base font-bold text-white bg-indigo-600 hover:bg-indigo-500 transition">
                <i class="fa-solid fa-users-gear mr-2"></i> हाजिरी (Daily Manpower)
            </a>"""

if target_desktop in content and 'attendance_view' not in content:
    content = content.replace(target_desktop, attendance_desktop_link, 1)

if target_mobile in content:
    content = content.replace(target_mobile, attendance_mobile_link, 1)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("templates/base.html updated with Manpower / Attendance link!")
