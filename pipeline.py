from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # =========================
    # STEP 1 - SEARCH AGENT
    # =========================
    print("\n" + "=" * 50)
    print("step 1 - search agent is working ....")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print("\nSearch Result:\n", state["search_results"])


    # =========================
    # STEP 2 - READER AGENT
    # =========================
    print("\n" + "=" * 50)
    print("step 2 - Reader agent is scraping top resources ....")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
                Based on the following search results about '{topic}',
                pick the most relevant URL and scrape it for deeper content.

                Search Results:
                {state['search_results'][:800]}
                """
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content:\n", state["scraped_content"])


    # =========================
    # STEP 3 - WRITER
    # =========================
    print("\n" + "=" * 50)
    print("step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    writer_result = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    state["report"] = str(writer_result)

    print("\nFinal Report:\n", state["report"])


    # =========================
    # STEP 4 - CRITIC
    # =========================
    print("\n" + "=" * 50)
    print("step 4 - Critic is reviewing the report ....")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Feedback:\n", state["feedback"])


    # IMPORTANT:
    # Return the complete state to Streamlit
    return state


# =========================
# RUN DIRECTLY
# =========================

if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")

    result = run_research_pipeline(topic)

    print("\n" + "=" * 50)
    print("RESEARCH PIPELINE COMPLETED")
    print("=" * 50)

    print("\nReport:")
    print(result["report"])

    print("\nCritic Feedback:")
    print(result["feedback"])