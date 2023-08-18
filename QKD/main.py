class Sender:
    def __init__(self,m):
        self.message = m
        self.encoding_rules = {"R":{"0":"H","1":"V"},"D":{"0":"W","1":"E"}}
        self.sending_queue = []
        self.chosen_basis = None
        print("Alice is initialized")

    def pick_basis(self):
        from random import choice
        return [choice(["R","D"]) for _ in range(len(self.message))]

    def encode_message(self):
        bases = self.pick_basis()
        self.chosen_basis = bases
        for i in range(len(self.message)):
            encoded_bit = Photon(bases[i],self.encoding_rules[bases[i]][self.message[i]])
            self.sending_queue.append(encoded_bit)    
        print("Encoding complete")

    def send(self,ch):
        for photon in self.sending_queue:
            ch.accept(photon)
        print("Sending Complete")


class QuantumChannel:
    def __init__(self):
        self.contents = []

    def accept(self,p):
        self.contents.append(p)

    def release(self):
        if len(self.contents) != 0:
            return self.contents.pop(0)
        return None        

class Receiver:
    def __init__(self):
        self.receiving_queue = []
        self.chosen_basis = []
        self.decoding_rules = {"H":"0","V":"1","W":"0","E":"1"}
        self.recovered_message = []
        print("Bob is initialized")
        
    def receive(self,ch):
        payload = ch.release()
        while payload != None:
            self.receiving_queue.append(payload)
            payload = ch.release()
        print("Receiving complete")

    def decode(self):
        from random import choice
        for photon in self.receiving_queue:
            random_basis = choice(["R","D"])
            self.chosen_basis.append(random_basis)
            measure_result = photon.measure(random_basis)
            self.recovered_message.append(self.decoding_rules[measure_result])
        print("Decoding Complete")    

    def compare_bases(self,b):
        for i in range(len(b)):
            if self.chosen_basis[i] != b[i]:
                self.chosen_basis[i] = "-"
                self.recovered_message[i] = "-"
        print("Recovered Message is {}".format("".join(self.recovered_message)))        

class Photon:
    def __init__(self,p,d):
        self.polarization = p
        self.direction = d
        #print("Photon Created with polarization {} and direction {}".format(p,d))

    def measure(self,p):
        from random import choice
        if p == self.polarization:
            return self.direction
        elif p == "R":
            return choice(["H","V"])
        else:
            return choice(["W","E"])             
    
    def intercept(self,p):
        from random import choice
        if p == self.polarization: #nothing happens since the polarization eve chose are the same as alice's
            pass 
        elif p == "R":
            self.polarization = p
            self.direction = choice(["H","V"])
        else:
            self.polarization = p
            self.direction = choice(["W","E"])

class Evesdropper:
    def __init__(self):
        print("Eve is initialized")

    def eavesdrop(self,ch):
        from random import choice
        for photon in ch.contents:
            basis = choice(["R","D"])
            photon.intercept(basis)
        print("Eavsdropping completed")    


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-m","--message",action="store",type=str,nargs="+")
    parser.add_argument("-e","--eavsdrop",action="store_true")
    args = parser.parse_args()
    message = args.message[0]
    alice = Sender(message)
    bob = Receiver()
    Channel = QuantumChannel()    
    alice.encode_message()
    alice.send(Channel)
    if args.eavsdrop:
        Eve = Evesdropper()
        Eve.eavesdrop(Channel)
    bob.receive(Channel)
    bob.decode()
    bob.compare_bases(alice.chosen_basis)

main()