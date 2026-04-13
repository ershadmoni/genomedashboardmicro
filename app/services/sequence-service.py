class SequenceService:

    @staticmethod
    def get_steps(sequence):

        return [
            sequence[i:i+2]
            for i in range(len(sequence)-1)
        ]
