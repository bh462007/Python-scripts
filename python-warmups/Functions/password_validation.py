def is_password_valid(password):

    if len(password)<8:
        return False
    
    upper_found=False
    lower_found=False
    digit_found=False

    for ch in password:
        if ch.isupper():
            upper_found=True

        if ch.islower():
            lower_found=True

        if ch.isdigit():
            digit_found=True

    return upper_found and lower_found and digit_found and len(password)>=8
        
        

password=input("Enter a password: ")
print(is_password_valid(password))