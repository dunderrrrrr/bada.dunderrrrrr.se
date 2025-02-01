import htpy as h

from constants import BATH_PLACES, BathPlace
from markupsafe import Markup


def head_html() -> h.Element:
    return h.head[
        h.script(src="https://unpkg.com/htmx.org@2.0.4"),
        h.meta(name="viewport", content="width=device-width, initial-scale=1"),
        h.title["BADA!"],
        h.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
        ),
        h.script(
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js"
        ),
        h.script(src="https://unpkg.com/alpinejs", defer=""),
        h.script(src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"),
        h.link(
            rel="stylesheet", href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        ),
    ]


def spinner_html() -> h.Element:
    return h.div(".spinner-border.spinner-border-sm", role="status")


def temp_table_html() -> h.Element:
    return h.div(".table-responsive-sm")[
        h.table(".table.table-striped.table-hover.table-sm")[
            h.tbody[
                (
                    h.tr[
                        h.td[
                            h.span(
                                hx_get=f"/map/{place.id}",
                                hx_trigger="click",
                                hx_target="#modals-here",
                                data_bs_toggle="modal",
                                data_bs_target="#modals-here",
                            )[place.title]
                        ],
                        h.td(
                            ".text-end",
                            hx_get=f"/temp/{place.id}",
                            hx_trigger="load",
                        )[spinner_html()],
                    ]
                    for place in BATH_PLACES
                ),
            ],
        ],
    ]


def map_modal_html(place: BathPlace) -> h.Element:
    lat, long = place.coordinates
    return h.div(".modal-dialog.modal-dialog-centered")[
        h.div(".modal-content")[
            h.div(".modal-header")[h.h5(".modal-title")[place.title]],
            h.div(".modal-body")[
                h.div("#map", style="height: 100vh; width: auto;"),
                h.script[
                    Markup(f"var map = L.map('map').setView([{lat}, {long}], 13);")
                ],
                h.script[
                    Markup(
                        """
                        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        }).addTo(map);
                    """
                    )
                ],
                h.script[Markup(f"L.marker([{lat}, {long}]).addTo(map);")],
                h.script[
                    Markup(
                        "map.whenReady(() => {setTimeout(() => {map.invalidateSize();}, 250);});"
                    )
                ],
            ],
            h.div(".modal-footer")[
                h.button(".btn.btn-secondary", type="button", data_bs_dismiss="modal")[
                    "Close"
                ]
            ],
        ]
    ]
