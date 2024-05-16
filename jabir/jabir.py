import reflex as rx
from jabir import style
from jabir.state import State
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime



klse_pred_data = pd.read_csv('./jabir/KLSE_preds.csv')
klse_old_data = pd.read_csv('./jabir/KLSE.csv')
palm_oil_pred_data = pd.read_csv('./jabir/palm-oil-preds.csv')
palm_oil_data = pd.read_csv('./jabir/palm-oil.csv')
usd_pkr_data = pd.read_csv('./jabir/usd-pkr.csv')


def get_meter():
    return rx.image(src=f'chart-{State.scale}.png', width='500px')

def get_klse_chart():
    # fig = px.line(klse_old_data, x="Date", y="Close", title='Life expectancy in Canada')
    # set up plotly figure
    fig = go.Figure(layout=go.Layout())

    # Add line / trace 1 to figure
    fig.add_trace(go.Scatter(
        x=klse_old_data['Date'],
        y=klse_old_data['Close'],
        marker=dict(color="blue"),
        showlegend=False,  # This hides the trace from the legend
        name='KLSE Close'  # This sets the label for the trace
    ))

    layout = go.Layout(
        title="Plot Title",
        xaxis_title="X Axis Title",
        yaxis_title="Y Axis Title",
        legend_title_text="Legend Title",  # This sets the legend title
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )

    
    fig.layout = layout
    return rx.plotly(data=fig)

def get_palm_oil_chart():
    fig = go.Figure()

    # add line / trace 1 to figure
    fig.add_trace(go.Scatter(
        x=palm_oil_data['Date'],
        y=palm_oil_data['Close'],
        marker=dict(
            color="blue"
        ),
        showlegend=False
    ))
    return rx.plotly(data=fig)

def get_usd_pkr_chart():
    fig = go.Figure()

    # add line / trace 1 to figure
    fig.add_trace(go.Scatter(
        x=usd_pkr_data['Date'],
        y=usd_pkr_data['Close'],
        marker=dict(
            color="blue"
        ),
        showlegend=False
    ))
    return rx.plotly(data=fig)


def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.chakra.avatar(size="sm"), 
            rx.heading('You', size="3")
        ),
        rx.hstack(
            rx.markdown(question, text_align='right'),
            style=style.avatay_styles
        ),
        rx.hstack(
            rx.chakra.avatar(src='avatar.jpeg', size="sm"), 
            rx.heading('Jabir.AI', size="3")
        ),
        rx.hstack(
            rx.markdown(answer, text_align='left'),
            style=style.avatay_styles
        ),
        rx.vstack(
            get_klse_chart(),
            get_palm_oil_chart(),
            get_usd_pkr_chart(),
            get_meter(),
            align='center'
        )
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


def header() -> rx.Component:
    return rx.flex(
        rx.callout(
            "Jabir.ai - Empower your procurement decisions",
            size="3",
            style=dict(margin_top="1em",width= "100%", justify_content="center")
        )
    )

def prompt() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.input(
                value=State.question,
                placeholder='Ask a question', 
                style=style.input_style,
                on_change=State.set_question,

            ),
            rx.button(
                'Ask', 
                style=style.button_style,
                on_click=State.answer    
            ),
            style=style.prompt_style
        )
    )


def index() -> rx.Component:
    return rx.container(
        header(),
        chat(),
        prompt()
    )


app = rx.App()
app.add_page(index)
