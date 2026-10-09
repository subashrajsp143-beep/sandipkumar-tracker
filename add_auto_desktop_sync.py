# -*- coding: utf-8 -*-
"""
Patch app.py to automatically regenerate Desktop HTML on every new entry,
and provide /api/live-entries endpoint so Site_Material_Tracker.html can auto-sync live from server!
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. In save_entries, call build_standalone_package
old_save_end = '''        return jsonify({"success": True, "message": f"{added_count} material entries safalta-purvak save ho gayi hain!", "count": added_count})'''

new_save_end = '''        try:
            import generate_standalone_package
            generate_standalone_package.build_standalone_package()
        except Exception as gen_err:
            print("Auto-generate desktop package error:", gen_err)

        return jsonify({"success": True, "message": f"{added_count} material entries safalta-purvak save ho gayi hain!", "count": added_count})'''

# 2. Add /api/live-entries endpoint
route_target = '@app.route("/api/live-status", methods=["GET"])'
new_route = '''@app.route("/api/live-entries", methods=["GET", "OPTIONS"])
def get_live_entries_api():
    if request.method == "OPTIONS":
        return "", 200
    try:
        entries, _ = database.get_site_report()
        return jsonify({"success": True, "entries": entries})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

''' + route_target

if old_save_end in content:
    content = content.replace(old_save_end, new_save_end, 1)

if '@app.route("/api/live-entries"' not in content:
    content = content.replace(route_target, new_route, 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("app.py patched with automatic desktop sync and /api/live-entries endpoint!")
