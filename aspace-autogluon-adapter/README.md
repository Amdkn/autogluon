# Adapter A'Space — autogluon (D-N053, pas A)

**Adresse :** `fiber:a0:autogluon` · **Gel :** `e3cb3b7` (commit amont
2026-11-03, branche par défaut `master`, version 1.6.4) · **Licence :**
Apache-2.0 · **État visé :** 1 Adapté · **Dérive amont :** 13 commits.

## Bind (avant l'adapter, §D8)

Le pin V5 était brut (sans bind). Bind créé sur la branche
`aspace-v5-native` : `aspace-plugin.json` (16L, format ML identique à
mitra-2 / tabfm / chronos-forecasting — diff contre le bind mitra-2 :
seuls `name`, `submodule_path`, `sovereign_fork_url` diffèrent),
commit `efadb39`, parent `e3cb3b7`, vérifié à l'API. Le fichier est
ignoré par le `.gitignore` amont (`*.json`, ligne 10) : ajout par
`git add -f`, consigné ici. Le bind est re-appliqué **verbatim** sur
`master` au-dessus de l'adapter (commit dédié, fichiers du bind seuls,
per F8 D2).

## Ce que fait l'adapter

`autogluon_aspace_adapter.AutogluonAspaceAdapter` — seule surface A'Space
du fork `Amdkn/autogluon`.

- `describe()` — épinglage, licence, contrat (aucun import lourd).
- `disable_telemetry()` — force `TABPFN_DISABLE_TELEMETRY=1` (idempotent ;
  l'amont défaut `model_telemetry` est déjà `False` dans les modèles
  TabPFN v2/v2.5/v3).
- `create_predictor(*args, **kwargs)` — construit `TabularPredictor`
  (import paresseux, télémétrie coupée avant).
- `telemetry_guard()` — garde-fous réseau constatés (0 appel par l'adapter).

## Ce que l'adapter ne fait pas

- Il ne modifie **aucun** fichier amont (`core/`, `tabular/`, `common/`,
  `autogluon/` intacts — H-M2).
- Il ne monte **aucun poids** (TabPFN / Mitra : téléchargement explicite
  par l'opérateur, hors adapter ; travail R1 pour les miroirs HF).
- Il n'appelle pas les moteurs d'inférence V5
  (`02_PredictiveWargame_MachineLearning/` — travail R1, branche
  `ryan/d-n052-r1`).

## Tests

- Smoke adapter : `tests/test_adapter_smoke.py` (import sans `autogluon`,
  pin, télémétrie coupée, `describe()`).
- Suite amont bornée (périmètre nommé avant exécution) :
  `tabular/tests/unittests/test_model_class_settings.py` (interrupteur
  télémétrie / réglages de classe) +
  `tabular/tests/unittests/test_global_settings.py` — bilan dans le
  rapport du pas A. La suite complète du framework (milliers de tests,
  fits réels, GPU) est hors périmètre sur cette VM (6 Go RAM, 1,5 CPU).
