"""Smoke tests de l'adapter A'Space autogluon (aucun import lourd)."""

import os
import sys

from autogluon_aspace_adapter import (
    FIBER_ID,
    PINNED_AUTOGLUON_BIND,
    PINNED_AUTOGLUON_COMMIT,
    PINNED_AUTOGLUON_VERSION,
    AutogluonAspaceAdapter,
)


def test_import_does_not_pull_autogluon():
    assert "autogluon" not in sys.modules


def test_describe_pins_gel():
    info = AutogluonAspaceAdapter().describe()
    assert info["fiber_id"] == FIBER_ID == "fiber:a0:autogluon"
    assert info["pinned_commit"] == PINNED_AUTOGLUON_COMMIT
    assert info["pinned_commit"] == "e3cb3b71386c54ff11155d6e7a67f6b43f117208"
    assert info["pinned_version"] == PINNED_AUTOGLUON_VERSION == "1.6.4"
    assert info["pinned_bind"] == PINNED_AUTOGLUON_BIND
    assert info["pinned_bind"] == "efadb394a2762ca3562920c25026dd64e36d4336"
    assert info["license"] == "Apache-2.0"


def test_disable_telemetry_sets_env():
    os.environ.pop("TABPFN_DISABLE_TELEMETRY", None)
    result = AutogluonAspaceAdapter().disable_telemetry()
    assert os.environ["TABPFN_DISABLE_TELEMETRY"] == "1"
    assert result["TABPFN_DISABLE_TELEMETRY"] == "1"
    assert result["previous_value"] is None
    assert result["tabpfn_model_telemetry_default"] is False


def test_create_predictor_fails_clean_without_autogluon():
    if "autogluon" in sys.modules:
        return
    adapter = AutogluonAspaceAdapter()
    try:
        adapter.create_predictor(label="target")
    except ImportError as error:
        assert "autogluon" in str(error).lower()
    assert os.environ.get("TABPFN_DISABLE_TELEMETRY") == "1"


def test_telemetry_guard_is_zero():
    guard = AutogluonAspaceAdapter().telemetry_guard()
    assert guard["network_calls_by_adapter"] == 0
    assert guard["telemetry_sdk"] is None
