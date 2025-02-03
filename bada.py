import os
import htpy as h
import sentry_sdk
from dotenv import load_dotenv
from flask import Flask, Response

from components import (
    footer_html,
    head_html,
    map_modal_html,
    spinner_html,
    temp_table_html,
)
from constants import BATH_PLACES_BY_ID

load_dotenv()

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), send_default_pii=True)

app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/temp/<int:id>")
def temp(id: int) -> Response:
    try:
        place = BATH_PLACES_BY_ID[id]
    except KeyError:
        return Response(status=404)

    temperature = place.temperature
    has_warning = place.has_warning

    if not temperature:
        temperature = "-"

    if has_warning:
        temperature = f"⚠️ {temperature}"

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
                    "x-data": '{removeModalContent() {document.getElementById(\'modals-here\').innerHTML = \'<div class="modal-dialog modal-dialog-centered"><div class="modal-content p-5"><div class="spinner-border spinner-border-sm" role="status"></div></div></div>\'}}',
                    "x-init": "document.getElementById('modals-here').addEventListener('hidden.bs.modal', () => {removeModalContent()})",
                }
            )[
                h.div(".container-sm")[
                    h.div(".row.justify-content-center")[
                        h.div(".col-12.col-md-9.col-lg-6.pt-3")[
                            temp_table_html(),
                            footer_html(),
                        ],
                    ]
                ],
                h.div(
                    "#modals-here.modal.modal-blur.fade",
                    style="display:none",
                    aria_hidden="false",
                    tab_index="-1",
                )[
                    h.div(
                        ".modal-dialog.modal-dialog-centered",
                        role="document",
                    )[h.div(".modal-content.p-5")[spinner_html()]]
                ],
            ],
        ],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
