"""A'Space adapter for AutoGluon (D-N053, pas A).

Seul code A'Space du fork. Le framework amont (``core/``, ``tabular/``,
``common/``, ...) n'est jamais modifie : l'adapter est une fine enveloppe
qui epingle le gel, coupe la telemetrie TabPFN avant tout fit et expose la
surface minimale utilisee par le Runtime A'Space (orchestrateur ML du
triptyque ``triptych_autogluon_engine.py``).

Regles :
- Aucun import tiers au niveau module (stdlib seule). ``autogluon`` n'est
  importe qu'a l'interieur des methodes qui en ont besoin, jamais a
  l'import de l'adapter.
- Telemetrie : l'amont ne declare aucun SDK de telemetrie ; le seul
  emetteur connu est la telemetrie TabPFN (``model_telemetry``, defaut
  ``False`` dans les modeles TabPFN v2/v2.5/v3). L'adapter force
  ``TABPFN_DISABLE_TELEMETRY=1`` avant tout import d'``autogluon`` et
  avant tout fit (voir ``disable_telemetry()``).
- Aucun appel reseau par l'adapter. Les modeles qui telechargent des poids
  (TabPFN, Mitra) ne le font que sur appel explicite de l'operateur, hors
  adapter.
"""

from __future__ import annotations

import os

PINNED_AUTOGLUON_COMMIT = "e3cb3b71386c54ff11155d6e7a67f6b43f117208"
PINNED_AUTOGLUON_VERSION = "1.6.4"
PINNED_AUTOGLUON_BIND = "efadb394a2762ca3562920c25026dd64e36d4336"
FIBER_ID = "fiber:a0:autogluon"
LICENSE = "Apache-2.0"
ADAPTER_VERSION = "0.1.0"


class AutogluonAspaceAdapter:
    """Surface A'Space minimale au-dessus de ``TabularPredictor``."""

    def describe(self) -> dict:
        """Decrit l'adapter epingle (aucun import lourd, aucune E/S)."""
        return {
            "fiber_id": FIBER_ID,
            "adapter": "aspace-autogluon-adapter",
            "adapter_version": ADAPTER_VERSION,
            "pinned_commit": PINNED_AUTOGLUON_COMMIT,
            "pinned_version": PINNED_AUTOGLUON_VERSION,
            "pinned_bind": PINNED_AUTOGLUON_BIND,
            "license": LICENSE,
            "upstream_class": "autogluon.tabular.TabularPredictor",
            "telemetry": "zero par contrat (voir autogluon-TELEMETRY-AUDIT.md)",
        }

    def disable_telemetry(self) -> dict:
        """Coupe la telemetrie TabPFN (idempotent, avant tout fit)."""
        before = os.environ.get("TABPFN_DISABLE_TELEMETRY")
        os.environ["TABPFN_DISABLE_TELEMETRY"] = "1"
        return {
            "TABPFN_DISABLE_TELEMETRY": "1",
            "previous_value": before,
            "tabpfn_model_telemetry_default": False,
        }

    def create_predictor(self, *args, **kwargs):
        """Construit ``TabularPredictor`` (import paresseux, telemetrie coupee)."""
        self.disable_telemetry()
        from autogluon.tabular import TabularPredictor

        return TabularPredictor(*args, **kwargs)

    def telemetry_guard(self) -> dict:
        """Garde-fous reseau de l'adapter (constat, pas une promesse)."""
        return {
            "network_calls_by_adapter": 0,
            "telemetry_sdk": None,
            "tabpfn_telemetry_forced_off": os.environ.get("TABPFN_DISABLE_TELEMETRY") == "1",
        }


__all__ = [
    "ADAPTER_VERSION",
    "FIBER_ID",
    "LICENSE",
    "PINNED_AUTOGLUON_BIND",
    "PINNED_AUTOGLUON_COMMIT",
    "PINNED_AUTOGLUON_VERSION",
    "AutogluonAspaceAdapter",
]
