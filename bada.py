import htpy as h
from flask import Flask, Response
from markupsafe import Markup

from components import head_html, map_modal_html, temp_table_html
from constants import BATH_PLACES_BY_ID


app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/temp/<int:id>")
def temp(id: int) -> Response:
    try:
        place = BATH_PLACES_BY_ID[id]
    except KeyError:
        return Response(status=404)

    temperature = place.temperature

    if not temperature:
        temperature = None

    return Response(temperature)


@app.route("/map/<int:id>")
def map(id: int) -> Response:
    try:
        place = BATH_PLACES_BY_ID[id]
    except KeyError:
        return Response(status=404)

    return Response(map_modal_html(place))


@app.route("/")
def index() -> Response:
    return Response(
        h.html[
            head_html(),
            h.body(
                {
                    "x-data": "{removeModalContent() {document.getElementById('modals-here').innerHTML = ''}}",
                    "x-init": "document.getElementById('modals-here').addEventListener('hidden.bs.modal', () => {removeModalContent()})",
                }
            )[
                h.div(".container-sm")[
                    h.div(".row")[h.div(".col.pt-3")[temp_table_html()]]
                ],
                h.div(
                    "#modals-here.modal.modal-blur.fade",
                    style="display:none",
                    aria_hidden="false",
                    tab_index="-1",
                )[
                    h.div(
                        ".modal-dialog.modal-lg.modal-dialog-centered",
                        role="document",
                    )[h.div(".modal-content")]
                ],
            ],
        ],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
