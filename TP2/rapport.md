
# CI2 - Fine-tuning a language model for text classification

##### Yohan DELIERE

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```



**Question 2**: What type is the object `setting`, and what is its structure (e.g. if it is a list, its length; if a dictionary, its keys, etc.)?

c’est un dictionnaire (dict). Sa structure = des clés (les paramètres de config du modèle) accessibles via settings.keys().

**Question 3**: What type is the object `params`, and what is its structure?

C’est un dictionnaire (dict). Sa structure = des clés (les poids/paramètres du modèle, sont organisés par modules/layers) accessibles via params.keys().


**Question 4:** Analyse the `__init__` method, and check what is the required structure for the `cfg` parameter. Is the `settings` variable we have obtained in the right format? If not, perform the mapping to convert the variable `setting` into a variable `model_config` with the right structure.

Le paramètre cfg doit être un dictionnaire avec les clés utilisées par GPTModel : vocab_size, context_length, emb_dim, n_heads, n_layers, drop_rate, qkv_bias.

settings est bien un dict, mais pas au bon format car ses clés sont celles de GPT-2/OpenAI (n_vocab, n_ctx, n_embd, n_head, n_layer). Donc il faut mapper settings -> model_config en renommant ces clés.



**Question 5.1**: In the cell above, why did we do `df = df.sample(frac=1, random_state=123)` when creating the train/test split?

On fait df.sample(frac=1, random_state=123) pour mélanger aléatoirement toutes les lignes avant de couper en train/test.
Sinon, si le fichier est un peu “trié” (par label, par type de message, par longueur, etc.), tu risques d’avoir un split biaisé.
random_state=123 sert juste à rendre le mélange reproductible (même split à chaque run).



**Question 5.2**: Analyse the datasets, what is the distribution of the two classes in the train set? Are they balanced or unbalanced? In case they are unbalanced, might this lead to issues for the fine-tuning of the model?

Dans le train set (4457 messages), on a :
ham : 3860 soit environ 86,6%
spam : 597 soit environ 13,4%

Donc c’est clairement déséquilibré (ham majoritaire).
Cela peut causer des soucis au fine-tuning : le modèle peut apprendre à prédire ham très souvent, ce qui donne une accuracy trompeusement élevée, mais une mauvaise détection des spams (recall/F1 sur spam plus faible).


**Question 7**: Looking at the batch size and the training size, how many batches will you have in total? Please report the size of the subsampled training data, you reduce it due to performance constraints.

Avec une taille de jeu d entraînement de 4457 exemples et une taille de batch de 16, le nombre total de batches est de 279. Ce résultat correspond à la valeur len(train_loader) égale à 279. Le jeu d entraînement n a pas été sous échantillonné et conserve donc une taille de 4457 exemples.




**Question 8**:

**8.1**: In the cell below, define the number of output classes (`num_classes`) for the new spam detection task.

**8.2**: Also, pring the original and updated output heads (hint: `out_head` from `GPTModel`)

**8.3**: Why do we freeze the internal layers with `param.requires_grad = False`?


8.1 Le nombre de classes de sortie est 2, correspondant aux classes ham et spam.

8.2 La tete de sortie originale est affichee avant modification, puis la tete de sortie mise a jour est affichee apres remplacement par une couche lineaire Linear 768 vers 2.

8.3 Les couches internes sont figees afin de ne pas modifier les representations generales deja apprises par GPT 2. Cela reduit le cout de calcul, limite le risque de sur apprentissage sur un petit jeu de donnees, et concentre l apprentissage sur la nouvelle tete de classification et la normalisation finale.





**Question 10**: 

Now run the cell above. You should see how the training loss changes after each batch (and epoch).
Describe thie trend: what do you see, is the model learning?

La loss baisse globalement au début puis elle fluctue beaucoup batch par batch. Entre les epochs, les métriques ne montent pas de façon monotone et on observe parfois des bascules fortes de la précision globale et de la précision spam. Cela montre que le modèle apprend quelque chose (la loss descend par rapport au tout début), mais que l apprentissage est instable et peut basculer entre des comportements trop ham ou trop spam au fil des epochs.

**Question 11 (optional)**: Change the number of epochs and/or the learning rate and/or the size of the training data, and investigate how the loss/accuracy of the model changes. You can do this editing and re-running the cells above, or creating new cells below.


En augmentant le nombre d epochs, on ne gagne pas forcément en performance, car l entraînement peut osciller et parfois se dégrader après une amélioration. Diminuer le learning rate tend à stabiliser l apprentissage mais rend la convergence plus lente.


**Question 12 (optional)**: Now test the model *on your own text*.

reussite : 

Text 1: Hello, I am the Prince of Nigeria. I am currently stuck abroad and I can't access my liquidity. If you can help by sending an advance of $2,500, I will repay you $50,000 as soon as my funds are released. Please reply quickly with your bank details. -> SPAM
Text 2: Hey, just wanted to check in and see if you're coming to the meeting tomorrow. Let me know! -> NOT SPAM