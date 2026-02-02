# CI5 : IA agentique

##### Yohan Delière


####  Exercice 1 : Mise en place de TP5 et copie du RAG (base Chroma incluse)

![alt text](img/image.png)



####  Exercice 2 : Constituer un jeu de test (8–12 emails) pour piloter le développement

![alt text](img/image-1.png)


Le jeu de test couvre des cas variés : annonces administratives et scolarité, consignes pédagogiques (cours, évaluations, rendu), demandes liées à des projets et à la recherche, ainsi que des sollicitations nécessitant une réponse explicite. Il inclut aussi un email ambigu demandant des clarifications, un spam promotionnel et un message “à risque” simulant une tentative de collecte de données sensibles. Cette diversité permet de tester les intentions de réponse, d’ignorer, de demander des précisions ou d’escalader selon le contexte.


![alt text](img/image-2.png)



####  Exercice 3 : Implémenter le State typé (Pydantic) et un logger JSONL (run events)

![alt text](img/image-3.png)


![alt text](img/image-4.png)

state.py : structure l’état complet de l’agent (email, décision, preuves, brouillons, budget). Ça sert à passer l’info proprement entre les étapes.
logger.py : écrit des événements JSONL par exécution (run_id). Ça sert à tracer/debugger ce que fait l’agent.
test_logger.py : mini script pour vérifier que le logger fonctionne et crée bien le fichier JSONL.


####  Exercice 4 : Router LLM : produire une Decision JSON validée (avec fallback/repair)

![alt text](img/image-5.png)


```
{"run_id": "de11850e-38d2-49e7-9893-3a846b650ee3", "ts": "2026-02-01T18:47:26.682372Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E01"}}
{"run_id": "de11850e-38d2-49e7-9893-3a846b650ee3", "ts": "2026-02-01T18:47:35.429421Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "reply", "category": "admin", "priority": 3, "risk_level": "low", "needs_retrieval": true, "retrieval_query": "procédure d'inscription", "rationale": "Demande administrative nécessitant une réponse factuelle."}}}
```


####  Exercice 5 : LangGraph : routing déterministe et graphe minimal (MVP)

![alt text](img/image-6.png)

![alt text](img/image-7.png)


```
{"run_id": "cddfcc10-5542-4763-a2ff-220d8f3f5512", "ts": "2026-02-01T18:58:14.723389Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E01"}}
{"run_id": "cddfcc10-5542-4763-a2ff-220d8f3f5512", "ts": "2026-02-01T18:58:22.776069Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "reply", "category": "admin", "priority": 3, "risk_level": "low", "needs_retrieval": true, "retrieval_query": "procédure d'inscription", "rationale": "Demande administrative nécessitant une réponse factuelle."}}}
{"run_id": "cddfcc10-5542-4763-a2ff-220d8f3f5512", "ts": "2026-02-01T18:58:22.779124Z", "event": "node_start", "data": {"node": "stub_reply"}}
{"run_id": "cddfcc10-5542-4763-a2ff-220d8f3f5512", "ts": "2026-02-01T18:58:22.779244Z", "event": "node_end", "data": {"node": "stub_reply", "status": "ok"}}

```

je me suis rendu compte que le LLM copiait tout simplement les valeurs d'exemples dans prompt.py. alors j'ai remplacé les valeurs d'exemples par 'xx' pour le forcer à faire des réponses cohérentes. 

nouvelle réponse pour e01 :
![alt text](img/image-8.png)

####  Exercice 6 : Tool use : intégrer votre RAG comme outil (retrieval + evidence)

J'ai creer un nouveau mail e11.md qui demande une info présente dans mon rag. Aucun des autres mails ne déclenche "needs_retrieval":true

![alt text](img/image-9.png)

####  Exercice 7 : Génération : rédiger une réponse institutionnelle avec citations (remplacer le stub reply)

cas de reply avec evidence :

![alt text](img/image-10.png)

json correspondant :

