import plotly.graph_objects as go
from sklearn.decomposition import PCA
from transformers import GPT2Model

model = GPT2Model.from_pretrained("gpt2")

position_embeddings = model.wpe.weight

print("Shape position embeddings:", position_embeddings.size())

print("n_embd:", model.config.n_embd)
print("n_positions:", model.config.n_positions)

positions_50 = position_embeddings[:50].detach().cpu().numpy()
positions_200 = position_embeddings[:200].detach().cpu().numpy()

pca_50 = PCA(n_components=2)
reduced_50 = pca_50.fit_transform(positions_50)

fig_50 = go.Figure(
    data=[
        go.Scatter(
            x=reduced_50[:, 0],
            y=reduced_50[:, 1],
            mode="markers+text",
            text=[str(i) for i in range(len(reduced_50))],
            textposition="top center",
            marker=dict(
                color=list(range(len(reduced_50))),
                colorscale="Viridis",
                showscale=True,
            ),
        )
    ]
)
fig_50.update_layout(
    title="Encodages positionnels GPT-2 (PCA, positions 0-50)",
    xaxis_title="PCA 1",
    yaxis_title="PCA 2",
)

fig_50.write_html("TP1/positions_50.html")

pca_200 = PCA(n_components=2)
reduced_200 = pca_200.fit_transform(positions_200)

fig_200 = go.Figure(
    data=[
        go.Scatter(
            x=reduced_200[:, 0],
            y=reduced_200[:, 1],
            mode="markers+text",
            text=[str(i) for i in range(len(reduced_200))],
            textposition="top center",
            marker=dict(
                color=list(range(len(reduced_200))),
                colorscale="Viridis",
                showscale=True,
            ),
        )
    ]
)
fig_200.update_layout(
    title="Encodages positionnels GPT-2 (PCA, positions 0-200)",
    xaxis_title="PCA 1",
    yaxis_title="PCA 2",
)

fig_200.write_html("TP1/positions_200.html")


        
