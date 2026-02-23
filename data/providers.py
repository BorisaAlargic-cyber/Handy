PROVIDERS = [
    {
        "id": 1, "name": "Carlos M.", "category": "Electrician",
        "rating": 4.9, "reviews": 134, "price": 45,
        "experience": 12, "distance": 1.2,
        "availability": ["Mon", "Tue", "Thu", "Fri"],
        "tags": ["Emergency calls", "Certified", "Insured"],
        "bio": "Licensed electrician with 12 years experience. Specialises in rewiring, panel upgrades and smart home installations.",
        "avatar": "⚡",
    },
    {
        "id": 2, "name": "Ana R.", "category": "Cleaning",
        "rating": 4.8, "reviews": 210, "price": 28,
        "experience": 7, "distance": 0.8,
        "availability": ["Mon", "Wed", "Fri", "Sat"],
        "tags": ["Eco products", "Deep clean", "Flexible hours"],
        "bio": "Professional cleaner offering regular and deep-cleaning services using eco-friendly products.",
        "avatar": "🧹",
    },
    {
        "id": 3, "name": "Mikel T.", "category": "Plumber",
        "rating": 4.7, "reviews": 89, "price": 50,
        "experience": 9, "distance": 2.5,
        "availability": ["Tue", "Wed", "Thu", "Sat"],
        "tags": ["24/7 emergency", "Boiler specialist"],
        "bio": "Experienced plumber covering all domestic plumbing needs from leaks to full bathroom installations.",
        "avatar": "🔧",
    },
    {
        "id": 4, "name": "Sofia B.", "category": "Cleaning",
        "rating": 4.6, "reviews": 56, "price": 25,
        "experience": 4, "distance": 3.1,
        "availability": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "tags": ["Available daily", "Pet-friendly"],
        "bio": "Reliable cleaner available Monday to Friday. Great with pets and happy to tailor cleaning to your home.",
        "avatar": "✨",
    },
    {
        "id": 5, "name": "Jordi P.", "category": "Electrician",
        "rating": 4.5, "reviews": 47, "price": 40,
        "experience": 5, "distance": 1.8,
        "availability": ["Wed", "Thu", "Fri", "Sun"],
        "tags": ["Solar panels", "EV chargers"],
        "bio": "Specialist in renewable energy installations including solar panels and EV charging points.",
        "avatar": "🔌",
    },
    {
        "id": 6, "name": "Lena K.", "category": "Handyman",
        "rating": 4.8, "reviews": 101, "price": 35,
        "experience": 8, "distance": 1.5,
        "availability": ["Mon", "Tue", "Sat", "Sun"],
        "tags": ["Furniture assembly", "Painting", "Odd jobs"],
        "bio": "Skilled handywoman for all those little jobs around the house — furniture assembly, painting, shelving and more.",
        "avatar": "🪚",
    },
    {
        "id": 7, "name": "Tomás N.", "category": "Gardening",
        "rating": 4.7, "reviews": 73, "price": 32,
        "experience": 10, "distance": 4.0,
        "availability": ["Tue", "Thu", "Sat", "Sun"],
        "tags": ["Lawn care", "Tree trimming", "Landscaping"],
        "bio": "Professional gardener offering regular maintenance, seasonal planting and full landscaping projects.",
        "avatar": "🌿",
    },
]

CATEGORIES = ["All", "Electrician", "Cleaning", "Plumber", "Handyman", "Gardening"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TIME_SLOTS = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

SAMPLE_REVIEWS = [
    ("Maria G.", "Very professional and quick. Highly recommend! ⭐⭐⭐⭐⭐"),
    ("Peter S.", "Fixed the problem efficiently. Fair pricing. ⭐⭐⭐⭐⭐"),
    ("Lucia F.", "Great communication and clean work. ⭐⭐⭐⭐"),
]

HOURS_MAP = {
    "Quick fix (< 1h)": 1,
    "Half day (2–4h)": 3,
    "Full day (6–8h)": 7,
    "Multi-day project": 16,
}
