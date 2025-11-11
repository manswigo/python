from collections import Counter
import random


text = ('''Politik på vift
För många amerikaner har semestern förvandlats till en oväntad politisk scen. Florida-bon Lauren Gay berättar att hon gång på gång blir konfronterad med frågor om Donald Trump – bara för att hon har en amerikansk accent. “Så fort de hör var jag kommer ifrån, vill de prata om presidenten,” säger hon till CNN. 

När en irländsk taxichaufför nyligen frågade hur amerikanerna “kunde göra det igen”, syftande på Trumps andra mandatperiod, svarade hon försiktigt. “Man vet aldrig vilken reaktion man får,” säger hon, och beskriver irländarnas raka stil med ett leende.

Politik – det förbjudna samtalsämnet
Researrangören Doni Belau har gjort politiken till tabu på sina gruppresor. Hennes företag Girls’ Guide to the World leder årligen tiotals resor för främst amerikanska kvinnor. “Vi lär våra guider att stoppa samtal om politik direkt,” säger hon. “Det skapar splittring – och det är motsatsen till vad vi vill.”

Men inte alla följer regeln. I Zürich hamnade den amerikanska turisten Angie Roach i ett frukostsamtal med ett nyzeeländskt par som plötsligt utbrast: “What about Trump?” Roach, som själv stödjer honom, svarade med ett skratt. Till slut blev diskussionen oväntat vänlig. “Man kan tycka olika och ändå ha ett civiliserat samtal,” säger hon.

Läs också

Utsikten från ovan: Varför satellitdata inte lämnar något tvivel om klimatförändringarna

Kina lockar världens tekniktalanger med nytt supervisum

Nyfikenhet och sympati
För andra väcker amerikansk politik snarare medlidande. Lauren Gay minns ett tillfälle i England under Trumps första period när en kvinna i ett apotek gav henne en kram och sa: “I’m so sorry about your president.”

“Som svart amerikanska möts jag ofta av sympati,” berättar hon.

“Hur reagerar de på oss?”
Reseexperten Josh Geller säger att USA:s politik inte hindrar folk från att resa – tvärtom. “Efter valet undrar vissa hur de kommer tas emot, men nästan alla kommer hem och säger att det gick bra,” säger han. Hotellchefer runt världen försäkrar honom att de vill välkomna amerikaner: “Turismen är för viktig för att politiken ska stå i vägen.”

När frågorna blir personliga
Las Vegas-bon Nicole Hernandez fick under en sex veckor lång vandring i Spanien höra frågan “Did you vote for Trump?” fler gånger än hon kan räkna. “Jag började nästan hålla andan varje gång jag sa att jag var från USA,” säger hon. En fransk man svarade rent ut: “Jag gillar inte amerikaner,” innan han vände henne ryggen.

Trots det beskriver hon resan som livsförändrande. “Man inser hur lite man behöver för att vara lycklig,” säger hon.

Så undviker du hetsiga samtal
Etikettexperten Danielle Kovachevich råder resenärer att vara förberedda. “Om du inte vill prata politik, byt ämne vänligt,” säger hon. Förslag: “Politik kan bli ganska intensivt – ska vi prata om något lättsammare?”

Lauren Gay summerar känslan hon möter utomlands:

“Världen ser vad som händer – och den dömer oss för det.”

Läs också

Rapporter: Natt utan värme och el i rysk miljonstad efter ukrainsk drönarattack

Zelensky säger att han ”inte är rädd” för Donald Trump mitt under en intervju med strömavbrott''')
text = text.replace('\n', ' ')


counter = Counter(text[i:i+3] for i in range(len(text)-3))


class ThreeGram:
    def __init__(self):
        self.counts = {}

    def train(self, text):
        for i in range(len(text) - 3):
            ngram = text[i:i+3]
            next_char = text[i+3]
            if ngram not in self.counts:
                self.counts[ngram] = Counter()
            self.counts[ngram][next_char] += 1
    def next_token_probability(self, ngram):
        #Compute the probability distribution of next token
        if ngram not in self.counts:
            return None
        next_chars = self.counts[ngram]
        total = next_chars.total()
        next_char_prob = {char: count/total for char, count in next_chars.items()}
        return next_char_prob
    def generate_next_char(self, context, randomize=True):
        context_window = context[-3:]
        if context_window not in self.counts:
            return None
        counter = self.counts[context_window]
        if randomize:
            chars, weights = list(counter.keys()), list(counter.values())
            sample = random.sample(chars, 1, counts=weights)
            return(sample[0])
        else:
            out = counter.most_common(1)[0][0]
            return out
    def generate_text(self, prompt, length=20):
        current_ngram = prompt[-3:]
        output = prompt
        for i in range(length):
            
            next_char = self.generate_next_char(current_ngram)
            if next_char is None:
                break
            output += next_char
            current_ngram = output[-3:]
        return output

def read_textfile(filepath):
    text = ''
    with open(filepath, 'r', encoding='utf-8') as f:
        skip_line = True
        for line in f.readlines():
            if 'START OF THE PROJECT GUTENBERG' in line:
                skip_line = False
                continue
            if 'END OF THE PROJECT GUTENBERG' in line:
                skip_line = True
            if not skip_line:
                text += line
    return text

text = read_textfile('sherlock_holmes.txt')

lm = ThreeGram()
lm.train(text)
print(lm.generate_text('fuck your mother', length=50))
