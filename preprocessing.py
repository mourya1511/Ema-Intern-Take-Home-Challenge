import os

def preprocess_lecture_notes(lecture_notes_dir):
    lectures = {}
    for filename in os.listdir(lecture_notes_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(lecture_notes_dir, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                lectures[filename] = content
    return lectures
