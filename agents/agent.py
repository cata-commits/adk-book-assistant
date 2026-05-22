from google.adk.agents import Agent
from agents.researcher.agent import researcher_agent
from agents.recommender.agent import recommender_agent


root_agent = Agent(
    name="book_agent",
    model="gemini-2.5-flash",
    description="A simple assistant that answers questions about books.",
    instruction=(
        "You are a helpful book assistant. "
        "You can answer questions about books and authors, and provide recommendations based on user preferences. "
        "Use the sub-agents to perform specific tasks: the researcher_agent for searching books and authors, and the recommender_agent for managing user preferences and providing recommendations. "
        "Always provide concise and relevant information to the user, and delegate tasks to the appropriate sub-agent when necessary. "
        "Be concise and friendly."
        "If the user asks you for a book but also tells you they like a specific genre, use the recommender_agent to add the book in their preferences and the researcher_agent to find information about those books. "
    ),
    sub_agents=[researcher_agent, recommender_agent],
)