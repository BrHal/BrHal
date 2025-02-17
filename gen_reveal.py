from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Données des hosts (à remplacer par une source dynamique si nécessaire)
hosts_data = [
    {
        "Name": "Host xx",
        "Hyp_address": "128.128.128.128",
        "VM_address": "129.129.129.129",
        "Components": [
            {"Version": "1.2.3", "Component": "extension1"},
            {"Version": "1.2.4", "Component": "base"}
        ]
    },
    {
        "Name": "Host yy",
        "Hyp_address": "130.130.130.130",
        "VM_address": "131.131.131.131",
        "Components": [
            {"Version": "4.2.6", "Component": "module1"},
            {"Version": "6.5.4", "Component": "base"}
        ]
    }
]

def generate_slides(hosts):
    slides = ""
    nav_links = ""
    for index, host in enumerate(hosts):
        base_component = next((c for c in host["Components"] if c["Component"] == "base"), None)
        base_version = base_component["Version"] if base_component else "N/A"
        slides += f"""
        <section>
            <h2>{host['Name']}</h2>
            <p><strong>Hyperviseur:</strong> {host['Hyp_address']}</p>
            <p><strong>VM:</strong> {host['VM_address']}</p>
            <p><strong>Version Base:</strong> {base_version}</p>
        </section>
        """
        nav_links += f"<a href='#' onclick='Reveal.slide({index + 1})'>{host['Name']}</a>"
    return slides, nav_links

slides_content, nav_content = generate_slides(hosts_data)

TEMPLATE = f"""<!DOCTYPE html>
<html lang=\"fr\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Présentation des Hosts</title>
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reset.min.css\">
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.css\">
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/theme/league.min.css\">
    <style>
        body { font-family: 'Arial', sans-serif; background: url('https://images.pexels.com/photos/442152/pexels-photo-442152.jpeg') no-repeat center center fixed; background-size: cover; }
        #host-nav { position: fixed; top: 10px; left: 10px; background: rgba(0, 50, 100, 0.8); color: white; padding: 15px; border-radius: 10px; z-index: 1000; box-shadow: 0 4px 8px rgba(0, 150, 255, 0.5); }
        #host-nav a { display: block; color: #00FFFF; text-decoration: none; margin: 10px 0; font-weight: bold; transition: color 0.3s ease; }
        #host-nav a:hover { color: #FFD700; }
        .slides section { text-align: center; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0, 150, 255, 0.5); background: rgba(0, 50, 100, 0.7); color: white; }
    </style>
</head>
<body>
    <div id=\"host-nav\">{nav_content}</div>
    <div class=\"reveal\">
        <div class=\"slides\">{slides_content}</div>
    </div>
    <script src=\"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.js\"></script>
    <script>
        document.addEventListener("DOMContentLoaded", () => { Reveal.initialize(); });
    </script>
</body>
</html>"""

@app.route('/')
def index():
    return TEMPLATE

@app.route('/api/hosts')
def get_hosts():
    return jsonify(hosts_data)

if __name__ == '__main__':
    app.run(debug=True)
