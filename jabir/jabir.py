import reflex as rx
from jabir import style
from jabir.state import State


data = [
    {"name": "Page A", "uv": 4000, "pv": 2400, "amt": 2400},
    {"name": "Page B", "uv": 3000, "pv": 1398, "amt": 2210},
    {"name": "Page C", "uv": 2000, "pv": 9800, "amt": 2290},
    {"name": "Page D", "uv": 2780, "pv": 3908, "amt": 2000},
    {"name": "Page E", "uv": 1890, "pv": 4800, "amt": 2181},
    {"name": "Page F", "uv": 2390, "pv": 3800, "amt": 2500},
    {"name": "Page G", "uv": 3490, "pv": 4300, "amt": 2100},
]


def get_chart():
    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key="pv",
            stroke="#8884d8",
        ),
        rx.recharts.line(
            data_key="uv",
            stroke="#82ca9d",
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(),
        data=data,
        width=500,
        height=200,
    )

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.hstack(rx.chakra.avatar(size="md"), rx.box(question, text_align='right')),
        rx.hstack(rx.chakra.avatar(size="md"), rx.box(answer, text_align='left')),
        rx.hstack(
            get_chart(),
            get_chart()
        )
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1])
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
        chat(),
        prompt()
    )


app = rx.App()
app.add_page(index)