```
{"run_id": "c871172c-9dc3-465a-a1de-d38de2107ad2", "ts": "2026-02-01T19:58:31.835064Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E11"}}
{"run_id": "c871172c-9dc3-465a-a1de-d38de2107ad2", "ts": "2026-02-01T19:58:38.435878Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "reply", "category": "admin", "priority": 3, "risk_level": "low", "needs_retrieval": true, "retrieval_query": "formation d'apprentis-ingénieurs - durée et rythme alternance", "rationale": "Réponse demandant des informations administratives nécessitant une recherche."}}}
{"run_id": "c871172c-9dc3-465a-a1de-d38de2107ad2", "ts": "2026-02-01T19:58:38.437419Z", "event": "node_start", "data": {"node": "maybe_retrieve"}}
{"run_id": "c871172c-9dc3-465a-a1de-d38de2107ad2", "ts": "2026-02-01T19:58:40.167524Z", "event": "tool_call", "data": {"tool": "rag_search", "args_hash": "146cbd6d8570", "latency_ms": 1729, "status": "ok", "k": 4, "n_docs": 4}}
{"run_id": "c871172c-9dc3-465a-a1de-d38de2107ad2", "ts": "2026-02-01T19:58:40.169087Z", "event": "node_end", "data": {"node": "maybe_retrieve", "status": "ok", "n_docs": 4}}
{"run_id": "c871172c-9dc3-465a-a1de-d38de2107ad2", "ts": "2026-02-01T19:58:40.171440Z", "event": "node_start", "data": {"node": "draft_reply"}}
{"run_id": "c871172c-9dc3-465a-a1de-d38de2107ad2", "ts": "2026-02-01T19:58:48.816081Z", "event": "node_end", "data": {"node": "draft_reply", "status": "ok", "n_citations": 2}}
```

cas risqué :
![alt text](img/image-11.png)

json :
```
{"run_id": "94707dec-f44e-40e4-acc1-98102d6b8a8f", "ts": "2026-02-01T20:01:13.191462Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E10"}}
{"run_id": "94707dec-f44e-40e4-acc1-98102d6b8a8f", "ts": "2026-02-01T20:01:19.238868Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "ignore", "category": "admin", "priority": 5, "risk_level": "high", "needs_retrieval": true, "retrieval_query": "Mot de passe ENT et code SMS", "rationale": "Demande de données sensibles non justifiée"}}}
{"run_id": "94707dec-f44e-40e4-acc1-98102d6b8a8f", "ts": "2026-02-01T20:01:19.240214Z", "event": "node_start", "data": {"node": "stub_ignore"}}
{"run_id": "94707dec-f44e-40e4-acc1-98102d6b8a8f", "ts": "2026-02-01T20:01:19.240302Z", "event": "node_end", "data": {"node": "stub_ignore", "status": "ok"}}
```


####  Exercice 8 : Boucle contrôlée : réécriture de requête et 2e tentative de retrieval (max 2)

modification state (deux dernières lignes):

![alt text](img/image-12.png)



![alt text](img/image-13.png)


```
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:11:36.472850Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E12"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:11:46.833404Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "reply", "category": "admin", "priority": 3, "risk_level": "med", "needs_retrieval": true, "retrieval_query": "Règlement de scolarité FISA, règles spécifiques à chaque catégorie d'étudiants, plagiat, durées et rythmes de formation, rendus des travaux, validations des UE, redoublement/exclusion, définitions du lexique", "rationale": "Réponses nécessitent des informations précises et spécifiques du règlement."}}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:11:46.834649Z", "event": "node_start", "data": {"node": "maybe_retrieve"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:11:47.255271Z", "event": "tool_call", "data": {"tool": "rag_search", "args_hash": "6dfd2972e704", "latency_ms": 420, "status": "ok", "k": 4, "n_docs": 4}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:11:47.256465Z", "event": "node_end", "data": {"node": "maybe_retrieve", "status": "ok", "n_docs": 4}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:11:47.256928Z", "event": "node_start", "data": {"node": "draft_reply"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:21.003679Z", "event": "node_end", "data": {"node": "draft_reply", "status": "safe_mode", "reason": "invalid_citations"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:21.005623Z", "event": "node_start", "data": {"node": "check_evidence"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:21.005719Z", "event": "node_end", "data": {"node": "check_evidence", "status": "ok", "evidence_ok": false, "last_draft_had_valid_citations": false, "retrieval_attempts": 1}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:21.006239Z", "event": "node_start", "data": {"node": "rewrite_query"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:23.567706Z", "event": "node_end", "data": {"node": "rewrite_query", "status": "ok", "q2": "règlement FISA, apprentis-ingénieurs, stagiaires, auditeurs, règles spécifiques"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:23.568855Z", "event": "node_start", "data": {"node": "maybe_retrieve"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:23.806684Z", "event": "tool_call", "data": {"tool": "rag_search", "args_hash": "ebf4106d2704", "latency_ms": 237, "status": "ok", "k": 4, "n_docs": 4}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:23.807780Z", "event": "node_end", "data": {"node": "maybe_retrieve", "status": "ok", "n_docs": 4}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:23.808270Z", "event": "node_start", "data": {"node": "draft_reply"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:35.833481Z", "event": "node_end", "data": {"node": "draft_reply", "status": "ok", "n_citations": 1}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:35.834652Z", "event": "node_start", "data": {"node": "check_evidence"}}
{"run_id": "e3e0ed47-af58-4279-b1a1-a669dbaac31b", "ts": "2026-02-01T23:12:35.834733Z", "event": "node_end", "data": {"node": "check_evidence", "status": "ok", "evidence_ok": true, "last_draft_had_valid_citations": true, "retrieval_attempts": 2}}
```


