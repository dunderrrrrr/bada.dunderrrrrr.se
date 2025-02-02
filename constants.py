import json
import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass

BASE_URL = "https://www.havochvatten.se"


@dataclass
class BathPlace:
    id: int
    title: str
    url: str

    def _get_temperature(self) -> str | None:
        try:
            response = httpx.get(BASE_URL + self.url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        self.soup = soup

        weather_elem = soup.find("div", id="Vaderprognos")
        graph = weather_elem.find_next_sibling("div")
        try:
            temp = graph.find("p").text.split(":")[1].split()[0]
        except AttributeError:
            return None

        return f"{temp}°"

    @property
    def coordinates(self) -> tuple[float, float]:
        json_element = self.soup.find("script", {"type": "application/ld+json"})
        json_data = json.loads(json_element.string)
        lat = json_data["geo"]["latitude"]
        long = json_data["geo"]["longitude"]
        return lat, long

    @property
    def temperature(self) -> str | None:
        return self._get_temperature()


BATH_PLACES = [
    BathPlace(
        id=1,
        title="Arkösund, Badholmarna",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/arkosund-badholmarna.html",
    ),
    BathPlace(
        id=2,
        title="Arkösund, Nordanskogsbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/arkosund-nordanskogsbadet-camping.html",
    ),
    BathPlace(
        id=3,
        title="Arkösund, Sköldvik",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/arkosund-skoldvik.html",
    ),
    BathPlace(
        id=4,
        title="Bolen, Bolenbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/bolen-bolenbadet.html",
    ),
    BathPlace(
        id=5,
        title="Bråviken, Kvarsebobadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/braviken-kvarsebobadet.html",
    ),
    BathPlace(
        id=6,
        title="Bråviken, Lindöbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/braviken-lindobadet.html",
    ),
    BathPlace(
        id=7,
        title="Böksjön, Böksjöbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/boksjon-boksjobadet.html",
    ),
    BathPlace(
        id=8,
        title="Dalbystrand",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/dalbystrand.html",
    ),
    BathPlace(
        id=9,
        title="Ensjön, Ensjöbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/ensjon-ensjobadet.html",
    ),
    BathPlace(
        id=10,
        title="Glan, Skarsätter",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/glan-skarsatter.html",
    ),
    BathPlace(
        id=11,
        title="Motala ström",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/inre-hamn--motala-strom.html",
    ),
    BathPlace(
        id=12,
        title="Lilla Älgsjön",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/lilla-algsjon.html",
    ),
    BathPlace(
        id=13,
        title="Lillsjöbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/lillsjobadet.html",
    ),
    BathPlace(
        id=14,
        title="Mårn, Mårängsbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/marn-marangsbadet.html",
    ),
    BathPlace(
        id=15,
        title="Gransjönäsbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/nedre-glottern-gransjonasbadet.html",
    ),
    BathPlace(
        id=16,
        title="Slätbaken, Stegeborgsgården",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/slatbaken-stegeborgsgarden.html",
    ),
    BathPlace(
        id=17,
        title="Sörsjöbadet",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/sorsjobadet.html",
    ),
    BathPlace(
        id=18,
        title="Ågelsjön",
        url="/badplatser-och-badvatten/kommuner/badplatser-i-norrkopings-kommun/agelsjon.html",
    ),
]

BATH_PLACES_BY_ID = {place.id: place for place in BATH_PLACES}
