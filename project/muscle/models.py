from .. import db

muscles_data = [
    {"name": "Biceps", "description": "The biceps brachii is a muscle located on the upper arm, between the shoulder and the elbow. It is composed of two heads, the long head, and the short head. The biceps is responsible for flexing the elbow and supinating the forearm.", "image_name": "biceps.jpg"},
    {"name": "Triceps", "description": "The triceps brachii is a three-headed muscle on the back of the upper arm. It is responsible for extending the elbow and is an antagonist to the biceps. The triceps play a crucial role in various pushing movements.", "image_name": "triceps.jpg"},
    {"name": "Quadriceps", "description": "The quadriceps femoris, commonly known as the quadriceps, is a group of four muscles located at the front of the thigh. These muscles, namely the rectus femoris, vastus lateralis, vastus medialis, and vastus intermedius, are crucial for knee extension and stability during standing and walking.", "image_name": "quadriceps.jpg"},
    {"name": "Hamstrings", "description": "The hamstrings are a group of muscles located at the back of the thigh. Comprising the biceps femoris, semitendinosus, and semimembranosus, the hamstrings play a significant role in knee flexion and hip extension. They are essential for activities such as running and jumping.", "image_name": "hamstrings.png"},
    {"name": "Pectoralis Major", "description": "The pectoralis major is a large muscle in the chest region. It consists of two parts, the clavicular head, and the sternal head. The pectoralis major is responsible for various movements, including flexion, adduction, and medial rotation of the arm, making it vital for chest exercises.", "image_name": "chest.png"},
    {"name": "Deltoids", "description": "The deltoids, or deltoid muscles, are triangular-shaped muscles located on the shoulder. Comprising the anterior, lateral, and posterior heads, the deltoids play a key role in shoulder movement and stability. They contribute to arm abduction and rotation.", "image_name": "deltoid.jpg"},
    {"name": "Latissimus Dorsi", "description": "The latissimus dorsi, often referred to as the lats, is a broad muscle in the back. It extends from the lower back to the upper arm. The latissimus dorsi is responsible for various movements, including shoulder adduction, extension, and internal rotation.", "image_name": "latissimus_dorsi.jpg"},
    {"name": "Abdominals", "description": "The abdominal muscles, commonly known as abs, include several muscles such as the rectus abdominis, external obliques, internal obliques, and transversus abdominis. These muscles provide core stability and play a crucial role in trunk flexion and rotation.", "image_name": "abdominals.jpg"},
    {"name": "Obliques", "description": "The obliques, comprising the external obliques and internal obliques, are muscles located on the sides of the abdomen. They play a significant role in trunk rotation and lateral flexion. The obliques contribute to core strength and stability.", "image_name": "obliques.jpg"},
    {"name": "Forearms", "description": "The forearms consist of various muscles, including the flexors and extensors. These muscles control movements of the wrist and fingers. The flexors bend the wrist and fingers, while the extensors straighten them. Strong forearms are crucial for grip strength and various hand-related activities.", "image_name": "forearms.jpg"},
    {"name": "Trapezius", "description": "The trapezius is a large muscle in the upper back and neck. It has three parts: the upper, middle, and lower trapezius. The trapezius is responsible for movements such as shoulder shrugging, shoulder blade retraction, and head/neck extension. It plays a role in maintaining posture and shoulder stability.", "image_name": "trapezius.jpg"},
    {"name": "Glutes", "description": "The glutes, or gluteal muscles, are a group of three muscles: the gluteus maximus, gluteus medius, and gluteus minimus. The glutes are essential for hip extension, abduction, and rotation. They play a key role in activities like walking, running, and standing upright.", "image_name": "glutes.jpg"},
    {"name": "Calves", "description": "The calves include the gastrocnemius and soleus muscles. These muscles are located at the back of the lower leg and are responsible for plantar flexion of the foot, pointing the toes downward. Strong and well-developed calves are important for activities such as walking, running, and jumping.", "image_name": "calves.jpg"},
    # Add more muscles with detailed descriptions as needed
]


"""Muscle building application."""
class Muscle(db.Model):
    __tablename__ = 'muscles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    image_name = db.Column(db.String(50), unique=True, nullable=True)
    description = db.Column(db.String(200), nullable=False)

    # Relationships.
    exercises = db.relationship('Exercise', backref='muscle', lazy='dynamic')

    def __repr__(self):
        return f"{self.name}"
    
    @staticmethod
    def insert_muscles():
        for muscle_data in muscles_data:
            muscle = Muscle(name=muscle_data["name"].lower(), description=muscle_data["description"],
                            image_name=f"img/{muscle_data['image_name']}")
            db.session.add(muscle)

        db.session.commit()



class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    muscle_id = db.Column(db.Integer, db.ForeignKey('muscles.id', name='fk_exercise_muscle'))

    name = db.Column(db.String(50), unique=True)
    video_link = db.Column(db.String(250), nullable=True)
    description = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author_name = db.Column(db.String(64))

    def __repr__(self):
        return f"{self.muscle}, {self.name}"