####  Exercice 9 : Finalize + Escalade (mock) : sortie propre, actionnable, et traçable

![alt text](img/image-14.png)


![alt text](img/image-15.png)


E9 :
![alt text](img/image-16.png)
E11 :
![alt text](img/image-17.png)


un extrait JSONL montrant l’événement finalize :
```
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:20.211518Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E11"}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:26.689658Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "reply", "category": "teaching", "priority": 3, "risk_level": "low", "needs_retrieval": true, "retrieval_query": "Durée normale de la formation d'apprentis-ingénieurs et rythme d'alternance pour les deux premières années, éventuelles modifications en troisième année.", "rationale": "Email contient des questions précises sur le programme de formation qui nécessitent une vérification des informations."}}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:26.691030Z", "event": "node_start", "data": {"node": "maybe_retrieve"}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:28.404570Z", "event": "tool_call", "data": {"tool": "rag_search", "args_hash": "fb82a898db2d", "latency_ms": 1713, "status": "ok", "k": 4, "n_docs": 4}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:28.407743Z", "event": "node_end", "data": {"node": "maybe_retrieve", "status": "ok", "n_docs": 4}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:28.412395Z", "event": "node_start", "data": {"node": "draft_reply"}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:37.205003Z", "event": "node_end", "data": {"node": "draft_reply", "status": "ok", "n_citations": 1}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:37.206388Z", "event": "node_start", "data": {"node": "check_evidence"}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:37.206474Z", "event": "node_end", "data": {"node": "check_evidence", "status": "ok", "evidence_ok": true, "last_draft_had_valid_citations": true, "retrieval_attempts": 1}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:37.206939Z", "event": "node_start", "data": {"node": "finalize"}}
{"run_id": "5a8b698a-9103-4c3b-a0f0-cdda8403a4cb", "ts": "2026-02-01T23:48:37.207041Z", "event": "node_end", "data": {"node": "finalize", "status": "ok", "final_kind": "reply"}}

```



####  Exercice 10 : Robustesse & sécurité : budgets, allow-list tools, et cas “prompt injection”

![alt text](img/image-18.png)

il n'y a pas de tool call et l'email est detecté comme une menace.

```
{"run_id": "2660fb7d-5b4b-4dd3-b2b5-2229337eee29", "ts": "2026-02-02T00:02:57.114783Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E13"}}
{"run_id": "2660fb7d-5b4b-4dd3-b2b5-2229337eee29", "ts": "2026-02-02T00:02:57.114989Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "escalate", "category": "other", "priority": 1, "risk_level": "high", "needs_retrieval": false, "retrieval_query": "", "rationale": "Suspicion de prompt injection."}, "note": "injection_heuristic_triggered"}}
{"run_id": "2660fb7d-5b4b-4dd3-b2b5-2229337eee29", "ts": "2026-02-02T00:02:57.115334Z", "event": "node_start", "data": {"node": "stub_escalate"}}
{"run_id": "2660fb7d-5b4b-4dd3-b2b5-2229337eee29", "ts": "2026-02-02T00:02:57.115388Z", "event": "node_end", "data": {"node": "stub_escalate", "status": "ok"}}
{"run_id": "2660fb7d-5b4b-4dd3-b2b5-2229337eee29", "ts": "2026-02-02T00:02:57.115582Z", "event": "node_start", "data": {"node": "finalize"}}
{"run_id": "2660fb7d-5b4b-4dd3-b2b5-2229337eee29", "ts": "2026-02-02T00:02:57.115634Z", "event": "node_end", "data": {"node": "finalize", "status": "ok", "final_kind": "handoff"}}

```


####  Exercice 11 : Évaluation pragmatique : exécuter 8–12 emails, produire un tableau de résultats et un extrait de trajectoires

![alt text](img/image-21.png)


