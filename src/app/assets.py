from flask_assets import Bundle, Environment, Filter

css = Bundle(
    "css/micropub.css",
    "css/normalize.css",
    filters=("cssrewrite"),
    output="gen/packed.css",
)

assets = Environment()
assets.register("css_packed", css)
