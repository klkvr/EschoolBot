def delete_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')