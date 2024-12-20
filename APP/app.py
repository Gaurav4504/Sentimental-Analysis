from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import Flask-CORS
from textblob import TextBlob

app = Flask(__name__)  # Initialize the app
CORS(app)  # Enable CORS

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    sentiment = db.Column(db.String(10), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Route to add and analyze a review
@app.route('/analyze', methods=['POST'])
def analyze_review():
    data = request.json
    review_text = data.get('review')
    if not review_text:
        return jsonify({"error": "Review text is required"}), 400

    # Perform sentiment analysis
    analysis = TextBlob(review_text)
    sentiment = "positive" if analysis.sentiment.polarity > 0 else "negative" if analysis.sentiment.polarity < 0 else "neutral"

    # Save to the database
    review = Review(text=review_text, sentiment=sentiment)
    db.session.add(review)
    db.session.commit()

    return jsonify({"review": review_text, "sentiment": sentiment})

# Route to get all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{"id": review.id, "text": review.text, "sentiment": review.sentiment} for review in reviews])

if __name__ == '__main__':
    app.run(debug=True)
