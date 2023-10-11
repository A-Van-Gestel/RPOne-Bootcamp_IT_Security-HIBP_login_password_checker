from init_flask import App


def create_app():
    return App.get_app()


if __name__ == '__main__':
    create_app().run(debug=False)
