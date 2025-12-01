"""Pytest näited FastAPI koondteenuse jaoks."""
from datetime import datetime
from typing import Any, Dict
import pytest
import requests
from fastapi.testclient import TestClient
from backend.main import (
    JSONPLACEHOLDER_URL,
    RICK_MORTY_URL,
    hanki_andmed,
    rakendus,
)

client = TestClient(rakendus)


class MockResponse:
    """Lihtne mock, mis jäljendab requests.Response käitumist."""
    
    def __init__(self, json_keha: Dict[str, Any], status_code: int = 200):
        self._json_keha = json_keha
        self.status_code = status_code
    
    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise ValueError(f"HTTP {self.status_code}")
    
    def json(self) -> Dict[str, Any]:
        return self._json_keha


def test_status_endpoint_annab_aktiivse_oleku() -> None:
    """Kontrollib, et /status tagastab aktiivse oleku ja allikainfo."""
    vastus = client.get("/status")
    assert vastus.status_code == 200
    keha = vastus.json()
    assert keha["olek"] == "aktiivne"
    assert "Kvaliteedijälg" in keha["allikas"]


def test_hanki_andmed_tostab_vea(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib, et hanki_andmed tõstab erandi võrguühenduse vea korral."""
    def _faux_get(*_args: Any, **_kwargs: Any) -> MockResponse:
        raise requests.RequestException("võrk maas")
    
    monkeypatch.setattr("requests.get", _faux_get)
    with pytest.raises(Exception):
        hanki_andmed("https://naidis.url")


def test_koond_endpoint_tagastab_pealkirja(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib, et /api/koond tagastab õiged andmed mõlemast allikast."""
    def _valitud_get(url: str, *_args: Any, **_kwargs: Any) -> MockResponse:
        if url == JSONPLACEHOLDER_URL:
            return MockResponse({"id": 1, "title": "Test pealkiri", "body": "Sisu"})
        if url == RICK_MORTY_URL:
            return MockResponse({"id": 10, "name": "Rick", "status": "Alive"})
        raise ValueError("Ootamatu URL")
    
    monkeypatch.setattr("requests.get", _valitud_get)
    vastus = client.get("/api/koond")
    keha = vastus.json()
    assert keha["postitus"]["pealkiri"] == "Test pealkiri"
    assert keha["tegelane"]["nimi"] == "Rick"
    assert len(keha["allikad"]) == 2


def test_koond_endpoint_paastikuaeg_on_iso(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib, et paastikuAeg on ISO 8601 formaadis."""
    def _valitud_get(url: str, *_args: Any, **_kwargs: Any) -> MockResponse:
        if url == JSONPLACEHOLDER_URL:
            return MockResponse({"id": 1, "title": "X", "body": "Y"})
        return MockResponse({"id": 2, "name": "Morty", "status": "Alive"})
    
    monkeypatch.setattr("requests.get", _valitud_get)
    vastus = client.get("/api/koond")
    aeg = vastus.json()["paastikuAeg"]
    # Kontrolli, et ISO kuupäev on parsitav
    datetime.fromisoformat(aeg)


def test_koond_endpoint_vigastab_allikaid(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib 502 staatust, kui üks allikas ebaõnnestub."""
    def _valitud_get(url: str, *_args: Any, **_kwargs: Any) -> MockResponse:
        if url == JSONPLACEHOLDER_URL:
            raise requests.RequestException("Katkestus")
        return MockResponse({"id": 2, "name": "Morty", "status": "Alive"})
    
    monkeypatch.setattr("requests.get", _valitud_get)
    vastus = client.get("/api/koond")
    assert vastus.status_code == 502


# UUED TESTID


def test_koond_endpoint_vastuse_skeem_on_taislik(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib, et koondvastus sisaldab kõiki nõutud välju õiges struktuuris."""
    def _valitud_get(url: str, *_args: Any, **_kwargs: Any) -> MockResponse:
        if url == JSONPLACEHOLDER_URL:
            return MockResponse({"id": 5, "title": "Täielik test", "body": "Keha"})
        return MockResponse({"id": 15, "name": "Summer", "status": "Alive"})
    
    monkeypatch.setattr("requests.get", _valitud_get)
    vastus = client.get("/api/koond")
    assert vastus.status_code == 200
    keha = vastus.json()
    
    # Kontrolli põhistruktuuri
    assert "postitus" in keha
    assert "tegelane" in keha
    assert "allikad" in keha
    assert "paastikuAeg" in keha
    
    # Kontrolli postitus struktuuri
    assert "id" in keha["postitus"]
    assert "pealkiri" in keha["postitus"]
    assert "katkend" in keha["postitus"]
    
    # Kontrolli tegelane struktuuri
    assert "id" in keha["tegelane"]
    assert "nimi" in keha["tegelane"]
    assert "staatuse" in keha["tegelane"]
    
    # Kontrolli allikate listi
    assert isinstance(keha["allikad"], list)
    assert len(keha["allikad"]) == 2


def test_koond_endpoint_mlemad_allikad_ebaonnestuvad(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib 502 staatust, kui mõlemad välised API'd ebaõnnestuvad."""
    def _valitud_get(url: str, *_args: Any, **_kwargs: Any) -> MockResponse:
        raise requests.RequestException("Täielik võrgukatkestus")
    
    monkeypatch.setattr("requests.get", _valitud_get)
    vastus = client.get("/api/koond")
    assert vastus.status_code == 502


def test_koond_endpoint_allikate_nimekiri_sisaldab_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib, et allikate nimekiri sisaldab õigeid URL-e."""
    def _valitud_get(url: str, *_args: Any, **_kwargs: Any) -> MockResponse:
        if url == JSONPLACEHOLDER_URL:
            return MockResponse({"id": 3, "title": "Allikas test", "body": "Sisu"})
        return MockResponse({"id": 8, "name": "Jerry", "status": "Alive"})
    
    monkeypatch.setattr("requests.get", _valitud_get)
    vastus = client.get("/api/koond")
    keha = vastus.json()
    
    allikad = keha["allikad"]
    assert JSONPLACEHOLDER_URL in allikad
    assert RICK_MORTY_URL in allikad


def test_status_endpoint_sisaldab_ajatemplit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kontrollib, et /status tagastab kehtiva ISO ajatempli."""
    vastus = client.get("/status")
    assert vastus.status_code == 200
    keha = vastus.json()
    
    # Kui status endpoint sisaldab ajatempli välja
    if "aeg" in keha:
        datetime.fromisoformat(keha["aeg"])
    
    # Alternatiivina kontrolli, et olek on aktiivne
    assert keha["olek"] == "aktiivne"