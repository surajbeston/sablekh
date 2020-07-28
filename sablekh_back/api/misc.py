def filter_text(sent, punctuation):
    punctuation += ' '
    filtered_sent = ''
    for letter in sent:
        if letter in punctuation:
            letter = '_'
        filtered_sent += letter 
    return filtered_sent