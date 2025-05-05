class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


def is_authenticated_user(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
        else:
            print("Not logged in")
    return wrapper

@is_authenticated_user
def create_blog_post(user):
    print(f"This is {user.name}'s blog post")

new_user = User("Ariel")
new_user.is_logged_in = True
create_blog_post(new_user)
