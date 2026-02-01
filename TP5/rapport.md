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




