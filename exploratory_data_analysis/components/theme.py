from plotly.graph_objects import Figure


def update_layout(fig: Figure, title: str, font_size: int = 18, showlegend: bool = None):
    fig.update_layout(
        template='plotly_dark',
        title=title,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            size=font_size,
        ),
        showlegend=showlegend,
    )
