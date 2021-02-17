from natasha import (
    Segmenter, MorphVocab,
    NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger,
    NamesExtractor, DatesExtractor, MoneyExtractor, AddrExtractor,
    PER, Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)


def extract_names(text):
    """Извлекает имена из текста"""
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)
    for span in doc.spans:
        if span.type == PER:
            span.normalize(morph_vocab)
            span.extract_fact(names_extractor)
    names = [{'normal': _.normal, 'fio': _.fact.as_dict, 'start': _.start, 'end': _.stop} for _ in doc.spans if _.fact]
    return names


def extract_dates(text):
    """Извлекает даты"""
    return list(dates_extractor(text))