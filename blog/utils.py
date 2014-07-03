'''
    Creates a url readable link
'''
def generate_slug(string):
    return "-".join(string.split(" "))