import spacy
import re
from spacy.matcher import Matcher
from pathlib import Path

def pre_proces(texto, language):
    # Convert text to lowercase.
    text_minusculas = texto.lower()

    # Remove punctuation handled by the original prototype.
    text_sin_signos = re.sub( r'[=|?|$|.|!|,|;]',r'',text_minusculas)

    # Load the requested spaCy language model.
    if language == "es":
        nlp = spacy.load('es_core_news_sm')
    else:
        nlp = spacy.load('en_core_web_sm')

    doc = nlp(text_sin_signos)
    vec = doc.vector
    ent = doc.ents
    doc_con_signos = nlp(texto)

    # Split the original text into sentences.
    sentences = []
    for sent in doc_con_signos.sents:
        sentences.append(sent.text)

    # Tag and lemmatize tokens.
    etiquetado = []
    for token in doc:
        etiquetado.append((token.text, token.tag_, token.lemma_))

    # Optional dependency parsing diagnostics.
    # for token in doc:
    #     print("{0}/{1} <-- {2} <-- {3}/{4}".format(
    #         token.text, token.tag_, token.dep_, token.head.text, token.head.tag_
    #     ))

    # Optional named-entity and noun-phrase diagnostics.
    # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    # # Find named entities, phrases and concepts
    # for entity in doc.ents:
    #     print(entity.text, entity.label_)

    # Rule-based lexical-syntactic patterns.

    # Initialize the matcher with the shared vocabulary.
    matcher = Matcher(nlp.vocab)

    # Add rule-based patterns to the matcher.
    patterns_dir = Path(__file__).with_name("patterns")
    if language == "es":
        patterns_file = patterns_dir / "es_patterns.txt"
    elif language == "en":
        patterns_file = patterns_dir / "en_patterns.txt"
    else:
        raise ValueError(f"Unsupported language: {language!r}")
    patterns = patterns_file.read_text(encoding="utf-8").splitlines()
    for i in range(len(patterns)):
        poss = patterns[i].split(" ")
        p = []
        for pos in poss:
            p.append({"POS": pos})
        matcher.add(str(i+1), [p])

    # Run the matcher over the document.
    matches = matcher(doc)

    # Iterate over matched spans.
    phrases = []
    for match_id, start, end in matches:
        # Retrieve the resulting span.
        matched_span = doc[start:end]
        phrases.append(matched_span)
        #print(matched_span.text)

    # print(phrases)

    candidate_kp = []
    for phrase in phrases:
        tokens_list = []
        for token in phrase:
            if token.tag_ == "VERB":
                token = token.lemma_
            tokens_list.append(token.text)
        candidate_kp.append(tokens_list)

    return sentences, candidate_kp
