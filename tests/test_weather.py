"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""

import pytest

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)

#1
def test_parse_time_regular_time():
    assert parse_time("14:21") == 861

def test_parse_time_grenzen():
    assert parse_time("00:00") == 0
    assert parse_time("23:59") == 1439

def test_parse_time_format():
    assert parse_time("9:5") == 545
    assert parse_time("09:05") == 545

@pytest.mark.parametrize(
    "invalid_input",
    [
        "24:00",
        "-1:00",
        "12:60",
        "abc",
        "14-21",
        "14:21:00",
        "",
        "   ",
    ],
)

def test_parse_time_invalid_inputs(invalid_input):
    with pytest.raises(ValueError):
        parse_time(invalid_input)


#2
def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)

def test_parse_measurement_leerzeichen():
    assert parse_measurement(" Köln ; 14:21 ; 21.7 ") == ("Köln", 861, 21.7)

@pytest.mark.parametrize(
    "invalid_line",
    [
        12345,  # Kein String
        "Köln;14:21",  # Zu wenige Felder
        "Köln;14:21;21.7;extra",  # Zu viele Felder
        "  ;14:21;21.7",  # Stadt nach strip leer
        "Köln;25:00;21.7",  # Ungültige Uhrzeit
        "Köln;14:21;heiß",  # Temp kein Float
    ],
)

def test_parse_measurement_invalid_inputs(invalid_line):
    with pytest.raises(ValueError):
        parse_measurement(invalid_line)


#3
def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

def test_filter_by_temperature_grenzen_inklusive():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 20.0),
    ]
    assert filter_by_temperature(measurements, 10.0, 20.0) == measurements

def test_filter_by_temperature_grenzen_lower_gleich_upper():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 20.0),
    ]
    assert filter_by_temperature(measurements, 10.0, 10.0) == [
        ("Köln", 600, 10.0)
    ]

def test_filter_by_temperature_lower_größerals_upper():
    measurements = [("Köln", 600, 10.0)]
    with pytest.raises(ValueError):
        filter_by_temperature(measurements, 20.0, 10.0)

def test_filter_by_temperature_duplikate_bleiben():
    m = ("Köln", 600, 10.0)
    measurements = [m, m]
    assert filter_by_temperature(measurements, 5.0, 15.0) == [m, m]

def test_filter_by_temperature_originalliste_bleibt_und_neue_liste():
    measurements = [("Köln", 600, 10.0)]
    original_copy = list(measurements)

    result = filter_by_temperature(measurements, 5.0, 15.0)

    assert measurements == original_copy


#4
def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

def test_average_temperature_groß_kleinschreibung():
    measurements = [
        ("Köln", 600, 10.0),
        ("köln", 720, 20.0),
    ]
    assert average_temperature(measurements, "Köln") == 10.0

def test_average_temperature_fehlende_stadt_oder_leere_liste():
    measurements = [("Köln", 600, 10.0)]

    with pytest.raises(ValueError):
        average_temperature(measurements, "Bonn")

    with pytest.raises(ValueError):
        average_temperature([], "Köln")

def test_average_temperature_originalliste_gleich():
    measurements = [("Köln", 600, 10.0)]
    original_copy = list(measurements)

    average_temperature(measurements, "Köln")

    assert measurements == original_copy


#5
def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)

def test_hottest_measurement_früher_uhrzeit_gewinnt():
    measurements = [
        ("Köln", 720, 25.0),
        ("Düsseldorf", 600, 25.0),
    ]
    assert hottest_measurement(measurements) == ("Düsseldorf", 600, 25.0)

def test_hottest_measurement_gleiche_uhrzeit_erster_eintrag_gewinnt():
    m1 = ("Köln", 600, 25.0)
    m2 = ("Düsseldorf", 600, 25.0)
    measurements = [m1, m2]

    assert hottest_measurement(measurements) == m1

def test_hottest_measurement_leere_liste_erzeugt_fehler():
    with pytest.raises(ValueError):
        hottest_measurement([])

def test_hottest_measurement_originalliste_gleich():
    measurements = [("Köln", 600, 10.0)]
    original_copy = list(measurements)

    hottest_measurement(measurements)

    assert measurements == original_copy