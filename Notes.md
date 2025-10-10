https://machinelearningmastery.com/building-transformer-models-with-attention-crash-course-build-a-neural-machine-translator-in-12-days/
def normalize(line):
    """Normalize a line of text and split into two at the tab character"""
    line = unicodedata.normalize("NFKC", line.strip().lower())
    line = re.sub(r"^([^ \w])(?!\s)", r"\1 ", line)
    line = re.sub(r"(\s[^ \w])(?!\s)", r"\1 ", line)
    line = re.sub(r"(?!\s)([^ \w])$", r" \1", line)
    line = re.sub(r"(?!\s)([^ \w]\s)", r" \1", line)
    eng, fra = line.split("\t")
    fra = "[start] " + fra + " [end]"
    return eng, fra


    https://towardsdatascience.com/you-only-need-3-things-to-turn-ai-experiments-into-ai-advantage/
    https://towardsdatascience.com/dont-follow-generic-ml-engineer-roadmaps-do-this-instead-2/
    https://towardsdatascience.com/how-to-learn-the-math-needed-for-machine-learning/
    https://towardsdatascience.com/implementing-the-coffee-machine-in-python/
    https://towardsdatascience.com/implementing-the-hangman-game-in-python/

