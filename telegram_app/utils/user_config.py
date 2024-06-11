
def format_user_input(text: str):
    print('text', text)
    formatted_text = text.split('\n')
    print('formatted_text', formatted_text)
    social_media = formatted_text[0]
    content = {}

    for i in formatted_text[1::]:
        s = i.split('=')
        if len(s) == 2:
            key, val = s
            content[key.strip(' ')] = val.strip(' ')

    print('social_media, content', social_media, content)
    return social_media, content
