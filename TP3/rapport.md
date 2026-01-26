# CI3 - Parameter-Efficient Fine-Tuning with LoRA

##### Yohan DELIERE

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```




Dans l'exo 1, 2, 3, 4 nous avons créé la couche LoRA, l'avons fusionnée avec les couches linéaires d'origine, avons automatisé son injection récursive dans le modèle GPT et, enfin, gelé les paramètres initiaux pour ne rendre entraînables que les nouvelles matrices légères, optimisant ainsi drastiquement l'efficacité du fine-tuning.


```
Original Model Structure (Truncated):
TransformerBlock(
  (att): MultiHeadAttention(
    (W_query): Linear(in_features=768, out_features=768, bias=True)
    (W_key): Linear(in_features=768, out_features=768, bias=True)
    (W_value): Linear(in_features=768, out_features=768, bias=True)
    (out_proj): Linear(in_features=768, out_features=768, bias=True)
    (dropout): Dropout(p=0.1, inplace=False)
  )
  (ff): FeedForward(
    (layers): Sequential(
      (0): Linear(in_features=768, out_features=3072, bias=True)
      (1): GELU()
      (2): Linear(in_features=3072, out_features=768, bias=True)
    )
  )
  (norm1): LayerNorm()
  (norm2): LayerNorm()
  (drop_resid): Dropout(p=0.1, inplace=False)
)

Model Structure After LoRA (Truncated):
TransformerBlock(
  (att): MultiHeadAttention(
    (W_query): LinearWithLoRA(
      (linear): Linear(in_features=768, out_features=768, bias=True)
      (lora): LoRALayer()
    )
    (W_key): LinearWithLoRA(
      (linear): Linear(in_features=768, out_features=768, bias=True)
      (lora): LoRALayer()
    )
    (W_value): LinearWithLoRA(
      (linear): Linear(in_features=768, out_features=768, bias=True)
      (lora): LoRALayer()
    )
    (out_proj): LinearWithLoRA(
      (linear): Linear(in_features=768, out_features=768, bias=True)
      (lora): LoRALayer()
    )
    (dropout): Dropout(p=0.1, inplace=False)
  )
  (ff): FeedForward(
    (layers): Sequential(
      (0): LinearWithLoRA(
        (linear): Linear(in_features=768, out_features=3072, bias=True)
        (lora): LoRALayer()
      )
      (1): GELU()
      (2): LinearWithLoRA(
        (linear): Linear(in_features=3072, out_features=768, bias=True)
        (lora): LoRALayer()
      )
    )
  )
  (norm1): LayerNorm()
  (norm2): LayerNorm()
  (drop_resid): Dropout(p=0.1, inplace=False)
)

Parameter Count:
trainable params: 1,327,104 || all params: 164,364,288 || trainable%: 0.81%
```


**Question 1:** Do you see any difference between "Original Model Structure (Truncated)" and "Model Structure After LoRA (Truncated)"? Do you see the LinearWithLoRA you have defined above?

Une modification structurelle est bien visible. Les couches initialement identifiées comme Linear (par exemple pour W_query, W_key ou dans le bloc FeedForward) ont été remplacées par des instances de LinearWithLoRA. Cela confirme que la fonction de remplacement a correctement parcouru l'architecture pour injecter le wrapper autour des couches linéaires d'origine.


**Question 2:** What is the number of trainable parameters, all parameters, and the fraction of trainable parameters?

D'après les mesures effectuées, le modèle contient désormais :

- Paramètres entraînables : 1 327 104

- Total des paramètres : 164 364 288

Fraction : 0,81 %

Seule une infime partie du modèle (moins de 1 %) sera donc mise à jour pendant la phase d'apprentissage, ce qui valide l'efficacité de la méthode LoRA pour économiser les ressources.



**Question 3:** Check the number (and fraction) of trainable parameters, and compare it with the one above. Do you see any differences? Can you describe them?


L'augmentation du nombre de paramètres entraînables (de 1,32M à 1,33M) est due à l'ajout de la nouvelle tête de classification.

Parallèlement, le pourcentage grimpe à 1,06 % car le nombre total de paramètres a chuté (de 164M à 125M). Cette baisse s'explique par la suppression de la tête de langage d'origine, qui était très lourde, au profit d'une tête beaucoup plus légère limitée à deux sorties.



**Question 4:** Can you describe the trend of the loss, and the final accuracy. Is it reasonable considering the task at hand?



```
Epoch 1 | Batch 0 | Loss: 2.9491
Epoch 1 | Batch 10 | Loss: 0.2247
Epoch 1 | Batch 20 | Loss: 0.1505
Epoch 1 | Batch 30 | Loss: 0.2317
Epoch 1 | Batch 40 | Loss: 0.0492
Epoch 1 | Batch 50 | Loss: 0.0341
Epoch 1 | Batch 60 | Loss: 0.1230
Epoch 1 | Batch 70 | Loss: 0.0030
Epoch 1 | Batch 80 | Loss: 0.0017
Epoch 1 | Batch 90 | Loss: 0.0008
Epoch 1 | Batch 100 | Loss: 0.0050
Epoch 1 | Batch 110 | Loss: 0.0057
Epoch 1 | Batch 120 | Loss: 0.3190
Epoch 1 | Batch 130 | Loss: 0.2693
Epoch 1 | Batch 140 | Loss: 0.0186
Epoch 1 Finished | Avg Loss: 0.2007 | Acc: 94.30% | Time: 386.76s

```

La perte (loss) montre une chute rapide et impressionnante dès les premiers lots, passant de 2,94 à environ 0,22 en seulement dix itérations. Malgré quelques légers sursauts vers la fin (peut êtres des exemples ambigus), la tendance globale est une stabilisation vers des valeurs très basses.

La précision finale de 94,30 % en une seule époque est excellente. C'est peut être raisonnable et cohérent pour cette tâche :

La simplicité du problème : La détection de spam repose souvent sur des mots-clés ou des structures de phrases très spécifiques que GPT-2 capte très vite.

L'efficacité du LoRA : Même avec moins de 1 % de paramètres modifiés, le modèle arrive à réutiliser ses connaissances linguistiques massives pour se spécialiser efficacement.

Rapidité : Atteindre ce score en moins de 7 minutes montre que l'adaptation de bas rang est parfaitement adaptée au fine-tuning sur de petits jeux de données



**Question 5:** How is the accuracy, and how does it compare to the Train set accuracy?

La précision sur le jeu de test est excellente (96,32 %), dépassant même celle de l'entraînement (94,30 %). Sur le papier, cela indique que le modèle généralise très bien.

Cependant, les tests réels montrent une limite : le modèle est devenu un « expert » très ciblé sur les SMS. Il détecte parfaitement les spams avec des symboles de monnaie (£) ou des mots comme "WINNER", mais il échoue sur les arnaques de type "e-mail" (prince nigérian, prix en cash).

En résumé, l'accuracy est très haute parce qu'elle reflète le succès sur le dataset spécifique, mais le modèle reste (probablement vu nos tests) aveugle aux styles de spams qu'il n'a pas vus durant son entraînement LoRA.