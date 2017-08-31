class ProofOfWork:
    def __init__(self, last_proof):
        self.last_proof = last_proof

    def calculate(self):
        # create a variable that we will use to find our next proof of work
        incrementor = self.last_proof + 1

        # keep incrementing the incrementor until it's divisible by both 9 and the
        # proof of work of the previous block in the chain
        while not (incrementor % 9 == 0 and incrementor % self.last_proof == 0):
            incrementor += 1

        # once the incrementor number is found, we can return it as proof of our work
        return incrementor