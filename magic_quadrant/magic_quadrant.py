#/usr/bin/env python3

import plotly.express as px


def create_mq(df, x, x_min, x_max, y, y_min, y_max, text, lower_left, lower_right, upper_left, upper_right, height=800, width=800):

    # Consolidate rows with same x and y value by concatenating text labels
    df = (
        df.groupby([x, y])[text]
        .apply(lambda names: "&".join(names))  # concatenate names
        .reset_index()
    )


    fig = px.scatter(
        df,
        x=x,
        y=y,
        text=text
    )

    # Add quadrant lines at midpoint
    x_mid = (x_min + x_max) / 2
    y_mid = (y_min + y_max) / 2

    fig.add_shape(type="line", x0=x_mid, y0=y_min, x1=x_mid, y1=y_max, line=dict(color="gray", dash="dash"))
    fig.add_shape(type="line", x0=x_min, y0=y_mid, x1=x_max, y1=y_mid, line=dict(color="gray", dash="dash"))

    fig.add_shape(type="line", x0=x_min, y0=y_min, x1=x_min, y1=y_max, line=dict(color="black"))
    fig.add_shape(type="line", x0=x_min, y0=y_min, x1=x_max, y1=y_min, line=dict(color="black"))
    fig.add_shape(type="line", x0=x_max, y0=y_min, x1=x_max, y1=y_max, line=dict(color="black"))
    fig.add_shape(type="line", x0=x_min, y0=y_max, x1=x_max, y1=y_max, line=dict(color="black"))

    fig.add_annotation(x=4, y=5, xanchor="center", yanchor="top", text=upper_right, showarrow=False, font=dict(family="Helvetica Bold",size=18, color="blue"))
    fig.add_annotation(x=2, y=5, xanchor="center", yanchor="top",  text=upper_left, showarrow=False, font=dict(family="Helvetica Bold",size=18, color="blue"))
    fig.add_annotation(x=4, y=1, xanchor="center", yanchor="bottom", text=lower_right, showarrow=False, font=dict(family="Helvetica Bold",size=18, color="blue"))
    fig.add_annotation(x=2, y=1, xanchor="center", yanchor="bottom", text=lower_left, showarrow=False, font=dict(family="Helvetica Bold",size=18, color="blue"))

    # Adjust text labels
    fig.update_traces(textposition="top center")

    fig.update_layout(
        xaxis=dict(dtick=1),
        yaxis=dict(dtick=1),
        width=width, 
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=16, color="black", family="Helvetica Bold")
    )

    return fig


