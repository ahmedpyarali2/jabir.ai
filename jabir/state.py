import reflex as rx
import asyncio
import requests
import json
import time
import re
from datetime import date
import aiohttp


class State(rx.State):
    question: str
    chat_history: list[tuple[str]]

    async def answer(self):
        url = "https://127d-202-70-144-241.ngrok-free.app/api/chat"

        assistantData = open("jabir/assistantData.txt", "r")
        userData = '''
                    Question: ["prior context: I am a procurement specialist from bazaar i am looking to procure oil for manufacturing oil products, in pakistan the date is {date}
                     {prompt}
                    "]

                    Output:
                    Risk Analysis:
                    It should include easy-to-read and detailed explanation on the query asked by user regarding the raw material's procurement option. It should provide justified reasons based on the local Pakistani and global market trends.

                    Trend:
                    It should give user market trends of that raw material based on the local Pakistani and international market data.

                    Recommendations:
                    It should provide user with the potential business options with proper mathematical and logical reasonings so they can make an informed data-driven decision.

                    Justification:
                    Why, how and what led you to this conclusion and justify your claims.

                    Data Points:
                    It should provide us the forecasted data points in a tabular form.

                    Scale:
                    It should give us a score on a scale of 1 to 5 if it is a good bet or not to purchase or not purchase that raw material.
                '''
        # print("User Data: ")
        # print(userData.format(date=date.today(), prompt=self.question))

        payload = json.dumps({
        "model": "jabir.ai",
        # "prompt": f"{self.question}",
        "stream": False,
        "messages": [
            {
                "role": "assistant",
                "content": f"{assistantData.read()}"
            },
            {
                "role": "user",
                "content": userData.format(date=date.today(), prompt=self.question)
            }
        ]
        })

        
        headers = {
        'Content-Type': 'application/json'
        }

        try:
            print('Sending request...')
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload, timeout=300) as response:
                    print('Received response')
                    answer = await response.text()
                    # print('Response: ' + answer)

                    answer = json.loads(answer)["message"]["content"]
                    # print(answer)
                    AnsweringStateLoader.answering = True
                    self.chat_history.append((self.question, ''))
                    self.question = ''

                    print('Streaming answer')
                    print(answer)
                    for i in range(len(answer)):
                        # Pause to show the streaming effect.
                        await asyncio.sleep(0.01)
                        # Add one letter at a time to the output.
                        self.chat_history[-1] = (
                            self.chat_history[-1][0],
                            answer[: i + 1],
                        )
                        yield

                # answer = 'Hello Worldddddddddd!!'
                # self.chat_history.append((self.question, ''))
                # self.question = ''
                # for i in range(len(answer)):
                #     # Pause to show the streaming effect.
                #     await asyncio.sleep(0.01)
                #     # Add one letter at a time to the output.
                #     self.chat_history[-1] = (
                #         self.chat_history[-1][0],
                #         answer[: i + 1],
                #     )
                #     yield
        except asyncio.TimeoutError:
            print("Request timed out")

        AnsweringStateLoader.answering = False


class AnsweringStateLoader(rx.State):
    answering = False

    