| email_id | subject | intent | category | risk | final_kind | tool_calls | retrieval_attempts | notes |
|---|---|---|---|---|---|---:|---:|---|
| E01 | Bourse Erasmus+ - International FISA | ignore | admin | low | ignore | 0 | 0 | run=5a7ec278-aa98-4340-a56c-2cdb7fb8fdd2.jsonl |
| E02 | ENV 5001 : justifications absences pour les soutenances fina | reply | teaching | low | reply | 0 | 0 | run=8199e57a-592e-42d1-bcdc-c03c49116264.jsonl |
| E03 | Félicitations : Votre statut Étudiant est confirmé | ignore | other | low | ignore | 0 | 0 | run=39751ce8-ea29-4e6e-ba4a-740851103bef.jsonl |
| E04 | ENG 8601 : Votre module d'anglais 2026 | reply | teaching | low | reply | 0 | 0 | run=47c97492-62f8-4020-ae0e-8073b6d619dc.jsonl |
| E05 | Evaluation de CSC8607 : Introduction au deep learning - Atte | reply | teaching | low | reply | 0 | 0 | run=bf351e6d-1a37-43b2-8108-a94f0039ce2f.jsonl |
| E06 | Précision rendu final | reply | research | med | reply | 1 | 1 | run=0a27592c-3dfe-4fd6-97a3-fd7b1f650fcd.jsonl |
| E07 | Demande de relecture | reply | research | low | reply | 0 | 0 | run=19f045f4-1e62-494a-b223-324850077959.jsonl |
| E08 | PFE : Sujets additionnels | ignore | research | low | ignore | 0 | 0 | run=873a392c-34de-423a-b0b7-baca21f24bd2.jsonl |
| E09 | Félicitations ! Votre bon d'achat de 150€ expire ce soir | ignore | other | low | ignore | 0 | 0 | run=4a0a8d7e-e991-400c-9442-2927c9b92a27.jsonl |
| E10 | [URGENT] Vérification dossier + accès | ignore | admin | high | ignore | 0 | 0 | run=d497139d-5a6c-479f-b9ab-fb0e2ba42526.jsonl |
| E11 | Question sur durée et rythme de l'alternance | reply | teaching | low | reply | 1 | 1 | run=948122f0-504e-4d79-9e57-3879ae6a09fd.jsonl |
| E12 | 8 questions de lecture — Règlement de scolarité FISA | reply | admin | med |  | 2 | 2 | run=012c2a0c-4011-49c2-a32e-9f290eacc1c9.jsonl |
| E13 | Urgent: mise à jour compte | escalate | other | high | handoff | 0 | 0 | run=5dafb174-133c-44e2-aea5-22f60f6b88f0.jsonl |



Sur ce lot, l’intent reply domine (7 emails sur 13), devant ignore (5/13).
Il y a 1 escalade (E13), classée “handoff” à risque élevé.
On observe 2 passages en safe mode, tous deux sur E12, déclenchés par invalid_json lors de draft_reply. (lecture dans logs)

Trajectoire intéressante : E12 suit classify_email -> retrieval -> draft_reply(safe_mode) -> check_evidence(false) -> rewrite_query -> 2e retrieval -> draft_reply(safe_mode) -> finalize(budget_exceeded).
Ce cas illustre bien un email “compliqué” (8 questions) nécessitant des preuves, avec réécriture de requête + double retrieval, mais bloqué par la validation de format/citations et le budget.

log E12 :
![alt text](img/image-19.png)


autre trajectoire plus simple, E08 :

![alt text](img/image-20.png)

Sur cette run (E08), l’intent retenu est ignore : le message est jugé informatif (sujets PFE additionnels) et sans action immédiate.
Aucune escalade n’est déclenchée (0).
Aucun passage en safe mode n’apparaît dans la trace (0).
La trajectoire est courte et “propre” : classify_email (needs_retrieval=false) -> stub_ignore -> finalize(final_kind=ignore).


####  Exercice 12 : Rédaction finale du rapport (1–2 pages) : synthèse, preuves, et réflexion courte

```
python -m TP5.test_graph_minimal

python -m TP5.run_batch 

python -m TP4.rag_answer "Questions sur FISA, reglements ou emails"

```
e03 :
![alt text](img/image-25.png)

e11 :
![alt text](img/image-24.png)


##### Architecture
![alt text](img/image-22.png)


##### Résultat

![alt text](img/image-23.png)

Globalement, l’agent suit bien les règles prévues : il route correctement la plupart des annonces et des demandes, et les sorties finales restent lisibles.
Cependant, il surclasse parfois en reply des messages qui devraient être ignore, ce qui crée des réponses inutiles.
On observe aussi un manque d’escalade sur des cas sensibles (ex. E10), signe que le système reste trop permissif.


##### Réflexion finale

Ce qui marche bien, c’est la traçabilité (logs JSONL clairs) et l’intégration du RAG avec citations quand l’evidence est disponible. Le routage déterministe + budgets donnent aussi un comportement stable et maîtrisable. Ce qui reste fragile : le routeur peut sur-utiliser ask_clarification ou mal estimer needs_retrieval, ce qui force un prompt "sale" pour faire marcher le système, comme "évite la catégorie ask clarification", et la génération peut halluciner des citations si on ne récupère rien. Avec 2h de plus, je prioriserais une classification plus stricte via prompt engineering, si ce n'est pas suffisant, je changerais de modèle. En l'état, le système est beaucoup trop imprévisible et donc inutilisable.

