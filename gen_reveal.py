from flask import Flask, render_template, jsonify

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

@app.route('/')
def index():
    slides_content, nav_content = generate_slides(hosts_data)
    return render_template("reveal_template.html", slides_content=slides_content, nav_content=nav_content)

@app.route('/api/hosts')
def get_hosts():
    return jsonify(hosts_data)

if __name__ == '__main__':
    app.run(debug=True)
