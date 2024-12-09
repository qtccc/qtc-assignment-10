from flask import Flask, render_template, request, jsonify
from search_logic import perform_search

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query_type = request.form.get("query-type")
    text_query = request.form.get("text-query", "")
    hybrid_weight = float(request.form.get("hybrid-weight", 0.8))
    image_query = request.files.get("image-query")

    image_path = None
    if image_query:
        image_path = f"static/uploads/{image_query.filename}"
        image_query.save(image_path)

    try:
        results = perform_search(query_type, text_query, image_path, hybrid_weight)
        return jsonify({"results": results})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing your search."}), 500

if __name__ == "__main__":
    app.run(debug=True)