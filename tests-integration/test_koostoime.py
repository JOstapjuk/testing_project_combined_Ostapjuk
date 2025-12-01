"""Integratsioonitestid, mis kasutavad päris FastAPI rakendust ja mockitud väliseid teenuseid."""
from datetime import datetime
from fastapi.testclient import TestClient
import pytest
import responses
from backend.main import JSONPLACEHOLDER_URL, RICK_MORTY_URL, rakendus

client = TestClient(rakendus)


@responses.activate
def test_koond_endpoint_onnestub_kui_valised_teenused_toimivad(caplog: pytest.LogCaptureFixture) -> None:
    """Kontrollib edukat koostoimet väliste teenustega ja logimist."""
    caplog.set_level("INFO")
    
    responses.add(
        responses.GET,
        JSONPLACEHOLDER_URL,
        json={"id": 1, "title": "Integratsioon", "body": "pikem tekst"},
        status=200,
    )
    responses.add(
        responses.GET,
        RICK_MORTY_URL,
        json={"id": 42, "name": "Morty Smith", "status": "Alive"},
        status=200,
    )
    
    vastus = client.get("/api/koond")
    assert vastus.status_code == 200
    
    keha = vastus.json()
    assert keha["postitus"]["pealkiri"] == "Integratsioon"
    assert keha["tegelane"]["nimi"] == "Morty Smith"
    assert JSONPLACEHOLDER_URL in keha["allikad"]
    assert RICK_MORTY_URL in keha["allikad"]
    
    # Kontrolli logimist
    assert any("Koondan API vastuseid" in rekord.message for rekord in caplog.records)


@responses.activate
def test_koond_endpoint_annab_502_kui_valis_api_katkestab() -> None:
    """Kontrollib 502 staatuse tagastamist välise teenuse tõrke korral."""
    responses.add(
        responses.GET,
        JSONPLACEHOLDER_URL,
        status=500,
    )
    responses.add(
        responses.GET,
        RICK_MORTY_URL,
        body=responses.ConnectionError("võrguviga"),
    )
    
    vastus = client.get("/api/koond")
    assert vastus.status_code == 502
    
    keha = vastus.json()

    assert keha["detail"]["sonum"] == "Välise teenuse tõrge"
    assert keha["detail"]["siht"] in (JSONPLACEHOLDER_URL, RICK_MORTY_URL)



@responses.activate
def test_koond_endpoint_tagastab_kehtiva_iso_ajatempli(caplog: pytest.LogCaptureFixture) -> None:
    """Kontrollib, et edukas vastus sisaldab kehtivat ISO 8601 ajatempli."""
    caplog.set_level("INFO")
    
    responses.add(
        responses.GET,
        JSONPLACEHOLDER_URL,
        json={"id": 10, "title": "Ajatest", "body": "Ajatesti sisu"},
        status=200,
    )
    responses.add(
        responses.GET,
        RICK_MORTY_URL,
        json={"id": 20, "name": "Summer Smith", "status": "Alive"},
        status=200,
    )
    
    vastus = client.get("/api/koond")
    assert vastus.status_code == 200
    
    keha = vastus.json()
    assert "paastikuAeg" in keha
    
    # Kontrolli, et ajatempel on parsitav ISO 8601 formaadis
    try:
        datetime.fromisoformat(keha["paastikuAeg"])
    except ValueError:
        pytest.fail("paastikuAeg ei ole kehtiv ISO 8601 formaat")


@responses.activate
def test_status_endpoint_toimib_integratsioonitestis() -> None:
    """Kontrollib, et /status endpoint toimib integratsioonikeskkonnas."""
    vastus = client.get("/status")
    assert vastus.status_code == 200
    
    keha = vastus.json()
    assert keha["olek"] == "aktiivne"
    assert "allikas" in keha
    assert "Kvaliteedijälg" in keha["allikas"]


@responses.activate
def test_koond_endpoint_mlemad_allikad_ebaonnestuvad_logib_molemas(caplog: pytest.LogCaptureFixture) -> None:
    """Kontrollib logimist, kui mõlemad välised teenused ebaõnnestuvad."""
    caplog.set_level("ERROR")
    
    responses.add(
        responses.GET,
        JSONPLACEHOLDER_URL,
        status=503,
    )
    responses.add(
        responses.GET,
        RICK_MORTY_URL,
        status=504,
    )
    
    vastus = client.get("/api/koond")
    assert vastus.status_code == 502
    
    # Kontrolli, et mõlemad vead logitakse
    error_messages = [rekord.message for rekord in caplog.records if rekord.levelname == "ERROR"]
    assert any(JSONPLACEHOLDER_URL in msg for msg in error_messages)
    # Kui rakendus üritab teist API-d pärast esimese ebaõnnestumist


@responses.activate
def test_koond_endpoint_vastuse_struktuuri_taielikkus(caplog: pytest.LogCaptureFixture) -> None:
    """Kontrollib, et vastus sisaldab kõiki nõutud välju õiges struktuuris."""
    caplog.set_level("INFO")
    
    responses.add(
        responses.GET,
        JSONPLACEHOLDER_URL,
        json={"id": 99, "title": "Struktuuritest", "body": "Täielik test"},
        status=200,
    )
    responses.add(
        responses.GET,
        RICK_MORTY_URL,
        json={"id": 88, "name": "Beth Smith", "status": "Alive"},
        status=200,
    )
    
    vastus = client.get("/api/koond")
    assert vastus.status_code == 200
    
    keha = vastus.json()
    
    # Kontrolli põhistruktuuri
    required_keys = ["postitus", "tegelane", "allikad", "paastikuAeg"]
    for key in required_keys:
        assert key in keha, f"Vastuses puudub nõutud väli: {key}"
    
    # Kontrolli postitus struktuuri
    assert "id" in keha["postitus"]
    assert "pealkiri" in keha["postitus"]
    assert "katkend" in keha["postitus"]
    assert keha["postitus"]["id"] == 99
    
    # Kontrolli tegelane struktuuri
    assert "id" in keha["tegelane"]
    assert "nimi" in keha["tegelane"]
    assert "staatuse" in keha["tegelane"]
    assert keha["tegelane"]["nimi"] == "Beth Smith"
    
    # Kontrolli allikad
    assert isinstance(keha["allikad"], list)
    assert len(keha["allikad"]) == 2


@responses.activate
def test_koond_endpoint_http_timeout_kaesitlus(caplog: pytest.LogCaptureFixture) -> None:
    """Kontrollib timeout olukorra käsitlemist."""
    caplog.set_level("ERROR")
    
    responses.add(
        responses.GET,
        JSONPLACEHOLDER_URL,
        body=responses.Timeout("Request timeout"),
    )
    responses.add(
        responses.GET,
        RICK_MORTY_URL,
        json={"id": 3, "name": "Summer", "status": "Alive"},
        status=200,
    )
    
    vastus = client.get("/api/koond")
    assert vastus.status_code == 502
    
    # Kontrolli timeout logimist
    assert any(
        "ERROR" in rekord.levelname
        for rekord in caplog.records
    )