from controllers.database import load_category
import dash


external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
    '/public/styles/theme.css',
    '/public/styles/menu.css',
    '/public/styles/base_style.css',
    '/public/styles/side_bar.css',
    '/public/styles/table.css',
    '/public/styles/loading.css',
]

external_scripts = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
    'https://use.fontawesome.com/releases/v5.0.13/js/solid.js',
    'https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js',
]

app = dash.Dash(
    __name__,

    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,

    suppress_callback_exceptions=True,
)

categories = load_category()
categories = categories['product_category_name'].tolist()

server = app.server
