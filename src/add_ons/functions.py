import random, string

def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def text_selector(en_text, fr_text, ar_text):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    language = request.session.get('language')

    if language == 'en-us':
        return en_text
    if language == 'fr-fr':
        return fr_text
    if language == 'ar-dz':
        return ar_text