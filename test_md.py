import spacy

nlp = spacy.load('en_core_web_md')

# with open('greet.txt', 'r') as f:
#   text = f.read()
#   doc = nlp(text)

str1 = "Good morning"
str2 = "Good afternoon"
  
doc1 = nlp(str1)
doc2 = nlp(str2)

for ent in doc1.ents:
    print(ent.text, ent.label_)

for ent in doc2.ents:
    print(ent.text, ent.label_)

print(doc1.similarity(doc2))



inputStr = "How's the weather"
min_similarity = 0.72
