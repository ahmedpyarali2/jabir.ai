import reflex as rx
import asyncio


class State(rx.State):
    question: str
    chat_history: list[tuple[str]]

    async def answer(self):
        answer = '''
Risk Analysis


As procurement specialist from Bazaar, I analyzed the market trends and patterns for edible oil (e.g., palm oil) and clarified butter in Pakistan as well as globally.


Market Trend: The global demand for vegetable oils has been increasing due to population growth, urbanization, and changes in consumer preferences. In recent years, there's a shift towards healthier options like plant-based fats.
Pakistan-specific factors:



Increasing Demand: Population expansion drives up the need for edible oil consumption (especially palm oil).

Supply Shortage: Local supply chains have been impacted by production constraints and import restrictions.


Recommendation: Considering these trends, I recommend procuring both products in bulk to ensure a stable inventory before prices rise further due to potential demand surges.
Scale 4/5 for edible oils (palm oil)


Justification


To justify this recommendation:



Palm Oil Supply: Malaysia and Indonesia are the top palm-oil producers, with increasing global consumption driving up their production capacity.


2-3 months ahead of current market trends). This surge could be driven by increased demand in Pakistan due to growing population.
Clarified Butter (Ghee) Market Trend:



Steady Demand: Pakistani consumers continue embracing traditional food habits, maintaining a steady demand for clarified butter.
Pakistan-specific factors:

Import restrictions and production constraints may lead to supply shortages.


Recommendation:** Given the stable global market trend of ghee consumption in Pakistan, I suggest procuring small-to-medium quantities as needed (no more than 1-3 months' worth) due to potential fluctuations caused by local import/distribution issues.
Scale: 4/5 for clarified butter


Data Points:


| Category | Forecasted Data Point |
|-- -- |--|
|| Edible Oils || Global demand increase, up by <10% in Q2 2023 and further growth expected. ||
|||| Clarified Butter (Ghee) || Pakistan's ghee consumption steady with no significant changes forecast for the next quarter.


Justification


This assessment is based on:



Global Market Trends: Analyzing international market trends, I observed a consistent increase in edible oil demand over recent years.
2-3 months ahead of current market trends). This surge could be driven by increased demand in Pakistan due to growing population and urbanization.


Recommendations


For Edible Oils (Palm Oil):



Purchase bulk quantities for stockpiling

Expected price increase: <5% within the next 6-8 weeks.
To secure a stable inventory before market fluctuations occur





Pakistan's Clarified Butter (Ghee) Market: Local demand remains steady, with no significant changes forecast.


Conclusion
Based on local and international market trends, I recommend procuring both edible oils in bulk for stockpiling purposes to ensure stability while also securing smaller quantities of clarified butter as needed due to potential supply fluctuations.
'''
        AnsweringStateLoader.answering = True
        self.chat_history.append((self.question, ''))
        self.question = ''

        yield

        for i in range(len(answer)):
            # Pause to show the streaming effect.
            await asyncio.sleep(0.001)
            # Add one letter at a time to the output.
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer[: i + 1],
            )
            yield

        AnsweringStateLoader.answering = False


class AnsweringStateLoader(rx.State):
    answering = False

    