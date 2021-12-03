def split_email_get_username(email):
    return email.split('@')[0]

def two_username_to_one_username(u1, u2):
    """Takes two username and converts them into one"""
    u1 = split_email_get_username(u1)
    u2 = split_email_get_username(u2)
    if u1 > u2:
        return '-chat-'.join([u2, u1])
    else:
        return '-chat-'.join([u1, u2])

if __name__ == '__main__':
    print(two_username_to_one_username('heshabhishek@gmail.com', 'jaygaur99@gmail.com'))