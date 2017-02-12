# from https://github.com/bspaans/python-mingus/pull/27/files#diff-bd87fd4e9cc87fb10e6072f32dc1ca2cR363
import mingus.core.intervals as intervals
from mingus.core.scales import _Scale
from mingus.core.notes import reduce_accidentals
BLUES_INTERVALS = [
    intervals.minor_third,
    intervals.major_second,
    intervals.minor_second,
    intervals.minor_second,
    intervals.minor_third,
    intervals.major_second,
]

class Blues(_Scale):
    """The blues scale

    Example:
    >>> print(Blues('C'))
    Ascending:  C Eb F Gb G Bb C
    Descending: C Bb G Gb F Eb C

    >>> f_blues = Blues('F')
    >>> print(f_blues)
    Ascending:  F Ab Bb B C Eb F
    Descending: F Eb C B Bb Ab F

    >>> f_blues.degree(4)
    'B'
    """

    type = 'major'

    def __init__(self, note, octaves=1):
        """Create the major scale starting on the chosen note."""
        super(Blues, self).__init__(note, octaves)
        self.name = '{} blues'.format(self.tonic)

    def ascending(self):
        notes = [self.tonic]
        current_note = self.tonic
        for ival in BLUES_INTERVALS:
            new_note = reduce_accidentals(ival(current_note))
            notes.append(new_note)
            current_note = new_note

        return notes