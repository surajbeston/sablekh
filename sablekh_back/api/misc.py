import random
from string import ascii_letters, digits
def filter_text(sent, punctuation, in_middle = "_"):
    if len(sent) > 1:
        punctuation += ' '
        filtered_sent = ''
        for i, letter in enumerate(sent):
            if letter in punctuation:
                if i > 0 and sent[i-1] in punctuation:
                    letter = ''
                else:
                    letter = in_middle
            filtered_sent += letter 
        if filtered_sent[-1] == in_middle:
            filtered_sent = filtered_sent[:-1]
    else:
        filtered_sent = sent
    return filtered_sent

def title_to_link(title, punctuation):
    link_str = filter_text(title, punctuation, in_middle="-") +'-' +''.join(random.sample(ascii_letters+digits, 5))
    return link_str
