import pytest
from dash import html, dcc
from app import app

def test_header_present():
    layout = app.layout
    header = [comp for comp in layout.children if isinstance(comp, html.H1)]
    assert header, "Main header (H1) is missing"
    assert "Soul Foods Sales Visualizer" in header[0].children

def test_visualisation_present():
    layout = app.layout
    graph = next((comp for comp in layout.children if isinstance(comp, dcc.Graph)), None)
    assert graph is not None, "Graph (dcc.Graph) is missing"
    assert graph.id == "sales-chart"

def test_region_picker_present():
    layout = app.layout
    radio = None
    for child in layout.children:
        if isinstance(child, html.Div):
            grandchildren = getattr(child, 'children', [])
            if isinstance(grandchildren, list):
                for grandchild in grandchildren:
                    if isinstance(grandchild, dcc.RadioItems) and grandchild.id == 'region-filter':
                        radio = grandchild
    assert radio is not None, "Region picker (dcc.RadioItems) is missing"
    assert len(radio.options) == 5

