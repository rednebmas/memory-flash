import os
from jinja2 import Environment, FileSystemLoader
import mingus.core.scales as scales
from model.themusic.blues import Blues
import copy

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class ScaleGenerator:

    @staticmethod
    def natural_minor():
        return ScaleGenerator.scale_cards(scales.NaturalMinor, "natural minor")

    @staticmethod
    def harmonic_minor():
        return ScaleGenerator.scale_cards(scales.HarmonicMinor, "harmonic minor")

    @staticmethod
    def melodic_minor():
        return ScaleGenerator.scale_cards(scales.MelodicMinor, "melodic minor")
    
    @staticmethod
    def blues():
        return ScaleGenerator.scale_cards(Blues, "minor blues")

    @staticmethod
    def scale_cards(scale_func, scale_name):
        notes = [ 
            "C",
            "D",
            "E",
            "F",
            "G",
            "A",
            "B",

            "C#",
            "D#",
            "F#",
            "G#",

            "Eb",
            "Ab",
            "Bb",
        ]
        cards = []
        for root in notes:
            scale_tones = scale_func(root).ascending()
            scale_degrees = list( map(lambda x: str(x), list(range(1, len(scale_tones) + 1))) )

            scale_tones += scale_func(root).descending()[1:]
            scale_degrees += scale_degrees[-2::-1] # backwards and don't repeat root
            
            root = root.replace('#', '♯').replace('b','♭')
            cards.append({
                "question": templates.get_template('cards/multipart-card.html').render(
                    symbols=scale_degrees,
                    in_text=root + " " + scale_name
                ),
                "answer": "→".join(scale_tones),
                "scale" : root + " " + scale_name,
                "answer_validator": "equals"
            })
        return cards
