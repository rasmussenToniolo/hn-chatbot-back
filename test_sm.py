import spacy
nlp = spacy.load('en_core_web_sm')

# with open("wiki_us.txt", 'r') as f:
#   text = f.read()
#   # # print(text)
#   doc = nlp(text)
#   # # print(doc)

#   # # for sent in doc.sents:
#   # #   print(sent)
  
#   # sentence1 = list(doc.sents)[0]
#   # print(sentence1)
#   # word = sentence1[2]
#   # print(word)
#   # print(word.lemma_)
#   # print(word.morph)

#   # doc = nlp("Hi! How's it going?")

#   for ent in doc.ents:
#     print(ent.text, ent.label_)

with open("greet.txt", 'r') as f:
  text = f.read()
  doc = nlp(text)

  for sent in doc.sents:
    print(sent)
    for token in sent:
      print(token.lemma_)
    print('----------------')

  for ent in doc.ents:
    print(ent.text, ent.label_)