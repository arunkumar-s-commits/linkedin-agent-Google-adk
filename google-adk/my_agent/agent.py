from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
Model="gemini-2.0-flash"
# The model name — NOT the API key!
# ADK reads GOOGLE_API_KEY from your .env automatically for authentication.



image_agent = Agent(
    name="image",
    model=Model,
    instruction="""generet the image that suitable to the article content""",
    tools=[google_search],
    output_key="image_of_article"
)

content_agent = Agent(
    name="contentwriter",
    model=Model,
    instruction="""You are a skilled content writer.
    Steps:
    1) Take the user's topic.
    2) Use google_search to find real-time data and facts about the topic.
    3) Write engaging, well-structured content based on your research.
    4) Return the final content.""",
    tools=[google_search],
    output_key="content_for_article"
)

# SequentialAgent runs image_agent first, then content_agent, in order.
article_maker = SequentialAgent(
    name="article_maker",
    description="Runs image search and content writing in sequence to produce an article.",
    sub_agents=[image_agent, content_agent],
)

# Root agent — orchestrates everything.
# Since article_maker already contains image & content agents,
# we only need article_maker as a sub-agent here.
root_agent = Agent(
    name="ArticleWriter",
    model=Model,
    description="Write a LinkedIn article with images and content.",
    instruction="""You are a LinkedIn article creation assistant.
    When the user asks you to write an article:
    1) Delegate to the 'article_maker' agent which will find an image and write content.
    2) Once it returns, combine the image [image_of_article] and content [content_for_article]
       into a polished LinkedIn article format.
    """,
    sub_agents=[article_maker]
)