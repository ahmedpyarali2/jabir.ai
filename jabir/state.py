import reflex as rx
import asyncio
import requests
import json
import time
import re
from datetime import date
import aiohttp
import matplotlib.pyplot as plt



class State(rx.State):
    question: str
    chat_history: list[tuple[str]]
    scale: int


    def image(self):
        colors = ['#4dab6d', "#72c66e", "#fabd57", "#f36d54", "#ee4d55"]

        values = [5,4,3,2,1,0]

        x_axis_vals = [0,0.66,1.32,1.98,2.64]
        axes=[(3.0,2.25),(2.26,2.25),(1.6,2.25),(0.95,1.95),(0.20,2.1)]
        fig = plt.figure(figsize=(10,10))

        ax = fig.add_subplot(projection="polar");

        ax.bar(x=[0,0.66,1.32,1.98,2.64], width=0.5, height=0.5, bottom=2,
                linewidth=3, edgecolor="white",
                color=colors, align="edge");

        plt.annotate("Great", xy=(0.20,2.1), rotation=-77, color="white", fontweight="bold");
        plt.annotate("Very Good", xy=(0.95,1.95), rotation=-40, color="white", fontweight="bold");
        plt.annotate("Good", xy=(1.6,2.25), rotation=0, color="white", fontweight="bold");
        plt.annotate("Bad", xy=(2.26,2.25), rotation=47,color="white", fontweight="bold");
        plt.annotate("Very Bad", xy=(3.0,2.25), rotation=77, color="white", fontweight="bold");
        # plt.annotate("Volatile", xy=(2.46,2.25), rotation=45, color="white", fontweight="bold");
        # plt.annotate("Unsustainable", xy=(3.0,2.25), rotation=75, color="white", fontweight="bold");

        # for loc, val in zip([0,0.66,1.32,1.98,2.64], values):
        #     plt.annotate(val, xy=(loc, 2.5), ha="right" if val<=20 else "left");

        plt.annotate("score", xytext=(0,0), xy=axes[self.scale],
                    arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="black", shrinkA=0),
                    bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0, ),
                    fontsize=25, color="white", ha="center"
                    );


        plt.title("Buying Indicator ", loc="center", pad=20, fontsize=35, fontweight="bold");

        ax.set_axis_off();
        plt.savefig(f'./assets/chart-{self.scale}.png', dpi=300, bbox_inches='tight')

    def find_scale(self, answer):
        pattern = r"(\d+)(?:\s+out of 5|/5)"
        matches = re.findall(pattern, answer)
        extracted_values = [int(match[0]) for match in matches]

        # Print the extracted ratings (x values)
        self.scale = extracted_values[0] - 1
        print(self.scale)

    async def answer(self):
        url = "http://localhost:11434/api/chat"

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
                    self.find_scale(answer)

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

                # answer = 'Hello Worldddddddddd!! Score is 1 out of 5'
                # self.chat_history.append((self.question, ''))
                # self.question = ''
                # self.find_scale(answer)
                # for i in range(len(answer)):
                #     # Pause to show the streaming effect.
                #     await asyncio.sleep(0.01)
                #     # Add one letter at a time to the output.
                #     self.chat_history[-1] = (
                #         self.chat_history[-1][0],
                #         answer[: i + 1],
                #     )
                #     yield
                # self.image()
        except asyncio.TimeoutError:
            print("Request timed out")

        AnsweringStateLoader.answering = False


class AnsweringStateLoader(rx.State):
    answering = False

    


    